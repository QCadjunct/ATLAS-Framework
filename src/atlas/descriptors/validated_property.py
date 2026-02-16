"""
Validated property descriptor for the ATLAS Framework.

This module provides a descriptor for validating property values,
with custom validation functions and error messages.
"""

from typing import Any, Callable, Dict, Optional, TypeVar, Union, cast

T = TypeVar("T")
ValidationFunc = Callable[[Any, Any], bool]


class ValidationError(Exception):
    """Exception raised when validation fails."""
    pass


class ValidatedProperty:
    """
    Descriptor for validating property values.
    
    This descriptor validates values before setting them,
    using a custom validation function.
    """
    
    def __init__(
        self, 
        validator: ValidationFunc,
        default: Optional[Any] = None,
        error_message: Optional[str] = None,
        name: Optional[str] = None
    ) -> None:
        """
        Initialize the validated property descriptor.
        
        Args:
            validator: Function that takes (instance, value) and returns bool
            default: Default value for the property
            error_message: Custom error message for validation failures
            name: Optional name for the property
        """
        self.validator = validator
        self.default = default
        self.error_message = error_message
        self.name = name
        
    def __set_name__(self, owner: Any, name: str) -> None:
        """
        Set the name of the descriptor.
        
        Args:
            owner: The owner class
            name: The name of the descriptor
        """
        if self.name is None:
            self.name = name
            
    def __get__(self, instance: Any, owner: Any) -> Any:
        """
        Get the validated property value.
        
        Args:
            instance: The instance to get the value for
            owner: The owner class
            
        Returns:
            The property value
            
        Raises:
            AttributeError: If accessed on the class rather than an instance
        """
        if instance is None:
            return self
        
        # Create validated properties dict if it doesn't exist
        if not hasattr(instance, "_validated_properties"):
            instance._validated_properties = {}
            
        validated_props = cast(Dict[str, Any], instance._validated_properties)
        
        # Return the value or default
        return validated_props.get(self.name, self.default)
    
    def __set__(self, instance: Any, value: Any) -> None:
        """
        Set the validated property value after validation.
        
        Args:
            instance: The instance to set the value for
            value: The value to validate and set
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate the value
        if not self.validator(instance, value):
            error_message = self.error_message or f"Validation failed for {self.name}"
            raise ValidationError(f"{error_message}: {value}")
        
        # Create validated properties dict if it doesn't exist
        if not hasattr(instance, "_validated_properties"):
            instance._validated_properties = {}
            
        validated_props = cast(Dict[str, Any], instance._validated_properties)
        validated_props[self.name] = value
        
    def __delete__(self, instance: Any) -> None:
        """
        Delete the validated property value.
        
        Args:
            instance: The instance to delete the value for
        """
        if hasattr(instance, "_validated_properties"):
            validated_props = cast(Dict[str, Any], instance._validated_properties)
            if self.name in validated_props:
                del validated_props[self.name]

