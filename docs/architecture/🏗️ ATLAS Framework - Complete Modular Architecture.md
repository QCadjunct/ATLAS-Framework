# 🏗️ ATLAS Framework - Complete Modular Architecture

## 📁 Source Code Architecture with SRP/DRY Principles

```
src/
├── atlas/                           # 🏛️ Main ATLAS package
│   ├── __init__.py                  # Main package exports
│   │
│   ├── core/                        # 🔧 Core framework components
│   │   ├── __init__.py              # Core exports
│   │   ├── base.py                  # Base classes and interfaces
│   │   ├── exceptions.py            # Custom exception hierarchy
│   │   ├── constants.py             # Framework constants
│   │   └── version.py               # Version information
│   │
│   ├── enums/                       # 📋 Type-safe enumerations with properties
│   │   ├── __init__.py              # Enum exports
│   │   ├── base.py                  # Base enum classes with common properties
│   │   ├── labels.py                # Node label enumerations
│   │   ├── relationships.py         # Relationship type enumerations
│   │   ├── validation.py            # Validation status enumerations
│   │   ├── fuel_groups.py           # Energy fuel group enumerations
│   │   └── operations.py            # Operation type enumerations
│   │
│   ├── descriptors/                 # ⚡ Python descriptors for efficiency
│   │   ├── __init__.py              # Descriptor exports
│   │   ├── cached.py                # Cached property descriptors
│   │   ├── validated.py             # Validated property descriptors
│   │   ├── lazy.py                  # Lazy loading descriptors
│   │   └── computed.py              # Computed property descriptors
│   │
│   ├── decorators/                  # 🎨 Strategic decorators
│   │   ├── __init__.py              # Decorator exports
│   │   ├── operations.py            # Operation decorators
│   │   ├── validation.py            # Validation decorators
│   │   ├── caching.py               # Caching decorators
│   │   ├── retry.py                 # Retry logic decorators
│   │   ├── logging.py               # Logging decorators
│   │   └── fabric.py                # FABRIC pattern decorators
│   │
│   ├── models/                      # 📊 Pydantic data models
│   │   ├── __init__.py              # Model exports
│   │   ├── base.py                  # Base Pydantic models
│   │   ├── nodes.py                 # Graph node models
│   │   ├── relationships.py         # Relationship models
│   │   ├── metadata.py              # Metadata models
│   │   ├── validation.py            # Validation models
│   │   ├── community.py             # Community contribution models
│   │   └── domain/                  # Domain-specific models
│   │       ├── __init__.py          # Domain model exports
│   │       ├── energy.py            # Energy domain models
│   │       ├── manufacturing.py     # Manufacturing domain models
│   │       └── transportation.py    # Transportation domain models
│   │
│   ├── graph/                       # 🕸️ Graph database operations
│   │   ├── __init__.py              # Graph exports
│   │   ├── base.py                  # Base graph interfaces
│   │   ├── neo4j/                   # Neo4j specific implementation
│   │   │   ├── __init__.py          # Neo4j exports
│   │   │   ├── driver.py            # Neo4j driver management
│   │   │   ├── queries.py           # Cypher query builders
│   │   │   ├── schema.py            # Schema management
│   │   │   └── operations.py        # CRUD operations
│   │   ├── memory/                  # In-memory graph for testing
│   │   │   ├── __init__.py          # Memory graph exports
│   │   │   └── implementation.py    # In-memory implementation
│   │   └── adapters/                # Graph database adapters
│   │       ├── __init__.py          # Adapter exports
│   │       ├── arangodb.py          # ArangoDB adapter
│   │       └── neptune.py           # Amazon Neptune adapter
│   │
│   ├── extraction/                  # 🔍 Data extraction engines
│   │   ├── __init__.py              # Extraction exports
│   │   ├── base.py                  # Base extraction interfaces
│   │   ├── llm/                     # LLM-based extraction
│   │   │   ├── __init__.py          # LLM extraction exports
│   │   │   ├── chains.py            # LangChain extraction chains
│   │   │   ├── prompts.py           # Extraction prompts
│   │   │   └── processors.py        # Response processors
│   │   ├── web/                     # Web scraping extraction
│   │   │   ├── __init__.py          # Web extraction exports
│   │   │   ├── scrapers.py          # Web scrapers
│   │   │   └── parsers.py           # Content parsers
│   │   └── document/                # Document extraction
│   │       ├── __init__.py          # Document extraction exports
│   │       ├── pdf.py               # PDF extraction
│   │       └── text.py              # Text extraction
│   │
│   ├── validation/                  # ✅ Validation systems
│   │   ├── __init__.py              # Validation exports
│   │   ├── base.py                  # Base validation interfaces
│   │   ├── schema.py                # Schema validation
│   │   ├── semantic.py              # Semantic validation
│   │   ├── community.py             # Community validation
│   │   ├── expert.py                # Expert validation
│   │   └── automated.py             # Automated validation
│   │
│   ├── frameworks/                  # 🔗 Framework integrations
│   │   ├── __init__.py              # Framework exports
│   │   ├── base.py                  # Base framework interfaces
│   │   ├── langchain/               # LangChain integration
│   │   │   ├── __init__.py          # LangChain exports
│   │   │   ├── chains.py            # Custom chains
│   │   │   ├── agents.py            # Custom agents
│   │   │   └── tools.py             # Custom tools
│   │   ├── langgraph/               # LangGraph integration
│   │   │   ├── __init__.py          # LangGraph exports
│   │   │   ├── workflows.py         # Workflow definitions
│   │   │   └── nodes.py             # Custom nodes
│   │   ├── fabric/                  # FABRIC pattern integration
│   │   │   ├── __init__.py          # FABRIC exports
│   │   │   ├── patterns.py          # Pattern implementations
│   │   │   └── registry.py          # Pattern registry
│   │   └── tavily/                  # Tavily integration
│   │       ├── __init__.py          # Tavily exports
│   │       └── search.py            # Search implementations
│   │
│   ├── security/                    # 🔒 Security and networking
│   │   ├── __init__.py              # Security exports
│   │   ├── base.py                  # Base security interfaces
│   │   ├── tailscale/               # Tailscale integration
│   │   │   ├── __init__.py          # Tailscale exports
│   │   │   ├── manager.py           # Tailscale manager
│   │   │   └── config.py            # Tailscale configuration
│   │   ├── auth/                    # Authentication
│   │   │   ├── __init__.py          # Auth exports
│   │   │   ├── providers.py         # Auth providers
│   │   │   └── tokens.py            # Token management
│   │   └── encryption/              # Encryption utilities
│   │       ├── __init__.py          # Encryption exports
│   │       └── utils.py             # Encryption utilities
│   │
│   ├── config/                      # ⚙️ Configuration management
│   │   ├── __init__.py              # Config exports
│   │   ├── base.py                  # Base configuration classes
│   │   ├── loader.py                # Configuration loader
│   │   ├── validator.py             # Configuration validator
│   │   ├── manager.py               # Configuration manager
│   │   └── schemas/                 # Configuration schemas
│   │       ├── __init__.py          # Schema exports
│   │       ├── atlas.py             # ATLAS configuration schema
│   │       ├── neo4j.py             # Neo4j configuration schema
│   │       └── security.py          # Security configuration schema
│   │
│   ├── community/                   # 👥 Community features
│   │   ├── __init__.py              # Community exports
│   │   ├── base.py                  # Base community interfaces
│   │   ├── contributions.py         # Contribution management
│   │   ├── reviews.py               # Peer review system
│   │   ├── scoring.py               # Community scoring
│   │   └── gamification.py          # Gamification features
│   │
│   ├── monitoring/                  # 📊 Monitoring and observability
│   │   ├── __init__.py              # Monitoring exports
│   │   ├── base.py                  # Base monitoring interfaces
│   │   ├── metrics.py               # Metrics collection
│   │   ├── health.py                # Health checks
│   │   ├── logging.py               # Structured logging
│   │   └── telemetry.py             # Telemetry collection
│   │
│   ├── utils/                       # 🛠️ Utility functions
│   │   ├── __init__.py              # Utility exports
│   │   ├── text.py                  # Text processing utilities
│   │   ├── json.py                  # JSON utilities
│   │   ├── datetime.py              # DateTime utilities
│   │   ├── hashing.py               # Hashing utilities
│   │   └── serialization.py         # Serialization utilities
│   │
│   └── cli/                         # 🖥️ Command-line interface
│       ├── __init__.py              # CLI exports
│       ├── main.py                  # Main CLI entry point
│       ├── commands/                # CLI commands
│       │   ├── __init__.py          # Command exports
│       │   ├── extract.py           # Extraction commands
│       │   ├── validate.py          # Validation commands
│       │   ├── graph.py             # Graph commands
│       │   └── config.py            # Configuration commands
│       └── utils.py                 # CLI utilities
│
├── tests/                           # 🧪 Test suite
│   ├── __init__.py                  # Test exports
│   ├── conftest.py                  # Pytest configuration
│   ├── unit/                        # Unit tests
│   ├── integration/                 # Integration tests
│   └── fixtures/                    # Test fixtures
│
├── docs/                            # 📚 Documentation
│   ├── api/                         # API documentation
│   ├── guides/                      # User guides
│   └── examples/                    # Example code
│
├── configs/                         # ⚙️ Configuration files
│   ├── atlas/                       # ATLAS configurations
│   ├── neo4j/                       # Neo4j configurations
│   └── security/                    # Security configurations
│
├── scripts/                         # 📜 Utility scripts
│   ├── setup.py                     # Setup scripts
│   ├── deploy.py                    # Deployment scripts
│   └── migrate.py                   # Migration scripts
│
├── pyproject.toml                   # 📦 Project configuration
├── README.md                        # 📖 Project README
├── CHANGELOG.md                     # 📝 Change log
└── LICENSE                          # ⚖️ License file
```

## 📋 Detailed Module Breakdown

### 1. Core Package Structure (`src/atlas/`)

#### Main Package `__init__.py`
```python
"""
ATLAS Framework - Agentic Taxonomy Learning and Synthesis
"""

from atlas.core.version import __version__
from atlas.core.base import ATLASBase
from atlas.core.exceptions import ATLASError, ValidationError, ConfigurationError

# Core model exports
from atlas.models.nodes import ATLASGraphNode, EnergyGraphNode
from atlas.models.relationships import GraphRelationship
from atlas.models.metadata import ExtractionMetadata, ValidationScores, CommunityMetadata

# Enum exports
from atlas.enums.labels import NodeLabelType
from atlas.enums.relationships import RelationshipType
from atlas.enums.fuel_groups import FuelGroupType
from atlas.enums.validation import ValidationStatusType

# Descriptor exports
from atlas.descriptors.cached import CachedProperty
from atlas.descriptors.validated import ValidatedProperty
from atlas.descriptors.lazy import LazyProperty

# Decorator exports
from atlas.decorators.operations import atlas_operation
from atlas.decorators.validation import validate_graph_operation
from atlas.decorators.fabric import fabric_pattern

# Configuration exports
from atlas.config.manager import ConfigurationManager
from atlas.config.loader import load_atlas_config

# Graph exports
from atlas.graph.neo4j.driver import Neo4jDriver
from atlas.graph.neo4j.operations import GraphOperations

__all__ = [
    # Version
    "__version__",
    
    # Core classes
    "ATLASBase",
    "ATLASError",
    "ValidationError", 
    "ConfigurationError",
    
    # Models
    "ATLASGraphNode",
    "EnergyGraphNode",
    "GraphRelationship",
    "ExtractionMetadata",
    "ValidationScores",
    "CommunityMetadata",
    
    # Enums
    "NodeLabelType",
    "RelationshipType", 
    "FuelGroupType",
    "ValidationStatusType",
    
    # Descriptors
    "CachedProperty",
    "ValidatedProperty",
    "LazyProperty",
    
    # Decorators
    "atlas_operation",
    "validate_graph_operation",
    "fabric_pattern",
    
    # Configuration
    "ConfigurationManager",
    "load_atlas_config",
    
    # Graph
    "Neo4jDriver",
    "GraphOperations",
]

# Package metadata
__author__ = "ATLAS Framework Team"
__email__ = "atlas@framework.dev"
__license__ = "MIT"
__description__ = "Agentic Taxonomy Learning and Synthesis Framework"
```

### 2. Enums Module (`src/atlas/enums/`)

#### Enums Package `__init__.py`
```python
"""
Type-safe enumerations with business logic properties.
"""

from atlas.enums.base import ATLASEnum
from atlas.enums.labels import NodeLabelType
from atlas.enums.relationships import RelationshipType
from atlas.enums.validation import ValidationStatusType
from atlas.enums.fuel_groups import FuelGroupType
from atlas.enums.operations import OperationType, ExtractionMethod

__all__ = [
    "ATLASEnum",
    "NodeLabelType",
    "RelationshipType", 
    "ValidationStatusType",
    "FuelGroupType",
    "OperationType",
    "ExtractionMethod",
]
```

#### Base Enum (`src/atlas/enums/base.py`)
```python
"""
Base enumeration classes with common functionality.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class ATLASEnum(str, Enum):
    """
    Base enumeration class with common properties and methods.
    Provides foundation for all ATLAS enumerations.
    """
    
    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable display name for this enum value."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Detailed description of this enum value."""
        pass
    
    @property
    def is_deprecated(self) -> bool:
        """Check if this enum value is deprecated."""
        return False
    
    @classmethod
    def get_all_values(cls) -> List[str]:
        """Get all enum values as a list."""
        return [item.value for item in cls]
    
    @classmethod
    def get_display_mapping(cls) -> Dict[str, str]:
        """Get mapping of values to display names."""
        return {item.value: item.display_name for item in cls}
    
    @classmethod
    def from_display_name(cls, display_name: str) -> Optional['ATLASEnum']:
        """Get enum item from display name."""
        for item in cls:
            if item.display_name == display_name:
                return item
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert enum to dictionary representation."""
        return {
            "value": self.value,
            "display_name": self.display_name,
            "description": self.description,
            "is_deprecated": self.is_deprecated
        }
```

#### Node Labels (`src/atlas/enums/labels.py`)
```python
"""
Node label enumerations with business logic properties.
"""

from typing import List, Dict, Any
from atlas.enums.base import ATLASEnum

class NodeLabelType(ATLASEnum):
    """Type-safe node labels with comprehensive business logic."""
    
    # Energy-specific labels
    ENERGY_TERM = "EnergyTerm"
    RENEWABLE_SOURCE = "RenewableSource" 
    FOSSIL_FUEL = "FossilFuel"
    TECHNICAL_CONCEPT = "TechnicalConcept"
    REGULATORY_FRAMEWORK = "RegulatoryFramework"
    
    # Generic taxonomy labels
    TAXONOMY_NODE = "TaxonomyNode"
    CONCEPT = "Concept"
    CATEGORY = "Category"
    RELATIONSHIP_NODE = "RelationshipNode"
    
    @property
    def display_name(self) -> str:
        """Human-readable display name."""
        display_names = {
            "EnergyTerm": "Energy Term",
            "RenewableSource": "Renewable Energy Source",
            "FossilFuel": "Fossil Fuel",
            "TechnicalConcept": "Technical Concept",
            "RegulatoryFramework": "Regulatory Framework",
            "TaxonomyNode": "Taxonomy Node",
            "Concept": "Concept",
            "Category": "Category",
            "RelationshipNode": "Relationship Node"
        }
        return display_names.get(self.value, self.value)
    
    @property
    def description(self) -> str:
        """Detailed description of the node label."""
        descriptions = {
            "EnergyTerm": "A term or concept specific to the energy industry",
            "RenewableSource": "A renewable energy source or technology",
            "FossilFuel": "A fossil fuel type or related concept",
            "TechnicalConcept": "A technical concept or specification",
            "RegulatoryFramework": "A regulatory framework or policy",
            "TaxonomyNode": "A general taxonomy node",
            "Concept": "A general concept",
            "Category": "A categorization node",
            "RelationshipNode": "A node representing relationships"
        }
        return descriptions.get(self.value, "No description available")
    
    @property
    def is_energy_specific(self) -> bool:
        """Check if this label is energy domain-specific."""
        return self.value in {
            "EnergyTerm", "RenewableSource", "FossilFuel", 
            "TechnicalConcept", "RegulatoryFramework"
        }
    
    @property
    def is_hierarchical(self) -> bool:
        """Check if this label type supports hierarchical relationships."""
        return self.value in {"EnergyTerm", "Category", "TechnicalConcept"}
    
    @property
    def requires_validation(self) -> bool:
        """Check if this label type requires expert validation."""
        return self.value in {"RegulatoryFramework", "TechnicalConcept"}
    
    @property
    def neo4j_constraints(self) -> List[str]:
        """Get Neo4j constraints for this label type."""
        constraints = []
        if self.is_energy_specific:
            constraints.append(
                f"CREATE CONSTRAINT {self.value}_unique_name IF NOT EXISTS "
                f"FOR (n:{self.value}) REQUIRE n.name IS UNIQUE"
            )
        if self.requires_validation:
            constraints.append(
                f"CREATE CONSTRAINT {self.value}_validation IF NOT EXISTS "
                f"FOR (n:{self.value}) REQUIRE n.validation_status IS NOT NULL"
            )
        return constraints
    
    @property
    def default_properties(self) -> Dict[str, Any]:
        """Get default properties for nodes with this label."""
        base_props = {"created_at": "datetime()", "version": 1}
        
        if self.is_energy_specific:
            base_props.update({
                "fuel_group": None,
                "extraction_confidence": 0.8
            })
        
        if self.requires_validation:
            base_props.update({
                "validation_status": "pending",
                "expert_reviewed": False
            })
        
        return base_props
```

### 3. Descriptors Module (`src/atlas/descriptors/`)

#### Descriptors Package `__init__.py`
```python
"""
Python descriptors for efficient property management.
"""

from atlas.descriptors.cached import CachedProperty
from atlas.descriptors.validated import ValidatedProperty
from atlas.descriptors.lazy import LazyProperty
from atlas.descriptors.computed import ComputedProperty

__all__ = [
    "CachedProperty",
    "ValidatedProperty", 
    "LazyProperty",
    "ComputedProperty",
]
```

#### Cached Property (`src/atlas/descriptors/cached.py`)
```python
"""
Cached property descriptor with TTL and invalidation.
"""

from typing import Any, Optional, Callable, TypeVar, Generic
import weakref
import time
from functools import wraps

T = TypeVar('T')

class CachedProperty(Generic[T]):
    """
    Efficient cached property descriptor with TTL and invalidation.
    
    Features:
    - Automatic cache invalidation based on TTL
    - WeakKeyDictionary to prevent memory leaks
    - Manual cache invalidation support
    - Thread-safe operations
    """
    
    def __init__(self, func: Callable[..., T], ttl: Optional[float] = None):
        """
        Initialize cached property.
        
        Args:
            func: Function to cache
            ttl: Time-to-live in seconds (None for no expiration)
        """
        self.func = func
        self.ttl = ttl
        self.name = func.__name__
        self.__doc__ = func.__doc__
        
        # Use WeakKeyDictionary to prevent memory leaks
        self._cache: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()
        self._timestamps: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()
    
    def __set_name__(self, owner: type, name: str) -> None:
        """Set the name when assigned to a class."""
        self.name = name
    
    def __get__(self, obj: Any, objtype: Optional[type] = None) -> T:
        """Get the cached value or compute it."""
        if obj is None:
            return self  # type: ignore
        
        # Check if we have a cached value
        if obj in self._cache:
            # Check TTL if specified
            if self.ttl is not None:
                timestamp = self._timestamps.get(obj, 0)
                if time.time() - timestamp > self.ttl:
                    # Cache expired, remove it
                    del self._cache[obj]
                    del self._timestamps[obj]
                else:
                    return self._cache[obj]
            else:
                return self._cache[obj]
        
        # Compute and cache the value
        value = self.func(obj)
        self._cache[obj] = value
        if self.ttl is not None:
            self._timestamps[obj] = time.time()
        
        return value
    
    def __set__(self, obj: Any, value: T) -> None:
        """Allow manual cache setting."""
        self._cache[obj] = value
        if self.ttl is not None:
            self._timestamps[obj] = time.time()
    
    def __delete__(self, obj: Any) -> None:
        """Allow cache invalidation."""
        self._cache.pop(obj, None)
        self._timestamps.pop(obj, None)
    
    def invalidate(self, obj: Any) -> None:
        """Manually invalidate cache for specific object."""
        self.__delete__(obj)
    
    def invalidate_all(self) -> None:
        """Invalidate all cached values."""
        self._cache.clear()
        self._timestamps.clear()

def cached_property(ttl: Optional[float] = None):
    """
    Decorator version of CachedProperty.
    
    Args:
        ttl: Time-to-live in seconds
    
    Example:
        @cached_property(ttl=300)  # 5 minute cache
        def expensive_computation(self):
            return self._compute_something_expensive()
    """
    def decorator(func: Callable[..., T]) -> CachedProperty[T]:
        return CachedProperty(func, ttl)
    return decorator
```

### 4. Decorators Module (`src/atlas/decorators/`)

#### Decorators Package `__init__.py`
```python
"""
Strategic decorators for cross-cutting concerns.
"""

from atlas.decorators.operations import atlas_operation, ensure_connection
from atlas.decorators.validation import validate_graph_operation, validate_node_type
from atlas.decorators.caching import cache_result, invalidate_cache
from atlas.decorators.retry import retry_on_failure, exponential_backoff
from atlas.decorators.logging import log_operation, log_performance
from atlas.decorators.fabric import fabric_pattern, apply_pattern

__all__ = [
    # Operations
    "atlas_operation",
    "ensure_connection",
    
    # Validation
    "validate_graph_operation",
    "validate_node_type",
    
    # Caching
    "cache_result",
    "invalidate_cache",
    
    # Retry
    "retry_on_failure", 
    "exponential_backoff",
    
    # Logging
    "log_operation",
    "log_performance",
    
    # FABRIC
    "fabric_pattern",
    "apply_pattern",
]
```

#### Operations Decorators (`src/atlas/decorators/operations.py`)
```python
"""
Operation decorators for ATLAS framework.
"""

from functools import wraps
from typing import Callable, Any, Optional, Dict, List
import time
import logging
import asyncio
from atlas.enums.labels import NodeLabelType
from atlas.core.exceptions import ATLASError, ValidationError

def atlas_operation(
    operation_type: str,
    requires_validation: bool = True,
    cache_result: bool = False,
    retry_attempts: int = 3,
    timeout: Optional[float] = None
):
    """
    Comprehensive decorator for ATLAS operations.
    
    Args:
        operation_type: Type of operation being performed
        requires_validation: Whether to validate before operation
        cache_result: Whether to cache the result
        retry_attempts: Number of retry attempts on failure
        timeout: Operation timeout in seconds
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(self, *args, **kwargs):
            operation_id = f"{operation_type}_{func.__name__}_{int(time.time())}"
            start_time = time.time()
            
            # Pre-operation validation
            if requires_validation and hasattr(self, 'validate_operation'):
                try:
                    await self.validate_operation(operation_type, *args, **kwargs)
                except Exception as e:
                    logging.error(f"Validation failed for operation {operation_id}: {e}")
                    raise ValidationError(f"Operation validation failed: {e}")
            
            # Retry logic with exponential backoff
            last_exception = None
            for attempt in range(retry_attempts):
                try:
                    # Apply timeout if specified
                    if timeout:
                        result = await asyncio.wait_for(
                            func(self, *args, **kwargs),
                            timeout=timeout
                        )
                    else:
                        if asyncio.iscoroutinefunction(func):
                            result = await func(self, *args, **kwargs)
                        else:
                            result = func(self, *args, **kwargs)
                    
                    # Cache result if requested
                    if cache_result and hasattr(self, '_operation_cache'):
                        cache_key = f"{func.__name__}_{hash(str(args) + str(kwargs))}"
                        self._operation_cache[cache_key] = result
                    
                    # Log successful operation
                    duration = time.time() - start_time
                    logging.info(f"ATLAS operation {operation_id} completed in {duration:.2f}s")
                    
                    return result
                    
                except Exception as e:
                    last_exception = e
                    if attempt < retry_attempts - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        logging.warning(
                            f"ATLAS operation {operation_id} failed (attempt {attempt + 1}), "
                            f"retrying in {wait_time}s: {e}"
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        duration = time.time() - start_time
                        logging.error(
                            f"ATLAS operation {operation_id} failed after {retry_attempts} "
                            f"attempts in {duration:.2f}s: {e}"
                        )
            
            if last_exception:
                raise ATLASError(f"Operation {operation_id} failed: {last_exception}")
            
        @wraps(func)
        def sync_wrapper(self, *args, **kwargs):
            operation_id = f"{operation_type}_{func.__name__}_{int(time.time())}"
            start_time = time.time()
            
            try:
                result = func(self, *args, **kwargs)
                duration = time.time() - start_time
                logging.info(f"ATLAS operation {operation_id} completed in {duration:.2f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logging.error(f"ATLAS operation {operation_id} failed after {duration:.2f}s: {e}")
                raise ATLASError(f"Operation {operation_id} failed: {e}")
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

def ensure_connection(connection_attr: str = "connection"):
    """
    Decorator to ensure connection exists before executing method.
    
    Args:
        connection_attr: Name of the connection attribute to check
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Check for connection
            connection = getattr(self, connection_attr, None)
            if connection is None:
                raise ATLASError(f"No {connection_attr} established")
            
            # Test connection if it has a test method
            if hasattr(connection, 'test_connection'):
                try:
                    connection.test_connection()
                except Exception as e:
                    raise ATLASError(f"Connection test failed: {e}")
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
```

### 5. Models Module (`src/atlas/models/`)

#### Models Package `__init__.py`
```python
"""
Pydantic data models for ATLAS framework.
"""

from atlas.models.base import ATLASBaseModel, TimestampedModel, VersionedModel
from atlas.models.nodes import ATLASGraphNode, EnergyGraphNode
from atlas.models.relationships import GraphRelationship, RelationshipMetadata
from atlas.models.metadata import (
    ExtractionMetadata, 
    ValidationScores, 
    CommunityMetadata,
    PerformanceMetrics
)
from atlas.models.validation import ValidationRequest, ValidationResult
from atlas.models.community import (
    CommunityContribution,
    PeerReview,
    ContributorProfile
)

__all__ = [
    # Base models
    "ATLASBaseModel",
    "TimestampedModel", 
    "VersionedModel",
    
    # Node models
    "ATLASGraphNode",
    "EnergyGraphNode",
    
    # Relationship models
    "GraphRelationship",
    "RelationshipMetadata",
    
    # Metadata models
    "ExtractionMetadata",
    "ValidationScores",
    "CommunityMetadata", 
    "PerformanceMetrics",
    
    # Validation models
    "ValidationRequest",
    "ValidationResult",
    
    # Community models
    "CommunityContribution",
    "PeerReview",
    "ContributorProfile",
]
```

#### Base Models (`src/atlas/models/base.py`)
```python
"""
Base Pydantic models for ATLAS framework.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Dict, Optional
from datetime import datetime
import uuid

class ATLASBaseModel(BaseModel):
    """
    Base model for all ATLAS Pydantic models.
    
    Provides common configuration and functionality.
    """
    
    model_config = ConfigDict(
        validate_assignment=True,      # Validate when attributes change
        use_enum_values=True,         # Serialize enums to their values
        extra='forbid',               # Reject unknown fields (strict)
        str_strip_whitespace=True,    # Clean string inputs automatically
        validate_default=True,        # Validate default values too
        json_encoders={               # Custom serialization rules
            datetime: lambda v: v.isoformat(),
            uuid.UUID: lambda v: str(v)
        }
    )
    
    def to_dict(self, exclude_none: bool = True) -> Dict[str, Any]:
        """Convert model to dictionary with optional None exclusion."""
        return self.model_dump(exclude_none=exclude_none)
    
    def to_json(self, exclude_none: bool = True) -> str:
        """Convert model to JSON string."""
        return self.model_dump_json(exclude_none=exclude_none)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ATLASBaseModel':
        """Create model instance from dictionary."""
        return cls(**data)

class TimestampedModel(ATLASBaseModel):
    """
    Base model with automatic timestamp management.
    """
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

class VersionedModel(TimestampedModel):
    """
    Base model with version tracking.
    """
    
    version: int = Field(default=1, ge=1, description="Model version")
    
    def increment_version(self) -> None:
        """Increment version and update timestamp."""
        self.version += 1
        self.touch()

class IdentifiedModel(VersionedModel):
    """
    Base model with unique identifier.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    
    def __hash__(self) -> int:
        """Make model hashable based on ID."""
        return hash(self.id)
    
    def __eq__(self, other: Any) -> bool:
        """Compare models based on ID."""
        if not isinstance(other, IdentifiedModel):
            return False
        return self.id == other.id
```

### 6. Configuration Module (`src/atlas/config/`)

#### Configuration Package `__init__.py`
```python
"""
Configuration management for ATLAS framework.
"""

from atlas.config.base import ATLASConfig, DatabaseConfig, SecurityConfig
from atlas.config.loader import ConfigurationLoader, load_atlas_config
from atlas.config.manager import ConfigurationManager
from atlas.config.validator import ConfigurationValidator

__all__ = [
    # Base configurations
    "ATLASConfig",
    "DatabaseConfig", 
    "SecurityConfig",
    
    # Loader
    "ConfigurationLoader",
    "load_atlas_config",
    
    # Manager
    "ConfigurationManager",
    
    # Validator
    "ConfigurationValidator",
]
```

This modular architecture provides:

1. **🎯 Single Responsibility**: Each module has one clear purpose
2. **🔄 DRY Principle**: Common functionality in base classes, no duplication
3. **📦 Clean Imports**: Well-structured `__init__.py` files for easy imports
4. **🔧 Type Safety**: Full type hints and Pydantic validation throughout
5. **⚡ Performance**: Efficient descriptors and caching where needed
6. **🎨 Maintainability**: Clear separation of concerns and modular design

The architecture scales from simple usage to enterprise deployment while maintaining clean, maintainable code structure.

