"""
Atlas operation decorator for the ATLAS Framework.

This module provides a decorator for tracking and managing operations
in the ATLAS Framework, with support for retry, logging, and monitoring.
"""

import functools
import logging
import time
from typing import Any, Callable, Dict, Optional, TypeVar, cast

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])

logger = logging.getLogger(__name__)


def atlas_operation(
    operation_type: str,
    requires_validation: bool = False,
    retry_attempts: int = 0,
    retry_delay: float = 1.0,
    cache_result: bool = False,
    log_level: int = logging.INFO,
) -> Callable[[F], F]:
    """
    Decorator for ATLAS Framework operations.
    
    This decorator adds tracking, logging, retry logic, and optional caching
    to ATLAS Framework operations.
    
    Args:
        operation_type: Type of operation (e.g., "validation", "graph_update")
        requires_validation: Whether the operation requires validation
        retry_attempts: Number of retry attempts for failed operations
        retry_delay: Delay between retry attempts in seconds
        cache_result: Whether to cache the result of the operation
        log_level: Logging level for operation logs
        
    Returns:
        Decorated function
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get instance (self) if this is a method
            instance = args[0] if args else None
            
            # Generate operation ID
            operation_id = f"{operation_type}_{func.__name__}_{time.time()}"
            
            # Log operation start
            logger.log(log_level, f"Starting operation {operation_id}")
            
            # Check if result is already cached
            if cache_result and hasattr(instance, "_operation_cache"):
                cache_key = f"{func.__name__}_{args}_{kwargs}"
                if cache_key in instance._operation_cache:
                    logger.log(log_level, f"Returning cached result for {operation_id}")
                    return instance._operation_cache[cache_key]
            
            # Check if validation is required
            if requires_validation and instance is not None:
                if hasattr(instance, "validate"):
                    validation_result = instance.validate()
                    if not validation_result:
                        logger.error(f"Validation failed for {operation_id}")
                        raise ValueError(f"Validation failed for {operation_type} operation")
            
            # Execute with retry logic
            attempt = 0
            last_error = None
            
            while attempt <= retry_attempts:
                try:
                    start_time = time.time()
                    result = func(*args, **kwargs)
                    end_time = time.time()
                    
                    # Log operation completion
                    duration = end_time - start_time
                    logger.log(log_level, f"Completed operation {operation_id} in {duration:.3f}s")
                    
                    # Cache result if requested
                    if cache_result and instance is not None:
                        if not hasattr(instance, "_operation_cache"):
                            instance._operation_cache = {}
                        cache_key = f"{func.__name__}_{args}_{kwargs}"
                        instance._operation_cache[cache_key] = result
                    
                    return result
                    
                except Exception as e:
                    last_error = e
                    attempt += 1
                    
                    if attempt <= retry_attempts:
                        logger.warning(
                            f"Operation {operation_id} failed (attempt {attempt}/{retry_attempts+1}): {e}"
                        )
                        time.sleep(retry_delay)
                    else:
                        logger.error(f"Operation {operation_id} failed after {retry_attempts+1} attempts: {e}")
                        raise
            
            # This should never be reached due to the raise in the loop
            assert last_error is not None
            raise last_error
            
        return cast(F, wrapper)
    
    return decorator

