"""
Node class for the ATLAS Framework.

This module provides the ATLASNode class, which represents a node
in the knowledge graph with properties and behaviors.
"""

import datetime
import uuid
from typing import Any, Dict, List, Optional, Set, Type, TypeVar, Union, cast

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict

from atlas.core.exceptions import ValidationError
from atlas.decorators import atlas_operation, cached_property, fabric_pattern
from atlas.enums import NodeLabelType, ValidationStatusType


T = TypeVar("T", bound=BaseModel)


class ATLASNode(BaseModel):
    """
    Base class for nodes in the ATLAS Framework knowledge graph.
    
    This class represents a node in the knowledge graph, with properties
    and behaviors that can be composed at runtime.
    """
    
    # Core node properties
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    labels: List[NodeLabelType] = Field(default_factory=list)
    properties: Dict[str, Any] = Field(default_factory=dict)
    
    # Metadata
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    validation_status: ValidationStatusType = Field(default=ValidationStatusType.UNVALIDATED)
    
    # Configuration
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True,
        extra="allow",
    )
    
    # Behavior registry
    _behaviors: Dict[str, Any] = {}
    
    @model_validator(mode="after")
    def validate_labels(self) -> "ATLASNode":
        """
        Validate that the node has at least one label.
        
        Returns:
            ATLASNode: The validated node
            
        Raises:
            ValidationError: If the node has no labels
        """
        if not self.labels:
            raise ValidationError("Node must have at least one label")
        return self
    
    @field_validator("labels")
    @classmethod
    def validate_label_types(cls, v: List[Any]) -> List[NodeLabelType]:
        """
        Validate that all labels are NodeLabelType instances.
        
        Args:
            v: List of labels to validate
            
        Returns:
            List[NodeLabelType]: List of validated labels
            
        Raises:
            ValidationError: If any label is not a NodeLabelType
        """
        result = []
        for label in v:
            if isinstance(label, str):
                try:
                    result.append(NodeLabelType(label))
                except ValueError:
                    try:
                        result.append(NodeLabelType.from_string(label))
                    except ValueError:
                        raise ValidationError(f"Invalid node label: {label}")
            elif isinstance(label, NodeLabelType):
                result.append(label)
            else:
                raise ValidationError(f"Invalid node label type: {type(label)}")
        return result
    
    @cached_property
    def required_properties(self) -> Set[str]:
        """
        Get the set of required properties for this node.
        
        Returns:
            Set[str]: Set of property names that are required
        """
        required = set()
        for label in self.labels:
            required.update(label.required_properties)
        return required
    
    @cached_property
    def missing_properties(self) -> Set[str]:
        """
        Get the set of required properties that are missing.
        
        Returns:
            Set[str]: Set of missing property names
        """
        return self.required_properties - set(self.properties.keys())
    
    @property
    def is_valid(self) -> bool:
        """
        Check if this node is valid.
        
        A node is valid if it has all required properties and its
        validation status indicates validity.
        
        Returns:
            bool: True if the node is valid, False otherwise
        """
        return (
            not self.missing_properties and
            self.validation_status.is_valid
        )
    
    @property
    def primary_label(self) -> NodeLabelType:
        """
        Get the primary label for this node.
        
        The primary label is the first label in the list.
        
        Returns:
            NodeLabelType: The primary label
        """
        return self.labels[0] if self.labels else NodeLabelType.TAXONOMY_NODE
    
    @atlas_operation("update", requires_validation=True)
    def update(self, properties: Dict[str, Any]) -> "ATLASNode":
        """
        Update the node properties.
        
        Args:
            properties: Dictionary of properties to update
            
        Returns:
            ATLASNode: The updated node
        """
        self.properties.update(properties)
        self.updated_at = datetime.datetime.now()
        return self
    
    @atlas_operation("validation")
    def validate(self) -> bool:
        """
        Validate the node.
        
        Returns:
            bool: True if the node is valid, False otherwise
        """
        # Check for required properties
        if self.missing_properties:
            return False
        
        # Check property types
        for prop, value in self.properties.items():
            if prop in self.required_properties:
                # TODO: Add type checking for required properties
                pass
        
        return True
    
    @fabric_pattern("analyze_claims")
    def analyze_relationships(self) -> Dict[str, Any]:
        """
        Analyze the relationships of this node.
        
        Returns:
            Dict[str, Any]: Analysis results
        """
        # This is a placeholder for the FABRIC pattern
        # The actual implementation would be provided by the pattern
        return {"node_id": self.id, "analysis": "Placeholder"}
    
    @classmethod
    def create(
        cls,
        labels: List[Union[str, NodeLabelType]],
        properties: Dict[str, Any],
        behaviors: Optional[List[str]] = None,
    ) -> "ATLASNode":
        """
        Create a new node with the specified labels, properties, and behaviors.
        
        Args:
            labels: List of node labels
            properties: Dictionary of node properties
            behaviors: Optional list of behavior names to attach
            
        Returns:
            ATLASNode: The created node
        """
        # Create the node
        node = cls(labels=labels, properties=properties)
        
        # Attach behaviors
        if behaviors:
            for behavior in behaviors:
                if behavior in cls._behaviors:
                    behavior_func = cls._behaviors[behavior]
                    setattr(node, behavior, behavior_func.__get__(node, cls))
        
        return node
    
    @classmethod
    def register_behavior(cls, name: str) -> Callable[[Callable], Callable]:
        """
        Decorator to register a behavior function.
        
        Args:
            name: Name of the behavior
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            cls._behaviors[name] = func
            return func
        return decorator
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the node to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the node
        """
        return {
            "id": self.id,
            "labels": [label.value for label in self.labels],
            "properties": self.properties,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "validation_status": self.validation_status.value,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ATLASNode":
        """
        Create a node from a dictionary.
        
        Args:
            data: Dictionary representation of the node
            
        Returns:
            ATLASNode: The created node
        """
        # Convert string timestamps to datetime objects
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.datetime.fromisoformat(data["updated_at"])
        
        # Convert validation status string to enum
        if isinstance(data.get("validation_status"), str):
            data["validation_status"] = ValidationStatusType(data["validation_status"])
        
        return cls(**data)

