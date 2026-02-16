"""
Graph operation validation decorator for the ATLAS Framework.

This module provides a decorator for validating graph operations,
ensuring that they meet certain criteria before execution.
"""

import functools
import logging
from typing import Any, Callable, List, Optional, TypeVar, Union, cast

from atlas.core.exceptions import GraphError

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])

logger = logging.getLogger(__name__)


def validate_graph_operation(
    require_connection: bool = True,
    allowed_node_labels: Optional[List[str]] = None,
    allowed_relationship_types: Optional[List[str]] = None,
    check_node_exists: bool = False,
    check_relationship_exists: bool = False,
) -> Callable[[F], F]:
    """
    Decorator for validating graph operations.
    
    This decorator validates graph operations before execution,
    ensuring that they meet certain criteria.
    
    Args:
        require_connection: Whether to require an active graph connection
        allowed_node_labels: List of allowed node labels, or None for any
        allowed_relationship_types: List of allowed relationship types, or None for any
        check_node_exists: Whether to check if nodes exist before operations
        check_relationship_exists: Whether to check if relationships exist before operations
        
    Returns:
        Decorated function
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get instance (self) if this is a method
            instance = args[0] if args else None
            
            # Check if graph adapter is available
            graph_adapter = None
            if instance is not None:
                if hasattr(instance, "graph_adapter"):
                    graph_adapter = instance.graph_adapter
                elif hasattr(instance, "client") and hasattr(instance.client, "graph_adapter"):
                    graph_adapter = instance.client.graph_adapter
            
            if require_connection and (graph_adapter is None or not graph_adapter.is_connected()):
                raise GraphError("No active graph connection")
            
            # Extract node labels and relationship types from args/kwargs
            node_labels = []
            relationship_types = []
            
            # Check for node labels in kwargs
            if "labels" in kwargs:
                node_labels = kwargs["labels"]
            elif "label" in kwargs:
                node_labels = [kwargs["label"]]
                
            # Check for relationship types in kwargs
            if "relationship_type" in kwargs:
                relationship_types = [kwargs["relationship_type"]]
            elif "type" in kwargs and "relationship" in kwargs.get("entity_type", ""):
                relationship_types = [kwargs["type"]]
            
            # Validate node labels if specified
            if allowed_node_labels and node_labels:
                for label in node_labels:
                    if label not in allowed_node_labels:
                        raise GraphError(f"Node label '{label}' is not allowed")
            
            # Validate relationship types if specified
            if allowed_relationship_types and relationship_types:
                for rel_type in relationship_types:
                    if rel_type not in allowed_relationship_types:
                        raise GraphError(f"Relationship type '{rel_type}' is not allowed")
            
            # Check if nodes exist if required
            if check_node_exists and graph_adapter is not None:
                node_ids = []
                
                # Extract node IDs from args/kwargs
                if "node_id" in kwargs:
                    node_ids.append(kwargs["node_id"])
                elif "id" in kwargs and "node" in kwargs.get("entity_type", ""):
                    node_ids.append(kwargs["id"])
                elif "start_node_id" in kwargs:
                    node_ids.append(kwargs["start_node_id"])
                elif "end_node_id" in kwargs:
                    node_ids.append(kwargs["end_node_id"])
                
                # Check each node ID
                for node_id in node_ids:
                    if not graph_adapter.node_exists(node_id):
                        raise GraphError(f"Node with ID '{node_id}' does not exist")
            
            # Check if relationships exist if required
            if check_relationship_exists and graph_adapter is not None:
                rel_ids = []
                
                # Extract relationship IDs from args/kwargs
                if "relationship_id" in kwargs:
                    rel_ids.append(kwargs["relationship_id"])
                elif "id" in kwargs and "relationship" in kwargs.get("entity_type", ""):
                    rel_ids.append(kwargs["id"])
                
                # Check each relationship ID
                for rel_id in rel_ids:
                    if not graph_adapter.relationship_exists(rel_id):
                        raise GraphError(f"Relationship with ID '{rel_id}' does not exist")
            
            # All validations passed, execute the function
            return func(*args, **kwargs)
            
        return cast(F, wrapper)
    
    return decorator

