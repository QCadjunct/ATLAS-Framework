# 🚀 Getting Started with ATLAS Framework

**Your Complete Guide to Intelligent Taxonomy Extraction**

[![ATLAS Version](https://img.shields.io/badge/ATLAS-v1.0.0-blue.svg)](https://github.com/atlas-framework/atlas)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://atlas-framework.readthedocs.io)

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [⚡ Quick Installation](#-quick-installation)
- [🔧 Basic Setup](#-basic-setup)
- [🏗️ Your First ATLAS Project](#️-your-first-atlas-project)
- [📊 Understanding the Architecture](#-understanding-the-architecture)
- [🎨 Configuration-Driven Development](#-configuration-driven-development)
- [🤖 Adding AI Behaviors](#-adding-ai-behaviors)
- [🔒 Security Setup](#-security-setup)
- [📈 Next Steps](#-next-steps)

---

## 🎯 Overview

ATLAS Framework revolutionizes taxonomy extraction and knowledge graph generation through:

- **🔄 Zero Code Duplication**: Composition-based architecture eliminates inheritance patterns
- **⚡ Type-Safe Everything**: Pydantic v2 with comprehensive validation
- **🤖 AI-First Design**: Native LangChain, LangGraph, and FABRIC integration
- **🕸️ Graph Database**: Neo4j-powered knowledge graphs
- **🔒 Zero Trust Security**: Built-in Tailscale VPN support

```mermaid
graph LR
    subgraph "🎯 ATLAS Core"
        A[Configuration] --> B[Node Factory]
        B --> C[ATLASNode]
        C --> D[Behaviors]
    end
    
    subgraph "🤖 AI Layer"
        E[LangChain] --> F[Extraction]
        G[FABRIC] --> H[Patterns]
    end
    
    subgraph "🕸️ Graph Layer"
        I[Neo4j] --> J[Knowledge Graph]
    end
    
    D --> E
    F --> I
    
    style A fill:#e1f5fe
    style E fill:#f3e5f5
    style I fill:#e8f5e8
```

[⬆️ Back to TOC](#-table-of-contents)

---

## ⚡ Quick Installation

### **Prerequisites**

- **Python 3.11+** (Required for advanced type hints)
- **Neo4j Database** (Optional for graph features)
- **OpenAI API Key** (Optional for AI features)

### **Installation Options**

```bash
# 🚀 Basic installation
pip install atlas-framework

# 🎯 Full installation with all features
pip install atlas-framework[all]

# 🔧 Development installation
git clone https://github.com/atlas-framework/atlas.git
cd atlas
pip install -e .[dev]
```

### **Verify Installation**

```python
import atlas
print(f"ATLAS Framework v{atlas.__version__} ready!")
print(atlas.get_info())
```

**Expected Output:**
```
ATLAS Framework v1.0.0 ready!
{
    'name': 'ATLAS Framework',
    'version': '1.0.0',
    'pydantic_v2': 'True',
    'neo4j_support': 'True',
    'langchain_support': 'True'
}
```

[⬆️ Back to TOC](#-table-of-contents)

---

## 🔧 Basic Setup

### **1. Environment Configuration**

Create a `.env` file in your project root:

```bash
# .env
ATLAS_LOG_LEVEL=INFO
OPENAI_API_KEY=your_openai_key_here
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

### **2. Basic Configuration File**

Create `atlas_config.json`:

```json
{
    "version": "1.0",
    "node_types": {
        "energy_term": {
            "labels": ["EnergyTerm", "TaxonomyNode"],
            "default_properties": {
                "fuel_group": null,
                "extraction_confidence": 0.8
            },
            "behaviors": [
                {
                    "type": "computation",
                    "behavior_id": "relationship_analysis",
                    "computation_function": "_compute_relationship_metrics",
                    "cache_ttl": 300,
                    "priority": 100
                }
            ]
        }
    },
    "graph": {
        "driver": "neo4j",
        "connection": {
            "uri": "${NEO4J_URI}",
            "auth": ["${NEO4J_USER}", "${NEO4J_PASSWORD}"]
        }
    }
}
```

### **3. Initialize ATLAS**

```python
from atlas import ConfigurationManager, load_atlas_config

# Load configuration
config = load_atlas_config("atlas_config.json")
config_manager = ConfigurationManager(config)

print("✅ ATLAS Framework initialized successfully!")
```

[⬆️ Back to TOC](#-table-of-contents)

---

## 🏗️ Your First ATLAS Project

### **Step 1: Create Your First Node**

```python
from atlas import ConfigurationManager
from atlas.enums import FuelGroupType

# Initialize configuration manager
config_manager = ConfigurationManager.from_file("atlas_config.json")

# Create an energy term node (no inheritance needed!)
solar_node = config_manager.create_energy_term(
    term_name="Solar Photovoltaic",
    definition="Technology that converts sunlight directly into electricity using semiconductor materials",
    fuel_group=FuelGroupType.RENEWABLE
)

print(f"Created node: {solar_node.node_id}")
print(f"Labels: {[label.value for label in solar_node.labels]}")
print(f"Properties: {solar_node.properties}")
```

**Output:**
```
Created node: 550e8400-e29b-41d4-a716-446655440000
Labels: ['EnergyTerm', 'TaxonomyNode']
Properties: {'fuel_group': 'renewable', 'extraction_confidence': 0.8}
```

### **Step 2: Execute Node Behaviors**

```python
async def demonstrate_behaviors():
    """
    Demonstrate ATLAS node behaviors.
    
    All nodes use the same interface regardless of type!
    """
    
    # Execute cached computation
    computation_result = await solar_node.execute_behavior(
        "computation", 
        {"analysis_depth": "detailed", "include_metrics": True}
    )
    
    print("Computation Result:")
    print(f"  Success: {computation_result.get('success', False)}")
    print(f"  Metrics: {computation_result.get('metrics', {})}")
    
    # Execute all behaviors
    all_results = await solar_node.execute_all_behaviors({
        "context": "comprehensive_analysis",
        "timestamp": "2024-01-15T10:00:00Z"
    })
    
    print("\nAll Behaviors Results:")
    for behavior_type, result in all_results.items():
        status = "✅" if result["success"] else "❌"
        print(f"  {status} {behavior_type}: {result}")

# Run the demonstration
import asyncio
asyncio.run(demonstrate_behaviors())
```

### **Step 3: Add Dynamic Behaviors**

```python
from atlas.models.behaviors import ComputationBehavior, AnalysisBehavior

# Create custom computation behavior
efficiency_behavior = ComputationBehavior(
    behavior_id="efficiency_analysis",
    behavior_type="computation",
    computation_function="_compute_efficiency_metrics",
    cache_ttl=600,  # 10 minutes
    priority=50,    # Higher priority (lower number)
    dependencies=["solar_irradiance", "temperature_data"]
)

# Add behavior to node dynamically
solar_node.add_behavior(efficiency_behavior)

# Create analysis behavior
market_analysis = AnalysisBehavior(
    behavior_id="market_analysis",
    behavior_type="analysis",
    analysis_type="market_trends",
    retry_attempts=5,
    timeout_seconds=45.0,
    priority=75
)

solar_node.add_behavior(market_analysis)

print(f"Node now has {len(solar_node.behaviors)} behaviors")
print("Behavior types:", [b.behavior_type for b in solar_node.behaviors])
```

[⬆️ Back to TOC](#-table-of-contents)

---

## 📊 Understanding the Architecture

### **Composition vs Inheritance**

ATLAS eliminates the traditional inheritance pattern that leads to code duplication:

```mermaid
graph TB
    subgraph "❌ Traditional Inheritance (DRY Violation)"
        A1[BaseNode] --> B1[EnergyNode]
        B1 --> C1[SolarNode]
        B1 --> D1[WindNode]
        B1 --> E1[CoalNode]
        
        C1 --> F1[Duplicated Methods]
        D1 --> G1[Duplicated Methods]
        E1 --> H1[Duplicated Methods]
    end
    
    subgraph "✅ ATLAS Composition (True DRY)"
        A2[ATLASNode] --> B2[BehaviorRegistry]
        A2 --> C2[ConfigurationManager]
        
        B2 --> D2[ComputationBehavior]
        B2 --> E2[AnalysisBehavior]
        B2 --> F2[ValidationBehavior]
        
        C2 --> G2[NodeFactory]
        G2 --> H2[Reusable Components]
    end
    
    style A1 fill:#ffebee
    style A2 fill:#e8f5e8
    style B2 fill:#e1f5fe
    style C2 fill:#f3e5f5
```

### **Key Architectural Benefits**

| Feature | Traditional ORM | ATLAS Framework |
|---------|----------------|-----------------|
| **Code Duplication** | ❌ High (inheritance) | ✅ Zero (composition) |
| **Type Safety** | ⚠️ Partial | ✅ Complete (Pydantic v2) |
| **Runtime Flexibility** | ❌ Static | ✅ Dynamic behaviors |
| **Configuration** | ❌ Code-based | ✅ JSON-driven |
| **AI Integration** | ❌ Manual | ✅ Native |

[⬆️ Back to TOC](#-table-of-contents)

---

## 🎨 Configuration-Driven Development

### **Node Type Definitions**

Instead of creating classes, define node types in configuration:

```json
{
    "node_types": {
        "renewable_source": {
            "labels": ["RenewableSource", "EnergyTerm"],
            "default_properties": {
                "fuel_group": "renewable",
                "carbon_intensity": "low",
                "sustainability_rating": 0.9
            },
            "behaviors": [
                {
                    "type": "computation",
                    "behavior_id": "efficiency_computation",
                    "computation_function": "_compute_efficiency_metrics",
                    "cache_ttl": 600,
                    "priority": 50,
                    "dependencies": ["weather_data", "location_data"]
                },
                {
                    "type": "analysis",
                    "behavior_id": "environmental_impact",
                    "analysis_type": "environmental_assessment",
                    "retry_attempts": 3,
                    "timeout_seconds": 30.0,
                    "priority": 100
                }
            ]
        },
        "fossil_fuel": {
            "labels": ["FossilFuel", "EnergyTerm"],
            "default_properties": {
                "fuel_group": "fossil",
                "carbon_intensity": "high",
                "sustainability_rating": 0.2
            },
            "behaviors": [
                {
                    "type": "computation",
                    "behavior_id": "emissions_computation",
                    "computation_function": "_compute_emission_metrics",
                    "cache_ttl": 300,
                    "priority": 25
                }
            ]
        }
    }
}
```

### **Creating Nodes from Configuration**

```python
# Create different node types using the same interface
wind_turbine = config_manager.create_renewable_source(
    source_name="Offshore Wind Turbine",
    technology_type="horizontal_axis",
    efficiency_rating=0.52,
    capacity_mw=8.0
)

natural_gas = config_manager.create_fossil_fuel(
    fuel_name="Natural Gas",
    extraction_method="hydraulic_fracturing",
    carbon_content_kg_per_mwh=490.0
)

# Both nodes use identical interfaces despite different types!
wind_results = await wind_turbine.execute_all_behaviors({"analysis_context": "offshore"})
gas_results = await natural_gas.execute_all_behaviors({"analysis_context": "power_plant"})
```

### **Behavior Templates**

Create reusable behavior templates:

```json
{
    "behavior_templates": {
        "standard_efficiency": {
            "type": "computation",
            "computation_function": "_compute_standard_efficiency",
            "cache_ttl": 300,
            "priority": 100,
            "parameters": {
                "include_weather_adjustment": true,
                "use_industry_benchmarks": true
            }
        },
        "market_analysis": {
            "type": "analysis",
            "analysis_type": "market_trends",
            "retry_attempts": 3,
            "timeout_seconds": 45.0,
            "priority": 200,
            "parameters": {
                "time_horizon_years": 5,
                "include_policy_impact": true
            }
        }
    }
}
```

[⬆️ Back to TOC](#-table-of-contents)

---

## 🤖 Adding AI Behaviors

### **LangChain Integration**

```python
from atlas.frameworks.langchain import ExtractionChain, ValidationChain
from atlas.decorators import fabric_pattern

# Create AI-powered extraction behavior
class AIExtractionBehavior(NodeBehavior):
    """
    AI-powered taxonomy extraction using LangChain.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.extraction_chain = ExtractionChain(
            model="gpt-4-turbo",
            temperature=0.1,
            max_tokens=2000
        )
    
    @fabric_pattern("extract_wisdom")
    async def execute(self, node: ATLASNode, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute AI extraction with FABRIC pattern.
        
        Args:
            node: Target node for extraction
            context: Extraction context including source text
            
        Returns:
            Dict[str, Any]: Extraction results with confidence scores
        """
        source_text = context.get("source_text", "")
        domain = context.get("domain", "energy")
        
        # Use LangChain for intelligent extraction
        extraction_result = await self.extraction_chain.extract_taxonomy(
            text=source_text,
            domain=domain,
            existing_terms=[term.properties.get("term_name") for term in context.get("existing_nodes", [])]
        )
        
        return {
            "extracted_terms": extraction_result.terms,
            "relationships": extraction_result.relationships,
            "confidence_scores": extraction_result.confidence,
            "metadata": {
                "model_used": "gpt-4-turbo",
                "extraction_time": extraction_result.processing_time,
                "token_usage": extraction_result.token_count
            }
        }

# Add AI behavior to node
ai_extraction = AIExtractionBehavior(
    behavior_id="ai_extraction",
    behavior_type="ai_extraction",
    priority=10  # Highest priority
)

solar_node.add_behavior(ai_extraction)
```

### **FABRIC Pattern Integration**

```python
from atlas.frameworks.fabric import FabricPatternRegistry

# Initialize FABRIC patterns
fabric_registry = FabricPatternRegistry()
fabric_registry.load_patterns("configs/fabric/energy_patterns.json")

# Apply FABRIC patterns to behaviors
@fabric_pattern("analyze_claims")
async def validate_energy_claims(node: ATLASNode, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate energy-related claims using FABRIC analyze_claims pattern.
    
    Args:
        node: Node containing energy claims
        context: Validation context
        
    Returns:
        Dict[str, Any]: Validation results with evidence
    """
    claims = context.get("claims", [])
    
    validation_results = []
    for claim in claims:
        # Apply FABRIC pattern for claim analysis
        result = await fabric_registry.apply_pattern(
            pattern_name="analyze_claims",
            input_text=claim,
            context={"domain": "energy", "node_type": node.labels[0].value}
        )
        
        validation_results.append({
            "claim": claim,
            "validity": result.validity_score,
            "evidence": result.supporting_evidence,
            "concerns": result.potential_concerns
        })
    
    return {
        "validation_results": validation_results,
        "overall_confidence": sum(r["validity"] for r in validation_results) / len(validation_results),
        "fabric_pattern": "analyze_claims"
    }
```

[⬆️ Back to TOC](#-table-of-contents)

---

## 🔒 Security Setup

### **Tailscale Zero Trust Configuration**

```python
from atlas.security.tailscale import TailscaleManager
from atlas.security.auth import AuthProvider

# Initialize Tailscale for zero-trust networking
tailscale_manager = TailscaleManager(
    auth_key="tskey-auth-your-key-here",
    hostname="atlas-production",
    tags=["atlas", "production", "taxonomy"],
    advertise_routes=["10.0.0.0/24"],
    accept_routes=True
)

# Start Tailscale connection
await tailscale_manager.connect()
print(f"✅ Connected to Tailscale network: {tailscale_manager.network_name}")

# Configure secure Neo4j connection through Tailscale
from atlas.graph.neo4j import Neo4jDriver

secure_driver = Neo4jDriver(
    uri="neo4j://atlas-graph.tailnet:7687",  # Internal Tailscale address
    auth=("atlas_user", "secure_password"),
    encrypted=True,
    trust="TRUST_SYSTEM_CA_SIGNED_CERTIFICATES"
)

# Test secure connection
connection_info = await secure_driver.test_connection()
print(f"✅ Secure Neo4j connection: {connection_info}")
```

### **Authentication and Authorization**

```python
from atlas.security.auth import JWTAuthProvider
from atlas.decorators import require_permission

# Setup JWT authentication
auth_provider = JWTAuthProvider(
    secret_key="your-secret-key-here",
    algorithm="HS256",
    token_expiry_hours=24
)

# Protect sensitive operations
@require_permission("taxonomy.write")
async def create_sensitive_node(user_context: Dict[str, Any]) -> ATLASNode:
    """
    Create node with write permission requirement.
    
    Args:
        user_context: Authenticated user context
        
    Returns:
        ATLASNode: Created node
    """
    # Verify user has required permissions
    if not auth_provider.has_permission(user_context["user_id"], "taxonomy.write"):
        raise SecurityError("Insufficient permissions for node creation")
    
    # Create node with audit trail
    node = config_manager.create_energy_term(
        term_name="Classified Energy Technology",
        definition="Sensitive energy technology information",
        fuel_group=FuelGroupType.ADVANCED
    )
    
    # Add audit metadata
    node.properties.update({
        "created_by": user_context["user_id"],
        "security_level": "restricted",
        "audit_trail": {
            "action": "create",
            "timestamp": datetime.utcnow().isoformat(),
            "ip_address": user_context.get("ip_address"),
            "user_agent": user_context.get("user_agent")
        }
    })
    
    return node
```

[⬆️ Back to TOC](#-table-of-contents)

---

## 📈 Next Steps

### **🎯 Immediate Actions**

1. **Explore Examples**: Check out the [examples directory](../../examples/) for more complex scenarios
2. **Read Architecture Docs**: Understand the [design principles](../architecture/design-principles.md)
3. **Join Community**: Participate in [GitHub Discussions](https://github.com/atlas-framework/atlas/discussions)

### **📚 Advanced Topics**

- **[Custom Behaviors](advanced-behaviors.md)**: Create domain-specific behaviors
- **[Graph Operations](graph-operations.md)**: Advanced Neo4j integration
- **[Performance Tuning](performance-tuning.md)**: Optimize for production
- **[Deployment Guide](deployment.md)**: Production deployment strategies

### **🔧 Development Resources**

- **[API Reference](../api/)**: Complete API documentation
- **[Contributing Guide](../../CONTRIBUTING.md)**: How to contribute to ATLAS
- **[Testing Guide](testing.md)**: Writing tests for ATLAS applications

### **🌟 Community Examples**

Explore real-world implementations:

- **[Energy Taxonomy Extractor](../../examples/enterprise/energy-extractor/)**: Complete EIA glossary extraction
- **[Manufacturing Taxonomy](../../examples/advanced/manufacturing/)**: Industrial classification system
- **[Research Paper Analysis](../../examples/intermediate/research-analysis/)**: Academic taxonomy extraction

---

## 🎉 Congratulations!

You've successfully set up ATLAS Framework and created your first intelligent taxonomy nodes! 

**What you've learned:**
- ✅ Installation and basic configuration
- ✅ Creating nodes without inheritance
- ✅ Adding and executing behaviors
- ✅ Configuration-driven development
- ✅ AI integration basics
- ✅ Security setup fundamentals

**Ready for more?** Dive into our [intermediate examples](../../examples/intermediate/) or explore the [complete API reference](../api/).

---

**Need Help?**
- 💬 [GitHub Discussions](https://github.com/atlas-framework/atlas/discussions)
- 🐛 [Report Issues](https://github.com/atlas-framework/atlas/issues)
- 📧 [Email Support](mailto:atlas@framework.dev)
- 📖 [Full Documentation](https://atlas-framework.readthedocs.io)

[⬆️ Back to TOC](#-table-of-contents)

