#!/usr/bin/env python3
"""
Comprehensive EIA Glossary Extractor using Advanced Agentic LLMs
This script extracts ALL glossary terms, cross-references, and site map
from the EIA website using LangChain, LangGraph, LangSmith, and Tavily.
"""

import os
import json
import requests
import re
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup, Tag
import time
from urllib.parse import urljoin, urlparse

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

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
class CrossReference:
    """Data class for cross-references"""
    term: str
    url: str
    context: str

@dataclass
class GlossaryTerm:
    """Enhanced data class for a glossary term"""
    term: str
    definition: str
    fuel_groups: List[str]
    cross_references: List[CrossReference]
    source_url: str
    alphabetical_section: str
    hyperlinks: List[str]

@dataclass
class SiteMapEntry:
    """Data class for site map entries"""
    url: str
    title: str
    description: str
    term_count: int
    category: str

class TermExtraction(BaseModel):
    """Pydantic model for comprehensive term extraction"""
    terms: List[Dict[str, Any]] = Field(description="List of extracted terms with complete metadata")

class AgentState(TypedDict):
    """Enhanced state for the LangGraph agent"""
    extraction_targets: List[str]
    current_target: str
    extracted_terms: List[GlossaryTerm]
    site_map: List[SiteMapEntry]
    cross_reference_map: Dict[str, List[str]]
    processed_count: int
    total_terms_found: int
    messages: List[Any]

class ComprehensiveEIAExtractor:
    """Enhanced extractor class using advanced agentic LLMs"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
            max_tokens=4000
        )
        
        self.base_url = "https://www.eia.gov/tools/glossary/"
        self.fuel_groups = [
            "alternative fuels",
            "coal", 
            "electricity",
            "natural gas",
            "nuclear",
            "petroleum",
            "renewable"
        ]
        
        # Alphabetical sections for complete extraction
        self.alphabetical_sections = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'XYZ'
        ]
        
        self.extracted_data = {}
        self.site_map = []
        self.all_terms = set()
        
        # Initialize Tavily if available
        self.tavily_client = None
        if TAVILY_AVAILABLE:
            try:
                self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY", ""))
            except:
                pass
    
    @traceable
    def fetch_page_content(self, url: str) -> Tuple[str, BeautifulSoup]:
        """Fetch HTML content and return both text and BeautifulSoup object"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.find_all(['nav', 'header', 'footer', 'script', 'style']):
                element.decompose()
            
            text_content = soup.get_text(separator='\n', strip=True)
            return text_content, soup
            
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return "", None
    
    @traceable
    def extract_cross_references(self, soup: BeautifulSoup, base_url: str) -> List[CrossReference]:
        """Extract all cross-references and hyperlinks from the page"""
        cross_refs = []
        
        if not soup:
            return cross_refs
        
        # Find all links within the glossary content
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text(strip=True)
            
            # Skip navigation links
            if not text or len(text) < 2:
                continue
                
            # Convert relative URLs to absolute
            if href.startswith('?'):
                full_url = urljoin(base_url, href)
            elif href.startswith('/'):
                full_url = urljoin('https://www.eia.gov', href)
            else:
                full_url = href
            
            # Get context around the link
            parent = link.parent
            context = parent.get_text(strip=True)[:200] if parent else ""
            
            cross_ref = CrossReference(
                term=text,
                url=full_url,
                context=context
            )
            cross_refs.append(cross_ref)
        
        return cross_refs
    
    @traceable
    def extract_terms_with_llm(self, content: str, source_info: str, cross_refs: List[CrossReference]) -> List[GlossaryTerm]:
        """Use LLM to extract and structure glossary terms with enhanced metadata"""
        
        # Limit content size to avoid token limits
        if len(content) > 15000:
            content = content[:15000] + "..."
        
        # Prepare cross-reference information for the LLM
        cross_ref_info = "\n".join([f"- {ref.term}: {ref.url}" for ref in cross_refs[:20]])
        
        extraction_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at extracting comprehensive structured information from energy industry glossaries.

Your task is to extract ALL glossary terms with complete metadata including:
1. Term name (exact as appears)
2. Complete definition (unabridged)
3. Cross-references to other terms
4. Hyperlinks mentioned in definitions
5. Fuel group associations (if any)

Rules:
1. Extract EVERY term that appears to be a glossary entry
2. Preserve exact terminology and complete definitions
3. Identify all cross-references and hyperlinks
4. Note any fuel group associations
5. Maintain source attribution

Available cross-references on this page:
{cross_ref_info}

Return ONLY a valid JSON object with this structure:
{{
    "terms": [
        {{
            "term": "exact term name",
            "definition": "complete unabridged definition",
            "cross_references": ["list", "of", "referenced", "terms"],
            "hyperlinks": ["list", "of", "urls", "mentioned"],
            "fuel_groups": ["associated", "fuel", "groups"],
            "alphabetical_section": "letter section (A, B, C, etc.)"
        }}
    ]
}}
"""),
            ("human", f"Extract all glossary terms from this {source_info} content:\n\n{content}")
        ])
        
        try:
            response = self.llm.invoke(extraction_prompt.format_messages(
                content=content, 
                source_info=source_info,
                cross_ref_info=cross_ref_info
            ))
            
            # Parse JSON response
            response_text = response.content.strip()
            
            # Clean up response if needed
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            result = json.loads(response_text)
            
            # Convert to GlossaryTerm objects
            terms = []
            for term_data in result.get("terms", []):
                # Convert cross-references to CrossReference objects
                cross_references = []
                for ref_term in term_data.get("cross_references", []):
                    # Find matching cross-reference from page
                    matching_ref = next((ref for ref in cross_refs if ref.term.lower() == ref_term.lower()), None)
                    if matching_ref:
                        cross_references.append(matching_ref)
                    else:
                        # Create a basic cross-reference
                        cross_references.append(CrossReference(
                            term=ref_term,
                            url="",
                            context=""
                        ))
                
                term = GlossaryTerm(
                    term=term_data.get("term", ""),
                    definition=term_data.get("definition", ""),
                    fuel_groups=term_data.get("fuel_groups", []),
                    cross_references=cross_references,
                    source_url=source_info,
                    alphabetical_section=term_data.get("alphabetical_section", ""),
                    hyperlinks=term_data.get("hyperlinks", [])
                )
                terms.append(term)
            
            return terms
            
        except Exception as e:
            print(f"Error extracting terms with LLM for {source_info}: {e}")
            return []
    
    @traceable
    def extract_from_fuel_group(self, fuel_group: str) -> List[GlossaryTerm]:
        """Extract terms from a specific fuel group page"""
        url = f"{self.base_url}?id={fuel_group}"
        print(f"Extracting from fuel group: {fuel_group}")
        
        content, soup = self.fetch_page_content(url)
        if not content:
            return []
        
        cross_refs = self.extract_cross_references(soup, url)
        terms = self.extract_terms_with_llm(content, f"fuel group: {fuel_group}", cross_refs)
        
        # Add fuel group to all terms
        for term in terms:
            if fuel_group not in term.fuel_groups:
                term.fuel_groups.append(fuel_group)
        
        print(f"Extracted {len(terms)} terms from {fuel_group}")
        return terms
    
    @traceable
    def extract_from_alphabetical_section(self, section: str) -> List[GlossaryTerm]:
        """Extract terms from an alphabetical section"""
        url = f"{self.base_url}?id={section}"
        print(f"Extracting from alphabetical section: {section}")
        
        content, soup = self.fetch_page_content(url)
        if not content:
            return []
        
        cross_refs = self.extract_cross_references(soup, url)
        terms = self.extract_terms_with_llm(content, f"alphabetical section: {section}", cross_refs)
        
        # Set alphabetical section for all terms
        for term in terms:
            term.alphabetical_section = section
        
        print(f"Extracted {len(terms)} terms from section {section}")
        return terms
    
    @traceable
    def build_site_map(self) -> List[SiteMapEntry]:
        """Build comprehensive site map of the EIA glossary"""
        site_map = []
        
        # Main glossary page
        site_map.append(SiteMapEntry(
            url=self.base_url,
            title="EIA Energy Glossary - Main Page",
            description="Main entry point for EIA energy industry glossary",
            term_count=0,  # Will be updated
            category="main"
        ))
        
        # Fuel group pages
        for fuel_group in self.fuel_groups:
            url = f"{self.base_url}?id={fuel_group}"
            # Get term count from the page
            content, soup = self.fetch_page_content(url)
            term_count = len(self.extract_terms_with_llm(content, f"fuel group: {fuel_group}", []))
            
            site_map.append(SiteMapEntry(
                url=url,
                title=f"EIA Glossary - {fuel_group.title()}",
                description=f"Glossary terms related to {fuel_group}",
                term_count=term_count,
                category="fuel_group"
            ))
        
        # Alphabetical sections
        for section in self.alphabetical_sections:
            url = f"{self.base_url}?id={section}"
            site_map.append(SiteMapEntry(
                url=url,
                title=f"EIA Glossary - Section {section}",
                description=f"Alphabetical glossary section {section}",
                term_count=0,  # Will be updated during extraction
                category="alphabetical"
            ))
        
        return site_map
    
    def create_comprehensive_workflow(self) -> StateGraph:
        """Create enhanced LangGraph workflow for comprehensive extraction"""
        
        def initialize_extraction(state: AgentState) -> AgentState:
            """Initialize the comprehensive extraction process"""
            print("Initializing comprehensive EIA glossary extraction...")
            
            # Build extraction targets (fuel groups + alphabetical sections)
            targets = []
            
            # Add fuel groups
            for fuel_group in self.fuel_groups:
                targets.append(f"fuel_group:{fuel_group}")
            
            # Add alphabetical sections
            for section in self.alphabetical_sections:
                targets.append(f"alphabetical:{section}")
            
            state["extraction_targets"] = targets
            state["current_target"] = targets[0] if targets else ""
            state["site_map"] = self.build_site_map()
            state["messages"].append(f"Initialized extraction for {len(targets)} targets")
            
            return state
        
        def extract_current_target(state: AgentState) -> AgentState:
            """Extract terms from the current target"""
            current = state["current_target"]
            
            if current.startswith("fuel_group:"):
                fuel_group = current.replace("fuel_group:", "")
                terms = self.extract_from_fuel_group(fuel_group)
            elif current.startswith("alphabetical:"):
                section = current.replace("alphabetical:", "")
                terms = self.extract_from_alphabetical_section(section)
            else:
                terms = []
            
            # Add unique terms to the collection
            existing_terms = {term.term.lower() for term in state["extracted_terms"]}
            new_terms = [term for term in terms if term.term.lower() not in existing_terms]
            
            state["extracted_terms"].extend(new_terms)
            state["total_terms_found"] += len(terms)
            state["processed_count"] += 1
            
            state["messages"].append(f"Processed {current}: {len(terms)} terms ({len(new_terms)} new)")
            
            return state
        
        def check_completion(state: AgentState) -> str:
            """Check if all targets have been processed"""
            if state["processed_count"] >= len(state["extraction_targets"]):
                return "complete"
            else:
                return "continue"
        
        def next_target(state: AgentState) -> AgentState:
            """Move to the next extraction target"""
            current_index = state["extraction_targets"].index(state["current_target"])
            if current_index + 1 < len(state["extraction_targets"]):
                state["current_target"] = state["extraction_targets"][current_index + 1]
            return state
        
        def finalize_extraction(state: AgentState) -> AgentState:
            """Finalize the extraction with cross-reference analysis"""
            print("Finalizing extraction and building cross-reference map...")
            
            # Build comprehensive cross-reference map
            cross_ref_map = {}
            for term in state["extracted_terms"]:
                term_refs = [ref.term for ref in term.cross_references]
                cross_ref_map[term.term] = term_refs
            
            state["cross_reference_map"] = cross_ref_map
            state["messages"].append(f"Finalized extraction: {len(state['extracted_terms'])} unique terms")
            
            return state
        
        # Build the workflow graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("initialize", initialize_extraction)
        workflow.add_node("extract", extract_current_target)
        workflow.add_node("next_target", next_target)
        workflow.add_node("finalize", finalize_extraction)
        
        # Add edges
        workflow.add_edge("initialize", "extract")
        workflow.add_conditional_edges(
            "extract",
            check_completion,
            {
                "complete": "finalize",
                "continue": "next_target"
            }
        )
        workflow.add_edge("next_target", "extract")
        workflow.add_edge("finalize", END)
        
        # Set entry point
        workflow.set_entry_point("initialize")
        
        return workflow.compile()
    
    @traceable
    def run_comprehensive_extraction(self) -> Dict[str, Any]:
        """Run the complete comprehensive extraction process"""
        
        print("Starting Comprehensive EIA Glossary Extraction with Agentic LLMs...")
        print("=" * 70)
        
        # Initialize state
        initial_state = AgentState(
            extraction_targets=[],
            current_target="",
            extracted_terms=[],
            site_map=[],
            cross_reference_map={},
            processed_count=0,
            total_terms_found=0,
            messages=[]
        )
        
        # Create and run workflow
        workflow = self.create_comprehensive_workflow()
        final_state = workflow.invoke(initial_state)
        
        # Organize results
        results = {
            "total_unique_terms": len(final_state["extracted_terms"]),
            "total_terms_found": final_state["total_terms_found"],
            "fuel_groups": {},
            "alphabetical_sections": {},
            "all_terms": final_state["extracted_terms"],
            "site_map": final_state["site_map"],
            "cross_reference_map": final_state["cross_reference_map"],
            "extraction_summary": final_state["messages"]
        }
        
        # Organize by fuel groups
        for term in final_state["extracted_terms"]:
            for fuel_group in term.fuel_groups:
                if fuel_group not in results["fuel_groups"]:
                    results["fuel_groups"][fuel_group] = []
                results["fuel_groups"][fuel_group].append(term)
        
        # Organize by alphabetical sections
        for term in final_state["extracted_terms"]:
            section = term.alphabetical_section or "Unknown"
            if section not in results["alphabetical_sections"]:
                results["alphabetical_sections"][section] = []
            results["alphabetical_sections"][section].append(term)
        
        return results
    
    def save_comprehensive_results(self, results: Dict[str, Any], base_filename: str = "eia_comprehensive_extraction"):
        """Save comprehensive results in multiple formats"""
        
        # Convert GlossaryTerm objects to dictionaries for JSON serialization
        def term_to_dict(term):
            term_dict = asdict(term)
            # Convert CrossReference objects to dictionaries
            term_dict["cross_references"] = [asdict(ref) for ref in term.cross_references]
            return term_dict
        
        # Prepare serializable data
        serializable_results = {
            "metadata": {
                "total_unique_terms": results["total_unique_terms"],
                "total_terms_found": results["total_terms_found"],
                "extraction_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "fuel_groups_count": len(results["fuel_groups"]),
                "alphabetical_sections_count": len(results["alphabetical_sections"])
            },
            "fuel_groups": {},
            "alphabetical_sections": {},
            "all_terms": [term_to_dict(term) for term in results["all_terms"]],
            "site_map": [asdict(entry) for entry in results["site_map"]],
            "cross_reference_map": results["cross_reference_map"],
            "extraction_summary": results["extraction_summary"]
        }
        
        # Organize fuel groups
        for fuel_group, terms in results["fuel_groups"].items():
            serializable_results["fuel_groups"][fuel_group] = [term_to_dict(term) for term in terms]
        
        # Organize alphabetical sections
        for section, terms in results["alphabetical_sections"].items():
            serializable_results["alphabetical_sections"][section] = [term_to_dict(term) for term in terms]
        
        # Save main JSON file
        json_filename = f"{base_filename}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        print(f"Comprehensive results saved to {json_filename}")
        return json_filename

def main():
    """Main execution function for comprehensive extraction"""
    print("EIA Comprehensive Glossary Extractor - Advanced Agentic LLM Version")
    print("=" * 70)
    
    # Initialize extractor
    extractor = ComprehensiveEIAExtractor()
    
    # Run comprehensive extraction
    results = extractor.run_comprehensive_extraction()
    
    # Save results
    output_file = extractor.save_comprehensive_results(results)
    
    # Print comprehensive summary
    print("\n" + "=" * 70)
    print("COMPREHENSIVE EXTRACTION SUMMARY")
    print("=" * 70)
    
    print(f"Total Unique Terms Extracted: {results['total_unique_terms']}")
    print(f"Total Terms Found (including duplicates): {results['total_terms_found']}")
    print(f"Cross-References Mapped: {len(results['cross_reference_map'])}")
    print(f"Site Map Entries: {len(results['site_map'])}")
    
    print("\nTerms by Fuel Group:")
    print("-" * 30)
    for fuel_group, terms in results["fuel_groups"].items():
        print(f"{fuel_group}: {len(terms)} terms")
    
    print("\nTerms by Alphabetical Section:")
    print("-" * 30)
    for section, terms in results["alphabetical_sections"].items():
        if section != "Unknown":
            print(f"Section {section}: {len(terms)} terms")
    
    print(f"\nResults saved to: {output_file}")
    print("Comprehensive extraction completed successfully!")
    
    return results, output_file

if __name__ == "__main__":
    main()

