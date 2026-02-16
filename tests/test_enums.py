"""
ATLAS Framework - Unit Tests for Enum Classes

This module contains comprehensive unit tests for all enum classes in the ATLAS Framework.
Tests cover enum values, properties, methods, and business logic.

Test Coverage:
- NodeLabelType enum with properties
- FuelGroupType enum with properties  
- ValidationStatusType enum with state transitions
- RelationshipType enum with semantic properties
- All enum @property methods and business logic
"""

import pytest
from typing import List, Set

from atlas.enums import (
    NodeLabelType, 
    FuelGroupType, 
    ValidationStatusType, 
    RelationshipType,
    ChangeDefaultUsernameAndPassword
)


class TestNodeLabelType:
    """Test cases for NodeLabelType enum."""
    
    def test_enum_values(self):
        """Test that all expected enum values exist."""
        
        expected_values = {
            "EnergyTerm", "RenewableSource", "FossilFuel", 
            "TechnicalConcept", "RegulatoryFramework",
            "TaxonomyNode", "Concept", "Category", "RelationshipNode"
        }
        
        actual_values = {label.value for label in NodeLabelType}
        assert actual_values == expected_values
    
    def test_is_energy_specific_property(self):
        """Test the is_energy_specific property."""
        
        # Energy-specific labels
        energy_labels = [
            NodeLabelType.ENERGY_TERM,
            NodeLabelType.RENEWABLE_SOURCE,
            NodeLabelType.FOSSIL_FUEL,
            NodeLabelType.TECHNICAL_CONCEPT,
            NodeLabelType.REGULATORY_FRAMEWORK
        ]
        
        for label in energy_labels:
            assert label.is_energy_specific, f"{label.value} should be energy-specific"
        
        # Generic labels
        generic_labels = [
            NodeLabelType.TAXONOMY_NODE,
            NodeLabelType.CONCEPT,
            NodeLabelType.CATEGORY,
            NodeLabelType.RELATIONSHIP_NODE
        ]
        
        for label in generic_labels:
            assert not label.is_energy_specific, f"{label.value} should not be energy-specific"
    
    def test_is_hierarchical_property(self):
        """Test the is_hierarchical property."""
        
        hierarchical_labels = [
            NodeLabelType.ENERGY_TERM,
            NodeLabelType.CATEGORY,
            NodeLabelType.TECHNICAL_CONCEPT
        ]
        
        for label in hierarchical_labels:
            assert label.is_hierarchical, f"{label.value} should support hierarchical relationships"
        
        non_hierarchical_labels = [
            NodeLabelType.RENEWABLE_SOURCE,
            NodeLabelType.FOSSIL_FUEL,
            NodeLabelType.REGULATORY_FRAMEWORK,
            NodeLabelType.RELATIONSHIP_NODE
        ]
        
        for label in non_hierarchical_labels:
            assert not label.is_hierarchical, f"{label.value} should not support hierarchical relationships"
    
    def test_requires_validation_property(self):
        """Test the requires_validation property."""
        
        validation_required = [
            NodeLabelType.ENERGY_TERM,
            NodeLabelType.TECHNICAL_CONCEPT,
            NodeLabelType.REGULATORY_FRAMEWORK
        ]
        
        for label in validation_required:
            assert label.requires_validation, f"{label.value} should require validation"
        
        validation_optional = [
            NodeLabelType.TAXONOMY_NODE,
            NodeLabelType.CONCEPT,
            NodeLabelType.CATEGORY
        ]
        
        for label in validation_optional:
            assert not label.requires_validation, f"{label.value} should not require validation"
    
    def test_is_renewable_property(self):
        """Test the is_renewable property."""
        
        assert NodeLabelType.RENEWABLE_SOURCE.is_renewable
        assert not NodeLabelType.FOSSIL_FUEL.is_renewable
        assert not NodeLabelType.ENERGY_TERM.is_renewable
    
    def test_enum_string_representation(self):
        """Test string representation of enum values."""
        
        assert str(NodeLabelType.ENERGY_TERM) == "NodeLabelType.ENERGY_TERM"
        assert NodeLabelType.ENERGY_TERM.value == "EnergyTerm"


class TestFuelGroupType:
    """Test cases for FuelGroupType enum."""
    
    def test_enum_values(self):
        """Test that all expected fuel group values exist."""
        
        expected_values = {
            "renewable", "fossil", "nuclear", "alternative", "storage", "hybrid"
        }
        
        actual_values = {fuel_group.value for fuel_group in FuelGroupType}
        assert actual_values == expected_values
    
    def test_is_renewable_property(self):
        """Test the is_renewable property."""
        
        renewable_groups = [FuelGroupType.RENEWABLE, FuelGroupType.HYBRID]
        
        for group in renewable_groups:
            assert group.is_renewable, f"{group.value} should be renewable"
        
        non_renewable_groups = [
            FuelGroupType.FOSSIL, 
            FuelGroupType.NUCLEAR, 
            FuelGroupType.ALTERNATIVE,
            FuelGroupType.STORAGE
        ]
        
        for group in non_renewable_groups:
            assert not group.is_renewable, f"{group.value} should not be renewable"
    
    def test_is_carbon_intensive_property(self):
        """Test the is_carbon_intensive property."""
        
        carbon_intensive = [FuelGroupType.FOSSIL]
        
        for group in carbon_intensive:
            assert group.is_carbon_intensive, f"{group.value} should be carbon intensive"
        
        low_carbon = [
            FuelGroupType.RENEWABLE,
            FuelGroupType.NUCLEAR,
            FuelGroupType.STORAGE,
            FuelGroupType.HYBRID
        ]
        
        for group in low_carbon:
            assert not group.is_carbon_intensive, f"{group.value} should not be carbon intensive"
    
    def test_requires_special_handling_property(self):
        """Test the requires_special_handling property."""
        
        special_handling = [FuelGroupType.NUCLEAR, FuelGroupType.STORAGE]
        
        for group in special_handling:
            assert group.requires_special_handling, f"{group.value} should require special handling"
        
        standard_handling = [
            FuelGroupType.RENEWABLE,
            FuelGroupType.FOSSIL,
            FuelGroupType.ALTERNATIVE,
            FuelGroupType.HYBRID
        ]
        
        for group in standard_handling:
            assert not group.requires_special_handling, f"{group.value} should not require special handling"
    
    def test_carbon_category_property(self):
        """Test the carbon_category property."""
        
        assert FuelGroupType.RENEWABLE.carbon_category == "zero_carbon"
        assert FuelGroupType.NUCLEAR.carbon_category == "low_carbon"
        assert FuelGroupType.FOSSIL.carbon_category == "high_carbon"
        assert FuelGroupType.STORAGE.carbon_category == "neutral"
        assert FuelGroupType.HYBRID.carbon_category == "mixed"
        assert FuelGroupType.ALTERNATIVE.carbon_category == "variable"
    
    def test_typical_efficiency_range_property(self):
        """Test the typical_efficiency_range property."""
        
        # Test that all fuel groups return valid efficiency ranges
        for fuel_group in FuelGroupType:
            efficiency_range = fuel_group.typical_efficiency_range
            assert isinstance(efficiency_range, tuple)
            assert len(efficiency_range) == 2
            assert 0.0 <= efficiency_range[0] <= efficiency_range[1] <= 1.0
    
    def test_regulatory_complexity_property(self):
        """Test the regulatory_complexity property."""
        
        expected_complexity = {
            FuelGroupType.NUCLEAR: "high",
            FuelGroupType.FOSSIL: "medium",
            FuelGroupType.RENEWABLE: "medium",
            FuelGroupType.STORAGE: "medium",
            FuelGroupType.ALTERNATIVE: "low",
            FuelGroupType.HYBRID: "high"
        }
        
        for fuel_group, expected in expected_complexity.items():
            assert fuel_group.regulatory_complexity == expected


class TestValidationStatusType:
    """Test cases for ValidationStatusType enum."""
    
    def test_enum_values(self):
        """Test that all expected validation status values exist."""
        
        expected_values = {
            "pending", "in_review", "requires_expert", "approved", 
            "rejected", "validation_failed"
        }
        
        actual_values = {status.value for status in ValidationStatusType}
        assert actual_values == expected_values
    
    def test_is_final_status_property(self):
        """Test the is_final_status property."""
        
        final_statuses = [
            ValidationStatusType.APPROVED,
            ValidationStatusType.REJECTED,
            ValidationStatusType.VALIDATION_FAILED
        ]
        
        for status in final_statuses:
            assert status.is_final_status, f"{status.value} should be a final status"
        
        non_final_statuses = [
            ValidationStatusType.PENDING,
            ValidationStatusType.IN_REVIEW,
            ValidationStatusType.REQUIRES_EXPERT
        ]
        
        for status in non_final_statuses:
            assert not status.is_final_status, f"{status.value} should not be a final status"
    
    def test_requires_human_review_property(self):
        """Test the requires_human_review property."""
        
        human_review_required = [
            ValidationStatusType.IN_REVIEW,
            ValidationStatusType.REQUIRES_EXPERT
        ]
        
        for status in human_review_required:
            assert status.requires_human_review, f"{status.value} should require human review"
        
        no_human_review = [
            ValidationStatusType.PENDING,
            ValidationStatusType.APPROVED,
            ValidationStatusType.REJECTED,
            ValidationStatusType.VALIDATION_FAILED
        ]
        
        for status in no_human_review:
            assert not status.requires_human_review, f"{status.value} should not require human review"
    
    def test_can_transition_to_property(self):
        """Test the can_transition_to property for state transitions."""
        
        # Test specific transition rules
        assert ValidationStatusType.APPROVED in ValidationStatusType.PENDING.can_transition_to
        assert ValidationStatusType.IN_REVIEW in ValidationStatusType.PENDING.can_transition_to
        assert ValidationStatusType.REJECTED in ValidationStatusType.PENDING.can_transition_to
        
        assert ValidationStatusType.APPROVED in ValidationStatusType.IN_REVIEW.can_transition_to
        assert ValidationStatusType.REQUIRES_EXPERT in ValidationStatusType.IN_REVIEW.can_transition_to
        assert ValidationStatusType.REJECTED in ValidationStatusType.IN_REVIEW.can_transition_to
        
        # Test that final statuses cannot transition
        final_statuses = [
            ValidationStatusType.APPROVED,
            ValidationStatusType.REJECTED,
            ValidationStatusType.VALIDATION_FAILED
        ]
        
        for status in final_statuses:
            assert len(status.can_transition_to) == 0, f"Final status {status.value} should not allow transitions"
    
    def test_priority_level_property(self):
        """Test the priority_level property."""
        
        expected_priorities = {
            ValidationStatusType.VALIDATION_FAILED: 1,
            ValidationStatusType.REQUIRES_EXPERT: 2,
            ValidationStatusType.IN_REVIEW: 3,
            ValidationStatusType.PENDING: 4,
            ValidationStatusType.REJECTED: 5,
            ValidationStatusType.APPROVED: 6
        }
        
        for status, expected_priority in expected_priorities.items():
            assert status.priority_level == expected_priority
    
    def test_status_color_property(self):
        """Test the status_color property for UI representation."""
        
        expected_colors = {
            ValidationStatusType.PENDING: "yellow",
            ValidationStatusType.IN_REVIEW: "blue",
            ValidationStatusType.REQUIRES_EXPERT: "orange",
            ValidationStatusType.APPROVED: "green",
            ValidationStatusType.REJECTED: "red",
            ValidationStatusType.VALIDATION_FAILED: "red"
        }
        
        for status, expected_color in expected_colors.items():
            assert status.status_color == expected_color


class TestRelationshipType:
    """Test cases for RelationshipType enum."""
    
    def test_enum_values(self):
        """Test that all expected relationship type values exist."""
        
        expected_values = {
            "PART_OF", "CONTAINS", "IS_A", "SUBCLASS_OF",
            "RELATED_TO", "SIMILAR_TO", "OPPOSITE_OF", "DERIVED_FROM",
            "REQUIRES", "PRODUCES", "CONSUMES", "ENABLES",
            "COMPETES_WITH", "COMPLEMENTS", "REPLACES"
        }
        
        actual_values = {rel_type.value for rel_type in RelationshipType}
        assert actual_values == expected_values
    
    def test_is_hierarchical_property(self):
        """Test the is_hierarchical property."""
        
        hierarchical_types = [
            RelationshipType.PART_OF,
            RelationshipType.CONTAINS,
            RelationshipType.IS_A,
            RelationshipType.SUBCLASS_OF
        ]
        
        for rel_type in hierarchical_types:
            assert rel_type.is_hierarchical, f"{rel_type.value} should be hierarchical"
        
        non_hierarchical_types = [
            RelationshipType.RELATED_TO,
            RelationshipType.COMPETES_WITH,
            RelationshipType.REQUIRES
        ]
        
        for rel_type in non_hierarchical_types:
            assert not rel_type.is_hierarchical, f"{rel_type.value} should not be hierarchical"
    
    def test_is_semantic_property(self):
        """Test the is_semantic property."""
        
        semantic_types = [
            RelationshipType.RELATED_TO,
            RelationshipType.SIMILAR_TO,
            RelationshipType.OPPOSITE_OF,
            RelationshipType.DERIVED_FROM
        ]
        
        for rel_type in semantic_types:
            assert rel_type.is_semantic, f"{rel_type.value} should be semantic"
    
    def test_is_functional_property(self):
        """Test the is_functional property."""
        
        functional_types = [
            RelationshipType.REQUIRES,
            RelationshipType.PRODUCES,
            RelationshipType.CONSUMES,
            RelationshipType.ENABLES
        ]
        
        for rel_type in functional_types:
            assert rel_type.is_functional, f"{rel_type.value} should be functional"
    
    def test_is_competitive_property(self):
        """Test the is_competitive property."""
        
        competitive_types = [
            RelationshipType.COMPETES_WITH,
            RelationshipType.REPLACES
        ]
        
        for rel_type in competitive_types:
            assert rel_type.is_competitive, f"{rel_type.value} should be competitive"
        
        non_competitive_types = [
            RelationshipType.COMPLEMENTS,
            RelationshipType.RELATED_TO,
            RelationshipType.REQUIRES
        ]
        
        for rel_type in non_competitive_types:
            assert not rel_type.is_competitive, f"{rel_type.value} should not be competitive"
    
    def test_inverse_relationship_property(self):
        """Test the inverse_relationship property."""
        
        expected_inverses = {
            RelationshipType.PART_OF: RelationshipType.CONTAINS,
            RelationshipType.CONTAINS: RelationshipType.PART_OF,
            RelationshipType.PRODUCES: RelationshipType.CONSUMES,
            RelationshipType.CONSUMES: RelationshipType.PRODUCES,
            RelationshipType.COMPETES_WITH: RelationshipType.COMPETES_WITH,  # Self-inverse
            RelationshipType.SIMILAR_TO: RelationshipType.SIMILAR_TO  # Self-inverse
        }
        
        for rel_type, expected_inverse in expected_inverses.items():
            assert rel_type.inverse_relationship == expected_inverse
    
    def test_relationship_strength_property(self):
        """Test the relationship_strength property."""
        
        strong_relationships = [
            RelationshipType.IS_A,
            RelationshipType.PART_OF,
            RelationshipType.REQUIRES
        ]
        
        for rel_type in strong_relationships:
            assert rel_type.relationship_strength == "strong"
        
        medium_relationships = [
            RelationshipType.RELATED_TO,
            RelationshipType.SIMILAR_TO,
            RelationshipType.COMPETES_WITH
        ]
        
        for rel_type in medium_relationships:
            assert rel_type.relationship_strength == "medium"
    
    def test_directionality_property(self):
        """Test the directionality property."""
        
        directed_relationships = [
            RelationshipType.PART_OF,
            RelationshipType.IS_A,
            RelationshipType.REQUIRES,
            RelationshipType.PRODUCES
        ]
        
        for rel_type in directed_relationships:
            assert rel_type.directionality == "directed"
        
        undirected_relationships = [
            RelationshipType.SIMILAR_TO,
            RelationshipType.COMPETES_WITH,
            RelationshipType.RELATED_TO
        ]
        
        for rel_type in undirected_relationships:
            assert rel_type.directionality == "undirected"


class TestChangeDefaultUsernameAndPassword:
    """Test cases for ChangeDefaultUsernameAndPassword enum (example from user)."""
    
    def test_enum_values(self):
        """Test that all expected enum values exist."""
        
        expected_values = {1, 2, 3}
        actual_values = {option.value for option in ChangeDefaultUsernameAndPassword}
        assert actual_values == expected_values
    
    def test_changes_default_credentials_property(self):
        """Test the changes_default_credentials property."""
        
        assert not ChangeDefaultUsernameAndPassword.DoNotChangeUserAndPwd.changes_default_credentials
        assert ChangeDefaultUsernameAndPassword.ChangeUserAndPwd.changes_default_credentials
        assert ChangeDefaultUsernameAndPassword.ChangeUserAndPwdPlusShow.changes_default_credentials
    
    def test_show_password_property(self):
        """Test the show_password property."""
        
        assert not ChangeDefaultUsernameAndPassword.DoNotChangeUserAndPwd.show_password
        assert not ChangeDefaultUsernameAndPassword.ChangeUserAndPwd.show_password
        assert ChangeDefaultUsernameAndPassword.ChangeUserAndPwdPlusShow.show_password
    
    def test_change_default_username_and_password_property(self):
        """Test the change_default_username_and_password property."""
        
        assert ChangeDefaultUsernameAndPassword.DoNotChangeUserAndPwd.change_default_username_and_password == 1
        assert ChangeDefaultUsernameAndPassword.ChangeUserAndPwd.change_default_username_and_password == 2
        assert ChangeDefaultUsernameAndPassword.ChangeUserAndPwdPlusShow.change_default_username_and_password == 3


class TestEnumIntegration:
    """Integration tests for enum interactions."""
    
    def test_enum_combinations(self):
        """Test valid combinations of enum values."""
        
        # Test that renewable fuel groups work with appropriate labels
        renewable_labels = [NodeLabelType.RENEWABLE_SOURCE, NodeLabelType.ENERGY_TERM]
        renewable_fuel = FuelGroupType.RENEWABLE
        
        assert renewable_fuel.is_renewable
        assert any(label.is_energy_specific for label in renewable_labels)
    
    def test_validation_workflow(self):
        """Test validation status workflow."""
        
        # Test a typical validation workflow
        current_status = ValidationStatusType.PENDING
        
        # Can transition to in_review
        assert ValidationStatusType.IN_REVIEW in current_status.can_transition_to
        
        # Move to in_review
        current_status = ValidationStatusType.IN_REVIEW
        assert current_status.requires_human_review
        
        # Can transition to approved
        assert ValidationStatusType.APPROVED in current_status.can_transition_to
        
        # Move to approved (final state)
        current_status = ValidationStatusType.APPROVED
        assert current_status.is_final_status
        assert len(current_status.can_transition_to) == 0
    
    def test_relationship_symmetry(self):
        """Test relationship type symmetry and inverses."""
        
        # Test symmetric relationships
        symmetric_types = [
            RelationshipType.SIMILAR_TO,
            RelationshipType.COMPETES_WITH,
            RelationshipType.RELATED_TO
        ]
        
        for rel_type in symmetric_types:
            assert rel_type.inverse_relationship == rel_type
    
    def test_hierarchical_relationships(self):
        """Test hierarchical relationship consistency."""
        
        hierarchical_labels = [
            label for label in NodeLabelType 
            if label.is_hierarchical
        ]
        
        hierarchical_relationships = [
            rel_type for rel_type in RelationshipType 
            if rel_type.is_hierarchical
        ]
        
        # Ensure we have both hierarchical labels and relationships
        assert len(hierarchical_labels) > 0
        assert len(hierarchical_relationships) > 0
    
    @pytest.mark.parametrize("fuel_group", [
        FuelGroupType.RENEWABLE,
        FuelGroupType.FOSSIL,
        FuelGroupType.NUCLEAR,
        FuelGroupType.ALTERNATIVE
    ])
    def test_fuel_group_properties_consistency(self, fuel_group: FuelGroupType):
        """Test that fuel group properties are consistent."""
        
        # All fuel groups should have valid efficiency ranges
        efficiency_range = fuel_group.typical_efficiency_range
        assert isinstance(efficiency_range, tuple)
        assert len(efficiency_range) == 2
        assert efficiency_range[0] <= efficiency_range[1]
        
        # All fuel groups should have valid carbon categories
        carbon_category = fuel_group.carbon_category
        assert carbon_category in ["zero_carbon", "low_carbon", "high_carbon", "neutral", "mixed", "variable"]
        
        # All fuel groups should have valid regulatory complexity
        complexity = fuel_group.regulatory_complexity
        assert complexity in ["low", "medium", "high"]
    
    def test_enum_serialization(self):
        """Test that enums can be properly serialized."""
        
        # Test that enum values can be converted to strings and back
        for fuel_group in FuelGroupType:
            value_str = fuel_group.value
            assert isinstance(value_str, str)
            
            # Should be able to recreate enum from value
            recreated = FuelGroupType(value_str)
            assert recreated == fuel_group
    
    def test_enum_hashing(self):
        """Test that enums can be used as dictionary keys."""
        
        # Test using enums as dictionary keys
        fuel_group_data = {
            FuelGroupType.RENEWABLE: {"count": 10, "efficiency": 0.25},
            FuelGroupType.FOSSIL: {"count": 15, "efficiency": 0.35},
            FuelGroupType.NUCLEAR: {"count": 5, "efficiency": 0.33}
        }
        
        assert len(fuel_group_data) == 3
        assert fuel_group_data[FuelGroupType.RENEWABLE]["count"] == 10
    
    def test_enum_ordering(self):
        """Test enum ordering where applicable."""
        
        # Test validation status priority ordering
        statuses = [
            ValidationStatusType.APPROVED,
            ValidationStatusType.PENDING,
            ValidationStatusType.VALIDATION_FAILED,
            ValidationStatusType.IN_REVIEW
        ]
        
        # Sort by priority level
        sorted_statuses = sorted(statuses, key=lambda s: s.priority_level)
        
        # Validation failed should be first (highest priority)
        assert sorted_statuses[0] == ValidationStatusType.VALIDATION_FAILED
        # Approved should be last (lowest priority)
        assert sorted_statuses[-1] == ValidationStatusType.APPROVED

