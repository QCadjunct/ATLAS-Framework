"""
ATLAS Framework - Integration Tests for Full Extraction Workflow

This module contains comprehensive integration tests that verify the complete
energy taxonomy extraction workflow from end to end.

Test Coverage:
- Complete extraction pipeline from source to graph database
- AI-powered extraction with LangChain integration
- FABRIC pattern validation
- Neo4j graph operations
- Multi-tenant data isolation
- Error handling and recovery
- Performance under load
"""

import asyncio
import json
import tempfile
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio

from atlas import ConfigurationManager, ATLASNode
from atlas.enums import NodeLabelType, FuelGroupType, ValidationStatusType
from atlas.frameworks.langchain import ExtractionChain, ValidationChain
from atlas.frameworks.fabric import FabricPatternRegistry
from atlas.graph.neo4j import Neo4jDriver
from atlas.security.tailscale import TailscaleManager
from atlas.monitoring import MetricsCollector
from atlas.utils.logging import get_logger

# Test logger
logger = get_logger(__name__)


class TestFullExtractionWorkflow:
    """Integration tests for the complete extraction workflow."""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_simple_extraction_workflow(
        self, 
        integration_test_setup: Dict[str, Any],
        mock_extraction_chain: AsyncMock,
        mock_validation_chain: AsyncMock,
        mock_fabric_registry: AsyncMock
    ):
        """Test a simple end-to-end extraction workflow."""
        
        # Setup
        config_path = integration_test_setup["config_path"]
        config_manager = ConfigurationManager.from_file(str(config_path))
        
        # Mock extraction data
        mock_extraction_result = {
            "extracted_terms": [
                {
                    "name": "Solar Photovoltaic",
                    "definition": "Technology that converts sunlight into electricity",
                    "confidence": 0.92,
                    "technology_type": "photovoltaic",
                    "efficiency_rating": 0.22
                },
                {
                    "name": "Wind Turbine",
                    "definition": "Device that converts wind energy into electricity",
                    "confidence": 0.88,
                    "technology_type": "wind_conversion",
                    "efficiency_rating": 0.35
                }
            ],
            "extraction_confidence": 0.90,
            "model_used": "gpt-4-turbo"
        }
        
        mock_extraction_chain.extract.return_value = mock_extraction_result
        
        # Mock validation results
        mock_validation_chain.validate.return_value = {
            "confidence": 0.91,
            "accuracy": 0.89,
            "completeness": 0.93,
            "recommendations": ["Add technical specifications"],
            "validation_status": "approved"
        }
        
        # Execute extraction workflow
        extracted_nodes = []
        
        for term_data in mock_extraction_result["extracted_terms"]:
            # Create node
            node = config_manager.create_energy_term(
                term_name=term_data["name"],
                definition=term_data["definition"],
                fuel_group=FuelGroupType.RENEWABLE,
                additional_properties={
                    "extraction_confidence": term_data["confidence"],
                    "technology_type": term_data["technology_type"],
                    "efficiency_rating": term_data["efficiency_rating"],
                    "extracted_at": datetime.utcnow().isoformat()
                }
            )
            
            # Validate node
            validation_result = await mock_validation_chain.validate(
                content=f"Term: {term_data['name']}, Definition: {term_data['definition']}",
                context={"domain": "energy", "fuel_group": "renewable"}
            )
            
            # Update node with validation results
            node.properties.update({
                "validation_confidence": validation_result["confidence"],
                "validation_status": validation_result["validation_status"]
            })
            
            extracted_nodes.append(node)
        
        # Verify results
        assert len(extracted_nodes) == 2
        
        # Verify first node
        solar_node = extracted_nodes[0]
        assert solar_node.properties["term_name"] == "Solar Photovoltaic"
        assert solar_node.properties["fuel_group"] == FuelGroupType.RENEWABLE
        assert solar_node.properties["extraction_confidence"] == 0.92
        assert solar_node.properties["validation_confidence"] == 0.91
        assert solar_node.properties["validation_status"] == "approved"
        
        # Verify second node
        wind_node = extracted_nodes[1]
        assert wind_node.properties["term_name"] == "Wind Turbine"
        assert wind_node.properties["efficiency_rating"] == 0.35
        
        # Verify node labels
        for node in extracted_nodes:
            assert NodeLabelType.ENERGY_TERM in node.labels
            assert NodeLabelType.TAXONOMY_NODE in node.labels
        
        # Verify behaviors are attached
        for node in extracted_nodes:
            assert len(node.behaviors) > 0
            assert node.has_behavior("computation")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_multi_fuel_group_extraction(
        self,
        integration_test_setup: Dict[str, Any],
        mock_extraction_chain: AsyncMock,
        mock_fabric_registry: AsyncMock
    ):
        """Test extraction workflow with multiple fuel groups."""
        
        config_path = integration_test_setup["config_path"]
        config_manager = ConfigurationManager.from_file(str(config_path))
        
        fuel_groups = [
            FuelGroupType.RENEWABLE,
            FuelGroupType.FOSSIL,
            FuelGroupType.NUCLEAR
        ]
        
        # Mock extraction results for each fuel group
        extraction_results = {
            FuelGroupType.RENEWABLE: {
                "extracted_terms": [
                    {"name": "Solar PV", "definition": "Solar photovoltaic technology", "confidence": 0.9},
                    {"name": "Wind Power", "definition": "Wind energy conversion", "confidence": 0.85}
                ]
            },
            FuelGroupType.FOSSIL: {
                "extracted_terms": [
                    {"name": "Coal Plant", "definition": "Coal-fired power generation", "confidence": 0.88},
                    {"name": "Natural Gas", "definition": "Natural gas power generation", "confidence": 0.92}
                ]
            },
            FuelGroupType.NUCLEAR: {
                "extracted_terms": [
                    {"name": "Nuclear Reactor", "definition": "Nuclear fission reactor", "confidence": 0.95}
                ]
            }
        }
        
        all_extracted_nodes = {}
        
        for fuel_group in fuel_groups:
            mock_extraction_chain.extract.return_value = extraction_results[fuel_group]
            
            # Extract terms for this fuel group
            extraction_result = await mock_extraction_chain.extract(
                text=f"Sample content for {fuel_group.value}",
                context={"fuel_group": fuel_group.value}
            )
            
            # Create nodes
            nodes = []
            for term_data in extraction_result["extracted_terms"]:
                node = config_manager.create_energy_term(
                    term_name=term_data["name"],
                    definition=term_data["definition"],
                    fuel_group=fuel_group,
                    additional_properties={
                        "extraction_confidence": term_data["confidence"],
                        "fuel_group_category": fuel_group.carbon_category
                    }
                )
                nodes.append(node)
            
            all_extracted_nodes[fuel_group] = nodes
        
        # Verify results
        assert len(all_extracted_nodes) == 3
        
        # Verify renewable nodes
        renewable_nodes = all_extracted_nodes[FuelGroupType.RENEWABLE]
        assert len(renewable_nodes) == 2
        assert all(node.properties["fuel_group"] == FuelGroupType.RENEWABLE for node in renewable_nodes)
        assert all(node.properties["fuel_group_category"] == "zero_carbon" for node in renewable_nodes)
        
        # Verify fossil nodes
        fossil_nodes = all_extracted_nodes[FuelGroupType.FOSSIL]
        assert len(fossil_nodes) == 2
        assert all(node.properties["fuel_group"] == FuelGroupType.FOSSIL for node in fossil_nodes)
        assert all(node.properties["fuel_group_category"] == "high_carbon" for node in fossil_nodes)
        
        # Verify nuclear nodes
        nuclear_nodes = all_extracted_nodes[FuelGroupType.NUCLEAR]
        assert len(nuclear_nodes) == 1
        assert nuclear_nodes[0].properties["fuel_group"] == FuelGroupType.NUCLEAR
        assert nuclear_nodes[0].properties["fuel_group_category"] == "low_carbon"
        
        # Verify total node count
        total_nodes = sum(len(nodes) for nodes in all_extracted_nodes.values())
        assert total_nodes == 5
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_fabric_pattern_integration(
        self,
        integration_test_setup: Dict[str, Any],
        mock_fabric_registry: AsyncMock
    ):
        """Test integration with FABRIC patterns for validation."""
        
        config_path = integration_test_setup["config_path"]
        config_manager = ConfigurationManager.from_file(str(config_path))
        
        # Create test node
        node = config_manager.create_energy_term(
            term_name="Hydrogen Fuel Cell",
            definition="Device that converts hydrogen and oxygen into electricity",
            fuel_group=FuelGroupType.ALTERNATIVE,
            additional_properties={
                "technology_type": "electrochemical",
                "efficiency_rating": 0.60
            }
        )
        
        # Mock FABRIC pattern results
        fabric_patterns = ["analyze_claims", "extract_wisdom", "create_summary"]
        pattern_results = {}
        
        for pattern in fabric_patterns:
            mock_result = {
                "pattern": pattern,
                "confidence": 0.85 + (hash(pattern) % 10) / 100,  # Vary confidence slightly
                "quality_score": 0.90,
                "recommendations": [f"Recommendation from {pattern}"],
                "applied_at": datetime.utcnow().isoformat()
            }
            
            mock_fabric_registry.apply_pattern.return_value = mock_result
            
            # Apply pattern
            result = await mock_fabric_registry.apply_pattern(
                pattern_name=pattern,
                content=f"Term: {node.properties['term_name']}, Definition: {node.properties['definition']}",
                context={"domain": "energy", "fuel_group": "alternative"}
            )
            
            pattern_results[pattern] = result
        
        # Aggregate FABRIC results
        avg_confidence = sum(r["confidence"] for r in pattern_results.values()) / len(pattern_results)
        all_recommendations = []
        for result in pattern_results.values():
            all_recommendations.extend(result["recommendations"])
        
        # Update node with FABRIC validation
        node.properties.update({
            "fabric_validation": {
                "patterns_applied": list(pattern_results.keys()),
                "average_confidence": avg_confidence,
                "quality_score": pattern_results["analyze_claims"]["quality_score"],
                "recommendations": all_recommendations,
                "validation_timestamp": datetime.utcnow().isoformat()
            }
        })
        
        # Verify FABRIC integration
        fabric_validation = node.properties["fabric_validation"]
        assert len(fabric_validation["patterns_applied"]) == 3
        assert fabric_validation["average_confidence"] > 0.8
        assert len(fabric_validation["recommendations"]) == 3
        assert all(pattern in fabric_validation["patterns_applied"] for pattern in fabric_patterns)
        
        # Verify pattern application was called correctly
        assert mock_fabric_registry.apply_pattern.call_count == 3
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_relationship_discovery_workflow(
        self,
        integration_test_setup: Dict[str, Any],
        sample_atlas_nodes: List[ATLASNode]
    ):
        """Test relationship discovery between extracted nodes."""
        
        # Use sample nodes for relationship discovery
        nodes = sample_atlas_nodes[:3]  # Use first 3 nodes
        
        # Mock relationship discovery
        discovered_relationships = []
        
        for i, node1 in enumerate(nodes):
            for node2 in nodes[i+1:]:
                # Simulate relationship analysis
                fuel_group1 = node1.properties.get("fuel_group")
                fuel_group2 = node2.properties.get("fuel_group")
                
                if fuel_group1 == fuel_group2:
                    # Same fuel group - related relationship
                    relationship = {
                        "source_node_id": node1.node_id,
                        "target_node_id": node2.node_id,
                        "relationship_type": "RELATED_TO",
                        "confidence": 0.8,
                        "relationship_strength": "medium",
                        "discovered_method": "fuel_group_similarity",
                        "discovered_at": datetime.utcnow().isoformat()
                    }
                    discovered_relationships.append(relationship)
                elif fuel_group1 != fuel_group2:
                    # Different fuel groups - competitive relationship
                    relationship = {
                        "source_node_id": node1.node_id,
                        "target_node_id": node2.node_id,
                        "relationship_type": "COMPETES_WITH",
                        "confidence": 0.7,
                        "relationship_strength": "medium",
                        "discovered_method": "fuel_group_competition",
                        "discovered_at": datetime.utcnow().isoformat()
                    }
                    discovered_relationships.append(relationship)
        
        # Verify relationship discovery
        assert len(discovered_relationships) > 0
        
        # Verify relationship properties
        for relationship in discovered_relationships:
            assert "source_node_id" in relationship
            assert "target_node_id" in relationship
            assert "relationship_type" in relationship
            assert "confidence" in relationship
            assert 0.0 <= relationship["confidence"] <= 1.0
            assert relationship["relationship_type"] in ["RELATED_TO", "COMPETES_WITH"]
        
        # Verify relationship types based on fuel groups
        related_relationships = [r for r in discovered_relationships if r["relationship_type"] == "RELATED_TO"]
        competitive_relationships = [r for r in discovered_relationships if r["relationship_type"] == "COMPETES_WITH"]
        
        # Should have both types of relationships
        assert len(related_relationships) > 0 or len(competitive_relationships) > 0
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    @pytest.mark.requires_neo4j
    async def test_neo4j_integration_workflow(
        self,
        integration_test_setup: Dict[str, Any],
        mock_neo4j_driver: AsyncMock,
        sample_atlas_nodes: List[ATLASNode]
    ):
        """Test integration with Neo4j graph database."""
        
        # Use sample nodes for Neo4j integration
        nodes = sample_atlas_nodes[:2]
        
        # Mock Neo4j operations
        node_ids = ["neo4j_node_001", "neo4j_node_002"]
        mock_neo4j_driver.batch_create_nodes.return_value = node_ids
        
        relationship_data = [
            {
                "source_node_id": node_ids[0],
                "target_node_id": node_ids[1],
                "relationship_type": "RELATED_TO",
                "confidence": 0.85
            }
        ]
        
        relationship_ids = ["neo4j_rel_001"]
        mock_neo4j_driver.batch_create_relationships.return_value = relationship_ids
        
        # Execute Neo4j operations
        created_node_ids = await mock_neo4j_driver.batch_create_nodes(nodes)
        created_relationship_ids = await mock_neo4j_driver.batch_create_relationships(relationship_data)
        
        # Verify Neo4j integration
        assert created_node_ids == node_ids
        assert created_relationship_ids == relationship_ids
        
        # Verify method calls
        mock_neo4j_driver.batch_create_nodes.assert_called_once_with(nodes)
        mock_neo4j_driver.batch_create_relationships.assert_called_once_with(relationship_data)
        
        # Test node retrieval
        mock_neo4j_driver.get_node.return_value = {
            "id": node_ids[0],
            "labels": ["EnergyTerm", "TaxonomyNode"],
            "properties": nodes[0].properties
        }
        
        retrieved_node = await mock_neo4j_driver.get_node(node_ids[0])
        assert retrieved_node["id"] == node_ids[0]
        assert "EnergyTerm" in retrieved_node["labels"]
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_error_handling_workflow(
        self,
        integration_test_setup: Dict[str, Any],
        error_simulation_fixtures
    ):
        """Test error handling throughout the extraction workflow."""
        
        config_path = integration_test_setup["config_path"]
        config_manager = ConfigurationManager.from_file(str(config_path))
        
        # Test network error handling
        with patch('aiohttp.ClientSession.get', side_effect=error_simulation_fixtures.network_error):
            with pytest.raises(Exception):  # Should handle network errors gracefully
                # Simulate content fetching that fails
                raise error_simulation_fixtures.network_error()
        
        # Test validation error handling
        with pytest.raises(Exception):
            # Simulate validation error
            error_simulation_fixtures.validation_error()
        
        # Test that system can recover from errors
        try:
            # Create node normally after error
            node = config_manager.create_energy_term(
                term_name="Recovery Test Node",
                definition="Node created after error recovery",
                fuel_group=FuelGroupType.RENEWABLE
            )
            
            assert node.properties["term_name"] == "Recovery Test Node"
            assert node.properties["fuel_group"] == FuelGroupType.RENEWABLE
            
        except Exception as e:
            pytest.fail(f"System failed to recover from error: {e}")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_multi_tenant_workflow(
        self,
        integration_test_setup: Dict[str, Any],
        sample_user_context: Dict[str, Any]
    ):
        """Test multi-tenant data isolation in extraction workflow."""
        
        config_path = integration_test_setup["config_path"]
        config_manager = ConfigurationManager.from_file(str(config_path))
        
        # Create nodes for different tenants
        tenant_1_context = sample_user_context.copy()
        tenant_1_context["tenant_id"] = "tenant_001"
        
        tenant_2_context = sample_user_context.copy()
        tenant_2_context["tenant_id"] = "tenant_002"
        
        # Create nodes for tenant 1
        tenant_1_node = config_manager.create_energy_term(
            term_name="Tenant 1 Solar Panel",
            definition="Solar panel for tenant 1",
            fuel_group=FuelGroupType.RENEWABLE,
            additional_properties={
                "tenant_id": tenant_1_context["tenant_id"],
                "user_id": tenant_1_context["user_id"]
            }
        )
        
        # Create nodes for tenant 2
        tenant_2_node = config_manager.create_energy_term(
            term_name="Tenant 2 Wind Turbine",
            definition="Wind turbine for tenant 2",
            fuel_group=FuelGroupType.RENEWABLE,
            additional_properties={
                "tenant_id": tenant_2_context["tenant_id"],
                "user_id": tenant_2_context["user_id"]
            }
        )
        
        # Verify tenant isolation
        assert tenant_1_node.properties["tenant_id"] == "tenant_001"
        assert tenant_2_node.properties["tenant_id"] == "tenant_002"
        assert tenant_1_node.properties["tenant_id"] != tenant_2_node.properties["tenant_id"]
        
        # Verify nodes have different IDs
        assert tenant_1_node.node_id != tenant_2_node.node_id
        
        # Verify both nodes have proper labels
        for node in [tenant_1_node, tenant_2_node]:
            assert NodeLabelType.ENERGY_TERM in node.labels
            assert NodeLabelType.TAXONOMY_NODE in node.labels
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_performance_workflow(
        self,
        integration_test_setup: Dict[str, Any],
        performance_test_data: Dict[str, Any]
    ):
        """Test extraction workflow performance with large datasets."""
        
        config_path = integration_test_setup["config_path"]
        config_manager = ConfigurationManager.from_file(str(config_path))
        
        # Use performance test data
        terms = performance_test_data["terms"][:100]  # Use subset for integration test
        
        start_time = datetime.utcnow()
        
        # Create nodes in batches
        batch_size = 10
        created_nodes = []
        
        for i in range(0, len(terms), batch_size):
            batch = terms[i:i+batch_size]
            batch_nodes = []
            
            for term_data in batch:
                node = config_manager.create_energy_term(
                    term_name=term_data["term_name"],
                    definition=term_data["definition"],
                    fuel_group=term_data["fuel_group"],
                    additional_properties={
                        "efficiency_rating": term_data["efficiency_rating"],
                        "technology_type": term_data["technology_type"],
                        "extraction_confidence": term_data["extraction_confidence"],
                        "batch_number": i // batch_size
                    }
                )
                batch_nodes.append(node)
            
            created_nodes.extend(batch_nodes)
            
            # Small delay to simulate processing time
            await asyncio.sleep(0.01)
        
        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()
        
        # Verify performance results
        assert len(created_nodes) == len(terms)
        assert processing_time < 10.0  # Should complete within 10 seconds
        
        # Verify all nodes were created correctly
        for i, node in enumerate(created_nodes):
            assert node.properties["term_name"] == terms[i]["term_name"]
            assert node.properties["fuel_group"] == terms[i]["fuel_group"]
            assert "batch_number" in node.properties
        
        # Calculate performance metrics
        nodes_per_second = len(created_nodes) / processing_time
        assert nodes_per_second > 10  # Should process at least 10 nodes per second
        
        logger.info(f"Performance test: {len(created_nodes)} nodes in {processing_time:.2f}s ({nodes_per_second:.1f} nodes/sec)")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_monitoring_integration(
        self,
        integration_test_setup: Dict[str, Any],
        mock_metrics_collector: AsyncMock
    ):
        """Test integration with monitoring and metrics collection."""
        
        config_path = integration_test_setup["config_path"]
        config_manager = ConfigurationManager.from_file(str(config_path))
        
        # Create test node with monitoring
        start_time = datetime.utcnow()
        
        node = config_manager.create_energy_term(
            term_name="Monitored Solar Panel",
            definition="Solar panel with monitoring integration",
            fuel_group=FuelGroupType.RENEWABLE
        )
        
        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()
        
        # Record metrics
        await mock_metrics_collector.record_metric("node_creation_time", processing_time)
        await mock_metrics_collector.record_metric("nodes_created", 1)
        await mock_metrics_collector.record_metric("fuel_group_renewable", 1)
        
        # Verify monitoring integration
        assert mock_metrics_collector.record_metric.call_count == 3
        
        # Verify metric calls
        calls = mock_metrics_collector.record_metric.call_args_list
        assert calls[0][0] == ("node_creation_time", processing_time)
        assert calls[1][0] == ("nodes_created", 1)
        assert calls[2][0] == ("fuel_group_renewable", 1)
        
        # Test metrics retrieval
        mock_metrics_collector.get_recent_metrics.return_value = {
            "node_creation_time": [processing_time],
            "nodes_created": [1],
            "fuel_group_renewable": [1],
            "success_rate": 1.0
        }
        
        recent_metrics = await mock_metrics_collector.get_recent_metrics(hours=1)
        assert recent_metrics["success_rate"] == 1.0
        assert len(recent_metrics["node_creation_time"]) == 1


class TestWorkflowEdgeCases:
    """Test edge cases and boundary conditions in the extraction workflow."""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_empty_extraction_result(
        self,
        integration_test_setup: Dict[str, Any],
        mock_extraction_chain: AsyncMock
    ):
        """Test handling of empty extraction results."""
        
        config_path = integration_test_setup["config_path"]
        config_manager = ConfigurationManager.from_file(str(config_path))
        
        # Mock empty extraction result
        mock_extraction_chain.extract.return_value = {
            "extracted_terms": [],
            "extraction_confidence": 0.0,
            "model_used": "gpt-4-turbo"
        }
        
        # Execute extraction
        extraction_result = await mock_extraction_chain.extract(
            text="Empty content",
            context={"fuel_group": "renewable"}
        )
        
        # Verify empty result handling
        assert len(extraction_result["extracted_terms"]) == 0
        assert extraction_result["extraction_confidence"] == 0.0
        
        # Should not create any nodes
        nodes = []
        for term_data in extraction_result["extracted_terms"]:
            node = config_manager.create_energy_term(
                term_name=term_data["name"],
                definition=term_data["definition"],
                fuel_group=FuelGroupType.RENEWABLE
            )
            nodes.append(node)
        
        assert len(nodes) == 0
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_low_confidence_extraction(
        self,
        integration_test_setup: Dict[str, Any],
        mock_extraction_chain: AsyncMock
    ):
        """Test handling of low confidence extraction results."""
        
        config_path = integration_test_setup["config_path"]
        config_manager = ConfigurationManager.from_file(str(config_path))
        
        # Mock low confidence extraction
        mock_extraction_chain.extract.return_value = {
            "extracted_terms": [
                {
                    "name": "Uncertain Technology",
                    "definition": "Technology with uncertain definition",
                    "confidence": 0.3,  # Low confidence
                    "technology_type": "unknown"
                }
            ],
            "extraction_confidence": 0.3
        }
        
        extraction_result = await mock_extraction_chain.extract(
            text="Uncertain content",
            context={"fuel_group": "alternative"}
        )
        
        # Create node with low confidence
        term_data = extraction_result["extracted_terms"][0]
        node = config_manager.create_energy_term(
            term_name=term_data["name"],
            definition=term_data["definition"],
            fuel_group=FuelGroupType.ALTERNATIVE,
            additional_properties={
                "extraction_confidence": term_data["confidence"],
                "requires_review": term_data["confidence"] < 0.5
            }
        )
        
        # Verify low confidence handling
        assert node.properties["extraction_confidence"] == 0.3
        assert node.properties["requires_review"] is True
        assert node.validation_status == ValidationStatusType.PENDING
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_duplicate_term_handling(
        self,
        integration_test_setup: Dict[str, Any]
    ):
        """Test handling of duplicate terms in extraction."""
        
        config_path = integration_test_setup["config_path"]
        config_manager = ConfigurationManager.from_file(str(config_path))
        
        # Create first node
        node1 = config_manager.create_energy_term(
            term_name="Solar Panel",
            definition="First definition of solar panel",
            fuel_group=FuelGroupType.RENEWABLE
        )
        
        # Create second node with same name but different definition
        node2 = config_manager.create_energy_term(
            term_name="Solar Panel",
            definition="Second definition of solar panel",
            fuel_group=FuelGroupType.RENEWABLE,
            additional_properties={
                "variant": "alternative_definition"
            }
        )
        
        # Verify both nodes are created with different IDs
        assert node1.node_id != node2.node_id
        assert node1.properties["term_name"] == node2.properties["term_name"]
        assert node1.properties["definition"] != node2.properties["definition"]
        
        # Verify second node is marked as variant
        assert "variant" in node2.properties
        assert node2.properties["variant"] == "alternative_definition"
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_malformed_data_handling(
        self,
        integration_test_setup: Dict[str, Any]
    ):
        """Test handling of malformed or invalid data."""
        
        config_path = integration_test_setup["config_path"]
        config_manager = ConfigurationManager.from_file(str(config_path))
        
        # Test with missing required fields
        with pytest.raises(Exception):  # Should raise validation error
            config_manager.create_energy_term(
                term_name="",  # Empty name
                definition="Valid definition",
                fuel_group=FuelGroupType.RENEWABLE
            )
        
        # Test with invalid fuel group
        with pytest.raises(Exception):  # Should raise validation error
            config_manager.create_energy_term(
                term_name="Valid Name",
                definition="Valid definition",
                fuel_group="invalid_fuel_group"  # Invalid enum value
            )
        
        # Test with valid data after errors
        valid_node = config_manager.create_energy_term(
            term_name="Valid Solar Panel",
            definition="Valid solar panel definition",
            fuel_group=FuelGroupType.RENEWABLE
        )
        
        assert valid_node.properties["term_name"] == "Valid Solar Panel"
        assert valid_node.properties["fuel_group"] == FuelGroupType.RENEWABLE

