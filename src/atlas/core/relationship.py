"""
Relationship type enumeration for knowledge graph relationships.

This module defines the RelationshipType enum, which represents different
types of relationships between nodes in the knowledge graph.
"""

from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


class RelationshipType(str, Enum):
    """
    Enumeration of relationship types for knowledge graph relationships.
    
    This enum represents different types of relationships between nodes
    in the knowledge graph, with properties to determine their characteristics.
    """
    
    # Hierarchical relationships
    IS_A = "IS_A"
    PART_OF = "PART_OF"
    CONTAINS = "CONTAINS"
    SUBCLASS_OF = "SUBCLASS_OF"
    
    # Semantic relationships
    RELATED_TO = "RELATED_TO"
    SIMILAR_TO = "SIMILAR_TO"
    OPPOSITE_OF = "OPPOSITE_OF"
    
    # Energy-specific relationships
    PRODUCES = "PRODUCES"
    CONSUMES = "CONSUMES"
    USES = "USES"
    REGULATES = "REGULATES"
    REGULATED_BY = "REGULATED_BY"
    EXTRACTED_FROM = "EXTRACTED_FROM"
    LOCATED_IN = "LOCATED_IN"
    
    # Technical relationships
    DEPENDS_ON = "DEPENDS_ON"
    IMPROVES = "IMPROVES"
    REPLACES = "REPLACES"
    CONNECTS = "CONNECTS"
    DEFINED_BY = "DEFINED_BY"
    REFERENCES = "REFERENCES"
    SUPERSEDES = "SUPERSEDES"
    ENFORCED_BY = "ENFORCED_BY"
    
    @property
    def is_hierarchical(self) -> bool:
        """
        Check if this relationship type is hierarchical.
        
        Hierarchical relationships form a tree-like structure.
        
        Returns:
            bool: True if the relationship is hierarchical, False otherwise
        """
        return self.value in {
            self.IS_A.value,
            self.PART_OF.value,
            self.CONTAINS.value,
            self.SUBCLASS_OF.value,
        }
    
    @property
    def is_directional(self) -> bool:
        """
        Check if this relationship type is directional.
        
        Directional relationships have a specific meaning from source to target.
        
        Returns:
            bool: True if the relationship is directional, False otherwise
        """
        # All relationships are directional except for these
        return self.value not in {
            self.RELATED_TO.value,
            self.SIMILAR_TO.value,
            self.CONNECTS.value,
        }
    
    @property
    def is_transitive(self) -> bool:
        """
        Check if this relationship type is transitive.
        
        Transitive relationships can be inferred across multiple hops.
        For example, if A IS_A B and B IS_A C, then A IS_A C.
        
        Returns:
            bool: True if the relationship is transitive, False otherwise
        """
        return self.value in {
            self.IS_A.value,
            self.SUBCLASS_OF.value,
            self.PART_OF.value,
            self.CONTAINS.value,
        }
    
    @property
    def inverse_relationship(self) -> Optional["RelationshipType"]:
        """
        Get the inverse relationship type, if one exists.
        
        Returns:
            Optional[RelationshipType]: The inverse relationship type, or None if no inverse exists
        """
        inverse_map = {
            self.IS_A.value: None,  # No direct inverse
            self.PART_OF.value: self.CONTAINS,
            self.CONTAINS.value: self.PART_OF,
            self.SUBCLASS_OF.value: None,  # No direct inverse
            self.RELATED_TO.value: self.RELATED_TO,  # Self-inverse
            self.SIMILAR_TO.value: self.SIMILAR_TO,  # Self-inverse
            self.OPPOSITE_OF.value: self.OPPOSITE_OF,  # Self-inverse
            self.PRODUCES.value: self.PRODUCED_BY,
            self.CONSUMES.value: self.CONSUMED_BY,
            self.USES.value: self.USED_BY,
            self.REGULATES.value: self.REGULATED_BY,
            self.REGULATED_BY.value: self.REGULATES,
            self.EXTRACTED_FROM.value: self.EXTRACTION_SOURCE_FOR,
            self.LOCATED_IN.value: self.LOCATION_OF,
            self.DEPENDS_ON.value: self.DEPENDENCY_FOR,
            self.IMPROVES.value: self.IMPROVED_BY,
            self.REPLACES.value: self.REPLACED_BY,
            self.CONNECTS.value: self.CONNECTS,  # Self-inverse
            self.DEFINED_BY.value: self.DEFINES,
            self.REFERENCES.value: self.REFERENCED_BY,
            self.SUPERSEDES.value: self.SUPERSEDED_BY,
            self.ENFORCED_BY.value: self.ENFORCES,
        }
        
        inverse = inverse_map.get(self.value)
        if inverse is None:
            return None
        
        try:
            return RelationshipType(inverse)
        except ValueError:
            return None
    
    @property
    def required_properties(self) -> Set[str]:
        """
        Get the set of required properties for this relationship type.
        
        Returns:
            Set[str]: Set of property names that are required
        """
        base_properties = {"created_at", "updated_at"}
        
        type_properties = {
            self.IS_A.value: {"confidence"},
            self.PART_OF.value: {"confidence"},
            self.CONTAINS.value: {"confidence"},
            self.SUBCLASS_OF.value: {"confidence"},
            self.RELATED_TO.value: {"strength", "description"},
            self.SIMILAR_TO.value: {"similarity_score"},
            self.OPPOSITE_OF.value: {"confidence"},
            self.PRODUCES.value: {"quantity", "unit"},
            self.CONSUMES.value: {"quantity", "unit"},
            self.USES.value: {"purpose"},
            self.REGULATES.value: {"regulation_type", "effective_date"},
            self.REGULATED_BY.value: {"regulation_type", "effective_date"},
            self.EXTRACTED_FROM.value: {"extraction_method"},
            self.LOCATED_IN.value: {"location_type"},
            self.DEPENDS_ON.value: {"dependency_type", "criticality"},
            self.IMPROVES.value: {"improvement_metric", "improvement_value"},
            self.REPLACES.value: {"replacement_date", "replacement_reason"},
            self.CONNECTS.value: {"connection_type"},
            self.DEFINED_BY.value: {"definition_source"},
            self.REFERENCES.value: {"reference_type", "reference_date"},
            self.SUPERSEDES.value: {"supersession_date"},
            self.ENFORCED_BY.value: {"enforcement_mechanism"},
        }
        
        return base_properties.union(type_properties.get(self.value, set()))
    
    @property
    def default_weight(self) -> float:
        """
        Get the default weight for this relationship type.
        
        Higher weights indicate stronger relationships.
        
        Returns:
            float: Default weight value (0.0 to 1.0)
        """
        weights = {
            self.IS_A.value: 1.0,
            self.PART_OF.value: 0.9,
            self.CONTAINS.value: 0.9,
            self.SUBCLASS_OF.value: 0.95,
            self.RELATED_TO.value: 0.5,
            self.SIMILAR_TO.value: 0.7,
            self.OPPOSITE_OF.value: 0.8,
            self.PRODUCES.value: 0.8,
            self.CONSUMES.value: 0.8,
            self.USES.value: 0.7,
            self.REGULATES.value: 0.6,
            self.REGULATED_BY.value: 0.6,
            self.EXTRACTED_FROM.value: 0.7,
            self.LOCATED_IN.value: 0.5,
            self.DEPENDS_ON.value: 0.8,
            self.IMPROVES.value: 0.6,
            self.REPLACES.value: 0.9,
            self.CONNECTS.value: 0.4,
            self.DEFINED_BY.value: 0.7,
            self.REFERENCES.value: 0.4,
            self.SUPERSEDES.value: 0.8,
            self.ENFORCED_BY.value: 0.6,
        }
        
        return weights.get(self.value, 0.5)
    
    @property
    def compatible_node_pairs(self) -> List[Tuple[str, str]]:
        """
        Get a list of compatible node label pairs for this relationship type.
        
        Returns:
            List[Tuple[str, str]]: List of (source_label, target_label) pairs
        """
        from atlas.enums.node_label import NodeLabelType
        
        compatibility = {
            self.IS_A.value: [
                (NodeLabelType.RENEWABLE_SOURCE.value, NodeLabelType.ENERGY_TERM.value),
                (NodeLabelType.FOSSIL_FUEL.value, NodeLabelType.ENERGY_TERM.value),
                (NodeLabelType.TECHNICAL_CONCEPT.value, NodeLabelType.CONCEPT.value),
                (NodeLabelType.ENERGY_TERM.value, NodeLabelType.TAXONOMY_NODE.value),
            ],
            self.PART_OF.value: [
                (NodeLabelType.TECHNICAL_CONCEPT.value, NodeLabelType.TECHNICAL_CONCEPT.value),
                (NodeLabelType.ENERGY_TERM.value, NodeLabelType.ENERGY_TERM.value),
            ],
            self.CONTAINS.value: [
                (NodeLabelType.CATEGORY.value, NodeLabelType.ENERGY_TERM.value),
                (NodeLabelType.CATEGORY.value, NodeLabelType.CONCEPT.value),
                (NodeLabelType.TECHNICAL_CONCEPT.value, NodeLabelType.TECHNICAL_CONCEPT.value),
            ],
            # Add more compatibility rules for other relationship types
        }
        
        return compatibility.get(self.value, [])
    
    @classmethod
    def get_relationship_groups(cls) -> Dict[str, List["RelationshipType"]]:
        """
        Get groups of related relationship types.
        
        Returns:
            Dict[str, List[RelationshipType]]: Dictionary mapping group names to lists of relationship types
        """
        return {
            "Hierarchical": [
                cls.IS_A,
                cls.PART_OF,
                cls.CONTAINS,
                cls.SUBCLASS_OF,
            ],
            "Semantic": [
                cls.RELATED_TO,
                cls.SIMILAR_TO,
                cls.OPPOSITE_OF,
            ],
            "Energy": [
                cls.PRODUCES,
                cls.CONSUMES,
                cls.USES,
                cls.REGULATES,
                cls.REGULATED_BY,
                cls.EXTRACTED_FROM,
                cls.LOCATED_IN,
            ],
            "Technical": [
                cls.DEPENDS_ON,
                cls.IMPROVES,
                cls.REPLACES,
                cls.CONNECTS,
                cls.DEFINED_BY,
                cls.REFERENCES,
                cls.SUPERSEDES,
                cls.ENFORCED_BY,
            ],
        }
    
    @classmethod
    def from_string(cls, value: str) -> "RelationshipType":
        """
        Create a RelationshipType from a string, with fuzzy matching.
        
        Args:
            value: String representation of the relationship type
            
        Returns:
            RelationshipType: The matching relationship type
            
        Raises:
            ValueError: If no matching relationship type is found
        """
        value = value.upper().strip().replace(" ", "_")
        
        # Try direct match
        try:
            return cls(value)
        except ValueError:
            pass
        
        # Fuzzy match
        if "IS" in value and "A" in value:
            return cls.IS_A
        elif "PART" in value:
            return cls.PART_OF
        elif "CONTAIN" in value:
            return cls.CONTAINS
        elif "CLASS" in value or "SUBCLASS" in value:
            return cls.SUBCLASS_OF
        elif "RELAT" in value:
            return cls.RELATED_TO
        elif "SIMILAR" in value:
            return cls.SIMILAR_TO
        elif "OPPOSITE" in value or "CONTRARY" in value:
            return cls.OPPOSITE_OF
        elif "PRODUC" in value:
            return cls.PRODUCES
        elif "CONSUM" in value:
            return cls.CONSUMES
        elif "USE" in value or "USES" in value or "USING" in value:
            return cls.USES
        elif "REGULAT" in value and "BY" in value:
            return cls.REGULATED_BY
        elif "REGULAT" in value:
            return cls.REGULATES
        elif "EXTRACT" in value:
            return cls.EXTRACTED_FROM
        elif "LOCAT" in value:
            return cls.LOCATED_IN
        elif "DEPEND" in value:
            return cls.DEPENDS_ON
        elif "IMPROV" in value:
            return cls.IMPROVES
        elif "REPLAC" in value:
            return cls.REPLACES
        elif "CONNECT" in value:
            return cls.CONNECTS
        elif "DEFIN" in value:
            return cls.DEFINED_BY
        elif "REFER" in value:
            return cls.REFERENCES
        elif "SUPER" in value:
            return cls.SUPERSEDES
        elif "ENFORC" in value:
            return cls.ENFORCED_BY
        
        # Default to related_to
        return cls.RELATED_TO

