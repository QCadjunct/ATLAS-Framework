"""
Enums for the ATLAS Framework.

This module provides type-safe enumerations with business logic properties
for various aspects of the ATLAS Framework.
"""

from atlas.enums.fuel_group import FuelGroupType
from atlas.enums.node_label import NodeLabelType
from atlas.enums.relationship import RelationshipType
from atlas.enums.validation import ValidationStatusType

__all__ = [
    "FuelGroupType",
    "NodeLabelType",
    "RelationshipType",
    "ValidationStatusType",
]

