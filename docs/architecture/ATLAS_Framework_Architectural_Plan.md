# ATLAS Framework - Comprehensive Architectural Plan

**Version:** 1.0  
**Date:** 2025-01-24  
**Status:** PENDING APPROVAL

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architectural Principles (Non-Negotiable)](#architectural-principles-non-negotiable)
3. [System Architecture Overview](#system-architecture-overview)
4. [Environment Separation Strategy](#environment-separation-strategy)
5. [Integration Architecture](#integration-architecture)
6. [SKILL.md Structure and FQSN Design](#skillmd-structure-and-fqsn-design)
7. [Skills Chaining with LangGraph](#skills-chaining-with-langgraph)
8. [Domain-Driven Database Design (D⁴)](#domain-driven-database-design-d)
9. [Repository Structure](#repository-structure)
10. [Implementation Phases](#implementation-phases)
11. [Approval Checklist](#approval-checklist)

---

## 1. Executive Summary

The ATLAS Framework (Agentic Taxonomy Learning and Synthesis) is a comprehensive system for extracting, managing, and synthesizing industry taxonomies using agentic LLMs, graph databases, and FABRIC patterns. This architectural plan defines the complete integration strategy with modern Python tooling, LangChain ecosystem, and strict adherence to KISS, SRP, D⁴, and FQSN principles.

### Key Objectives

- **Integration**: Seamless integration with Claude Code, LangChain, LangGraph, LangSmith, Tavily, Marimo
- **Environment Separation**: Clear distinction between Dev/QA (Conda/Conda-forge) and Production (Astral UV/Ruff)
- **Skills Architecture**: FQSN-based filesystem organization with SKILL.md specifications
- **Agentic Delivery**: Marimo.py-based interactive notebooks for production deployment
- **Graph Orchestration**: LangGraph DAG/DCG patterns for skills chaining

---

## 2. Architectural Principles (Non-Negotiable)

### 2.1 KISS: Keep It Simple and Standard

**Definition**: Prioritize simplicity and adherence to established standards over clever complexity.

**Application**:
- One configuration file per concern (pyproject.toml for Python, not multiple config formats)
- Standard Python package structure (src layout)
- Standard environment variables (ATLAS_* prefix)
- Standard file formats (JSON for data, Markdown for docs)

### 2.2 SRP: Single Responsibility Principle

**Definition**: Each module, class, function, and skill has ONE clearly defined responsibility.

**Application**:
- Each SKILL.md defines ONE specific capability
- Each Python module handles ONE domain concern
- Each LangGraph node performs ONE transformation
- Each database schema represents ONE business domain

### 2.3 D⁴: Domain-Driven Database Design

**Definition**: Database schemas use Fully Qualified Domain Names (FQDNs) with business definitions as queryable metadata.

**Application**:
- Schema naming: `dEnergy`, `dTransportation`, `dManufacturing`
- Sub-domain naming: `sdRenewable`, `sdFossilFuel`, `sdNuclear`
- Business definitions stored as queryable metadata (not comments)
- Temporal metadata using Allen Intervals (meets relationship)

### 2.4 FQSN: Fully Qualified Skill Name

**Definition**: The filesystem path IS the skill identifier - no separate naming registry needed.

**Application**:
- Skill path: `skills/energy/extraction/eia_glossary/SKILL.md`
- Skill name: `energy.extraction.eia_glossary`
- No duplication - path determines identity
- Lazy loading based on filesystem traversal

---

## 3. System Architecture Overview

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     ATLAS Framework                              │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐   │
│  │  Marimo.py     │  │  LangGraph     │  │  Neo4j Graph   │   │
│  │  Interactive   │  │  Orchestration │  │  Database      │   │
│  │  Notebooks     │  │  (DAG/DCG)     │  │  (D⁴ Schema)   │   │
│  └────────┬───────┘  └────────┬───────┘  └────────┬───────┘   │
│           │                   │                   │            │
│           └───────────────────┼───────────────────┘            │
│                               │                                │
│  ┌────────────────────────────┴────────────────────────────┐  │
│  │              Skills Registry (FQSN-based)               │  │
│  │  skills/                                                │  │
│  │    ├── energy/                                          │  │
│  │    │   ├── extraction/                                  │  │
│  │    │   │   ├── eia_glossary/SKILL.md                   │  │
│  │    │   │   └── iea_data/SKILL.md                       │  │
│  │    │   └── analysis/                                    │  │
│  │    │       └── relationship_discovery/SKILL.md         │  │
│  │    └── transportation/                                  │  │
│  │        └── ...                                          │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         Integration Layer                              │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │    │
│  │  │LangChain │ │LangSmith │ │  Tavily  │ │  Claude  │ │    │
│  │  │  Core    │ │Monitoring│ │  Search  │ │   Code   │ │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 Component Responsibilities

| Component | Responsibility | Principle |
|-----------|---------------|-----------|
| Marimo.py Notebooks | Interactive agentic delivery and visualization | SRP: User interaction |
| LangGraph Orchestrator | Skills chaining and workflow management | SRP: Workflow control |
| Neo4j Database | Graph storage with D⁴ schema design | D⁴: Domain-driven storage |
| Skills Registry | FQSN-based skill discovery and loading | FQSN: Filesystem identity |
| LangChain Core | LLM interaction and prompt management | SRP: LLM abstraction |
| LangSmith | Monitoring and observability | SRP: Telemetry |
| Tavily | Enhanced search capabilities | SRP: Information retrieval |
| Claude Code | Code generation and analysis | SRP: Code intelligence |

---

## 4. Environment Separation Strategy

### 4.1 Development/QA Environment

**Purpose**: Experimentation, testing, and quality assurance

**Tooling**:
- **Conda/Conda-forge**: Environment and package management
- **Jupyter/Marimo**: Interactive development
- **pytest**: Testing framework
- **LangSmith**: Development monitoring

**Configuration**:
```bash
# Environment file: environments/dev.yml
name: atlas-dev
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - langchain
  - langchain-openai
  - langgraph
  - langsmith
  - marimo
  - neo4j-python-driver
  - pydantic=2.*
  - pytest
  - pytest-cov
  - jupyter
```

**Activation**:
```bash
conda env create -f environments/dev.yml
conda activate atlas-dev
```

### 4.2 Production Environment

**Purpose**: Deployment and production workloads

**Tooling**:
- **Astral UV**: Fast dependency resolution and installation
- **Ruff**: Linting and formatting
- **Marimo.py**: Production-ready interactive notebooks
- **LangSmith**: Production monitoring

**Configuration**:
```toml
# pyproject.toml
[project]
name = "atlas-framework"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "langchain>=0.1.0",
    "langchain-openai>=0.0.5",
    "langgraph>=0.0.20",
    "langsmith>=0.0.80",
    "marimo>=0.1.0",
    "neo4j>=5.13.0",
    "pydantic>=2.5.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 100
target-version = "py311"
```

**Installation**:
```bash
uv pip install -e .
```

### 4.3 Environment Separation Matrix

| Aspect | Dev/QA | Production |
|--------|--------|------------|
| Package Manager | Conda | UV |
| Environment Manager | Conda | UV venv |
| Code Quality | Manual + pytest | Ruff + automated CI |
| Notebooks | Jupyter + Marimo | Marimo.py only |
| Monitoring | LangSmith (verbose) | LangSmith (optimized) |
| Configuration | YAML + .env | pyproject.toml + env vars |
| Deployment | Local/Docker | Docker Swarm/K8s |

---

## 5. Integration Architecture

### 5.1 Claude Code Integration

**Purpose**: AI-assisted code generation and analysis

**Integration Points**:
- Code generation for new skills
- Code review and optimization
- Documentation generation
- Test case generation

**Implementation**:
- Claude Code API integration through LangChain
- Prompt templates in `fabric/patterns/code_generation.json`
- Skill-specific code generation templates

### 5.2 LangChain Integration

**Purpose**: LLM interaction abstraction layer

**Components**:
- **LangChain Core**: Base LLM interactions
- **LangChain OpenAI**: OpenAI/Claude model integration
- **LangChain Community**: Additional integrations

**Implementation**:
```python
# src/atlas/integrations/langchain/client.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class ATLASLangChainClient:
    """Single responsibility: LangChain LLM client management"""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        self.llm = ChatOpenAI(
            model=config["model"],
            temperature=config["temperature"]
        )
```

### 5.3 LangGraph Integration

**Purpose**: Workflow orchestration and skills chaining

**Graph Types**:
- **DAG (Directed Acyclic Graph)**: Linear workflows without cycles
- **DCG (Directed Cyclic Graph)**: Workflows with feedback loops

**Implementation**:
```python
# src/atlas/integrations/langgraph/orchestrator.py
from langgraph.graph import StateGraph

class ATLASOrchestrator:
    """Single responsibility: Workflow orchestration"""
    
    def __init__(self, skills_registry: SkillsRegistry) -> None:
        self.graph = StateGraph()
        self.skills = skills_registry
```

### 5.4 LangSmith Integration

**Purpose**: Monitoring, tracing, and observability

**Monitoring Levels**:
- **Development**: Verbose logging, all traces
- **Production**: Optimized logging, sampled traces

**Implementation**:
```python
# src/atlas/integrations/langsmith/monitor.py
from langsmith import Client

class ATLASMonitor:
    """Single responsibility: Telemetry and monitoring"""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        self.client = Client(api_key=config["api_key"])
```

### 5.5 Tavily Integration

**Purpose**: Enhanced search and information retrieval

**Use Cases**:
- Web search for taxonomy sources
- Document retrieval
- Real-time data gathering

**Implementation**:
```python
# src/atlas/integrations/tavily/search.py
from tavily import TavilyClient

class ATLASTavilySearch:
    """Single responsibility: Search operations"""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        self.client = TavilyClient(api_key=config["api_key"])
```

### 5.6 Marimo Integration

**Purpose**: Interactive notebook-based agentic delivery

**Deployment Modes**:
- **Development**: `marimo edit notebook.py` (editable)
- **Production**: `marimo run notebook.py` (read-only, optimized)

**Implementation**:
```python
# notebooks/energy_extraction.py
import marimo as mo

app = mo.App()

@app.cell
def extract_energy_taxonomy():
    """Single responsibility: Energy taxonomy extraction UI"""
    return mo.ui.form(...)
```

---

## 6. SKILL.md Structure and FQSN Design

### 6.1 FQSN Filesystem Organization

**Principle**: The filesystem path IS the skill identifier

**Structure**:
```
skills/
├── energy/                           # Domain: energy
│   ├── extraction/                   # Sub-domain: extraction
│   │   ├── eia_glossary/            # Skill: eia_glossary
│   │   │   ├── SKILL.md             # Skill specification
│   │   │   ├── prompts/             # Skill-specific prompts
│   │   │   │   └── extract.json
│   │   │   └── examples/            # Usage examples
│   │   │       └── basic.py
│   │   └── iea_data/                # Skill: iea_data
│   │       └── SKILL.md
│   ├── analysis/                     # Sub-domain: analysis
│   │   ├── relationship_discovery/  # Skill: relationship_discovery
│   │   │   └── SKILL.md
│   │   └── validation/              # Skill: validation
│   │       └── SKILL.md
│   └── synthesis/                    # Sub-domain: synthesis
│       └── knowledge_graph/         # Skill: knowledge_graph
│           └── SKILL.md
└── transportation/                   # Domain: transportation
    └── ...
```

**FQSN Examples**:
- `energy.extraction.eia_glossary`
- `energy.analysis.relationship_discovery`
- `transportation.fleet.optimization`

### 6.2 SKILL.md Template

**Purpose**: Single source of truth for skill specification

**Structure**:
```markdown
# Skill: {FQSN}

## Metadata

- **FQSN**: `{domain}.{subdomain}.{skill_name}`
- **Version**: 1.0.0
- **Status**: Active | Deprecated | Experimental
- **Responsibility**: {Single clear responsibility statement}
- **Dependencies**: {List of required skills or services}

## Description

{Clear, concise description of what this skill does}

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| param1    | str  | Yes      | ...         |
| param2    | int  | No       | ...         |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| field1 | List[Node] | ... |
| field2 | Dict[str, Any] | ... |

## Configuration

```json
{
  "llm_model": "gpt-4-1106-preview",
  "temperature": 0.7,
  "max_retries": 3
}
```

## Prompts

- **Primary**: `prompts/extract.json`
- **Fallback**: `prompts/extract_simple.json`

## Examples

See `examples/` directory for usage examples.

## Integration

### LangGraph Node

```python
def create_node() -> Callable:
    # Implementation
    pass
```

### Standalone Usage

```python
from atlas.skills.energy.extraction.eia_glossary import EIAGlossaryExtractor

extractor = EIAGlossaryExtractor(config)
result = extractor.extract(url="https://...")
```

## Testing

- Unit tests: `tests/unit/skills/energy/extraction/test_eia_glossary.py`
- Integration tests: `tests/integration/skills/energy/extraction/test_eia_glossary.py`

## Monitoring

- LangSmith project: `atlas-energy-extraction`
- Key metrics: extraction_time, node_count, relationship_count

## Changelog

### 1.0.0 (2025-01-24)
- Initial release
```

### 6.3 SKILL.md Loading Mechanism

**Principle**: Lazy loading based on FQSN

**Implementation**:
```python
# src/atlas/skills/registry.py
from pathlib import Path
from typing import Dict, Optional

class SkillsRegistry:
    """Single responsibility: Skill discovery and loading via FQSN"""
    
    def __init__(self, skills_root: Path) -> None:
        self.skills_root = skills_root
        self._cache: Dict[str, Skill] = {}
    
    def get_skill(self, fqsn: str) -> Optional[Skill]:
        """
        Get skill by FQSN (e.g., 'energy.extraction.eia_glossary')
        
        Args:
            fqsn: Fully Qualified Skill Name
            
        Returns:
            Skill instance or None if not found
        """
        # Check cache first
        if fqsn in self._cache:
            return self._cache[fqsn]
        
        # Convert FQSN to filesystem path
        path_parts = fqsn.split('.')
        skill_path = self.skills_root / Path(*path_parts) / "SKILL.md"
        
        if not skill_path.exists():
            return None
        
        # Load and cache skill
        skill = Skill.from_markdown(skill_path)
        self._cache[fqsn] = skill
        
        return skill
```

---

## 7. Skills Chaining with LangGraph

### 7.1 DAG vs DCG Patterns

**DAG (Directed Acyclic Graph)**:
- No cycles - linear progression
- Suitable for: Extraction → Analysis → Validation → Storage
- Example: Energy taxonomy extraction workflow

**DCG (Directed Cyclic Graph)**:
- Contains cycles - feedback loops
- Suitable for: Iterative refinement, validation loops
- Example: Extraction → Validation → (if invalid) → Re-extraction

### 7.2 Skills Chain Specification

**Format**: JSON-based chain definition with DAG/DCG annotation

**Example**:
```json
{
  "chain_name": "energy_taxonomy_extraction",
  "graph_type": "DAG",
  "description": "Extract energy taxonomy from EIA glossary",
  "skills": [
    {
      "fqsn": "energy.extraction.eia_glossary",
      "node_id": "extract",
      "inputs": {
        "url": "${input.url}",
        "fuel_groups": "${input.fuel_groups}"
      },
      "outputs": {
        "nodes": "extracted_nodes",
        "relationships": "extracted_relationships"
      }
    },
    {
      "fqsn": "energy.analysis.relationship_discovery",
      "node_id": "analyze",
      "inputs": {
        "nodes": "${extract.nodes}"
      },
      "outputs": {
        "relationships": "discovered_relationships"
      },
      "depends_on": ["extract"]
    },
    {
      "fqsn": "energy.validation.taxonomy_validator",
      "node_id": "validate",
      "inputs": {
        "nodes": "${extract.nodes}",
        "relationships": "${analyze.relationships}"
      },
      "outputs": {
        "validation_status": "status",
        "issues": "validation_issues"
      },
      "depends_on": ["analyze"]
    }
  ],
  "edges": [
    {"from": "extract", "to": "analyze"},
    {"from": "analyze", "to": "validate"}
  ]
}
```

**DCG Example with Feedback Loop**:
```json
{
  "chain_name": "iterative_taxonomy_refinement",
  "graph_type": "DCG",
  "description": "Iteratively refine taxonomy with validation feedback",
  "skills": [
    {
      "fqsn": "energy.extraction.eia_glossary",
      "node_id": "extract",
      "inputs": {
        "url": "${input.url}",
        "refinement_hints": "${validate.hints}"
      }
    },
    {
      "fqsn": "energy.validation.taxonomy_validator",
      "node_id": "validate",
      "inputs": {
        "nodes": "${extract.nodes}"
      },
      "outputs": {
        "is_valid": "valid",
        "hints": "refinement_hints"
      }
    }
  ],
  "edges": [
    {"from": "extract", "to": "validate"},
    {
      "from": "validate",
      "to": "extract",
      "condition": "not ${validate.valid}",
      "max_iterations": 3,
      "note": "DCG: Feedback loop for refinement"
    }
  ]
}
```

### 7.3 LangGraph Implementation

**Principle**: One chain definition = One LangGraph state machine

**Implementation**:
```python
# src/atlas/integrations/langgraph/chain_builder.py
from langgraph.graph import StateGraph, END
from typing import Dict, Any, List

class ChainBuilder:
    """Single responsibility: Build LangGraph from chain specification"""
    
    def __init__(self, skills_registry: SkillsRegistry) -> None:
        self.skills = skills_registry
    
    def build_graph(self, chain_spec: Dict[str, Any]) -> StateGraph:
        """
        Build LangGraph from chain specification
        
        Args:
            chain_spec: Chain specification with skills and edges
            
        Returns:
            StateGraph: Configured LangGraph
        """
        graph = StateGraph()
        
        # Add nodes for each skill
        for skill_spec in chain_spec["skills"]:
            fqsn = skill_spec["fqsn"]
            node_id = skill_spec["node_id"]
            
            # Load skill
            skill = self.skills.get_skill(fqsn)
            
            # Create node function
            def node_fn(state: Dict[str, Any]) -> Dict[str, Any]:
                return skill.execute(state)
            
            graph.add_node(node_id, node_fn)
        
        # Add edges
        for edge in chain_spec["edges"]:
            from_node = edge["from"]
            to_node = edge["to"]
            
            if "condition" in edge:
                # Conditional edge (DCG)
                graph.add_conditional_edges(
                    from_node,
                    lambda state: to_node if eval(edge["condition"]) else END
                )
            else:
                # Regular edge (DAG)
                graph.add_edge(from_node, to_node)
        
        return graph
```

### 7.4 Chain Annotations

**Purpose**: Document graph type and characteristics

**Annotations in Chain Files**:
```json
{
  "chain_name": "...",
  "graph_type": "DAG",
  "annotations": {
    "is_cyclic": false,
    "max_depth": 5,
    "parallel_execution": false,
    "notes": [
      "DAG: Linear extraction pipeline",
      "No feedback loops",
      "Suitable for batch processing"
    ]
  }
}
```

---

## 8. Domain-Driven Database Design (D⁴)

### 8.1 Schema Naming Conventions

**Domain Schemas**: `dDomainName`
- `dEnergy`: Energy domain
- `dTransportation`: Transportation domain
- `dManufacturing`: Manufacturing domain

**Sub-Domain Schemas**: `sdSubDomainName`
- `dEnergy.sdRenewable`: Renewable energy sub-domain
- `dEnergy.sdFossilFuel`: Fossil fuel sub-domain
- `dEnergy.sdNuclear`: Nuclear energy sub-domain

**Lineage Tracing**:
- Schema names enable automatic lineage tracing
- Sub-domains can be nested: `dEnergy.sdRenewable.sdSolar`

### 8.2 Business Definitions as Queryable Metadata

**Principle**: Business definitions must be queryable, not comments

**Implementation**:
```cypher
// ❌ WRONG: Non-queryable comment
CREATE (n:EnergyTerm {name: "Solar PV"})
// Definition: Photovoltaic technology that converts sunlight to electricity

// ✅ CORRECT: Queryable metadata
CREATE (n:EnergyTerm {
  name: "Solar PV",
  business_definition: "Photovoltaic technology that converts sunlight to electricity",
  definition_hash: "sha256:abc123...",
  domain: "dEnergy",
  subdomain: "dEnergy.sdRenewable"
})
```

### 8.3 Temporal Metadata with Allen Intervals

**Principle**: Use Allen Intervals (meets relationship) for state transitions

**Implementation**:
```cypher
// Create node with temporal metadata
CREATE (n:EnergyTerm {
  name: "Solar PV",
  business_definition: "Photovoltaic technology...",
  definition_hash: "sha256:abc123...",
  start_datetime: datetime("2025-01-24T00:00:00Z"),
  end_datetime: null  // Open-ended, currently active
})

// Update creates new version with meets relationship
MATCH (old:EnergyTerm {name: "Solar PV", end_datetime: null})
SET old.end_datetime = datetime("2025-02-01T00:00:00Z")
CREATE (new:EnergyTerm {
  name: "Solar PV",
  business_definition: "Updated definition...",
  definition_hash: "sha256:def456...",
  start_datetime: datetime("2025-02-01T00:00:00Z"),
  end_datetime: null
})
CREATE (old)-[:MEETS]->(new)
```

### 8.4 Neo4j Schema Design

**Node Labels**:
- Domain-prefixed: `dEnergy:EnergyTerm`
- Sub-domain-prefixed: `sdRenewable:SolarTechnology`

**Relationship Types**:
- Domain-aware: `dEnergy:PART_OF`, `dEnergy:RELATED_TO`

**Indexes**:
```cypher
// Domain-specific indexes
CREATE INDEX energy_term_name FOR (n:dEnergy:EnergyTerm) ON (n.name);
CREATE INDEX energy_term_hash FOR (n:dEnergy:EnergyTerm) ON (n.definition_hash);
CREATE INDEX energy_term_temporal FOR (n:dEnergy:EnergyTerm) ON (n.start_datetime, n.end_datetime);
```

---

## 9. Repository Structure

### 9.1 Complete Directory Layout

```
atlas-framework/
├── README.md
├── LICENSE
├── pyproject.toml                    # UV/Ruff configuration (Production)
├── environments/
│   ├── dev.yml                       # Conda environment (Dev/QA)
│   └── prod.yml                      # Production environment spec
├── src/
│   └── atlas/
│       ├── __init__.py
│       ├── core/                     # Core framework (SRP: Core logic)
│       │   ├── __init__.py
│       │   ├── node.py
│       │   ├── relationship.py
│       │   ├── client.py
│       │   └── exceptions.py
│       ├── config/                   # Configuration (SRP: Config management)
│       │   ├── __init__.py
│       │   ├── loader.py
│       │   ├── registry.py
│       │   └── schema.py
│       ├── enums/                    # Enumerations (SRP: Type definitions)
│       │   ├── __init__.py
│       │   ├── loader.py
│       │   ├── node_label.py
│       │   ├── relationship.py
│       │   └── validation.py
│       ├── descriptors/              # Python descriptors (SRP: Property management)
│       │   ├── __init__.py
│       │   ├── cached_property.py
│       │   ├── lazy_property.py
│       │   └── validated_property.py
│       ├── decorators/               # Decorators (SRP: Cross-cutting concerns)
│       │   ├── __init__.py
│       │   ├── atlas_operation.py
│       │   ├── cached_property.py
│       │   ├── fabric_pattern.py
│       │   └── validate_graph_operation.py
│       ├── integrations/             # External integrations (SRP per integration)
│       │   ├── __init__.py
│       │   ├── langchain/
│       │   │   ├── __init__.py
│       │   │   └── client.py
│       │   ├── langgraph/
│       │   │   ├── __init__.py
│       │   │   ├── orchestrator.py
│       │   │   └── chain_builder.py
│       │   ├── langsmith/
│       │   │   ├── __init__.py
│       │   │   └── monitor.py
│       │   ├── tavily/
│       │   │   ├── __init__.py
│       │   │   └── search.py
│       │   ├── claude/
│       │   │   ├── __init__.py
│       │   │   └── code_assistant.py
│       │   └── neo4j/
│       │       ├── __init__.py
│       │       ├── adapter.py
│       │       └── d4_schema.py
│       └── skills/                   # Skills registry (FQSN-based)
│           ├── __init__.py
│           ├── registry.py
│           └── base.py
├── skills/                           # FQSN skill definitions
│   ├── energy/
│   │   ├── extraction/
│   │   │   ├── eia_glossary/
│   │   │   │   ├── SKILL.md
│   │   │   │   ├── prompts/
│   │   │   │   │   └── extract.json
│   │   │   │   └── examples/
│   │   │   │       └── basic.py
│   │   │   └── iea_data/
│   │   │       └── SKILL.md
│   │   ├── analysis/
│   │   │   ├── relationship_discovery/
│   │   │   │   └── SKILL.md
│   │   │   └── validation/
│   │   │       └── SKILL.md
│   │   └── synthesis/
│   │       └── knowledge_graph/
│   │           └── SKILL.md
│   └── transportation/
│       └── ...
├── chains/                           # LangGraph chain definitions
│   ├── energy/
│   │   ├── extraction_pipeline.json  # DAG
│   │   └── iterative_refinement.json # DCG
│   └── transportation/
│       └── ...
├── fabric/                           # FABRIC patterns
│   └── patterns/
│       ├── extract_wisdom.json
│       ├── find_patterns.json
│       └── analyze_claims.json
├── notebooks/                        # Marimo notebooks
│   ├── energy_extraction.py
│   ├── relationship_analysis.py
│   └── knowledge_graph_viz.py
├── tests/
│   ├── unit/
│   │   ├── core/
│   │   ├── skills/
│   │   └── integrations/
│   └── integration/
│       ├── chains/
│       └── end_to_end/
├── docs/
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── d4_design.md
│   │   └── skills_system.md
│   ├── guides/
│   │   ├── getting_started.md
│   │   ├── creating_skills.md
│   │   └── chain_development.md
│   └── api/
│       └── reference.md
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── docker-swarm.yml
└── .github/
    └── workflows/
        ├── ci.yml
        └── deploy.yml
```

### 9.2 Key Directories and Responsibilities

| Directory | Responsibility | Principle |
|-----------|---------------|-----------|
| `src/atlas/core/` | Core framework logic | SRP: Core domain |
| `src/atlas/config/` | Configuration management | SRP: Configuration |
| `src/atlas/integrations/` | External service integrations | SRP per integration |
| `skills/` | FQSN skill definitions | FQSN: Filesystem identity |
| `chains/` | LangGraph chain specifications | SRP: Workflow definition |
| `fabric/` | FABRIC pattern templates | SRP: Prompt patterns |
| `notebooks/` | Marimo interactive notebooks | SRP: User interaction |
| `tests/` | Test suites | SRP: Quality assurance |
| `docs/` | Documentation | SRP: Knowledge sharing |

---

## 10. Implementation Phases

### Phase 1: Foundation (Week 1-2)

**Objectives**:
- Set up repository structure
- Configure Dev/QA and Production environments
- Implement core framework with Pydantic v2

**Deliverables**:
- Repository with complete directory structure
- Working Conda environment for Dev/QA
- Working UV environment for Production
- Core classes: `ATLASNode`, `ATLASRelationship`, `ATLASClient`
- Configuration system with `ConfigLoader` and `ConfigRegistry`

**Success Criteria**:
- All environments install successfully
- Core classes pass unit tests
- Configuration loads from multiple sources

### Phase 2: Skills System (Week 3-4)

**Objectives**:
- Implement FQSN-based skills registry
- Create SKILL.md template and parser
- Develop first skills for energy domain

**Deliverables**:
- `SkillsRegistry` with lazy loading
- `Skill` class with SKILL.md parsing
- First skills:
  - `energy.extraction.eia_glossary`
  - `energy.analysis.relationship_discovery`
  - `energy.validation.taxonomy_validator`

**Success Criteria**:
- Skills load correctly via FQSN
- SKILL.md parsing works for all fields
- Skills execute successfully in isolation

### Phase 3: Integration Layer (Week 5-6)

**Objectives**:
- Integrate LangChain, LangGraph, LangSmith, Tavily, Claude Code
- Implement adapters for each integration
- Create monitoring and observability

**Deliverables**:
- LangChain client for LLM interactions
- LangGraph orchestrator for workflow management
- LangSmith monitor for telemetry
- Tavily search integration
- Claude Code assistant integration
- Neo4j adapter with D⁴ schema

**Success Criteria**:
- All integrations work independently
- LangSmith captures traces
- Neo4j stores data with D⁴ schema

### Phase 4: Skills Chaining (Week 7-8)

**Objectives**:
- Implement LangGraph chain builder
- Create DAG and DCG chain examples
- Develop chain execution engine

**Deliverables**:
- `ChainBuilder` class
- Chain specifications for:
  - Energy extraction pipeline (DAG)
  - Iterative refinement (DCG)
- Chain execution with state management

**Success Criteria**:
- DAG chains execute linearly
- DCG chains handle feedback loops
- State passes correctly between nodes

### Phase 5: Marimo Notebooks (Week 9-10)

**Objectives**:
- Create interactive notebooks for agentic delivery
- Implement visualization components
- Deploy production notebooks

**Deliverables**:
- Marimo notebooks:
  - Energy taxonomy extraction
  - Relationship analysis
  - Knowledge graph visualization
- Production deployment scripts

**Success Criteria**:
- Notebooks run in dev mode (editable)
- Notebooks run in production mode (optimized)
- Visualizations render correctly

### Phase 6: Testing and Documentation (Week 11-12)

**Objectives**:
- Complete test coverage
- Write comprehensive documentation
- Prepare for deployment

**Deliverables**:
- Unit tests for all modules (>90% coverage)
- Integration tests for chains
- End-to-end tests
- Complete documentation in `docs/`
- Deployment guides

**Success Criteria**:
- All tests pass
- Documentation is complete and accurate
- Deployment succeeds in test environment

---

## 11. Approval Checklist

### 11.1 Architectural Principles

- [ ] KISS: All components follow "Keep It Simple and Standard"
- [ ] SRP: Each module/class/skill has single responsibility
- [ ] D⁴: Database design uses FQDN with queryable metadata
- [ ] FQSN: Skills identified by filesystem path

### 11.2 Environment Separation

- [ ] Dev/QA uses Conda/Conda-forge
- [ ] Production uses Astral UV and Ruff
- [ ] Clear separation of concerns
- [ ] Both environments tested

### 11.3 Integration Architecture

- [ ] Claude Code integration defined
- [ ] LangChain integration defined
- [ ] LangGraph integration defined
- [ ] LangSmith integration defined
- [ ] Tavily integration defined
- [ ] Marimo integration defined

### 11.4 Skills System

- [ ] FQSN filesystem structure defined
- [ ] SKILL.md template complete
- [ ] Skills registry with lazy loading
- [ ] Example skills provided

### 11.5 Skills Chaining

- [ ] DAG pattern defined
- [ ] DCG pattern defined
- [ ] Chain specification format defined
- [ ] LangGraph implementation approach clear

### 11.6 D⁴ Database Design

- [ ] Schema naming conventions defined
- [ ] Business definitions as queryable metadata
- [ ] Temporal metadata with Allen Intervals
- [ ] Neo4j implementation approach clear

### 11.7 Repository Structure

- [ ] Complete directory layout defined
- [ ] Responsibilities clearly assigned
- [ ] SRP maintained throughout

### 11.8 Implementation Plan

- [ ] Phases clearly defined
- [ ] Deliverables specified
- [ ] Success criteria established
- [ ] Timeline reasonable

---

## 12. Next Steps After Approval

1. **Create Repository**: Initialize Git repository with structure
2. **Set Up Environments**: Configure Conda (Dev/QA) and UV (Production)
3. **Implement Foundation**: Core classes and configuration
4. **Develop Skills**: First set of energy domain skills
5. **Integrate Services**: LangChain, LangGraph, LangSmith, Tavily, Claude Code
6. **Build Chains**: DAG and DCG examples
7. **Create Notebooks**: Marimo interactive notebooks
8. **Test and Document**: Comprehensive testing and documentation

---

## Appendix A: Glossary

- **ATLAS**: Agentic Taxonomy Learning and Synthesis
- **FQSN**: Fully Qualified Skill Name
- **D⁴**: Domain-Driven Database Design
- **KISS**: Keep It Simple and Standard
- **SRP**: Single Responsibility Principle
- **DAG**: Directed Acyclic Graph
- **DCG**: Directed Cyclic Graph
- **FQDN**: Fully Qualified Domain Name

---

## Appendix B: References

- LangChain Documentation: https://python.langchain.com/
- LangGraph Documentation: https://langchain-ai.github.io/langgraph/
- LangSmith Documentation: https://docs.smith.langchain.com/
- Marimo Documentation: https://marimo.io/
- Neo4j Documentation: https://neo4j.com/docs/
- Astral UV: https://github.com/astral-sh/uv
- Ruff: https://github.com/astral-sh/ruff

---

**END OF ARCHITECTURAL PLAN**

**Status**: PENDING APPROVAL  
**Approval Required**: YES or NO from user before proceeding with implementation
