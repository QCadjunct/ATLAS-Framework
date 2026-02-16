"""
ATLAS Framework - Test Configuration and Fixtures

This module provides comprehensive test configuration and fixtures for the ATLAS Framework.
Includes fixtures for all major components, mock services, and test utilities.

Requirements:
- pytest >= 7.0.0
- pytest-asyncio >= 0.21.0
- pytest-mock >= 3.10.0
- pytest-cov >= 4.0.0
"""

import asyncio
import json
import tempfile
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional, AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta

import pytest
import pytest_asyncio
from pydantic import BaseModel

# ATLAS Framework imports
from atlas import ConfigurationManager, ATLASNode
from atlas.enums import NodeLabelType, FuelGroupType, ValidationStatusType, RelationshipType
from atlas.models.behaviors import ComputationBehavior, AnalysisBehavior
from atlas.models.validation import ValidationResult
from atlas.security.tailscale import TailscaleManager
from atlas.security.auth import JWTAuthProvider, PermissionManager
from atlas.graph.neo4j import Neo4jDriver, Neo4jCluster
from atlas.frameworks.langchain import ExtractionChain, ValidationChain
from atlas.frameworks.fabric import FabricPatternRegistry
from atlas.monitoring import MetricsCollector, AlertManager
from atlas.utils.logging import get_logger

# Test logger
logger = get_logger(__name__)


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "enterprise: mark test as an enterprise feature test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "requires_neo4j: mark test as requiring Neo4j database"
    )
    config.addinivalue_line(
        "markers", "requires_redis: mark test as requiring Redis"
    )
    config.addinivalue_line(
        "markers", "requires_tailscale: mark test as requiring Tailscale VPN"
    )
    config.addinivalue_line(
        "markers", "requires_openai: mark test as requiring OpenAI API"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names and paths."""
    
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "enterprise" in str(item.fspath):
            item.add_marker(pytest.mark.enterprise)
        
        # Add markers based on test name patterns
        if "slow" in item.name or "performance" in item.name:
            item.add_marker(pytest.mark.slow)
        
        if "neo4j" in item.name.lower():
            item.add_marker(pytest.mark.requires_neo4j)
        
        if "redis" in item.name.lower():
            item.add_marker(pytest.mark.requires_redis)
        
        if "tailscale" in item.name.lower():
            item.add_marker(pytest.mark.requires_tailscale)
        
        if "openai" in item.name.lower() or "ai" in item.name.lower():
            item.add_marker(pytest.mark.requires_openai)


# ============================================================================
# Event Loop and Async Configuration
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# Configuration Fixtures
# ============================================================================

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_config_data() -> Dict[str, Any]:
    """Provide sample configuration data for testing."""
    
    return {
        "version": "1.0",
        "metadata": {
            "name": "Test ATLAS Configuration",
            "description": "Configuration for unit testing",
            "created": "2024-01-15T10:00:00Z"
        },
        "node_types": {
            "energy_term": {
                "description": "Test energy terminology nodes",
                "labels": ["EnergyTerm", "TaxonomyNode"],
                "default_properties": {
                    "extraction_confidence": 0.8,
                    "validation_status": "pending"
                },
                "required_fields": ["term_name", "definition", "fuel_group"],
                "behaviors": [
                    {
                        "type": "computation",
                        "behavior_id": "test_computation",
                        "description": "Test computation behavior",
                        "computation_function": "_compute_test_metrics",
                        "cache_ttl": 300,
                        "priority": 100,
                        "parameters": {
                            "test_mode": True,
                            "mock_results": True
                        }
                    }
                ]
            }
        },
        "global_settings": {
            "default_cache_ttl": 300,
            "max_behavior_execution_time": 60,
            "validation_strictness": "medium",
            "test_mode": True
        }
    }


@pytest.fixture
def config_file(temp_dir: Path, sample_config_data: Dict[str, Any]) -> Path:
    """Create a temporary configuration file for testing."""
    
    config_path = temp_dir / "test_config.json"
    
    with open(config_path, 'w') as f:
        json.dump(sample_config_data, f, indent=2)
    
    return config_path


@pytest.fixture
def config_manager(config_file: Path) -> ConfigurationManager:
    """Create a ConfigurationManager instance for testing."""
    
    return ConfigurationManager.from_file(str(config_file))


# ============================================================================
# Node and Data Fixtures
# ============================================================================

@pytest.fixture
def sample_energy_terms() -> List[Dict[str, Any]]:
    """Provide sample energy term data for testing."""
    
    return [
        {
            "term_name": "Solar Photovoltaic",
            "definition": "Technology that converts sunlight directly into electricity",
            "fuel_group": FuelGroupType.RENEWABLE,
            "efficiency_rating": 0.22,
            "technology_type": "crystalline_silicon"
        },
        {
            "term_name": "Wind Turbine",
            "definition": "Device that converts wind energy into electrical energy",
            "fuel_group": FuelGroupType.RENEWABLE,
            "efficiency_rating": 0.35,
            "technology_type": "horizontal_axis"
        },
        {
            "term_name": "Coal Power Plant",
            "definition": "Thermal power station that burns coal to generate electricity",
            "fuel_group": FuelGroupType.FOSSIL,
            "efficiency_rating": 0.33,
            "carbon_intensity": 820.0
        },
        {
            "term_name": "Nuclear Reactor",
            "definition": "Device used to initiate and control nuclear chain reactions",
            "fuel_group": FuelGroupType.NUCLEAR,
            "efficiency_rating": 0.33,
            "fuel_type": "enriched_uranium"
        }
    ]


@pytest.fixture
def sample_atlas_nodes(
    config_manager: ConfigurationManager, 
    sample_energy_terms: List[Dict[str, Any]]
) -> List[ATLASNode]:
    """Create sample ATLAS nodes for testing."""
    
    nodes = []
    
    for term_data in sample_energy_terms:
        node = config_manager.create_energy_term(
            term_name=term_data["term_name"],
            definition=term_data["definition"],
            fuel_group=term_data["fuel_group"],
            additional_properties={
                k: v for k, v in term_data.items() 
                if k not in ["term_name", "definition", "fuel_group"]
            }
        )
        nodes.append(node)
    
    return nodes


@pytest.fixture
def sample_relationships() -> List[Dict[str, Any]]:
    """Provide sample relationship data for testing."""
    
    return [
        {
            "source_node_id": "node_001",
            "target_node_id": "node_002",
            "relationship_type": RelationshipType.RELATED_TO,
            "confidence": 0.85,
            "discovered_method": "test_analysis"
        },
        {
            "source_node_id": "node_002",
            "target_node_id": "node_003",
            "relationship_type": RelationshipType.COMPETES_WITH,
            "confidence": 0.75,
            "discovered_method": "test_analysis"
        }
    ]


# ============================================================================
# Mock Service Fixtures
# ============================================================================

@pytest.fixture
def mock_neo4j_driver():
    """Create a mock Neo4j driver for testing."""
    
    mock_driver = AsyncMock(spec=Neo4jDriver)
    
    # Mock common methods
    mock_driver.create_node.return_value = "mock_node_id"
    mock_driver.batch_create_nodes.return_value = ["node_001", "node_002", "node_003"]
    mock_driver.create_relationship.return_value = "mock_relationship_id"
    mock_driver.batch_create_relationships.return_value = ["rel_001", "rel_002"]
    mock_driver.get_node.return_value = {"id": "mock_node_id", "properties": {}}
    mock_driver.query_nodes.return_value = []
    mock_driver.close.return_value = None
    
    return mock_driver


@pytest.fixture
def mock_neo4j_cluster():
    """Create a mock Neo4j cluster for testing."""
    
    mock_cluster = AsyncMock(spec=Neo4jCluster)
    
    # Mock cluster methods
    mock_cluster.initialize_cluster.return_value = None
    mock_cluster.get_cluster_status.return_value = {
        "active_nodes": 3,
        "cluster_health": "healthy",
        "leader_node": "neo4j-1"
    }
    mock_cluster.get_tenant_driver.return_value = AsyncMock(spec=Neo4jDriver)
    mock_cluster.close_all_connections.return_value = None
    
    return mock_cluster


@pytest.fixture
def mock_redis_pool():
    """Create a mock Redis connection pool for testing."""
    
    mock_pool = AsyncMock()
    
    # Mock Redis operations
    mock_redis = AsyncMock()
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    mock_redis.delete.return_value = 1
    mock_redis.ping.return_value = True
    
    mock_pool.__aenter__.return_value = mock_redis
    mock_pool.__aexit__.return_value = None
    
    return mock_pool


@pytest.fixture
def mock_tailscale_manager():
    """Create a mock Tailscale manager for testing."""
    
    mock_manager = AsyncMock(spec=TailscaleManager)
    
    # Mock Tailscale methods
    mock_manager.connect.return_value = None
    mock_manager.get_network_status.return_value = {
        "connected": True,
        "network_name": "test-tailnet",
        "device_ip": "100.64.0.1"
    }
    mock_manager.execute_command.return_value = {"success": True, "output": ""}
    mock_manager.enabled = True
    mock_manager.network_name = "test-tailnet"
    
    return mock_manager


@pytest.fixture
def mock_extraction_chain():
    """Create a mock LangChain extraction chain for testing."""
    
    mock_chain = AsyncMock(spec=ExtractionChain)
    
    # Mock extraction results
    mock_chain.extract.return_value = {
        "extracted_terms": [
            {
                "name": "Test Solar Panel",
                "definition": "Test definition for solar panel",
                "confidence": 0.9,
                "technology_type": "photovoltaic"
            }
        ],
        "extraction_confidence": 0.85,
        "model_used": "gpt-4-turbo"
    }
    
    return mock_chain


@pytest.fixture
def mock_validation_chain():
    """Create a mock LangChain validation chain for testing."""
    
    mock_chain = AsyncMock(spec=ValidationChain)
    
    # Mock validation results
    mock_chain.validate.return_value = {
        "confidence": 0.9,
        "accuracy": 0.85,
        "completeness": 0.9,
        "recommendations": ["Consider adding technical specifications"],
        "validation_status": "approved"
    }
    
    return mock_chain


@pytest.fixture
def mock_fabric_registry():
    """Create a mock FABRIC pattern registry for testing."""
    
    mock_registry = AsyncMock(spec=FabricPatternRegistry)
    
    # Mock FABRIC pattern results
    mock_registry.apply_pattern.return_value = {
        "pattern": "analyze_claims",
        "confidence": 0.88,
        "quality_score": 0.92,
        "recommendations": ["Verify technical accuracy"],
        "applied_at": datetime.utcnow().isoformat()
    }
    
    mock_registry.get_available_patterns.return_value = [
        "analyze_claims", "extract_wisdom", "create_summary"
    ]
    
    return mock_registry


@pytest.fixture
def mock_metrics_collector():
    """Create a mock metrics collector for testing."""
    
    mock_collector = AsyncMock(spec=MetricsCollector)
    
    # Mock metrics methods
    mock_collector.record_metric.return_value = None
    mock_collector.get_recent_metrics.return_value = {
        "processing_time": [1.2, 1.5, 0.8, 2.1],
        "success_rate": 0.95,
        "error_count": 2
    }
    mock_collector.start_collection.return_value = None
    mock_collector.stop_collection.return_value = None
    
    return mock_collector


@pytest.fixture
def mock_alert_manager():
    """Create a mock alert manager for testing."""
    
    mock_manager = AsyncMock(spec=AlertManager)
    
    # Mock alert methods
    mock_manager.send_alert.return_value = None
    mock_manager.add_alert_rule.return_value = None
    mock_manager.get_active_alerts.return_value = []
    
    return mock_manager


# ============================================================================
# Security and Authentication Fixtures
# ============================================================================

@pytest.fixture
def mock_jwt_auth_provider():
    """Create a mock JWT authentication provider for testing."""
    
    mock_provider = AsyncMock(spec=JWTAuthProvider)
    
    # Mock authentication methods
    mock_provider.create_token.return_value = "mock.jwt.token"
    mock_provider.verify_token.return_value = {
        "user_id": "test_user",
        "tenant_id": "test_tenant",
        "permissions": ["taxonomy.read", "taxonomy.write"],
        "exp": (datetime.utcnow() + timedelta(hours=8)).timestamp()
    }
    mock_provider.refresh_token.return_value = "new.mock.jwt.token"
    
    return mock_provider


@pytest.fixture
def mock_permission_manager():
    """Create a mock permission manager for testing."""
    
    mock_manager = AsyncMock(spec=PermissionManager)
    
    # Mock permission methods
    mock_manager.has_permission.return_value = True
    mock_manager.can_submit_job.return_value = True
    mock_manager.get_user_permissions.return_value = [
        "taxonomy.read", "taxonomy.write", "taxonomy.admin"
    ]
    mock_manager.check_resource_access.return_value = True
    
    return mock_manager


@pytest.fixture
def sample_user_context() -> Dict[str, Any]:
    """Provide sample user context for testing."""
    
    return {
        "user_id": "test_user_001",
        "tenant_id": "test_tenant",
        "permissions": ["taxonomy.read", "taxonomy.write", "taxonomy.admin"],
        "clearance_level": "standard",
        "session_id": str(uuid.uuid4()),
        "authenticated_at": datetime.utcnow().isoformat()
    }


# ============================================================================
# Behavior and Validation Fixtures
# ============================================================================

@pytest.fixture
def sample_computation_behavior() -> ComputationBehavior:
    """Create a sample computation behavior for testing."""
    
    return ComputationBehavior(
        behavior_id="test_computation",
        description="Test computation behavior",
        computation_function="_compute_test_metrics",
        cache_ttl=300,
        priority=100,
        parameters={
            "test_mode": True,
            "mock_results": True
        }
    )


@pytest.fixture
def sample_analysis_behavior() -> AnalysisBehavior:
    """Create a sample analysis behavior for testing."""
    
    return AnalysisBehavior(
        behavior_id="test_analysis",
        description="Test analysis behavior",
        analysis_type="relationship_discovery",
        retry_attempts=3,
        timeout_seconds=60.0,
        priority=75,
        parameters={
            "max_relationships": 10,
            "confidence_threshold": 0.7
        }
    )


@pytest.fixture
def sample_validation_result() -> ValidationResult:
    """Create a sample validation result for testing."""
    
    return ValidationResult(
        node_id="test_node_001",
        validation_status=ValidationStatusType.APPROVED,
        confidence_score=0.92,
        quality_metrics={
            "accuracy": 0.95,
            "completeness": 0.88,
            "consistency": 0.91
        },
        recommendations=[
            "Consider adding more technical details",
            "Verify industry standard compliance"
        ],
        validated_at=datetime.utcnow(),
        validator_id="test_validator"
    )


# ============================================================================
# Integration Test Fixtures
# ============================================================================

@pytest.fixture
async def integration_test_setup(
    temp_dir: Path,
    sample_config_data: Dict[str, Any]
) -> AsyncGenerator[Dict[str, Any], None]:
    """Set up integration test environment."""
    
    # Create test configuration
    config_path = temp_dir / "integration_config.json"
    with open(config_path, 'w') as f:
        json.dump(sample_config_data, f, indent=2)
    
    # Create test data directory
    data_dir = temp_dir / "test_data"
    data_dir.mkdir()
    
    # Create sample test files
    sample_glossary = {
        "renewable": [
            {"term": "Solar PV", "definition": "Photovoltaic technology"},
            {"term": "Wind Power", "definition": "Wind energy conversion"}
        ],
        "fossil": [
            {"term": "Coal", "definition": "Combustible sedimentary rock"},
            {"term": "Natural Gas", "definition": "Hydrocarbon gas mixture"}
        ]
    }
    
    glossary_file = data_dir / "sample_glossary.json"
    with open(glossary_file, 'w') as f:
        json.dump(sample_glossary, f, indent=2)
    
    setup_data = {
        "config_path": config_path,
        "data_dir": data_dir,
        "glossary_file": glossary_file,
        "temp_dir": temp_dir
    }
    
    yield setup_data
    
    # Cleanup is handled by temp_dir fixture


# ============================================================================
# Performance Test Fixtures
# ============================================================================

@pytest.fixture
def performance_test_data() -> Dict[str, Any]:
    """Generate large dataset for performance testing."""
    
    # Generate 1000 sample energy terms
    terms = []
    fuel_groups = [FuelGroupType.RENEWABLE, FuelGroupType.FOSSIL, FuelGroupType.NUCLEAR, FuelGroupType.ALTERNATIVE]
    
    for i in range(1000):
        terms.append({
            "term_name": f"Energy Term {i:04d}",
            "definition": f"Definition for energy term {i:04d} with detailed technical specifications",
            "fuel_group": fuel_groups[i % len(fuel_groups)],
            "efficiency_rating": 0.2 + (i % 80) / 100,
            "technology_type": f"technology_type_{i % 10}",
            "extraction_confidence": 0.7 + (i % 30) / 100
        })
    
    # Generate relationships
    relationships = []
    for i in range(0, len(terms), 10):
        for j in range(i + 1, min(i + 5, len(terms))):
            relationships.append({
                "source_term_index": i,
                "target_term_index": j,
                "relationship_type": RelationshipType.RELATED_TO,
                "confidence": 0.6 + (i % 40) / 100
            })
    
    return {
        "terms": terms,
        "relationships": relationships,
        "term_count": len(terms),
        "relationship_count": len(relationships)
    }


# ============================================================================
# Error Simulation Fixtures
# ============================================================================

@pytest.fixture
def error_simulation_fixtures():
    """Provide fixtures for testing error handling."""
    
    class ErrorSimulator:
        """Helper class for simulating various error conditions."""
        
        @staticmethod
        def network_error():
            """Simulate network connectivity error."""
            from aiohttp import ClientError
            raise ClientError("Simulated network error")
        
        @staticmethod
        def database_error():
            """Simulate database connection error."""
            from neo4j.exceptions import ServiceUnavailable
            raise ServiceUnavailable("Simulated database error")
        
        @staticmethod
        def validation_error():
            """Simulate validation error."""
            from pydantic import ValidationError
            raise ValidationError("Simulated validation error", model=BaseModel)
        
        @staticmethod
        def permission_error():
            """Simulate permission denied error."""
            raise PermissionError("Simulated permission denied")
        
        @staticmethod
        def timeout_error():
            """Simulate timeout error."""
            raise asyncio.TimeoutError("Simulated timeout error")
        
        @staticmethod
        def ai_api_error():
            """Simulate AI API error."""
            from openai import APIError
            raise APIError("Simulated AI API error")
    
    return ErrorSimulator


# ============================================================================
# Utility Fixtures
# ============================================================================

@pytest.fixture
def test_utilities():
    """Provide utility functions for testing."""
    
    class TestUtilities:
        """Collection of utility functions for testing."""
        
        @staticmethod
        def assert_node_properties(node: ATLASNode, expected_properties: Dict[str, Any]):
            """Assert that a node has expected properties."""
            for key, expected_value in expected_properties.items():
                actual_value = node.properties.get(key)
                assert actual_value == expected_value, f"Property {key}: expected {expected_value}, got {actual_value}"
        
        @staticmethod
        def assert_behavior_exists(node: ATLASNode, behavior_id: str):
            """Assert that a node has a specific behavior."""
            behavior_ids = [b.behavior_id for b in node.behaviors]
            assert behavior_id in behavior_ids, f"Behavior {behavior_id} not found in node behaviors: {behavior_ids}"
        
        @staticmethod
        def create_mock_extraction_result(term_count: int = 5) -> Dict[str, Any]:
            """Create a mock extraction result with specified number of terms."""
            terms = []
            for i in range(term_count):
                terms.append({
                    "name": f"Mock Term {i}",
                    "definition": f"Mock definition for term {i}",
                    "confidence": 0.8 + (i * 0.02),
                    "technology_type": f"mock_tech_{i}"
                })
            
            return {
                "extracted_terms": terms,
                "extraction_confidence": 0.85,
                "model_used": "mock-model",
                "processing_time": 1.5
            }
        
        @staticmethod
        def generate_test_node_id() -> str:
            """Generate a unique test node ID."""
            return f"test_node_{uuid.uuid4().hex[:8]}"
        
        @staticmethod
        def create_test_timestamp() -> str:
            """Create a test timestamp in ISO format."""
            return datetime.utcnow().isoformat()
    
    return TestUtilities


# ============================================================================
# Cleanup Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
async def cleanup_after_test():
    """Automatic cleanup after each test."""
    
    # Setup (runs before test)
    yield
    
    # Cleanup (runs after test)
    # Clear any global state, close connections, etc.
    
    # Reset logging level
    logger.setLevel("INFO")
    
    # Clear any cached data
    # (Add specific cleanup as needed)


# ============================================================================
# Parametrized Fixtures
# ============================================================================

@pytest.fixture(params=[
    FuelGroupType.RENEWABLE,
    FuelGroupType.FOSSIL,
    FuelGroupType.NUCLEAR,
    FuelGroupType.ALTERNATIVE
])
def fuel_group_type(request) -> FuelGroupType:
    """Parametrized fixture for testing all fuel group types."""
    return request.param


@pytest.fixture(params=[
    ValidationStatusType.PENDING,
    ValidationStatusType.IN_REVIEW,
    ValidationStatusType.APPROVED,
    ValidationStatusType.REJECTED
])
def validation_status_type(request) -> ValidationStatusType:
    """Parametrized fixture for testing all validation status types."""
    return request.param


@pytest.fixture(params=[
    RelationshipType.RELATED_TO,
    RelationshipType.PART_OF,
    RelationshipType.COMPETES_WITH,
    RelationshipType.REQUIRES
])
def relationship_type(request) -> RelationshipType:
    """Parametrized fixture for testing all relationship types."""
    return request.param


# ============================================================================
# Environment-Specific Fixtures
# ============================================================================

@pytest.fixture
def skip_if_no_openai():
    """Skip test if OpenAI API key is not available."""
    
    import os
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")


@pytest.fixture
def skip_if_no_neo4j():
    """Skip test if Neo4j is not available."""
    
    import os
    if not os.getenv("NEO4J_URI"):
        pytest.skip("Neo4j connection not available")


@pytest.fixture
def skip_if_no_redis():
    """Skip test if Redis is not available."""
    
    import os
    if not os.getenv("REDIS_URL"):
        pytest.skip("Redis connection not available")


# ============================================================================
# Documentation and Examples
# ============================================================================

# Example usage in test files:
"""
# Basic usage:
def test_node_creation(config_manager, sample_energy_terms):
    # Test implementation here
    pass

# Async test:
@pytest.mark.asyncio
async def test_async_operation(mock_neo4j_driver):
    # Async test implementation here
    pass

# Parametrized test:
def test_all_fuel_groups(fuel_group_type, config_manager):
    # Test all fuel group types
    pass

# Integration test:
@pytest.mark.integration
async def test_full_extraction_workflow(integration_test_setup):
    # Integration test implementation here
    pass

# Performance test:
@pytest.mark.slow
def test_large_dataset_processing(performance_test_data):
    # Performance test implementation here
    pass

# Error handling test:
def test_error_handling(error_simulation_fixtures):
    # Error handling test implementation here
    pass
"""

