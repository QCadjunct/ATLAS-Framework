"""
Core components of the ATLAS Framework.

This module provides the core functionality of the ATLAS Framework,
including the client, node, relationship, and taxonomy extractor.
"""

from atlas.core.client import ATLASClient
from atlas.core.node import ATLASNode
from atlas.core.relationship import ATLASRelationship
from atlas.core.taxonomy import TaxonomyExtractor
from atlas.core.version import __version__

__all__ = [
    "ATLASClient",
    "ATLASNode",
    "ATLASRelationship",
    "TaxonomyExtractor",
    "__version__",
]

