#!/usr/bin/env python3
"""
ATLAS Framework - Intermediate Example: Energy Taxonomy Extractor

This example demonstrates intermediate ATLAS Framework concepts:
- AI-powered taxonomy extraction using LangChain
- FABRIC pattern integration
- Graph database operations with Neo4j
- Advanced behavior composition
- Real-world EIA glossary processing

Requirements:
- Python 3.11+
- ATLAS Framework with AI features
- OpenAI API key
- Neo4j database (optional)
"""

import asyncio
import json
import aiohttp
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

# ATLAS Framework imports
from atlas import ConfigurationManager, ATLASNode
from atlas.enums import NodeLabelType, FuelGroupType, ValidationStatusType
from atlas.frameworks.langchain import ExtractionChain, ValidationChain
from atlas.frameworks.fabric import FabricPatternRegistry
from atlas.graph.neo4j import Neo4jDriver
from atlas.decorators import fabric_pattern, atlas_operation
from atlas.utils.logging import get_logger

# Setup logging
logger = get_logger(__name__)


class EnergyTaxonomyExtractor:
    """
    Intermediate example: AI-powered energy taxonomy extraction.
    
    This class demonstrates:
    - LangChain integration for intelligent extraction
    - FABRIC patterns for content analysis
    - Neo4j graph operations
    - Advanced behavior composition
    - Real-world data processing
    """
    
    def __init__(self, config_path: str, neo4j_uri: Optional[str] = None):
        """
        Initialize the energy taxonomy extractor.
        
        Args:
            config_path: Path to ATLAS configuration file
            neo4j_uri: Optional Neo4j database URI
        """
        self.config_manager = ConfigurationManager.from_file(config_path)
        self.fabric_registry = FabricPatternRegistry()
        self.extraction_chain = ExtractionChain(
            model="gpt-4-turbo",
            temperature=0.1,
            max_tokens=2000
        )
        self.validation_chain = ValidationChain(
            model="gpt-4-turbo",
            temperature=0.0
        )
        
        # Optional Neo4j integration
        self.neo4j_driver = None
        if neo4j_uri:
            self.neo4j_driver = Neo4jDriver(neo4j_uri)
        
        # Statistics tracking
        self.extraction_stats = {
            "total_processed": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "relationships_discovered": 0,
            "validation_results": {}
        }
    
    async def extract_from_eia_glossary(
        self, 
        glossary_url: str = "https://www.eia.gov/tools/glossary/",
        fuel_groups: List[str] = None
    ) -> Dict[str, List[ATLASNode]]:
        """
        Extract taxonomy from EIA glossary using AI.
        
        Args:
            glossary_url: URL of the EIA glossary
            fuel_groups: List of fuel groups to focus on
            
        Returns:
            Dict[str, List[ATLASNode]]: Extracted nodes by fuel group
        """
        
        print("🤖 Starting AI-powered EIA glossary extraction...")
        print(f"📍 Source: {glossary_url}")
        
        if fuel_groups is None:
            fuel_groups = ["renewable", "fossil", "nuclear", "alternative"]
        
        extracted_nodes = {}
        
        for fuel_group in fuel_groups:
            print(f"\n🔍 Processing fuel group: {fuel_group}")
            
            try:
                # Step 1: Fetch glossary content for fuel group
                glossary_content = await self._fetch_glossary_content(glossary_url, fuel_group)
                
                # Step 2: AI extraction using LangChain
                extraction_result = await self._extract_terms_with_ai(
                    glossary_content, fuel_group
                )
                
                # Step 3: Create ATLAS nodes from extraction
                nodes = await self._create_nodes_from_extraction(
                    extraction_result, fuel_group
                )
                
                # Step 4: Validate with FABRIC patterns
                validated_nodes = await self._validate_nodes_with_fabric(nodes)
                
                # Step 5: Discover relationships
                relationships = await self._discover_relationships(validated_nodes)
                
                extracted_nodes[fuel_group] = validated_nodes
                
                print(f"✅ Extracted {len(validated_nodes)} terms for {fuel_group}")
                print(f"🔗 Discovered {len(relationships)} relationships")
                
                # Update statistics
                self.extraction_stats["successful_extractions"] += len(validated_nodes)
                self.extraction_stats["relationships_discovered"] += len(relationships)
                
            except Exception as e:
                logger.error(f"Failed to process {fuel_group}: {e}")
                self.extraction_stats["failed_extractions"] += 1
                extracted_nodes[fuel_group] = []
        
        self.extraction_stats["total_processed"] = sum(len(nodes) for nodes in extracted_nodes.values())
        
        return extracted_nodes
    
    async def _fetch_glossary_content(self, base_url: str, fuel_group: str) -> str:
        """
        Fetch glossary content for a specific fuel group.
        
        Args:
            base_url: Base URL of the glossary
            fuel_group: Fuel group to fetch content for
            
        Returns:
            str: Raw glossary content
        """
        
        # Simulate fetching content (in real implementation, use web scraping)
        sample_content = {
            "renewable": """
            Solar Photovoltaic: Technology that converts sunlight directly into electricity using semiconductor materials.
            Wind Turbine: Device that converts kinetic energy from wind into electrical energy.
            Hydroelectric: Generation of electricity using flowing or falling water.
            Geothermal: Energy derived from heat stored in the earth.
            Biomass: Organic material used as fuel to produce electricity or heat.
            """,
            "fossil": """
            Coal: Combustible black or brownish-black sedimentary rock used for energy production.
            Natural Gas: Naturally occurring hydrocarbon gas mixture used for heating and electricity generation.
            Petroleum: Liquid fossil fuel derived from organic matter.
            Oil Shale: Fine-grained sedimentary rock containing organic matter that can be processed into oil.
            """,
            "nuclear": """
            Nuclear Reactor: Device used to initiate and control nuclear chain reactions.
            Uranium: Radioactive element used as fuel in nuclear reactors.
            Nuclear Fission: Process of splitting atomic nuclei to release energy.
            Enriched Uranium: Uranium with increased concentration of U-235 isotope.
            """,
            "alternative": """
            Hydrogen Fuel Cell: Device that converts hydrogen and oxygen into electricity.
            Biofuel: Fuel derived from biological materials.
            Synthetic Fuel: Artificially produced fuel from various feedstocks.
            Energy Storage: Technologies for storing energy for later use.
            """
        }
        
        return sample_content.get(fuel_group, "")
    
    @atlas_operation("ai_extraction", retry_attempts=3)
    async def _extract_terms_with_ai(
        self, 
        content: str, 
        fuel_group: str
    ) -> Dict[str, Any]:
        """
        Extract terms using AI with LangChain.
        
        Args:
            content: Raw glossary content
            fuel_group: Target fuel group
            
        Returns:
            Dict[str, Any]: Extraction results
        """
        
        extraction_prompt = f"""
        Extract energy terminology from the following glossary content for the {fuel_group} fuel group.
        
        For each term, provide:
        1. Term name
        2. Definition
        3. Technology type (if applicable)
        4. Efficiency rating (if mentioned)
        5. Environmental impact category
        6. Related terms
        
        Content:
        {content}
        
        Return results in JSON format with confidence scores.
        """
        
        result = await self.extraction_chain.extract(
            text=content,
            context={
                "domain": "energy",
                "fuel_group": fuel_group,
                "extraction_type": "comprehensive"
            },
            prompt_template=extraction_prompt
        )
        
        return result
    
    async def _create_nodes_from_extraction(
        self, 
        extraction_result: Dict[str, Any], 
        fuel_group: str
    ) -> List[ATLASNode]:
        """
        Create ATLAS nodes from AI extraction results.
        
        Args:
            extraction_result: Results from AI extraction
            fuel_group: Source fuel group
            
        Returns:
            List[ATLASNode]: Created nodes
        """
        
        nodes = []
        
        # Parse extraction results (simplified for example)
        terms = extraction_result.get("extracted_terms", [])
        
        for term_data in terms:
            try:
                # Determine fuel group enum
                fuel_group_enum = self._map_fuel_group(fuel_group)
                
                # Create node using configuration manager
                node = self.config_manager.create_energy_term(
                    term_name=term_data.get("name", "Unknown"),
                    definition=term_data.get("definition", ""),
                    fuel_group=fuel_group_enum,
                    additional_properties={
                        "technology_type": term_data.get("technology_type"),
                        "efficiency_rating": term_data.get("efficiency_rating"),
                        "environmental_impact": term_data.get("environmental_impact"),
                        "extraction_confidence": term_data.get("confidence", 0.8),
                        "source": "EIA_glossary",
                        "extracted_at": datetime.utcnow().isoformat(),
                        "ai_metadata": {
                            "model": "gpt-4-turbo",
                            "extraction_method": "langchain",
                            "confidence_score": term_data.get("confidence", 0.8)
                        }
                    }
                )
                
                nodes.append(node)
                
            except Exception as e:
                logger.error(f"Failed to create node for term {term_data}: {e}")
                continue
        
        return nodes
    
    @fabric_pattern("analyze_claims")
    async def _validate_nodes_with_fabric(
        self, 
        nodes: List[ATLASNode]
    ) -> List[ATLASNode]:
        """
        Validate nodes using FABRIC patterns.
        
        Args:
            nodes: Nodes to validate
            
        Returns:
            List[ATLASNode]: Validated nodes
        """
        
        print(f"🔍 Validating {len(nodes)} nodes with FABRIC patterns...")
        
        validated_nodes = []
        
        for node in nodes:
            try:
                # Use FABRIC analyze_claims pattern
                validation_context = {
                    "term_name": node.properties.get("term_name"),
                    "definition": node.properties.get("definition"),
                    "fuel_group": node.properties.get("fuel_group"),
                    "domain": "energy"
                }
                
                # Apply FABRIC pattern (simplified for example)
                validation_result = await self._apply_fabric_validation(
                    node, validation_context
                )
                
                # Update node with validation results
                node.properties.update({
                    "fabric_validation": validation_result,
                    "validation_confidence": validation_result.get("confidence", 0.8),
                    "validation_status": self._determine_validation_status(validation_result)
                })
                
                validated_nodes.append(node)
                
                # Track validation statistics
                status = validation_result.get("status", "unknown")
                if status not in self.extraction_stats["validation_results"]:
                    self.extraction_stats["validation_results"][status] = 0
                self.extraction_stats["validation_results"][status] += 1
                
            except Exception as e:
                logger.error(f"Validation failed for node {node.node_id}: {e}")
                # Keep node but mark validation as failed
                node.properties["validation_status"] = "validation_failed"
                validated_nodes.append(node)
        
        return validated_nodes
    
    async def _apply_fabric_validation(
        self, 
        node: ATLASNode, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply FABRIC pattern for validation.
        
        Args:
            node: Node to validate
            context: Validation context
            
        Returns:
            Dict[str, Any]: Validation results
        """
        
        # Simulate FABRIC pattern application
        validation_prompt = f"""
        Analyze the following energy term for accuracy and completeness:
        
        Term: {context['term_name']}
        Definition: {context['definition']}
        Fuel Group: {context['fuel_group']}
        
        Evaluate:
        1. Technical accuracy
        2. Definition completeness
        3. Proper categorization
        4. Industry standard compliance
        
        Provide confidence score and recommendations.
        """
        
        # In real implementation, this would use actual FABRIC patterns
        result = await self.validation_chain.validate(
            content=validation_prompt,
            context=context
        )
        
        return {
            "status": "validated",
            "confidence": result.get("confidence", 0.8),
            "accuracy_score": result.get("accuracy", 0.85),
            "completeness_score": result.get("completeness", 0.9),
            "recommendations": result.get("recommendations", []),
            "fabric_pattern": "analyze_claims"
        }
    
    async def _discover_relationships(
        self, 
        nodes: List[ATLASNode]
    ) -> List[Dict[str, Any]]:
        """
        Discover relationships between nodes using AI.
        
        Args:
            nodes: Nodes to analyze for relationships
            
        Returns:
            List[Dict[str, Any]]: Discovered relationships
        """
        
        print(f"🔗 Discovering relationships between {len(nodes)} nodes...")
        
        relationships = []
        
        # Analyze pairs of nodes for relationships
        for i, node1 in enumerate(nodes):
            for node2 in nodes[i+1:]:
                try:
                    relationship = await self._analyze_node_relationship(node1, node2)
                    if relationship and relationship.get("confidence", 0) > 0.7:
                        relationships.append(relationship)
                        
                except Exception as e:
                    logger.error(f"Relationship analysis failed: {e}")
                    continue
        
        return relationships
    
    async def _analyze_node_relationship(
        self, 
        node1: ATLASNode, 
        node2: ATLASNode
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze potential relationship between two nodes.
        
        Args:
            node1: First node
            node2: Second node
            
        Returns:
            Optional[Dict[str, Any]]: Relationship data if found
        """
        
        relationship_prompt = f"""
        Analyze the relationship between these two energy terms:
        
        Term 1: {node1.properties.get('term_name')}
        Definition 1: {node1.properties.get('definition')}
        Fuel Group 1: {node1.properties.get('fuel_group')}
        
        Term 2: {node2.properties.get('term_name')}
        Definition 2: {node2.properties.get('definition')}
        Fuel Group 2: {node2.properties.get('fuel_group')}
        
        Determine if there is a meaningful relationship and classify it:
        - RELATED_TO: General relationship
        - PART_OF: Hierarchical relationship
        - COMPETES_WITH: Competitive relationship
        - REQUIRES: Dependency relationship
        - PRODUCES: Production relationship
        
        Provide confidence score and explanation.
        """
        
        # Simulate AI relationship analysis
        result = await self.extraction_chain.extract(
            text=relationship_prompt,
            context={
                "analysis_type": "relationship_discovery",
                "node1_id": node1.node_id,
                "node2_id": node2.node_id
            }
        )
        
        # Parse result (simplified)
        if result.get("has_relationship", False):
            return {
                "source_node_id": node1.node_id,
                "target_node_id": node2.node_id,
                "relationship_type": result.get("relationship_type", "RELATED_TO"),
                "confidence": result.get("confidence", 0.8),
                "explanation": result.get("explanation", ""),
                "discovered_by": "ai_analysis",
                "discovered_at": datetime.utcnow().isoformat()
            }
        
        return None
    
    async def save_to_neo4j(
        self, 
        extracted_nodes: Dict[str, List[ATLASNode]],
        relationships: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Save extracted nodes and relationships to Neo4j.
        
        Args:
            extracted_nodes: Nodes organized by fuel group
            relationships: Optional relationships to save
            
        Returns:
            Dict[str, Any]: Save operation results
        """
        
        if not self.neo4j_driver:
            print("⚠️  Neo4j driver not configured, skipping graph save")
            return {"status": "skipped", "reason": "no_neo4j_driver"}
        
        print("💾 Saving to Neo4j graph database...")
        
        save_results = {
            "nodes_created": 0,
            "relationships_created": 0,
            "errors": []
        }
        
        try:
            # Save nodes
            all_nodes = []
            for fuel_group, nodes in extracted_nodes.items():
                all_nodes.extend(nodes)
            
            node_ids = await self.neo4j_driver.batch_create_nodes(all_nodes)
            save_results["nodes_created"] = len(node_ids)
            
            # Save relationships if provided
            if relationships:
                relationship_ids = await self.neo4j_driver.batch_create_relationships(relationships)
                save_results["relationships_created"] = len(relationship_ids)
            
            print(f"✅ Saved {save_results['nodes_created']} nodes and {save_results['relationships_created']} relationships")
            
        except Exception as e:
            error_msg = f"Neo4j save failed: {e}"
            logger.error(error_msg)
            save_results["errors"].append(error_msg)
        
        return save_results
    
    def _map_fuel_group(self, fuel_group_str: str) -> FuelGroupType:
        """Map string fuel group to enum."""
        mapping = {
            "renewable": FuelGroupType.RENEWABLE,
            "fossil": FuelGroupType.FOSSIL,
            "nuclear": FuelGroupType.NUCLEAR,
            "alternative": FuelGroupType.ALTERNATIVE
        }
        return mapping.get(fuel_group_str.lower(), FuelGroupType.ALTERNATIVE)
    
    def _determine_validation_status(self, validation_result: Dict[str, Any]) -> str:
        """Determine validation status from FABRIC results."""
        confidence = validation_result.get("confidence", 0.0)
        accuracy = validation_result.get("accuracy_score", 0.0)
        
        if confidence > 0.9 and accuracy > 0.9:
            return "approved"
        elif confidence > 0.7 and accuracy > 0.7:
            return "in_review"
        elif confidence > 0.5:
            return "requires_expert"
        else:
            return "rejected"
    
    def get_extraction_summary(self) -> Dict[str, Any]:
        """Get summary of extraction operations."""
        return {
            "extraction_stats": self.extraction_stats,
            "timestamp": datetime.utcnow().isoformat(),
            "configuration": {
                "ai_model": "gpt-4-turbo",
                "fabric_patterns": ["analyze_claims"],
                "neo4j_enabled": self.neo4j_driver is not None
            }
        }


async def main():
    """
    Main function demonstrating intermediate ATLAS Framework usage.
    """
    
    print("🚀 ATLAS Framework - Intermediate Example: Energy Taxonomy Extractor")
    print("=" * 70)
    
    # Setup paths
    config_path = Path(__file__).parent / "config" / "intermediate_config.json"
    output_path = Path(__file__).parent / "output"
    output_path.mkdir(exist_ok=True)
    
    # Create configuration if needed
    if not config_path.exists():
        await create_intermediate_config(config_path)
    
    # Initialize extractor
    extractor = EnergyTaxonomyExtractor(
        config_path=str(config_path),
        neo4j_uri=None  # Set to your Neo4j URI if available
    )
    
    # Extract taxonomy from EIA glossary
    fuel_groups = ["renewable", "fossil", "nuclear", "alternative"]
    extracted_nodes = await extractor.extract_from_eia_glossary(
        fuel_groups=fuel_groups
    )
    
    # Display results
    print("\n📊 Extraction Results Summary")
    print("=" * 40)
    
    total_nodes = 0
    for fuel_group, nodes in extracted_nodes.items():
        print(f"🔋 {fuel_group.title()}: {len(nodes)} terms")
        total_nodes += len(nodes)
    
    print(f"\n✅ Total extracted: {total_nodes} energy terms")
    
    # Show detailed statistics
    summary = extractor.get_extraction_summary()
    stats = summary["extraction_stats"]
    
    print(f"📈 Success rate: {stats['successful_extractions']}/{stats['total_processed']} ({stats['successful_extractions']/max(stats['total_processed'], 1)*100:.1f}%)")
    print(f"🔗 Relationships discovered: {stats['relationships_discovered']}")
    print(f"✅ Validation results: {stats['validation_results']}")
    
    # Save results to JSON
    output_file = output_path / f"extraction_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Prepare data for JSON serialization
    serializable_data = {}
    for fuel_group, nodes in extracted_nodes.items():
        serializable_data[fuel_group] = [
            {
                "node_id": node.node_id,
                "labels": [label.value for label in node.labels],
                "properties": node.properties,
                "behavior_count": len(node.behaviors)
            }
            for node in nodes
        ]
    
    # Add summary
    serializable_data["_summary"] = summary
    
    with open(output_file, 'w') as f:
        json.dump(serializable_data, f, indent=2, default=str)
    
    print(f"💾 Results saved to: {output_file}")
    
    # Demonstrate advanced features
    if extracted_nodes:
        print("\n🎯 Demonstrating Advanced Features")
        print("=" * 40)
        
        # Show first few nodes from each fuel group
        for fuel_group, nodes in extracted_nodes.items():
            if nodes:
                node = nodes[0]
                print(f"\n🔋 Sample {fuel_group} node:")
                print(f"   - Name: {node.properties.get('term_name')}")
                print(f"   - Definition: {node.properties.get('definition', '')[:100]}...")
                print(f"   - AI Confidence: {node.properties.get('extraction_confidence', 'N/A')}")
                print(f"   - Validation Status: {node.properties.get('validation_status', 'N/A')}")
                print(f"   - Behaviors: {len(node.behaviors)}")
    
    print("\n🎉 Intermediate example completed successfully!")
    print("🚀 Ready for enterprise-level examples!")


async def create_intermediate_config(config_path: Path) -> None:
    """Create intermediate configuration file."""
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    intermediate_config = {
        "version": "1.0",
        "metadata": {
            "name": "Intermediate ATLAS Configuration",
            "description": "AI-enhanced configuration for taxonomy extraction",
            "created": "2024-01-15T10:00:00Z"
        },
        "node_types": {
            "energy_term": {
                "description": "AI-extracted energy terminology",
                "labels": ["EnergyTerm", "TaxonomyNode"],
                "default_properties": {
                    "extraction_confidence": 0.8,
                    "validation_status": "pending",
                    "ai_extracted": True
                },
                "required_fields": ["term_name", "definition", "fuel_group"],
                "behaviors": [
                    {
                        "type": "computation",
                        "behavior_id": "ai_enhanced_computation",
                        "description": "AI-enhanced computation with validation",
                        "computation_function": "_compute_ai_metrics",
                        "cache_ttl": 600,
                        "priority": 50,
                        "parameters": {
                            "use_ai_validation": True,
                            "confidence_threshold": 0.8
                        }
                    },
                    {
                        "type": "analysis",
                        "behavior_id": "relationship_analysis",
                        "description": "AI-powered relationship discovery",
                        "analysis_type": "relationship_discovery",
                        "retry_attempts": 3,
                        "timeout_seconds": 45.0,
                        "priority": 75,
                        "parameters": {
                            "max_relationships": 10,
                            "confidence_threshold": 0.7
                        }
                    }
                ]
            }
        },
        "ai_settings": {
            "default_model": "gpt-4-turbo",
            "temperature": 0.1,
            "max_tokens": 2000,
            "confidence_threshold": 0.8
        },
        "fabric_settings": {
            "patterns_enabled": ["analyze_claims", "extract_wisdom", "create_summary"],
            "default_confidence": 0.8
        },
        "global_settings": {
            "default_cache_ttl": 600,
            "max_behavior_execution_time": 120,
            "validation_strictness": "high",
            "enable_ai_features": True
        }
    }
    
    with open(config_path, 'w') as f:
        json.dump(intermediate_config, f, indent=2)
    
    print(f"📝 Created intermediate configuration at: {config_path}")


if __name__ == "__main__":
    """Run the intermediate example."""
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Example interrupted by user")
    except Exception as e:
        logger.error(f"Intermediate example failed: {e}")
        print(f"\n❌ Example failed: {e}")
        raise

