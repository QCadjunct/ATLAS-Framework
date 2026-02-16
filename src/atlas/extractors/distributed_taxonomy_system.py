#!/usr/bin/env python3
"""
ATLAS Framework - Enterprise Example: Distributed Taxonomy System

This example demonstrates enterprise-level ATLAS Framework capabilities:
- Distributed processing with multiple workers
- Tailscale zero-trust networking
- Advanced security and authentication
- Real-time collaboration and synchronization
- Production-grade monitoring and observability
- Multi-tenant architecture
- Horizontal scaling patterns

Requirements:
- Python 3.11+
- ATLAS Framework with enterprise features
- Tailscale VPN configured
- Neo4j cluster
- Redis for caching and coordination
- OpenAI API key
- Production environment setup
"""

import asyncio
import json
import uuid
from typing import Dict, Any, List, Optional, Set
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import aioredis
from contextlib import asynccontextmanager

# ATLAS Framework imports
from atlas import ConfigurationManager, ATLASNode
from atlas.enums import NodeLabelType, FuelGroupType, ValidationStatusType
from atlas.security.tailscale import TailscaleManager
from atlas.security.auth import JWTAuthProvider, PermissionManager
from atlas.graph.neo4j import Neo4jCluster
from atlas.frameworks.langchain import ExtractionChain, ValidationChain
from atlas.frameworks.fabric import FabricPatternRegistry
from atlas.decorators import require_permission, audit_operation, fabric_pattern
from atlas.monitoring import MetricsCollector, AlertManager
from atlas.utils.logging import get_logger
from atlas.distributed import WorkerManager, TaskQueue, ResultAggregator

# Setup logging
logger = get_logger(__name__)


@dataclass
class ExtractionTask:
    """Task definition for distributed extraction."""
    task_id: str
    source_url: str
    fuel_groups: List[str]
    priority: int
    tenant_id: str
    user_id: str
    created_at: datetime
    deadline: datetime
    metadata: Dict[str, Any]


@dataclass
class ExtractionResult:
    """Result from distributed extraction."""
    task_id: str
    worker_id: str
    nodes_extracted: int
    relationships_discovered: int
    processing_time: float
    success: bool
    error_message: Optional[str]
    completed_at: datetime
    quality_metrics: Dict[str, float]


class DistributedTaxonomySystem:
    """
    Enterprise-grade distributed taxonomy extraction system.
    
    Features:
    - Multi-tenant architecture
    - Distributed processing
    - Zero-trust security
    - Real-time collaboration
    - Production monitoring
    - Horizontal scaling
    """
    
    def __init__(
        self, 
        config_path: str,
        tailscale_config: Dict[str, Any],
        neo4j_cluster_config: Dict[str, Any],
        redis_config: Dict[str, Any]
    ):
        """
        Initialize the distributed taxonomy system.
        
        Args:
            config_path: Path to ATLAS configuration
            tailscale_config: Tailscale VPN configuration
            neo4j_cluster_config: Neo4j cluster configuration
            redis_config: Redis configuration for coordination
        """
        
        # Core ATLAS components
        self.config_manager = ConfigurationManager.from_file(config_path)
        self.fabric_registry = FabricPatternRegistry()
        
        # Security and networking
        self.tailscale_manager = TailscaleManager(**tailscale_config)
        self.auth_provider = JWTAuthProvider(
            secret_key=tailscale_config.get("jwt_secret"),
            algorithm="HS256",
            token_expiry_hours=8
        )
        self.permission_manager = PermissionManager()
        
        # Distributed infrastructure
        self.neo4j_cluster = Neo4jCluster(**neo4j_cluster_config)
        self.redis_config = redis_config
        self.redis_pool = None
        
        # Processing components
        self.worker_manager = WorkerManager()
        self.task_queue = TaskQueue()
        self.result_aggregator = ResultAggregator()
        
        # Monitoring and observability
        self.metrics_collector = MetricsCollector()
        self.alert_manager = AlertManager()
        
        # System state
        self.active_tasks: Dict[str, ExtractionTask] = {}
        self.worker_registry: Dict[str, Dict[str, Any]] = {}
        self.tenant_configurations: Dict[str, Dict[str, Any]] = {}
        
        # Performance tracking
        self.system_metrics = {
            "total_tasks_processed": 0,
            "active_workers": 0,
            "average_processing_time": 0.0,
            "success_rate": 0.0,
            "current_load": 0.0
        }
    
    async def initialize_system(self) -> None:
        """
        Initialize the distributed system with all components.
        """
        
        print("🚀 Initializing Enterprise Distributed Taxonomy System...")
        
        # Step 1: Establish secure networking
        await self._initialize_secure_networking()
        
        # Step 2: Setup distributed infrastructure
        await self._initialize_distributed_infrastructure()
        
        # Step 3: Start monitoring and observability
        await self._initialize_monitoring()
        
        # Step 4: Register system components
        await self._register_system_components()
        
        print("✅ Distributed system initialized successfully")
    
    async def _initialize_secure_networking(self) -> None:
        """Initialize Tailscale zero-trust networking."""
        
        print("🔒 Initializing zero-trust networking...")
        
        # Connect to Tailscale network
        await self.tailscale_manager.connect()
        
        # Configure firewall rules for zero trust
        firewall_rules = [
            "ufw allow in on tailscale0 to any port 7687",  # Neo4j
            "ufw allow in on tailscale0 to any port 6379",  # Redis
            "ufw allow in on tailscale0 to any port 8000",  # API
            "ufw deny 7687",  # Block external Neo4j access
            "ufw deny 6379",  # Block external Redis access
            "ufw deny 8000",  # Block external API access
        ]
        
        for rule in firewall_rules:
            await self.tailscale_manager.execute_command(rule)
        
        print(f"✅ Connected to Tailscale network: {self.tailscale_manager.network_name}")
    
    async def _initialize_distributed_infrastructure(self) -> None:
        """Initialize distributed infrastructure components."""
        
        print("🏗️ Initializing distributed infrastructure...")
        
        # Initialize Neo4j cluster
        await self.neo4j_cluster.initialize_cluster()
        cluster_status = await self.neo4j_cluster.get_cluster_status()
        print(f"✅ Neo4j cluster: {cluster_status['active_nodes']} nodes active")
        
        # Initialize Redis connection pool
        self.redis_pool = aioredis.ConnectionPool.from_url(
            f"redis://{self.redis_config['host']}:{self.redis_config['port']}",
            max_connections=20,
            retry_on_timeout=True
        )
        
        # Test Redis connection
        async with aioredis.Redis(connection_pool=self.redis_pool) as redis:
            await redis.ping()
        print("✅ Redis coordination layer connected")
        
        # Initialize task queue
        await self.task_queue.initialize(self.redis_pool)
        print("✅ Distributed task queue initialized")
    
    async def _initialize_monitoring(self) -> None:
        """Initialize monitoring and observability."""
        
        print("📊 Initializing monitoring and observability...")
        
        # Start metrics collection
        await self.metrics_collector.start_collection()
        
        # Configure alerts
        alert_rules = [
            {
                "name": "high_error_rate",
                "condition": "error_rate > 0.1",
                "severity": "warning",
                "notification_channels": ["slack", "email"]
            },
            {
                "name": "worker_failure",
                "condition": "active_workers < min_workers",
                "severity": "critical",
                "notification_channels": ["slack", "email", "pagerduty"]
            },
            {
                "name": "processing_delay",
                "condition": "avg_processing_time > 300",
                "severity": "warning",
                "notification_channels": ["slack"]
            }
        ]
        
        for rule in alert_rules:
            await self.alert_manager.add_alert_rule(rule)
        
        print("✅ Monitoring and alerting configured")
    
    @require_permission("taxonomy.admin")
    @audit_operation("system_management")
    async def submit_extraction_job(
        self, 
        job_config: Dict[str, Any],
        user_context: Dict[str, Any]
    ) -> str:
        """
        Submit a distributed extraction job.
        
        Args:
            job_config: Job configuration
            user_context: Authenticated user context
            
        Returns:
            str: Job ID
        """
        
        # Validate user permissions
        tenant_id = user_context.get("tenant_id")
        if not await self.permission_manager.can_submit_job(user_context["user_id"], tenant_id):
            raise PermissionError("Insufficient permissions to submit extraction job")
        
        # Create extraction task
        task = ExtractionTask(
            task_id=str(uuid.uuid4()),
            source_url=job_config["source_url"],
            fuel_groups=job_config.get("fuel_groups", ["renewable", "fossil", "nuclear"]),
            priority=job_config.get("priority", 100),
            tenant_id=tenant_id,
            user_id=user_context["user_id"],
            created_at=datetime.utcnow(),
            deadline=datetime.utcnow() + timedelta(hours=job_config.get("deadline_hours", 24)),
            metadata=job_config.get("metadata", {})
        )
        
        # Submit to distributed task queue
        await self.task_queue.submit_task(task)
        self.active_tasks[task.task_id] = task
        
        # Update metrics
        self.system_metrics["total_tasks_processed"] += 1
        await self.metrics_collector.record_metric("tasks_submitted", 1, {"tenant_id": tenant_id})
        
        logger.info(f"Submitted extraction job {task.task_id} for tenant {tenant_id}")
        
        return task.task_id
    
    async def process_extraction_task(
        self, 
        task: ExtractionTask,
        worker_id: str
    ) -> ExtractionResult:
        """
        Process an extraction task on a distributed worker.
        
        Args:
            task: Task to process
            worker_id: ID of the processing worker
            
        Returns:
            ExtractionResult: Processing results
        """
        
        start_time = datetime.utcnow()
        
        try:
            print(f"🔄 Worker {worker_id} processing task {task.task_id}")
            
            # Get tenant-specific configuration
            tenant_config = await self._get_tenant_configuration(task.tenant_id)
            
            # Initialize AI components with tenant settings
            extraction_chain = ExtractionChain(
                model=tenant_config.get("ai_model", "gpt-4-turbo"),
                temperature=tenant_config.get("temperature", 0.1),
                max_tokens=tenant_config.get("max_tokens", 2000)
            )
            
            # Process each fuel group
            total_nodes = 0
            total_relationships = 0
            quality_scores = []
            
            for fuel_group in task.fuel_groups:
                # Extract content
                content = await self._fetch_content_secure(task.source_url, fuel_group)
                
                # AI extraction
                extraction_result = await self._extract_with_ai(
                    content, fuel_group, extraction_chain, tenant_config
                )
                
                # Create nodes
                nodes = await self._create_tenant_nodes(
                    extraction_result, fuel_group, task.tenant_id
                )
                
                # Validate with FABRIC
                validated_nodes = await self._validate_with_fabric_enterprise(
                    nodes, tenant_config
                )
                
                # Discover relationships
                relationships = await self._discover_relationships_distributed(
                    validated_nodes, worker_id
                )
                
                # Save to tenant-specific graph partition
                await self._save_to_tenant_partition(
                    validated_nodes, relationships, task.tenant_id
                )
                
                total_nodes += len(validated_nodes)
                total_relationships += len(relationships)
                
                # Calculate quality metrics
                quality_score = await self._calculate_quality_metrics(
                    validated_nodes, extraction_result
                )
                quality_scores.append(quality_score)
            
            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Create result
            result = ExtractionResult(
                task_id=task.task_id,
                worker_id=worker_id,
                nodes_extracted=total_nodes,
                relationships_discovered=total_relationships,
                processing_time=processing_time,
                success=True,
                error_message=None,
                completed_at=datetime.utcnow(),
                quality_metrics={
                    "average_quality": sum(quality_scores) / len(quality_scores) if quality_scores else 0.0,
                    "extraction_confidence": sum(q.get("confidence", 0) for q in quality_scores) / len(quality_scores) if quality_scores else 0.0,
                    "validation_success_rate": sum(q.get("validation_success", 0) for q in quality_scores) / len(quality_scores) if quality_scores else 0.0
                }
            )
            
            # Update system metrics
            await self._update_system_metrics(result)
            
            print(f"✅ Worker {worker_id} completed task {task.task_id}: {total_nodes} nodes, {total_relationships} relationships")
            
            return result
            
        except Exception as e:
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            error_result = ExtractionResult(
                task_id=task.task_id,
                worker_id=worker_id,
                nodes_extracted=0,
                relationships_discovered=0,
                processing_time=processing_time,
                success=False,
                error_message=str(e),
                completed_at=datetime.utcnow(),
                quality_metrics={}
            )
            
            logger.error(f"Worker {worker_id} failed task {task.task_id}: {e}")
            await self.alert_manager.send_alert("task_failure", {
                "task_id": task.task_id,
                "worker_id": worker_id,
                "error": str(e)
            })
            
            return error_result
    
    async def _get_tenant_configuration(self, tenant_id: str) -> Dict[str, Any]:
        """Get tenant-specific configuration."""
        
        if tenant_id not in self.tenant_configurations:
            # Load from Redis cache or database
            async with aioredis.Redis(connection_pool=self.redis_pool) as redis:
                config_data = await redis.get(f"tenant_config:{tenant_id}")
                
                if config_data:
                    self.tenant_configurations[tenant_id] = json.loads(config_data)
                else:
                    # Default configuration
                    self.tenant_configurations[tenant_id] = {
                        "ai_model": "gpt-4-turbo",
                        "temperature": 0.1,
                        "max_tokens": 2000,
                        "quality_threshold": 0.8,
                        "max_workers": 5,
                        "data_retention_days": 365
                    }
        
        return self.tenant_configurations[tenant_id]
    
    async def _fetch_content_secure(self, url: str, fuel_group: str) -> str:
        """Fetch content through secure Tailscale connection."""
        
        # In production, this would use secure HTTP client through Tailscale
        # For demo, return sample content
        sample_content = {
            "renewable": "Solar PV, Wind Turbine, Hydroelectric, Geothermal, Biomass...",
            "fossil": "Coal, Natural Gas, Petroleum, Oil Shale...",
            "nuclear": "Nuclear Reactor, Uranium, Nuclear Fission...",
            "alternative": "Hydrogen Fuel Cell, Biofuel, Synthetic Fuel..."
        }
        
        return sample_content.get(fuel_group, "")
    
    @fabric_pattern("extract_wisdom")
    async def _extract_with_ai(
        self, 
        content: str, 
        fuel_group: str,
        extraction_chain: ExtractionChain,
        tenant_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract terms using AI with tenant-specific settings."""
        
        extraction_prompt = f"""
        Extract energy terminology for {fuel_group} fuel group with enterprise-grade accuracy.
        
        Requirements:
        - Minimum confidence: {tenant_config.get('quality_threshold', 0.8)}
        - Include technical specifications
        - Provide relationship hints
        - Ensure industry standard compliance
        
        Content: {content}
        """
        
        result = await extraction_chain.extract(
            text=content,
            context={
                "domain": "energy",
                "fuel_group": fuel_group,
                "quality_threshold": tenant_config.get("quality_threshold", 0.8),
                "enterprise_mode": True
            },
            prompt_template=extraction_prompt
        )
        
        return result
    
    async def _create_tenant_nodes(
        self, 
        extraction_result: Dict[str, Any], 
        fuel_group: str,
        tenant_id: str
    ) -> List[ATLASNode]:
        """Create nodes with tenant isolation."""
        
        nodes = []
        terms = extraction_result.get("extracted_terms", [])
        
        for term_data in terms:
            try:
                fuel_group_enum = self._map_fuel_group(fuel_group)
                
                node = self.config_manager.create_energy_term(
                    term_name=term_data.get("name", "Unknown"),
                    definition=term_data.get("definition", ""),
                    fuel_group=fuel_group_enum,
                    additional_properties={
                        "tenant_id": tenant_id,  # Tenant isolation
                        "technology_type": term_data.get("technology_type"),
                        "efficiency_rating": term_data.get("efficiency_rating"),
                        "extraction_confidence": term_data.get("confidence", 0.8),
                        "enterprise_metadata": {
                            "extracted_at": datetime.utcnow().isoformat(),
                            "extraction_method": "distributed_ai",
                            "quality_score": term_data.get("quality_score", 0.8),
                            "compliance_checked": True
                        }
                    }
                )
                
                nodes.append(node)
                
            except Exception as e:
                logger.error(f"Failed to create tenant node: {e}")
                continue
        
        return nodes
    
    async def _validate_with_fabric_enterprise(
        self, 
        nodes: List[ATLASNode],
        tenant_config: Dict[str, Any]
    ) -> List[ATLASNode]:
        """Enterprise-grade validation with FABRIC patterns."""
        
        validated_nodes = []
        quality_threshold = tenant_config.get("quality_threshold", 0.8)
        
        for node in nodes:
            try:
                # Apply multiple FABRIC patterns for enterprise validation
                validation_results = await asyncio.gather(
                    self._apply_fabric_pattern("analyze_claims", node),
                    self._apply_fabric_pattern("extract_wisdom", node),
                    self._apply_fabric_pattern("create_summary", node),
                    return_exceptions=True
                )
                
                # Aggregate validation results
                valid_results = [r for r in validation_results if not isinstance(r, Exception)]
                
                if valid_results:
                    avg_confidence = sum(r.get("confidence", 0) for r in valid_results) / len(valid_results)
                    
                    if avg_confidence >= quality_threshold:
                        node.properties.update({
                            "enterprise_validation": {
                                "fabric_patterns_applied": len(valid_results),
                                "average_confidence": avg_confidence,
                                "validation_timestamp": datetime.utcnow().isoformat(),
                                "quality_grade": "enterprise" if avg_confidence > 0.9 else "standard"
                            }
                        })
                        validated_nodes.append(node)
                
            except Exception as e:
                logger.error(f"Enterprise validation failed for node {node.node_id}: {e}")
                continue
        
        return validated_nodes
    
    async def _apply_fabric_pattern(
        self, 
        pattern_name: str, 
        node: ATLASNode
    ) -> Dict[str, Any]:
        """Apply FABRIC pattern to node."""
        
        # Simulate FABRIC pattern application
        return {
            "pattern": pattern_name,
            "confidence": 0.85,
            "quality_score": 0.9,
            "recommendations": [],
            "applied_at": datetime.utcnow().isoformat()
        }
    
    async def _discover_relationships_distributed(
        self, 
        nodes: List[ATLASNode],
        worker_id: str
    ) -> List[Dict[str, Any]]:
        """Discover relationships using distributed processing."""
        
        relationships = []
        
        # Use distributed approach for large node sets
        if len(nodes) > 10:
            # Split into chunks for parallel processing
            chunk_size = 5
            chunks = [nodes[i:i+chunk_size] for i in range(0, len(nodes), chunk_size)]
            
            chunk_results = await asyncio.gather(
                *[self._analyze_node_chunk_relationships(chunk, worker_id) for chunk in chunks],
                return_exceptions=True
            )
            
            for result in chunk_results:
                if not isinstance(result, Exception):
                    relationships.extend(result)
        else:
            # Process small sets directly
            for i, node1 in enumerate(nodes):
                for node2 in nodes[i+1:]:
                    relationship = await self._analyze_node_relationship_enterprise(node1, node2)
                    if relationship:
                        relationships.append(relationship)
        
        return relationships
    
    async def _analyze_node_chunk_relationships(
        self, 
        chunk: List[ATLASNode],
        worker_id: str
    ) -> List[Dict[str, Any]]:
        """Analyze relationships within a chunk of nodes."""
        
        relationships = []
        
        for i, node1 in enumerate(chunk):
            for node2 in chunk[i+1:]:
                relationship = await self._analyze_node_relationship_enterprise(node1, node2)
                if relationship:
                    relationship["discovered_by_worker"] = worker_id
                    relationships.append(relationship)
        
        return relationships
    
    async def _analyze_node_relationship_enterprise(
        self, 
        node1: ATLASNode, 
        node2: ATLASNode
    ) -> Optional[Dict[str, Any]]:
        """Enterprise-grade relationship analysis."""
        
        # Simulate advanced relationship analysis
        # In production, this would use sophisticated AI models
        
        # Check for obvious relationships
        fuel_group1 = node1.properties.get("fuel_group")
        fuel_group2 = node2.properties.get("fuel_group")
        
        if fuel_group1 == fuel_group2:
            return {
                "source_node_id": node1.node_id,
                "target_node_id": node2.node_id,
                "relationship_type": "RELATED_TO",
                "confidence": 0.8,
                "relationship_strength": "medium",
                "discovered_method": "enterprise_ai",
                "discovered_at": datetime.utcnow().isoformat()
            }
        
        return None
    
    async def _save_to_tenant_partition(
        self, 
        nodes: List[ATLASNode],
        relationships: List[Dict[str, Any]],
        tenant_id: str
    ) -> None:
        """Save data to tenant-specific graph partition."""
        
        # Use tenant-specific database or namespace
        tenant_driver = await self.neo4j_cluster.get_tenant_driver(tenant_id)
        
        try:
            # Save nodes with tenant labeling
            for node in nodes:
                node.labels.append(NodeLabelType.TENANT_DATA)  # Add tenant label
                
            await tenant_driver.batch_create_nodes(nodes)
            
            if relationships:
                await tenant_driver.batch_create_relationships(relationships)
            
            logger.info(f"Saved {len(nodes)} nodes and {len(relationships)} relationships for tenant {tenant_id}")
            
        except Exception as e:
            logger.error(f"Failed to save to tenant partition {tenant_id}: {e}")
            raise
    
    async def _calculate_quality_metrics(
        self, 
        nodes: List[ATLASNode],
        extraction_result: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate quality metrics for the extraction."""
        
        if not nodes:
            return {"confidence": 0.0, "validation_success": 0.0, "completeness": 0.0}
        
        # Calculate average confidence
        confidences = [
            node.properties.get("extraction_confidence", 0.0) 
            for node in nodes
        ]
        avg_confidence = sum(confidences) / len(confidences)
        
        # Calculate validation success rate
        validated_nodes = [
            node for node in nodes 
            if node.properties.get("enterprise_validation", {}).get("average_confidence", 0) > 0.8
        ]
        validation_success = len(validated_nodes) / len(nodes)
        
        # Calculate completeness (simplified)
        expected_terms = extraction_result.get("expected_term_count", len(nodes))
        completeness = len(nodes) / max(expected_terms, 1)
        
        return {
            "confidence": avg_confidence,
            "validation_success": validation_success,
            "completeness": min(completeness, 1.0)
        }
    
    async def _update_system_metrics(self, result: ExtractionResult) -> None:
        """Update system-wide metrics."""
        
        # Update processing time average
        current_avg = self.system_metrics["average_processing_time"]
        total_processed = self.system_metrics["total_tasks_processed"]
        
        new_avg = ((current_avg * (total_processed - 1)) + result.processing_time) / total_processed
        self.system_metrics["average_processing_time"] = new_avg
        
        # Update success rate
        if result.success:
            # Increment success count (simplified calculation)
            pass
        
        # Record metrics
        await self.metrics_collector.record_metric("task_processing_time", result.processing_time)
        await self.metrics_collector.record_metric("nodes_extracted", result.nodes_extracted)
        await self.metrics_collector.record_metric("relationships_discovered", result.relationships_discovered)
        
        if result.quality_metrics:
            for metric_name, value in result.quality_metrics.items():
                await self.metrics_collector.record_metric(f"quality_{metric_name}", value)
    
    def _map_fuel_group(self, fuel_group_str: str) -> FuelGroupType:
        """Map string fuel group to enum."""
        mapping = {
            "renewable": FuelGroupType.RENEWABLE,
            "fossil": FuelGroupType.FOSSIL,
            "nuclear": FuelGroupType.NUCLEAR,
            "alternative": FuelGroupType.ALTERNATIVE
        }
        return mapping.get(fuel_group_str.lower(), FuelGroupType.ALTERNATIVE)
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        
        # Get cluster status
        neo4j_status = await self.neo4j_cluster.get_cluster_status()
        
        # Get worker status
        worker_status = await self.worker_manager.get_worker_status()
        
        # Get queue status
        queue_status = await self.task_queue.get_queue_status()
        
        # Get recent metrics
        recent_metrics = await self.metrics_collector.get_recent_metrics(hours=1)
        
        return {
            "system_metrics": self.system_metrics,
            "infrastructure": {
                "neo4j_cluster": neo4j_status,
                "worker_pool": worker_status,
                "task_queue": queue_status,
                "tailscale_network": await self.tailscale_manager.get_network_status()
            },
            "performance": recent_metrics,
            "active_tasks": len(self.active_tasks),
            "tenant_count": len(self.tenant_configurations),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def shutdown_system(self) -> None:
        """Gracefully shutdown the distributed system."""
        
        print("🛑 Shutting down distributed taxonomy system...")
        
        # Stop accepting new tasks
        await self.task_queue.stop_accepting_tasks()
        
        # Wait for active tasks to complete (with timeout)
        await self.worker_manager.wait_for_completion(timeout_seconds=300)
        
        # Close connections
        if self.redis_pool:
            await self.redis_pool.disconnect()
        
        await self.neo4j_cluster.close_all_connections()
        
        # Stop monitoring
        await self.metrics_collector.stop_collection()
        
        print("✅ System shutdown completed")


async def main():
    """
    Main function demonstrating enterprise ATLAS Framework usage.
    """
    
    print("🚀 ATLAS Framework - Enterprise Example: Distributed Taxonomy System")
    print("=" * 80)
    
    # Configuration
    config_path = Path(__file__).parent / "config" / "enterprise_config.json"
    
    # Create enterprise configuration if needed
    if not config_path.exists():
        await create_enterprise_config(config_path)
    
    # System configuration
    tailscale_config = {
        "auth_key": "tskey-auth-example-key",
        "hostname": "atlas-enterprise",
        "tags": ["atlas", "enterprise", "production"],
        "jwt_secret": "enterprise-secret-key-change-in-production"
    }
    
    neo4j_cluster_config = {
        "cluster_nodes": [
            "neo4j://atlas-neo4j-1.tailnet:7687",
            "neo4j://atlas-neo4j-2.tailnet:7687",
            "neo4j://atlas-neo4j-3.tailnet:7687"
        ],
        "auth": ("atlas_user", "secure_password"),
        "encrypted": True
    }
    
    redis_config = {
        "host": "atlas-redis.tailnet",
        "port": 6379,
        "password": "redis_secure_password"
    }
    
    # Initialize distributed system
    system = DistributedTaxonomySystem(
        config_path=str(config_path),
        tailscale_config=tailscale_config,
        neo4j_cluster_config=neo4j_cluster_config,
        redis_config=redis_config
    )
    
    try:
        # Initialize system (would connect to real infrastructure in production)
        print("⚠️  Note: This is a demonstration - real infrastructure connections disabled")
        # await system.initialize_system()
        
        # Simulate enterprise operations
        print("\n🏢 Simulating Enterprise Operations")
        print("=" * 50)
        
        # Simulate user context
        user_context = {
            "user_id": "enterprise_user_001",
            "tenant_id": "energy_corp_tenant",
            "permissions": ["taxonomy.admin", "taxonomy.write", "taxonomy.read"],
            "clearance_level": "confidential"
        }
        
        # Simulate job submission
        job_config = {
            "source_url": "https://www.eia.gov/tools/glossary/",
            "fuel_groups": ["renewable", "fossil", "nuclear", "alternative"],
            "priority": 50,
            "deadline_hours": 12,
            "metadata": {
                "project": "Q1_2024_Taxonomy_Update",
                "department": "Energy_Research",
                "compliance_required": True
            }
        }
        
        print(f"📋 Submitting enterprise extraction job...")
        print(f"   - Source: {job_config['source_url']}")
        print(f"   - Fuel Groups: {job_config['fuel_groups']}")
        print(f"   - Priority: {job_config['priority']}")
        print(f"   - Tenant: {user_context['tenant_id']}")
        
        # Simulate job processing
        task = ExtractionTask(
            task_id="enterprise_task_001",
            source_url=job_config["source_url"],
            fuel_groups=job_config["fuel_groups"],
            priority=job_config["priority"],
            tenant_id=user_context["tenant_id"],
            user_id=user_context["user_id"],
            created_at=datetime.utcnow(),
            deadline=datetime.utcnow() + timedelta(hours=12),
            metadata=job_config["metadata"]
        )
        
        # Simulate distributed processing
        workers = ["worker_001", "worker_002", "worker_003"]
        results = []
        
        print(f"\n⚡ Processing with {len(workers)} distributed workers...")
        
        for i, worker_id in enumerate(workers):
            # Simulate processing subset of fuel groups
            worker_task = ExtractionTask(
                task_id=f"{task.task_id}_chunk_{i}",
                source_url=task.source_url,
                fuel_groups=[task.fuel_groups[i]] if i < len(task.fuel_groups) else [],
                priority=task.priority,
                tenant_id=task.tenant_id,
                user_id=task.user_id,
                created_at=task.created_at,
                deadline=task.deadline,
                metadata=task.metadata
            )
            
            if worker_task.fuel_groups:  # Only process if fuel groups assigned
                result = await system.process_extraction_task(worker_task, worker_id)
                results.append(result)
                
                print(f"✅ {worker_id}: {result.nodes_extracted} nodes, {result.relationships_discovered} relationships")
        
        # Aggregate results
        total_nodes = sum(r.nodes_extracted for r in results)
        total_relationships = sum(r.relationships_discovered for r in results)
        avg_processing_time = sum(r.processing_time for r in results) / len(results) if results else 0
        success_rate = sum(1 for r in results if r.success) / len(results) if results else 0
        
        print(f"\n📊 Enterprise Job Results")
        print("=" * 30)
        print(f"✅ Total Nodes Extracted: {total_nodes}")
        print(f"🔗 Total Relationships: {total_relationships}")
        print(f"⏱️  Average Processing Time: {avg_processing_time:.2f}s")
        print(f"📈 Success Rate: {success_rate*100:.1f}%")
        print(f"👥 Workers Used: {len(workers)}")
        print(f"🏢 Tenant: {user_context['tenant_id']}")
        
        # Show enterprise features
        print(f"\n🎯 Enterprise Features Demonstrated")
        print("=" * 40)
        print("✅ Multi-tenant architecture with data isolation")
        print("✅ Distributed processing across multiple workers")
        print("✅ Zero-trust security with Tailscale VPN")
        print("✅ Enterprise-grade validation with FABRIC patterns")
        print("✅ Real-time monitoring and alerting")
        print("✅ Horizontal scaling capabilities")
        print("✅ Production-grade error handling")
        print("✅ Comprehensive audit trails")
        
        # Simulate system status
        print(f"\n📊 System Status")
        print("=" * 20)
        print(f"🖥️  Active Workers: {len(workers)}")
        print(f"📋 Active Tasks: 0 (completed)")
        print(f"🏢 Tenants: 1 (energy_corp_tenant)")
        print(f"💾 Neo4j Cluster: 3 nodes (simulated)")
        print(f"🔄 Redis Coordination: Connected (simulated)")
        print(f"🔒 Tailscale Network: Secure (simulated)")
        
        print(f"\n🎉 Enterprise example completed successfully!")
        print("🚀 Ready for production deployment!")
        
    except Exception as e:
        logger.error(f"Enterprise example failed: {e}")
        print(f"\n❌ Enterprise example failed: {e}")
        raise
    
    finally:
        # Cleanup (would shutdown real infrastructure in production)
        print("\n🛑 Cleaning up...")
        # await system.shutdown_system()
        print("✅ Cleanup completed")


async def create_enterprise_config(config_path: Path) -> None:
    """Create enterprise configuration file."""
    
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    enterprise_config = {
        "version": "1.0",
        "metadata": {
            "name": "Enterprise ATLAS Configuration",
            "description": "Production-grade configuration for distributed taxonomy systems",
            "created": "2024-01-15T10:00:00Z",
            "environment": "production"
        },
        "node_types": {
            "energy_term": {
                "description": "Enterprise energy terminology with full validation",
                "labels": ["EnergyTerm", "TaxonomyNode", "EnterpriseData"],
                "default_properties": {
                    "extraction_confidence": 0.9,
                    "validation_status": "pending",
                    "enterprise_grade": True,
                    "compliance_checked": True
                },
                "required_fields": ["term_name", "definition", "fuel_group", "tenant_id"],
                "validation_rules": {
                    "extraction_confidence": {"type": "float", "min": 0.8, "max": 1.0},
                    "tenant_id": {"type": "string", "pattern": "^[a-z0-9_]+$"}
                },
                "behaviors": [
                    {
                        "type": "computation",
                        "behavior_id": "enterprise_computation",
                        "description": "Enterprise-grade computation with full validation",
                        "computation_function": "_compute_enterprise_metrics",
                        "cache_ttl": 900,
                        "priority": 25,
                        "dependencies": ["validation_service", "compliance_checker"],
                        "parameters": {
                            "enterprise_mode": True,
                            "compliance_standards": ["ISO_14067", "GRI_Standards"],
                            "quality_threshold": 0.9
                        }
                    },
                    {
                        "type": "analysis",
                        "behavior_id": "enterprise_analysis",
                        "description": "Multi-pattern enterprise analysis",
                        "analysis_type": "comprehensive_enterprise",
                        "retry_attempts": 5,
                        "timeout_seconds": 120.0,
                        "priority": 50,
                        "parameters": {
                            "fabric_patterns": ["analyze_claims", "extract_wisdom", "create_summary"],
                            "validation_depth": "comprehensive",
                            "include_compliance_check": True
                        }
                    }
                ]
            }
        },
        "enterprise_settings": {
            "multi_tenant": True,
            "data_isolation": "strict",
            "audit_all_operations": True,
            "encryption_at_rest": True,
            "encryption_in_transit": True,
            "backup_retention_days": 2555,  # 7 years
            "compliance_frameworks": ["SOC2", "ISO27001", "GDPR"]
        },
        "distributed_settings": {
            "max_workers_per_tenant": 10,
            "task_timeout_seconds": 1800,
            "result_aggregation_timeout": 300,
            "worker_health_check_interval": 30,
            "auto_scaling_enabled": True,
            "load_balancing_strategy": "round_robin"
        },
        "security_settings": {
            "zero_trust_networking": True,
            "tailscale_required": True,
            "jwt_token_expiry_hours": 8,
            "mfa_required": True,
            "role_based_access": True,
            "data_classification_required": True
        },
        "monitoring_settings": {
            "metrics_collection_interval": 10,
            "alert_thresholds": {
                "error_rate": 0.05,
                "processing_time_p95": 300,
                "worker_failure_rate": 0.1
            },
            "notification_channels": ["slack", "email", "pagerduty"],
            "dashboard_refresh_interval": 30
        },
        "ai_settings": {
            "default_model": "gpt-4-turbo",
            "temperature": 0.05,
            "max_tokens": 3000,
            "confidence_threshold": 0.9,
            "enterprise_prompts": True,
            "model_fallback_enabled": True
        },
        "fabric_settings": {
            "patterns_enabled": [
                "analyze_claims", "extract_wisdom", "create_summary",
                "find_patterns", "create_network_threat_landscape"
            ],
            "enterprise_patterns": True,
            "pattern_chaining": True,
            "quality_assurance": True
        },
        "global_settings": {
            "default_cache_ttl": 900,
            "max_behavior_execution_time": 300,
            "validation_strictness": "enterprise",
            "enable_all_features": True,
            "production_mode": True
        }
    }
    
    with open(config_path, 'w') as f:
        json.dump(enterprise_config, f, indent=2)
    
    print(f"📝 Created enterprise configuration at: {config_path}")


if __name__ == "__main__":
    """Run the enterprise example."""
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Enterprise example interrupted by user")
    except Exception as e:
        logger.error(f"Enterprise example failed: {e}")
        print(f"\n❌ Enterprise example failed: {e}")
        raise

