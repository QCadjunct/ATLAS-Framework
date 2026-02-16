"""
Cached property descriptor for the ATLAS Framework.

This module provides a descriptor for caching property values,
with optional time-to-live (TTL) functionality.
"""

import time
from typing import Any, Callable, Dict, Optional, TypeVar, cast

T = TypeVar("T")


class CachedProperty:
    """
    Descriptor for caching property values with optional TTL.
    
    This descriptor caches the result of a method call and returns the
    cached value on subsequent calls, until the TTL expires (if specified).
    """
    
    def __init__(
        self, 
        func: Callable[[Any], T], 
        ttl: Optional[float] = None,
        name: Optional[str] = None
    ) -> None:
        """
        Initialize the cached property descriptor.
        
        Args:
            func: The function to cache
            ttl: Time-to-live in seconds, or None for no expiration
            name: Optional name for the property, defaults to the function name
        """
        self.func = func
        self.ttl = ttl
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
        Get the cached value or compute and cache it.
        
        Args:
            instance: The instance to get the value for
            owner: The owner class
            
        Returns:
            The cached value
            
        Raises:
            AttributeError: If accessed on the class rather than an instance
        """
        if instance is None:
            return self
        
        # Create cache dict if it doesn't exist
        if not hasattr(instance, "_cached_properties"):
            instance._cached_properties = {}
            
        cache = cast(Dict[str, Dict[str, Any]], instance._cached_properties)
        
        # Check if value is cached and not expired
        if self.name in cache:
            entry = cache[self.name]
            if self.ttl is None or time.time() - entry["timestamp"] < self.ttl:
                return entry["value"]
        
        # Compute and cache the value
        value = self.func(instance)
        cache[self.name] = {
            "value": value,
            "timestamp": time.time()
        }
        
        return value
    
    def __set__(self, instance: Any, value: Any) -> None:
        """
        Set the cached value directly.
        
        Args:
            instance: The instance to set the value for
            value: The value to cache
        """
        if not hasattr(instance, "_cached_properties"):
            instance._cached_properties = {}
            
        cache = cast(Dict[str, Dict[str, Any]], instance._cached_properties)
        
        cache[self.name] = {
            "value": value,
            "timestamp": time.time()
        }
        
    def __delete__(self, instance: Any) -> None:
        """
        Delete the cached value.
        
        Args:
            instance: The instance to delete the value for
        """
        if hasattr(instance, "_cached_properties"):
            cache = cast(Dict[str, Dict[str, Any]], instance._cached_properties)
            if self.name in cache:
                del cache[self.name]

