#!/usr/bin/env python3
"""
Focused Comprehensive EIA Glossary Extractor
Extracts all fuel groups with cross-references and site map analysis
"""

import json
import requests
from typing import Dict, List, Any
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import time

class FocusedEIAExtractor:
    """Focused comprehensive extractor"""
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, max_tokens=4000)
        self.base_url = "https://www.eia.gov/tools/glossary/"
        self.fuel_groups = [
            "alternative fuels", "coal", "electricity", 
            "natural gas", "nuclear", "petroleum", "renewable"
        ]
        self.results = {
            "fuel_groups": {},
            "site_map": [],
            "cross_references": {},
            "total_terms": 0,
            "extraction_metadata": {}
        }
    
    def fetch_page_content(self, url: str) -> tuple:
        """Fetch page content and extract cross-references"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract cross-references (hyperlinks)
            cross_refs = []
            for link in soup.find_all('a', href=True):
                text = link.get_text(strip=True)
                href = link.get('href')
                if text and len(text) > 1 and 'glossary' in href:
                    cross_refs.append({"term": text, "url": href})
            
            # Clean text content
            for element in soup.find_all(['nav', 'header', 'footer', 'script', 'style']):
                element.decompose()
            
            text_content = soup.get_text(separator='\n', strip=True)
            return text_content, cross_refs
            
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return "", []
    
    def extract_terms_with_llm(self, content: str, fuel_group: str, cross_refs: List[Dict]) -> List[Dict]:
        """Extract terms using LLM with cross-reference awareness"""
        
        if len(content) > 15000:
            content = content[:15000] + "..."
        
        cross_ref_text = "\n".join([f"- {ref['term']}: {ref['url']}" for ref in cross_refs[:10]])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Extract ALL glossary terms from the energy industry content.

For each term, provide:
1. Exact term name
2. Complete definition
3. Cross-references to other terms (if any)
4. Associated fuel groups

Cross-references available on this page:
{cross_refs}

Return valid JSON:
{{
    "terms": [
        {{
            "term": "exact term name",
            "definition": "complete definition",
            "cross_references": ["referenced", "terms"],
            "fuel_group": "{fuel_group}"
        }}
    ]
}}"""),
            ("human", f"Extract terms from this {fuel_group} content:\n\n{content}")
        ])
        
        try:
            response = self.llm.invoke(prompt.format_messages(
                content=content, 
                fuel_group=fuel_group,
                cross_refs=cross_ref_text
            ))
            
            response_text = response.content.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3]
            
            result = json.loads(response_text)
            return result.get("terms", [])
            
        except Exception as e:
            print(f"Error extracting terms for {fuel_group}: {e}")
            return []
    
    def extract_fuel_group(self, fuel_group: str) -> Dict[str, Any]:
        """Extract comprehensive data for a fuel group"""
        print(f"Processing fuel group: {fuel_group}")
        
        url = f"{self.base_url}?id={fuel_group}"
        content, cross_refs = self.fetch_page_content(url)
        
        if not content:
            return {"terms": [], "cross_references": [], "url": url}
        
        terms = self.extract_terms_with_llm(content, fuel_group, cross_refs)
        
        # Add metadata to each term
        for term in terms:
            term["source_url"] = url
            term["extraction_timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        result = {
            "terms": terms,
            "cross_references": cross_refs,
            "url": url,
            "term_count": len(terms)
        }
        
        print(f"Extracted {len(terms)} terms from {fuel_group}")
        return result
    
    def build_site_map(self) -> List[Dict]:
        """Build comprehensive site map"""
        site_map = []
        
        # Main page
        site_map.append({
            "url": self.base_url,
            "title": "EIA Energy Glossary - Main Page",
            "type": "main",
            "description": "Main entry point for EIA energy glossary"
        })
        
        # Fuel group pages
        for fuel_group in self.fuel_groups:
            url = f"{self.base_url}?id={fuel_group}"
            term_count = len(self.results["fuel_groups"].get(fuel_group, {}).get("terms", []))
            
            site_map.append({
                "url": url,
                "title": f"EIA Glossary - {fuel_group.title()}",
                "type": "fuel_group",
                "fuel_group": fuel_group,
                "term_count": term_count,
                "description": f"Glossary terms related to {fuel_group}"
            })
        
        # Alphabetical sections
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'XYZ']
        
        for letter in alphabet:
            url = f"{self.base_url}?id={letter}"
            site_map.append({
                "url": url,
                "title": f"EIA Glossary - Section {letter}",
                "type": "alphabetical",
                "section": letter,
                "description": f"Alphabetical section {letter}"
            })
        
        return site_map
    
    def analyze_cross_references(self) -> Dict[str, List[str]]:
        """Analyze cross-references across all fuel groups"""
        cross_ref_map = {}
        
        for fuel_group, data in self.results["fuel_groups"].items():
            for term in data.get("terms", []):
                term_name = term.get("term", "")
                refs = term.get("cross_references", [])
                
                if term_name:
                    cross_ref_map[term_name] = refs
        
        return cross_ref_map
    
    def run_comprehensive_extraction(self) -> Dict[str, Any]:
        """Run the complete extraction process"""
        print("Starting Focused Comprehensive EIA Extraction...")
        print("=" * 60)
        
        # Extract all fuel groups
        for fuel_group in self.fuel_groups:
            group_data = self.extract_fuel_group(fuel_group)
            self.results["fuel_groups"][fuel_group] = group_data
            self.results["total_terms"] += group_data["term_count"]
        
        # Build site map
        print("Building site map...")
        self.results["site_map"] = self.build_site_map()
        
        # Analyze cross-references
        print("Analyzing cross-references...")
        self.results["cross_references"] = self.analyze_cross_references()
        
        # Add metadata
        self.results["extraction_metadata"] = {
            "extraction_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_fuel_groups": len(self.fuel_groups),
            "total_terms_extracted": self.results["total_terms"],
            "total_cross_references": len(self.results["cross_references"]),
            "site_map_entries": len(self.results["site_map"])
        }
        
        return self.results
    
    def save_results(self, filename: str = "eia_comprehensive_results.json"):
        """Save comprehensive results"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to {filename}")
        return filename

def main():
    """Main execution"""
    extractor = FocusedEIAExtractor()
    
    # Run extraction
    results = extractor.run_comprehensive_extraction()
    
    # Save results
    output_file = extractor.save_results()
    
    # Print summary
    print("\n" + "=" * 60)
    print("COMPREHENSIVE EXTRACTION SUMMARY")
    print("=" * 60)
    
    metadata = results["extraction_metadata"]
    print(f"Total Terms Extracted: {metadata['total_terms_extracted']}")
    print(f"Total Fuel Groups: {metadata['total_fuel_groups']}")
    print(f"Cross-References Mapped: {metadata['total_cross_references']}")
    print(f"Site Map Entries: {metadata['site_map_entries']}")
    
    print("\nTerms by Fuel Group:")
    print("-" * 30)
    for fuel_group, data in results["fuel_groups"].items():
        print(f"{fuel_group}: {data['term_count']} terms")
    
    print(f"\nResults saved to: {output_file}")
    
    return results, output_file

if __name__ == "__main__":
    main()

