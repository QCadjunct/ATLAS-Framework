"""
ATLAS Framework - Agentic Taxonomy Learning and Synthesis Framework
==================================================================

ATLAS Framework is a comprehensive solution for extracting, organizing, and analyzing
domain-specific taxonomies using agentic LLMs and knowledge graphs.

This package provides tools for:
- Extracting taxonomies from text and web sources
- Creating and managing knowledge graphs
- Using FABRIC patterns for complex reasoning
- Integrating with various graph databases
"""

from atlas.core.client import ATLASClient
from atlas.core.node import ATLASNode
from atlas.core.relationship import ATLASRelationship
from atlas.core.taxonomy import TaxonomyExtractor
from atlas.core.version import __version__

from atlas.decorators import (
    atlas_operation,
    cached_property,
    fabric_pattern,
    validate_graph_operation,
)

from atlas.descriptors import (
    CachedProperty,
    LazyProperty,
    ValidatedProperty,
)

from atlas.enums import (
    FuelGroupType,
    NodeLabelType,
    RelationshipType,
    ValidationStatusType,
)

from atlas.models import (
    EnergyTerm,
    EnergySource,
    EnergyTechnology,
)

__all__ = [
    # Core
    "ATLASClient",
    "ATLASNode",
    "ATLASRelationship",
    "TaxonomyExtractor",
    "__version__",
    
    # Decorators
    "atlas_operation",
    "cached_property",
    "fabric_pattern",
    "validate_graph_operation",
    
    # Descriptors
    "CachedProperty",
    "LazyProperty",
    "ValidatedProperty",
    
    # Enums
    "FuelGroupType",
    "NodeLabelType",
    "RelationshipType",
    "ValidationStatusType",
    
    # Models
    "EnergyTerm",
    "EnergySource",
    "EnergyTechnology",
]

