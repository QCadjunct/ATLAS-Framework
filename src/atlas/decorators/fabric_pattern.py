"""
FABRIC pattern decorator for the ATLAS Framework.

This module provides a decorator for applying FABRIC patterns to functions,
enabling complex reasoning and analysis.
"""

import functools
import logging
from typing import Any, Callable, Dict, Optional, TypeVar, cast

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])

logger = logging.getLogger(__name__)


def fabric_pattern(
    pattern_name: str,
    parameters: Optional[Dict[str, Any]] = None,
) -> Callable[[F], F]:
    """
    Decorator for applying FABRIC patterns to functions.
    
    This decorator wraps a function with a FABRIC pattern,
    which enhances its reasoning and analysis capabilities.
    
    Args:
        pattern_name: Name of the FABRIC pattern to apply
        parameters: Optional parameters for the pattern
        
    Returns:
        Decorated function
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get instance (self) if this is a method
            instance = args[0] if args else None
            
            # Log pattern application
            logger.info(f"Applying FABRIC pattern '{pattern_name}' to {func.__name__}")
            
            # Get pattern parameters
            pattern_params = parameters or {}
            
            # Check if FABRIC registry is available
            fabric_registry = None
            if instance is not None and hasattr(instance, "fabric_registry"):
                fabric_registry = instance.fabric_registry
            
            # Apply pattern if registry is available
            if fabric_registry is not None:
                # Get the pattern from the registry
                pattern = fabric_registry.get_pattern(pattern_name)
                if pattern is None:
                    logger.warning(f"FABRIC pattern '{pattern_name}' not found in registry")
                    return func(*args, **kwargs)
                
                # Apply the pattern
                try:
                    # Execute the function
                    result = func(*args, **kwargs)
                    
                    # Process the result with the pattern
                    enhanced_result = pattern.process(result, **pattern_params)
                    
                    logger.info(f"Successfully applied FABRIC pattern '{pattern_name}'")
                    return enhanced_result
                except Exception as e:
                    logger.error(f"Error applying FABRIC pattern '{pattern_name}': {e}")
                    # Fall back to original function
                    return func(*args, **kwargs)
            else:
                # No registry available, just call the function
                logger.warning("No FABRIC registry available, skipping pattern application")
                return func(*args, **kwargs)
            
        return cast(F, wrapper)
    
    return decorator

