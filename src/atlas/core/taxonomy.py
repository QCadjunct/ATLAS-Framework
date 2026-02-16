"""
Taxonomy extractor for the ATLAS Framework.

This module provides the TaxonomyExtractor class, which extracts taxonomies
from various sources using agentic LLMs.
"""

import logging
from typing import Any, Dict, List, Optional, Set, Union

from atlas.core.client import ATLASClient
from atlas.core.node import ATLASNode
from atlas.core.relationship import ATLASRelationship
from atlas.decorators import atlas_operation, fabric_pattern
from atlas.enums import NodeLabelType, RelationshipType


logger = logging.getLogger(__name__)


class TaxonomyExtractor:
    """
    Extractor for taxonomies from various sources.
    
    This class provides methods for extracting taxonomies from text,
    websites, and other sources using agentic LLMs.
    """
    
    def __init__(
        self,
        client: ATLASClient,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize the taxonomy extractor.
        
        Args:
            client: ATLAS client for interacting with the knowledge graph
            config: Optional configuration dictionary
        """
        self.client = client
        self.config = config or {}
    
    @atlas_operation("extraction")
    @fabric_pattern("extract_wisdom")
    def extract_from_text(
        self,
        text: str,
        domain: str,
        labels: Optional[List[Union[str, NodeLabelType]]] = None,
    ) -> List[ATLASNode]:
        """
        Extract taxonomy nodes from text.
        
        Args:
            text: Text to extract from
            domain: Domain of the taxonomy (e.g., "energy", "healthcare")
            labels: Optional list of node labels to assign
            
        Returns:
            List[ATLASNode]: List of extracted nodes
        """
        if self.client.llm_adapter is None:
            logger.warning("No LLM adapter available, cannot extract taxonomy")
            return []
        
        # Default labels if not provided
        if not labels:
            labels = [NodeLabelType.TAXONOMY_NODE]
        
        # Extract concepts using LLM
        extraction_result = self.client.llm_adapter.extract_concepts(
            text=text,
            domain=domain,
            extraction_type="taxonomy",
        )
        
        # Create nodes for extracted concepts
        nodes = []
        for concept in extraction_result.get("concepts", []):
            properties = {
                "name": concept["name"],
                "definition": concept.get("definition", ""),
                "domain": domain,
                "confidence": concept.get("confidence", 0.0),
                "source": "text_extraction",
            }
            
            # Add any additional properties from the extraction
            for key, value in concept.items():
                if key not in ["name", "definition", "relationships"]:
                    properties[key] = value
            
            # Create the node
            node = self.client.create_node(labels, properties)
            nodes.append(node)
        
        # Create relationships between nodes
        for concept in extraction_result.get("concepts", []):
            if "relationships" in concept:
                source_node = next(
                    (n for n in nodes if n.properties["name"] == concept["name"]),
                    None,
                )
                if source_node is None:
                    continue
                
                for rel in concept["relationships"]:
                    target_node = next(
                        (n for n in nodes if n.properties["name"] == rel["target"]),
                        None,
                    )
                    if target_node is None:
                        continue
                    
                    rel_type = rel.get("type", "RELATED_TO")
                    rel_props = {
                        "confidence": rel.get("confidence", 0.0),
                        "source": "text_extraction",
                    }
                    
                    # Add any additional properties from the relationship
                    for key, value in rel.items():
                        if key not in ["type", "target", "source"]:
                            rel_props[key] = value
                    
                    self.client.create_relationship(
                        rel_type, source_node.id, target_node.id, rel_props
                    )
        
        return nodes
    
    @atlas_operation("extraction")
    @fabric_pattern("extract_wisdom")
    def extract_from_website(
        self,
        url: str,
        domain: str,
        labels: Optional[List[Union[str, NodeLabelType]]] = None,
    ) -> List[ATLASNode]:
        """
        Extract taxonomy nodes from a website.
        
        Args:
            url: URL of the website to extract from
            domain: Domain of the taxonomy (e.g., "energy", "healthcare")
            labels: Optional list of node labels to assign
            
        Returns:
            List[ATLASNode]: List of extracted nodes
        """
        if self.client.llm_adapter is None:
            logger.warning("No LLM adapter available, cannot extract taxonomy")
            return []
        
        # Default labels if not provided
        if not labels:
            labels = [NodeLabelType.TAXONOMY_NODE]
        
        # Extract text from website
        if hasattr(self.client.llm_adapter, "extract_text_from_url"):
            text = self.client.llm_adapter.extract_text_from_url(url)
        else:
            logger.warning("LLM adapter does not support website extraction")
            return []
        
        # Extract concepts from the text
        return self.extract_from_text(text, domain, labels)
    
    @atlas_operation("extraction")
    @fabric_pattern("extract_wisdom")
    def extract_from_glossary(
        self,
        glossary: Dict[str, str],
        domain: str,
        labels: Optional[List[Union[str, NodeLabelType]]] = None,
    ) -> List[ATLASNode]:
        """
        Extract taxonomy nodes from a glossary.
        
        Args:
            glossary: Dictionary mapping terms to definitions
            domain: Domain of the taxonomy (e.g., "energy", "healthcare")
            labels: Optional list of node labels to assign
            
        Returns:
            List[ATLASNode]: List of extracted nodes
        """
        # Default labels if not provided
        if not labels:
            labels = [NodeLabelType.TAXONOMY_NODE]
        
        # Create nodes for glossary terms
        nodes = []
        for term, definition in glossary.items():
            properties = {
                "name": term,
                "definition": definition,
                "domain": domain,
                "source": "glossary",
            }
            
            # Create the node
            node = self.client.create_node(labels, properties)
            nodes.append(node)
        
        # If LLM adapter is available, extract relationships
        if self.client.llm_adapter is not None:
            # Extract relationships using LLM
            for source_node in nodes:
                for target_node in nodes:
                    if source_node.id == target_node.id:
                        continue
                    
                    relationship_result = self.client.llm_adapter.analyze_relationship(
                        source=source_node.properties["name"],
                        source_definition=source_node.properties["definition"],
                        target=target_node.properties["name"],
                        target_definition=target_node.properties["definition"],
                        domain=domain,
                    )
                    
                    if relationship_result.get("has_relationship", False):
                        rel_type = relationship_result.get("relationship_type", "RELATED_TO")
                        rel_props = {
                            "confidence": relationship_result.get("confidence", 0.0),
                            "source": "glossary_analysis",
                        }
                        
                        # Add any additional properties from the relationship analysis
                        for key, value in relationship_result.items():
                            if key not in ["has_relationship", "relationship_type", "source", "target"]:
                                rel_props[key] = value
                        
                        self.client.create_relationship(
                            rel_type, source_node.id, target_node.id, rel_props
                        )
        
        return nodes
    
    @atlas_operation("analysis")
    @fabric_pattern("find_patterns")
    def analyze_taxonomy(self, domain: str) -> Dict[str, Any]:
        """
        Analyze the extracted taxonomy.
        
        Args:
            domain: Domain of the taxonomy to analyze
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        if self.client.graph_adapter is None:
            logger.warning("No graph adapter available, cannot analyze taxonomy")
            return {}
        
        # Find all nodes in the domain
        nodes = self.client.find_nodes(
            properties={"domain": domain}
        )
        
        # Find all relationships between these nodes
        relationships = []
        for node in nodes:
            # Find relationships where this node is the start node
            outgoing = self.client.find_relationships(
                start_node_id=node.id
            )
            relationships.extend(outgoing)
            
            # Find relationships where this node is the end node
            incoming = self.client.find_relationships(
                end_node_id=node.id
            )
            relationships.extend(incoming)
        
        # Deduplicate relationships
        unique_relationships = {rel.id: rel for rel in relationships}.values()
        
        # Analyze the taxonomy
        analysis = {
            "domain": domain,
            "node_count": len(nodes),
            "relationship_count": len(unique_relationships),
            "node_label_distribution": self._count_node_labels(nodes),
            "relationship_type_distribution": self._count_relationship_types(unique_relationships),
            "connectivity": self._calculate_connectivity(nodes, unique_relationships),
            "hierarchical_depth": self._calculate_hierarchical_depth(nodes, unique_relationships),
        }
        
        return analysis
    
    def _count_node_labels(self, nodes: List[ATLASNode]) -> Dict[str, int]:
        """
        Count the distribution of node labels.
        
        Args:
            nodes: List of nodes to analyze
            
        Returns:
            Dict[str, int]: Mapping of label values to counts
        """
        label_counts = {}
        for node in nodes:
            for label in node.labels:
                label_value = label.value
                label_counts[label_value] = label_counts.get(label_value, 0) + 1
        return label_counts
    
    def _count_relationship_types(self, relationships: List[ATLASRelationship]) -> Dict[str, int]:
        """
        Count the distribution of relationship types.
        
        Args:
            relationships: List of relationships to analyze
            
        Returns:
            Dict[str, int]: Mapping of relationship type values to counts
        """
        type_counts = {}
        for rel in relationships:
            type_value = rel.type.value
            type_counts[type_value] = type_counts.get(type_value, 0) + 1
        return type_counts
    
    def _calculate_connectivity(
        self, nodes: List[ATLASNode], relationships: List[ATLASRelationship]
    ) -> float:
        """
        Calculate the connectivity of the taxonomy.
        
        Connectivity is the ratio of actual relationships to possible relationships.
        
        Args:
            nodes: List of nodes in the taxonomy
            relationships: List of relationships in the taxonomy
            
        Returns:
            float: Connectivity ratio (0.0 to 1.0)
        """
        if len(nodes) <= 1:
            return 0.0
        
        # Maximum possible relationships in a directed graph
        max_relationships = len(nodes) * (len(nodes) - 1)
        
        if max_relationships == 0:
            return 0.0
        
        return len(relationships) / max_relationships
    
    def _calculate_hierarchical_depth(
        self, nodes: List[ATLASNode], relationships: List[ATLASRelationship]
    ) -> int:
        """
        Calculate the maximum hierarchical depth of the taxonomy.
        
        Args:
            nodes: List of nodes in the taxonomy
            relationships: List of relationships in the taxonomy
            
        Returns:
            int: Maximum hierarchical depth
        """
        # Build adjacency list for hierarchical relationships
        adjacency = {}
        for node in nodes:
            adjacency[node.id] = []
        
        for rel in relationships:
            if rel.is_hierarchical:
                adjacency[rel.start_node_id].append(rel.end_node_id)
        
        # Find maximum depth using DFS
        max_depth = 0
        visited = set()
        
        def dfs(node_id: str, depth: int) -> None:
            nonlocal max_depth
            if depth > max_depth:
                max_depth = depth
            
            visited.add(node_id)
            for child_id in adjacency.get(node_id, []):
                if child_id not in visited:
                    dfs(child_id, depth + 1)
        
        # Start DFS from each node
        for node in nodes:
            if node.id not in visited:
                dfs(node.id, 0)
        
        return max_depth

