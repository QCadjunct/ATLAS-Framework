"""
Descriptors for the ATLAS Framework.

This module provides custom descriptors for property management,
including caching, lazy loading, and validation.
"""

from atlas.descriptors.cached_property import CachedProperty
from atlas.descriptors.lazy_property import LazyProperty
from atlas.descriptors.validated_property import ValidatedProperty

__all__ = [
    "CachedProperty",
    "LazyProperty",
    "ValidatedProperty",
]

