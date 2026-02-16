#!/usr/bin/env python3
"""
Simplified EIA Glossary Extractor using Agentic LLMs
"""

import json
import requests
from typing import Dict, List
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class TermExtraction(BaseModel):
    """Pydantic model for term extraction"""
    terms: List[Dict[str, str]] = Field(description="List of extracted terms with their definitions")

class SimpleEIAExtractor:
    """Simplified extractor class"""
    
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
    
    def fetch_page_content(self, fuel_group: str) -> str:
        """Fetch the HTML content for a specific fuel group"""
        url = f"{self.base_url}?id={fuel_group}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""
    
    def parse_html_content(self, html_content: str) -> str:
        """Parse HTML and extract the main glossary content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup.find_all(['nav', 'header', 'footer', 'script', 'style']):
            element.decompose()
        
        return soup.get_text(separator='\n', strip=True)
    
    def extract_terms_with_llm(self, content: str, fuel_group: str) -> List[Dict]:
        """Use LLM to extract and structure glossary terms"""
        
        # Limit content size to avoid token limits
        if len(content) > 15000:
            content = content[:15000] + "..."
        
        extraction_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at extracting structured information from energy industry glossaries.

Extract ALL glossary terms and their definitions from the provided text.
Each term should be clearly identified along with its complete definition.

Rules:
1. Extract EVERY term that appears to be a glossary entry (usually in bold or as headers)
2. Include the complete definition for each term
3. Identify any cross-references to other terms
4. Maintain the exact terminology used
5. Do not summarize or paraphrase definitions

Return ONLY a valid JSON object with this exact structure:
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
        
        try:
            response = self.llm.invoke(extraction_prompt.format_messages(content=content, fuel_group=fuel_group))
            
            # Parse JSON response
            response_text = response.content.strip()
            
            # Clean up response if needed
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            result = json.loads(response_text)
            return result.get("terms", [])
            
        except Exception as e:
            print(f"Error extracting terms with LLM for {fuel_group}: {e}")
            return []
    
    def extract_single_group(self, fuel_group: str) -> List[Dict]:
        """Extract terms for a single fuel group"""
        print(f"Processing: {fuel_group}")
        
        # Fetch content
        html_content = self.fetch_page_content(fuel_group)
        if not html_content:
            return []
        
        # Parse content
        parsed_content = self.parse_html_content(html_content)
        
        # Extract terms
        terms = self.extract_terms_with_llm(parsed_content, fuel_group)
        
        # Add fuel group to each term
        for term in terms:
            term["fuel_group"] = fuel_group
        
        print(f"Extracted {len(terms)} terms from {fuel_group}")
        return terms
    
    def run_extraction(self) -> Dict[str, List[Dict]]:
        """Run the complete extraction process"""
        print("Starting EIA Glossary extraction...")
        print("=" * 50)
        
        all_results = {}
        
        for fuel_group in self.fuel_groups:
            terms = self.extract_single_group(fuel_group)
            all_results[fuel_group] = terms
        
        return all_results
    
    def save_results(self, results: Dict[str, List[Dict]], filename: str = "eia_glossary_simple.json"):
        """Save extracted results to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to {filename}")
        return filename

def main():
    """Main execution function"""
    extractor = SimpleEIAExtractor()
    
    # Test with just one fuel group first
    print("Testing with alternative fuels...")
    test_terms = extractor.extract_single_group("alternative fuels")
    
    if test_terms:
        print(f"Test successful! Found {len(test_terms)} terms")
        print("Sample terms:")
        for i, term in enumerate(test_terms[:3]):
            print(f"{i+1}. {term.get('term', 'Unknown')}")
        
        # If test works, run full extraction
        print("\nRunning full extraction...")
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
        
    else:
        print("Test failed - no terms extracted")

if __name__ == "__main__":
    main()

