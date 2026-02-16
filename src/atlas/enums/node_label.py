"""
Node label enumeration for knowledge graph nodes.

This module defines the NodeLabelType enum, which represents different
types of nodes in the knowledge graph.
"""

from enum import Enum
from typing import Dict, List, Set


class NodeLabelType(str, Enum):
    """
    Enumeration of node labels for knowledge graph nodes.
    
    This enum represents different types of nodes in the knowledge graph,
    with properties to determine their characteristics and behavior.
    """
    
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
    def is_energy_specific(self) -> bool:
        """
        Check if this label is energy domain-specific.
        
        Returns:
            bool: True if the label is energy-specific, False otherwise
        """
        return self.value in {
            self.ENERGY_TERM.value,
            self.RENEWABLE_SOURCE.value,
            self.FOSSIL_FUEL.value,
            self.TECHNICAL_CONCEPT.value,
            self.REGULATORY_FRAMEWORK.value,
        }
    
    @property
    def is_hierarchical(self) -> bool:
        """
        Check if this label type supports hierarchical relationships.
        
        Returns:
            bool: True if the label supports hierarchical relationships, False otherwise
        """
        return self.value in {
            self.ENERGY_TERM.value,
            self.CATEGORY.value,
            self.TECHNICAL_CONCEPT.value,
            self.TAXONOMY_NODE.value,
        }
    
    @property
    def requires_validation(self) -> bool:
        """
        Check if this label type requires expert validation.
        
        Returns:
            bool: True if the label requires validation, False otherwise
        """
        return self.value in {
            self.REGULATORY_FRAMEWORK.value,
            self.TECHNICAL_CONCEPT.value,
        }
    
    @property
    def required_properties(self) -> Set[str]:
        """
        Get the set of required properties for this node label.
        
        Returns:
            Set[str]: Set of property names that are required
        """
        base_properties = {"name", "created_at", "updated_at"}
        
        label_properties = {
            self.ENERGY_TERM.value: {"definition", "fuel_group"},
            self.RENEWABLE_SOURCE.value: {"capacity", "technology_type"},
            self.FOSSIL_FUEL.value: {"carbon_intensity", "extraction_method"},
            self.TECHNICAL_CONCEPT.value: {"description", "maturity_level"},
            self.REGULATORY_FRAMEWORK.value: {"jurisdiction", "effective_date", "regulatory_body"},
            self.TAXONOMY_NODE.value: {"definition"},
            self.CONCEPT.value: {"definition"},
            self.CATEGORY.value: {"description"},
            self.RELATIONSHIP_NODE.value: {"relationship_type"},
        }
        
        return base_properties.union(label_properties.get(self.value, set()))
    
    @property
    def compatible_relationships(self) -> List[str]:
        """
        Get a list of relationship types that are compatible with this node label.
        
        Returns:
            List[str]: List of compatible relationship type names
        """
        compatibility = {
            self.ENERGY_TERM.value: [
                "IS_A", "PART_OF", "USES", "PRODUCES", "RELATED_TO"
            ],
            self.RENEWABLE_SOURCE.value: [
                "IS_A", "PRODUCES", "LOCATED_IN", "REGULATED_BY"
            ],
            self.FOSSIL_FUEL.value: [
                "IS_A", "EXTRACTED_FROM", "PRODUCES", "REGULATED_BY"
            ],
            self.TECHNICAL_CONCEPT.value: [
                "USES", "PRODUCES", "DEPENDS_ON", "IMPROVES", "REPLACES"
            ],
            self.REGULATORY_FRAMEWORK.value: [
                "REGULATES", "SUPERSEDES", "REFERENCES", "ENFORCED_BY"
            ],
            self.TAXONOMY_NODE.value: [
                "IS_A", "PART_OF", "RELATED_TO"
            ],
            self.CONCEPT.value: [
                "IS_A", "RELATED_TO", "DEFINED_BY"
            ],
            self.CATEGORY.value: [
                "CONTAINS", "RELATED_TO"
            ],
            self.RELATIONSHIP_NODE.value: [
                "CONNECTS"
            ],
        }
        
        return compatibility.get(self.value, [])
    
    @property
    def default_icon(self) -> str:
        """
        Get the default icon for this node label.
        
        Returns:
            str: Icon name or path
        """
        icons = {
            self.ENERGY_TERM.value: "bolt",
            self.RENEWABLE_SOURCE.value: "sun",
            self.FOSSIL_FUEL.value: "fire",
            self.TECHNICAL_CONCEPT.value: "cog",
            self.REGULATORY_FRAMEWORK.value: "balance-scale",
            self.TAXONOMY_NODE.value: "sitemap",
            self.CONCEPT.value: "lightbulb",
            self.CATEGORY.value: "folder",
            self.RELATIONSHIP_NODE.value: "link",
        }
        
        return icons.get(self.value, "circle")
    
    @property
    def default_color(self) -> str:
        """
        Get the default color for this node label.
        
        Returns:
            str: Color in hex format
        """
        colors = {
            self.ENERGY_TERM.value: "#1976d2",
            self.RENEWABLE_SOURCE.value: "#388e3c",
            self.FOSSIL_FUEL.value: "#d32f2f",
            self.TECHNICAL_CONCEPT.value: "#8e24aa",
            self.REGULATORY_FRAMEWORK.value: "#f57c00",
            self.TAXONOMY_NODE.value: "#0288d1",
            self.CONCEPT.value: "#7cb342",
            self.CATEGORY.value: "#ffa000",
            self.RELATIONSHIP_NODE.value: "#5d4037",
        }
        
        return colors.get(self.value, "#757575")
    
    @property
    def search_boost(self) -> float:
        """
        Get the search boost factor for this node label.
        
        Higher values make nodes with this label appear higher in search results.
        
        Returns:
            float: Search boost factor
        """
        boosts = {
            self.ENERGY_TERM.value: 2.0,
            self.RENEWABLE_SOURCE.value: 1.5,
            self.FOSSIL_FUEL.value: 1.5,
            self.TECHNICAL_CONCEPT.value: 1.8,
            self.REGULATORY_FRAMEWORK.value: 1.2,
            self.TAXONOMY_NODE.value: 1.0,
            self.CONCEPT.value: 1.3,
            self.CATEGORY.value: 1.7,
            self.RELATIONSHIP_NODE.value: 0.5,
        }
        
        return boosts.get(self.value, 1.0)
    
    @classmethod
    def get_label_hierarchy(cls) -> Dict[str, List[str]]:
        """
        Get the hierarchy of node labels.
        
        Returns:
            Dict[str, List[str]]: Dictionary mapping parent labels to lists of child labels
        """
        return {
            cls.TAXONOMY_NODE.value: [
                cls.ENERGY_TERM.value,
                cls.CONCEPT.value,
                cls.CATEGORY.value,
            ],
            cls.ENERGY_TERM.value: [
                cls.RENEWABLE_SOURCE.value,
                cls.FOSSIL_FUEL.value,
            ],
            cls.CONCEPT.value: [
                cls.TECHNICAL_CONCEPT.value,
                cls.REGULATORY_FRAMEWORK.value,
            ],
        }
    
    @classmethod
    def from_string(cls, value: str) -> "NodeLabelType":
        """
        Create a NodeLabelType from a string, with fuzzy matching.
        
        Args:
            value: String representation of the node label
            
        Returns:
            NodeLabelType: The matching node label type
            
        Raises:
            ValueError: If no matching node label is found
        """
        value = value.lower().strip()
        
        # Try direct match with case normalization
        for label in cls:
            if label.value.lower() == value:
                return label
        
        # Fuzzy match
        if "energy" in value or "term" in value:
            return cls.ENERGY_TERM
        elif "renew" in value:
            return cls.RENEWABLE_SOURCE
        elif "fossil" in value:
            return cls.FOSSIL_FUEL
        elif "tech" in value or "concept" in value:
            return cls.TECHNICAL_CONCEPT
        elif "regul" in value or "framework" in value or "law" in value:
            return cls.REGULATORY_FRAMEWORK
        elif "taxonomy" in value:
            return cls.TAXONOMY_NODE
        elif "concept" in value:
            return cls.CONCEPT
        elif "category" in value:
            return cls.CATEGORY
        elif "relation" in value:
            return cls.RELATIONSHIP_NODE
        
        # Default to taxonomy node
        return cls.TAXONOMY_NODE

