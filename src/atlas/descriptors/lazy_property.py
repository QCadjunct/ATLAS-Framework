"""
Lazy property descriptor for the ATLAS Framework.

This module provides a descriptor for lazy loading of property values,
which are only computed when first accessed.
"""

from typing import Any, Callable, Dict, Optional, TypeVar, cast

T = TypeVar("T")


class LazyProperty:
    """
    Descriptor for lazy loading of property values.
    
    This descriptor computes the value only when first accessed,
    and then stores it for subsequent access.
    """
    
    def __init__(
        self, 
        func: Callable[[Any], T], 
        name: Optional[str] = None
    ) -> None:
        """
        Initialize the lazy property descriptor.
        
        Args:
            func: The function to compute the value
            name: Optional name for the property, defaults to the function name
        """
        self.func = func
        self.name = name or func.__name__
        self.__doc__ = func.__doc__
        
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
        Get the lazy-loaded value or compute and store it.
        
        Args:
            instance: The instance to get the value for
            owner: The owner class
            
        Returns:
            The lazy-loaded value
            
        Raises:
            AttributeError: If accessed on the class rather than an instance
        """
        if instance is None:
            return self
        
        # Create lazy properties dict if it doesn't exist
        if not hasattr(instance, "_lazy_properties"):
            instance._lazy_properties = {}
            
        lazy_props = cast(Dict[str, Any], instance._lazy_properties)
        
        # Check if value is already computed
        if self.name not in lazy_props:
            # Compute and store the value
            lazy_props[self.name] = self.func(instance)
        
        return lazy_props[self.name]
    
    def __set__(self, instance: Any, value: Any) -> None:
        """
        Set the lazy-loaded value directly.
        
        Args:
            instance: The instance to set the value for
            value: The value to store
        """
        if not hasattr(instance, "_lazy_properties"):
            instance._lazy_properties = {}
            
        lazy_props = cast(Dict[str, Any], instance._lazy_properties)
        lazy_props[self.name] = value
        
    def __delete__(self, instance: Any) -> None:
        """
        Delete the lazy-loaded value.
        
        Args:
            instance: The instance to delete the value for
        """
        if hasattr(instance, "_lazy_properties"):
            lazy_props = cast(Dict[str, Any], instance._lazy_properties)
            if self.name in lazy_props:
                del lazy_props[self.name]

