#!/usr/bin/env python3
"""
EIA Glossary Extractor using Agentic LLMs
This script uses LangChain, LangGraph, LangSmith, and Tavily to extract
energy industry glossary terms from the EIA website.
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup
import time

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# LangGraph imports
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

# LangSmith for tracing (optional)
try:
    from langsmith import traceable
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False
    def traceable(func):
        return func

# Tavily for web search (optional enhancement)
try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False

@dataclass
class GlossaryTerm:
    """Data class for a glossary term"""
    term: str
    definition: str
    fuel_group: str
    cross_references: List[str] = None

class TermExtraction(BaseModel):
    """Pydantic model for term extraction"""
    terms: List[Dict[str, str]] = Field(description="List of extracted terms with their definitions")

class AgentState(TypedDict):
    """State for the LangGraph agent"""
    fuel_groups: List[str]
    current_group: str
    extracted_terms: List[GlossaryTerm]
    raw_html: str
    processed_count: int
    messages: List[Any]

class EIAGlossaryExtractor:
    """Main extractor class using agentic LLMs"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
            max_tokens=4000
        )
        
        self.fuel_groups = [
            "alternative fuels",
            "coal", 
            "electricity",
            "natural gas",
            "nuclear",
            "petroleum",
            "renewable"
        ]
        
        self.base_url = "https://www.eia.gov/tools/glossary/index.php"
        self.extracted_data = {}
        
        # Initialize Tavily if available
        self.tavily_client = None
        if TAVILY_AVAILABLE:
            try:
                # Note: Tavily requires API key, but we'll use it optionally
                self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY", ""))
            except:
                pass
    
    @traceable
    def fetch_page_content(self, fuel_group: str) -> str:
        """Fetch the HTML content for a specific fuel group"""
        url = f"{self.base_url}?id={fuel_group}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return ""
    
    @traceable
    def parse_html_content(self, html_content: str) -> str:
        """Parse HTML and extract the main glossary content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the main content area (this may need adjustment based on actual HTML structure)
        main_content = soup.find('div', class_='main-content') or soup.find('main') or soup.body
        
        if main_content:
            # Remove navigation and other non-content elements
            for element in main_content.find_all(['nav', 'header', 'footer', 'script', 'style']):
                element.decompose()
            
            return main_content.get_text(separator='\n', strip=True)
        
        return soup.get_text(separator='\n', strip=True)
    
    @traceable
    def extract_terms_with_llm(self, content: str, fuel_group: str) -> List[GlossaryTerm]:
        """Use LLM to extract and structure glossary terms"""
        
        extraction_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at extracting structured information from energy industry glossaries.
            
            Your task is to extract ALL glossary terms and their definitions from the provided text.
            Each term should be clearly identified along with its complete definition.
            
            Rules:
            1. Extract EVERY term that appears to be a glossary entry
            2. Include the complete definition for each term
            3. Identify any cross-references to other terms
            4. Maintain the exact terminology used
            5. Do not summarize or paraphrase definitions
            
            Return the results as a JSON object with this structure:
            {{
                "terms": [
                    {{
                        "term": "exact term name",
                        "definition": "complete definition text",
                        "cross_references": ["list", "of", "referenced", "terms"]
                    }}
                ]
            }}
            """),
            ("human", f"Extract all glossary terms from this {fuel_group} content:\n\n{content}")
        ])
        
        parser = JsonOutputParser(pydantic_object=TermExtraction)
        chain = extraction_prompt | self.llm | parser
        
        try:
            result = chain.invoke({"content": content, "fuel_group": fuel_group})
            
            terms = []
            for term_data in result.get("terms", []):
                term = GlossaryTerm(
                    term=term_data.get("term", ""),
                    definition=term_data.get("definition", ""),
                    fuel_group=fuel_group,
                    cross_references=term_data.get("cross_references", [])
                )
                terms.append(term)
            
            return terms
            
        except Exception as e:
            print(f"Error extracting terms with LLM: {e}")
            return []
    
    @traceable
    def enhance_with_tavily(self, terms: List[GlossaryTerm]) -> List[GlossaryTerm]:
        """Optionally enhance terms with additional context using Tavily"""
        if not self.tavily_client:
            return terms
        
        enhanced_terms = []
        for term in terms:
            try:
                # Search for additional context
                search_query = f"energy industry {term.term} definition"
                search_results = self.tavily_client.search(
                    query=search_query,
                    search_depth="basic",
                    max_results=2
                )
                
                # Add search context to the term (optional enhancement)
                term.additional_context = search_results.get("results", [])
                enhanced_terms.append(term)
                
            except Exception as e:
                print(f"Tavily enhancement failed for {term.term}: {e}")
                enhanced_terms.append(term)
        
        return enhanced_terms
    
    def create_langgraph_workflow(self) -> StateGraph:
        """Create a LangGraph workflow for the extraction process"""
        
        def fetch_content_node(state: AgentState) -> AgentState:
            """Node to fetch content for current fuel group"""
            current_group = state["current_group"]
            print(f"Fetching content for: {current_group}")
            
            html_content = self.fetch_page_content(current_group)
            parsed_content = self.parse_html_content(html_content)
            
            state["raw_html"] = parsed_content
            state["messages"].append(f"Fetched content for {current_group}")
            return state
        
        def extract_terms_node(state: AgentState) -> AgentState:
            """Node to extract terms using LLM"""
            current_group = state["current_group"]
            content = state["raw_html"]
            
            print(f"Extracting terms for: {current_group}")
            
            terms = self.extract_terms_with_llm(content, current_group)
            
            # Enhance with Tavily if available
            if TAVILY_AVAILABLE and self.tavily_client:
                terms = self.enhance_with_tavily(terms)
            
            state["extracted_terms"].extend(terms)
            state["processed_count"] += 1
            state["messages"].append(f"Extracted {len(terms)} terms from {current_group}")
            
            return state
        
        def check_completion_node(state: AgentState) -> str:
            """Check if all fuel groups have been processed"""
            if state["processed_count"] >= len(state["fuel_groups"]):
                return "complete"
            else:
                return "continue"
        
        def next_group_node(state: AgentState) -> AgentState:
            """Move to the next fuel group"""
            current_index = state["fuel_groups"].index(state["current_group"])
            if current_index + 1 < len(state["fuel_groups"]):
                state["current_group"] = state["fuel_groups"][current_index + 1]
            return state
        
        # Build the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("fetch_content", fetch_content_node)
        workflow.add_node("extract_terms", extract_terms_node)
        workflow.add_node("next_group", next_group_node)
        
        # Add edges
        workflow.add_edge("fetch_content", "extract_terms")
        workflow.add_conditional_edges(
            "extract_terms",
            check_completion_node,
            {
                "complete": END,
                "continue": "next_group"
            }
        )
        workflow.add_edge("next_group", "fetch_content")
        
        # Set entry point
        workflow.set_entry_point("fetch_content")
        
        return workflow.compile()
    
    @traceable
    def run_extraction(self) -> Dict[str, List[GlossaryTerm]]:
        """Run the complete extraction process using LangGraph"""
        
        print("Starting EIA Glossary extraction with agentic LLMs...")
        
        # Initialize state
        initial_state = AgentState(
            fuel_groups=self.fuel_groups,
            current_group=self.fuel_groups[0],
            extracted_terms=[],
            raw_html="",
            processed_count=0,
            messages=[]
        )
        
        # Create and run workflow
        workflow = self.create_langgraph_workflow()
        final_state = workflow.invoke(initial_state)
        
        # Organize results by fuel group
        results = {}
        for term in final_state["extracted_terms"]:
            if term.fuel_group not in results:
                results[term.fuel_group] = []
            results[term.fuel_group].append(term)
        
        return results
    
    def save_results(self, results: Dict[str, List[GlossaryTerm]], filename: str = "eia_glossary_extracted.json"):
        """Save extracted results to JSON file"""
        
        # Convert to serializable format
        serializable_results = {}
        for fuel_group, terms in results.items():
            serializable_results[fuel_group] = []
            for term in terms:
                term_dict = {
                    "term": term.term,
                    "definition": term.definition,
                    "fuel_group": term.fuel_group,
                    "cross_references": term.cross_references or []
                }
                if hasattr(term, 'additional_context'):
                    term_dict["additional_context"] = term.additional_context
                
                serializable_results[fuel_group].append(term_dict)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to {filename}")
        return filename

def main():
    """Main execution function"""
    print("EIA Glossary Extractor - Agentic LLM Version")
    print("=" * 50)
    
    # Initialize extractor
    extractor = EIAGlossaryExtractor()
    
    # Run extraction
    results = extractor.run_extraction()
    
    # Save results
    output_file = extractor.save_results(results)
    
    # Print summary
    print("\nExtraction Summary:")
    print("=" * 30)
    total_terms = 0
    for fuel_group, terms in results.items():
        count = len(terms)
        total_terms += count
        print(f"{fuel_group}: {count} terms")
    
    print(f"\nTotal terms extracted: {total_terms}")
    print(f"Results saved to: {output_file}")
    
    return results, output_file

if __name__ == "__main__":
    main()

