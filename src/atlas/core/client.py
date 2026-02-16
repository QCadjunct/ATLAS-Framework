"""
Client class for the ATLAS Framework.

This module provides the ATLASClient class, which is the main entry point
for interacting with the ATLAS Framework.
"""

import logging
from typing import Any, Dict, List, Optional, Set, Type, TypeVar, Union, cast

from pydantic import BaseModel

from atlas.core.node import ATLASNode
from atlas.core.relationship import ATLASRelationship
from atlas.decorators import atlas_operation
from atlas.enums import NodeLabelType, RelationshipType, ValidationStatusType


logger = logging.getLogger(__name__)


class ATLASClient:
    """
    Client for interacting with the ATLAS Framework.
    
    This class provides methods for creating, querying, and managing
    nodes and relationships in the knowledge graph.
    """
    
    def __init__(
        self,
        graph_adapter: Optional[Any] = None,
        llm_adapter: Optional[Any] = None,
        fabric_registry: Optional[Any] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize the ATLAS client.
        
        Args:
            graph_adapter: Adapter for the graph database
            llm_adapter: Adapter for the language model
            fabric_registry: Registry of FABRIC patterns
            config: Configuration dictionary
        """
        self.graph_adapter = graph_adapter
        self.llm_adapter = llm_adapter
        self.fabric_registry = fabric_registry
        self.config = config or {}
        
        # Initialize adapters if provided
        if self.graph_adapter is not None:
            self.graph_adapter.initialize(self.config.get("graph", {}))
        if self.llm_adapter is not None:
            self.llm_adapter.initialize(self.config.get("llm", {}))
        if self.fabric_registry is not None:
            self.fabric_registry.initialize(self.config.get("fabric", {}))
    
    @atlas_operation("node_creation")
    def create_node(
        self,
        labels: List[Union[str, NodeLabelType]],
        properties: Dict[str, Any],
        behaviors: Optional[List[str]] = None,
    ) -> ATLASNode:
        """
        Create a new node in the knowledge graph.
        
        Args:
            labels: List of node labels
            properties: Dictionary of node properties
            behaviors: Optional list of behavior names to attach
            
        Returns:
            ATLASNode: The created node
        """
        # Create the node
        node = ATLASNode.create(labels, properties, behaviors)
        
        # Persist the node if graph adapter is available
        if self.graph_adapter is not None:
            self.graph_adapter.create_node(node)
        
        return node
    
    @atlas_operation("relationship_creation")
    def create_relationship(
        self,
        relationship_type: Union[str, RelationshipType],
        start_node_id: str,
        end_node_id: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> ATLASRelationship:
        """
        Create a new relationship in the knowledge graph.
        
        Args:
            relationship_type: Type of the relationship
            start_node_id: ID of the start node
            end_node_id: ID of the end node
            properties: Optional dictionary of relationship properties
            
        Returns:
            ATLASRelationship: The created relationship
        """
        # Create the relationship
        relationship = ATLASRelationship.create(
            relationship_type, start_node_id, end_node_id, properties
        )
        
        # Persist the relationship if graph adapter is available
        if self.graph_adapter is not None:
            self.graph_adapter.create_relationship(relationship)
        
        return relationship
    
    @atlas_operation("node_query")
    def get_node(self, node_id: str) -> Optional[ATLASNode]:
        """
        Get a node by ID.
        
        Args:
            node_id: ID of the node to get
            
        Returns:
            Optional[ATLASNode]: The node, or None if not found
        """
        if self.graph_adapter is None:
            logger.warning("No graph adapter available, cannot get node")
            return None
        
        return self.graph_adapter.get_node(node_id)
    
    @atlas_operation("relationship_query")
    def get_relationship(self, relationship_id: str) -> Optional[ATLASRelationship]:
        """
        Get a relationship by ID.
        
        Args:
            relationship_id: ID of the relationship to get
            
        Returns:
            Optional[ATLASRelationship]: The relationship, or None if not found
        """
        if self.graph_adapter is None:
            logger.warning("No graph adapter available, cannot get relationship")
            return None
        
        return self.graph_adapter.get_relationship(relationship_id)
    
    @atlas_operation("node_query")
    def find_nodes(
        self,
        labels: Optional[List[Union[str, NodeLabelType]]] = None,
        properties: Optional[Dict[str, Any]] = None,
        limit: int = 100,
    ) -> List[ATLASNode]:
        """
        Find nodes by labels and properties.
        
        Args:
            labels: Optional list of node labels to filter by
            properties: Optional dictionary of properties to filter by
            limit: Maximum number of nodes to return
            
        Returns:
            List[ATLASNode]: List of matching nodes
        """
        if self.graph_adapter is None:
            logger.warning("No graph adapter available, cannot find nodes")
            return []
        
        return self.graph_adapter.find_nodes(labels, properties, limit)
    
    @atlas_operation("relationship_query")
    def find_relationships(
        self,
        relationship_type: Optional[Union[str, RelationshipType]] = None,
        start_node_id: Optional[str] = None,
        end_node_id: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        limit: int = 100,
    ) -> List[ATLASRelationship]:
        """
        Find relationships by type, nodes, and properties.
        
        Args:
            relationship_type: Optional relationship type to filter by
            start_node_id: Optional start node ID to filter by
            end_node_id: Optional end node ID to filter by
            properties: Optional dictionary of properties to filter by
            limit: Maximum number of relationships to return
            
        Returns:
            List[ATLASRelationship]: List of matching relationships
        """
        if self.graph_adapter is None:
            logger.warning("No graph adapter available, cannot find relationships")
            return []
        
        return self.graph_adapter.find_relationships(
            relationship_type, start_node_id, end_node_id, properties, limit
        )
    
    @atlas_operation("node_update")
    def update_node(self, node_id: str, properties: Dict[str, Any]) -> Optional[ATLASNode]:
        """
        Update a node's properties.
        
        Args:
            node_id: ID of the node to update
            properties: Dictionary of properties to update
            
        Returns:
            Optional[ATLASNode]: The updated node, or None if not found
        """
        if self.graph_adapter is None:
            logger.warning("No graph adapter available, cannot update node")
            return None
        
        node = self.graph_adapter.get_node(node_id)
        if node is None:
            return None
        
        node.update(properties)
        self.graph_adapter.update_node(node)
        
        return node
    
    @atlas_operation("relationship_update")
    def update_relationship(
        self, relationship_id: str, properties: Dict[str, Any]
    ) -> Optional[ATLASRelationship]:
        """
        Update a relationship's properties.
        
        Args:
            relationship_id: ID of the relationship to update
            properties: Dictionary of properties to update
            
        Returns:
            Optional[ATLASRelationship]: The updated relationship, or None if not found
        """
        if self.graph_adapter is None:
            logger.warning("No graph adapter available, cannot update relationship")
            return None
        
        relationship = self.graph_adapter.get_relationship(relationship_id)
        if relationship is None:
            return None
        
        relationship.update(properties)
        self.graph_adapter.update_relationship(relationship)
        
        return relationship
    
    @atlas_operation("node_deletion")
    def delete_node(self, node_id: str) -> bool:
        """
        Delete a node.
        
        Args:
            node_id: ID of the node to delete
            
        Returns:
            bool: True if the node was deleted, False otherwise
        """
        if self.graph_adapter is None:
            logger.warning("No graph adapter available, cannot delete node")
            return False
        
        return self.graph_adapter.delete_node(node_id)
    
    @atlas_operation("relationship_deletion")
    def delete_relationship(self, relationship_id: str) -> bool:
        """
        Delete a relationship.
        
        Args:
            relationship_id: ID of the relationship to delete
            
        Returns:
            bool: True if the relationship was deleted, False otherwise
        """
        if self.graph_adapter is None:
            logger.warning("No graph adapter available, cannot delete relationship")
            return False
        
        return self.graph_adapter.delete_relationship(relationship_id)
    
    @atlas_operation("validation")
    def validate_node(self, node_id: str) -> bool:
        """
        Validate a node.
        
        Args:
            node_id: ID of the node to validate
            
        Returns:
            bool: True if the node is valid, False otherwise
        """
        if self.graph_adapter is None:
            logger.warning("No graph adapter available, cannot validate node")
            return False
        
        node = self.graph_adapter.get_node(node_id)
        if node is None:
            return False
        
        is_valid = node.validate()
        
        if is_valid:
            node.validation_status = ValidationStatusType.VALIDATED
        else:
            node.validation_status = ValidationStatusType.NEEDS_REVIEW
        
        self.graph_adapter.update_node(node)
        
        return is_valid
    
    @atlas_operation("validation")
    def validate_relationship(self, relationship_id: str) -> bool:
        """
        Validate a relationship.
        
        Args:
            relationship_id: ID of the relationship to validate
            
        Returns:
            bool: True if the relationship is valid, False otherwise
        """
        if self.graph_adapter is None:
            logger.warning("No graph adapter available, cannot validate relationship")
            return False
        
        relationship = self.graph_adapter.get_relationship(relationship_id)
        if relationship is None:
            return False
        
        is_valid = relationship.validate()
        
        if is_valid:
            relationship.validation_status = ValidationStatusType.VALIDATED
        else:
            relationship.validation_status = ValidationStatusType.NEEDS_REVIEW
        
        self.graph_adapter.update_relationship(relationship)
        
        return is_valid
    
    @atlas_operation("query")
    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a custom query against the graph database.
        
        Args:
            query: Query string
            parameters: Optional query parameters
            
        Returns:
            Any: Query results
        """
        if self.graph_adapter is None:
            logger.warning("No graph adapter available, cannot execute query")
            return None
        
        return self.graph_adapter.execute_query(query, parameters or {})
    
    def close(self) -> None:
        """
        Close the client and release resources.
        """
        if self.graph_adapter is not None:
            self.graph_adapter.close()
        if self.llm_adapter is not None:
            self.llm_adapter.close()

