"""
Validation status enumeration for knowledge graph entities.

This module defines the ValidationStatusType enum, which represents different
validation states for nodes and relationships in the knowledge graph.
"""

from enum import Enum
from typing import Dict, List, Set


class ValidationStatusType(str, Enum):
    """
    Enumeration of validation statuses for knowledge graph entities.
    
    This enum represents different validation states for nodes and relationships,
    with properties to determine their characteristics and behavior.
    """
    
    UNVALIDATED = "unvalidated"
    VALIDATED = "validated"
    NEEDS_REVIEW = "needs_review"
    REJECTED = "rejected"
    PENDING = "pending"
    AUTOMATED_VALIDATED = "automated_validated"
    EXPERT_VALIDATED = "expert_validated"
    COMMUNITY_VALIDATED = "community_validated"
    
    @property
    def is_valid(self) -> bool:
        """
        Check if this validation status indicates a valid entity.
        
        Returns:
            bool: True if the entity is considered valid, False otherwise
        """
        return self.value in {
            self.VALIDATED.value,
            self.AUTOMATED_VALIDATED.value,
            self.EXPERT_VALIDATED.value,
            self.COMMUNITY_VALIDATED.value,
        }
    
    @property
    def requires_action(self) -> bool:
        """
        Check if this validation status requires action.
        
        Returns:
            bool: True if action is required, False otherwise
        """
        return self.value in {
            self.UNVALIDATED.value,
            self.NEEDS_REVIEW.value,
            self.PENDING.value,
        }
    
    @property
    def confidence_factor(self) -> float:
        """
        Get the confidence factor associated with this validation status.
        
        Returns:
            float: Confidence factor (0.0 to 1.0)
        """
        factors = {
            self.UNVALIDATED.value: 0.3,
            self.VALIDATED.value: 0.8,
            self.NEEDS_REVIEW.value: 0.4,
            self.REJECTED.value: 0.0,
            self.PENDING.value: 0.5,
            self.AUTOMATED_VALIDATED.value: 0.7,
            self.EXPERT_VALIDATED.value: 1.0,
            self.COMMUNITY_VALIDATED.value: 0.9,
        }
        
        return factors.get(self.value, 0.5)
    
    @property
    def display_badge(self) -> str:
        """
        Get the display badge for this validation status.
        
        Returns:
            str: Badge text for display
        """
        badges = {
            self.UNVALIDATED.value: "⚠️ Unvalidated",
            self.VALIDATED.value: "✅ Validated",
            self.NEEDS_REVIEW.value: "🔍 Needs Review",
            self.REJECTED.value: "❌ Rejected",
            self.PENDING.value: "⏳ Pending",
            self.AUTOMATED_VALIDATED.value: "🤖 Auto-Validated",
            self.EXPERT_VALIDATED.value: "👨‍🔬 Expert Validated",
            self.COMMUNITY_VALIDATED.value: "👥 Community Validated",
        }
        
        return badges.get(self.value, "Unknown")
    
    @property
    def allowed_transitions(self) -> Set["ValidationStatusType"]:
        """
        Get the set of allowed transitions from this validation status.
        
        Returns:
            Set[ValidationStatusType]: Set of validation statuses that can follow this one
        """
        transitions = {
            self.UNVALIDATED.value: {
                self.PENDING,
                self.AUTOMATED_VALIDATED,
                self.NEEDS_REVIEW,
                self.REJECTED,
            },
            self.VALIDATED.value: {
                self.NEEDS_REVIEW,
                self.REJECTED,
            },
            self.NEEDS_REVIEW.value: {
                self.VALIDATED,
                self.EXPERT_VALIDATED,
                self.COMMUNITY_VALIDATED,
                self.REJECTED,
            },
            self.REJECTED.value: {
                self.NEEDS_REVIEW,
                self.PENDING,
            },
            self.PENDING.value: {
                self.VALIDATED,
                self.NEEDS_REVIEW,
                self.REJECTED,
                self.AUTOMATED_VALIDATED,
            },
            self.AUTOMATED_VALIDATED.value: {
                self.EXPERT_VALIDATED,
                self.COMMUNITY_VALIDATED,
                self.NEEDS_REVIEW,
                self.REJECTED,
            },
            self.EXPERT_VALIDATED.value: {
                self.NEEDS_REVIEW,
                self.REJECTED,
            },
            self.COMMUNITY_VALIDATED.value: {
                self.EXPERT_VALIDATED,
                self.NEEDS_REVIEW,
                self.REJECTED,
            },
        }
        
        return transitions.get(self.value, set())
    
    @property
    def required_validation_fields(self) -> Set[str]:
        """
        Get the set of required fields for this validation status.
        
        Returns:
            Set[str]: Set of field names that are required
        """
        base_fields = {"validated_at", "validation_source"}
        
        status_fields = {
            self.UNVALIDATED.value: set(),
            self.VALIDATED.value: {"validator_id"},
            self.NEEDS_REVIEW.value: {"review_reason"},
            self.REJECTED.value: {"rejection_reason", "rejected_by"},
            self.PENDING.value: {"pending_reason"},
            self.AUTOMATED_VALIDATED.value: {"validation_method", "confidence_score"},
            self.EXPERT_VALIDATED.value: {"expert_id", "expert_credentials"},
            self.COMMUNITY_VALIDATED.value: {"community_votes", "validation_threshold"},
        }
        
        return base_fields.union(status_fields.get(self.value, set()))
    
    @classmethod
    def get_validation_levels(cls) -> Dict[str, List["ValidationStatusType"]]:
        """
        Get validation levels grouped by confidence.
        
        Returns:
            Dict[str, List[ValidationStatusType]]: Dictionary mapping level names to validation statuses
        """
        return {
            "High": [
                cls.EXPERT_VALIDATED,
                cls.COMMUNITY_VALIDATED,
            ],
            "Medium": [
                cls.VALIDATED,
                cls.AUTOMATED_VALIDATED,
            ],
            "Low": [
                cls.PENDING,
                cls.UNVALIDATED,
            ],
            "Invalid": [
                cls.REJECTED,
                cls.NEEDS_REVIEW,
            ],
        }
    
    @classmethod
    def from_string(cls, value: str) -> "ValidationStatusType":
        """
        Create a ValidationStatusType from a string, with fuzzy matching.
        
        Args:
            value: String representation of the validation status
            
        Returns:
            ValidationStatusType: The matching validation status
            
        Raises:
            ValueError: If no matching validation status is found
        """
        value = value.lower().strip().replace(" ", "_")
        
        # Try direct match
        try:
            return cls(value)
        except ValueError:
            pass
        
        # Fuzzy match
        if "unvalid" in value:
            return cls.UNVALIDATED
        elif "valid" in value and not any(x in value for x in ["auto", "expert", "community"]):
            return cls.VALIDATED
        elif "review" in value or "need" in value:
            return cls.NEEDS_REVIEW
        elif "reject" in value:
            return cls.REJECTED
        elif "pend" in value:
            return cls.PENDING
        elif "auto" in value:
            return cls.AUTOMATED_VALIDATED
        elif "expert" in value:
            return cls.EXPERT_VALIDATED
        elif "community" in value:
            return cls.COMMUNITY_VALIDATED
        
        # Default to unvalidated
        return cls.UNVALIDATED

