# Quick Start Guide

This guide will help you get started with ATLAS Framework quickly. You'll learn how to create a simple taxonomy, extract knowledge from text, and visualize the resulting knowledge graph.

## Prerequisites

Before you begin, make sure you have:

- Installed ATLAS Framework (see [Installation Guide](installation.md))
- Basic understanding of Python
- Neo4j database (optional, for advanced features)

## 5-Minute Quick Start

Let's create a simple energy taxonomy and extract knowledge from text:

### Step 1: Install ATLAS Framework

```bash
pip install atlas-framework
```

### Step 2: Create a Simple Script

Create a file named `quick_start.py` with the following content:

```python
from atlas import ATLASClient

# Initialize client
client = ATLASClient()

# Sample text about solar energy
text = """
Solar photovoltaic (PV) is a technology that converts sunlight directly into electricity.
Solar PV cells are made from silicon and other materials that exhibit the photovoltaic effect.
Solar PV is a renewable energy source and is one of the fastest-growing energy technologies.
"""

# Extract knowledge from text
result = client.extract_from_text(
    text=text,
    domain="energy",
    extraction_depth="basic"
)

# Print extracted nodes
print(f"Extracted {len(result.nodes)} nodes:")
for node in result.nodes:
    print(f"- {node.properties.get('name')}: {node.properties.get('definition', 'No definition')}")

# Print extracted relationships
print(f"\nExtracted {len(result.relationships)} relationships:")
for rel in result.relationships:
    start_node = client.get_node_by_id(rel.start_node_id)
    end_node = client.get_node_by_id(rel.end_node_id)
    print(f"- {start_node.properties.get('name')} {rel.type} {end_node.properties.get('name')}")

# Visualize the knowledge graph
client.visualize(
    nodes=result.nodes,
    relationships=result.relationships,
    output_path="knowledge_graph.html"
)

print("\nKnowledge graph visualization saved to knowledge_graph.html")
```

### Step 3: Run the Script

```bash
python quick_start.py
```

You should see output similar to:

```
Extracted 4 nodes:
- Solar PV: A technology that converts sunlight directly into electricity
- Photovoltaic Effect: The process of converting light into electricity using semiconducting materials
- Silicon: A chemical element commonly used in solar cells
- Renewable Energy: Energy derived from natural processes that are replenished constantly

Extracted 3 relationships:
- Solar PV IS_A Renewable Energy
- Solar PV USES Silicon
- Solar PV EXHIBITS Photovoltaic Effect

Knowledge graph visualization saved to knowledge_graph.html
```

### Step 4: View the Knowledge Graph

Open `knowledge_graph.html` in your web browser to see the visualization of your knowledge graph.

## 30-Minute Tutorial

Now let's create a more comprehensive energy taxonomy with custom configuration:

### Step 1: Create a Configuration File

Create a file named `atlas_config.json` with the following content:

```json
{
  "version": "1.0",
  "metadata": {
    "name": "Energy Taxonomy",
    "description": "Taxonomy for energy terms and concepts",
    "created": "2025-01-15T10:00:00Z"
  },
  "node_types": {
    "energy_term": {
      "labels": ["EnergyTerm", "TaxonomyNode"],
      "properties": {
        "name": {"type": "string", "required": true},
        "definition": {"type": "string", "required": true},
        "fuel_group": {"type": "string", "required": false, "enum": ["renewable", "fossil", "nuclear", "alternative"]}
      }
    },
    "energy_source": {
      "labels": ["EnergySource", "TaxonomyNode"],
      "properties": {
        "name": {"type": "string", "required": true},
        "description": {"type": "string", "required": true},
        "renewable": {"type": "boolean", "required": true}
      }
    }
  },
  "relationship_types": {
    "IS_A": {
      "description": "Indicates that one node is a type or subclass of another"
    },
    "PART_OF": {
      "description": "Indicates that one node is a part or component of another"
    },
    "USES": {
      "description": "Indicates that one node uses or utilizes another"
    },
    "PRODUCES": {
      "description": "Indicates that one node produces or generates another"
    }
  }
}
```

### Step 2: Create a Comprehensive Script

Create a file named `energy_taxonomy.py` with the following content:

```python
from atlas import ATLASClient, RelationshipType
import os

# Initialize client with custom configuration
client = ATLASClient(config_path="atlas_config.json")

# Sample text about energy sources
text = """
Renewable energy sources include solar, wind, hydro, geothermal, and biomass.
Solar energy is captured through photovoltaic panels and concentrated solar power systems.
Wind energy is harvested by wind turbines, which convert kinetic energy into electricity.
Hydroelectric power uses the energy of flowing water to generate electricity through turbines.
Fossil fuels include coal, oil, and natural gas, which are non-renewable and produce carbon emissions.
Nuclear energy is produced through nuclear fission of uranium in reactors.
"""

# Extract knowledge from text
print("Extracting knowledge from text...")
result = client.extract_from_text(
    text=text,
    domain="energy",
    extraction_depth="comprehensive"
)

# Create additional nodes manually
print("\nCreating additional nodes...")
solar_panel = client.create_node(
    node_type="energy_term",
    properties={
        "name": "Solar Panel",
        "definition": "A device that converts sunlight into electricity using photovoltaic cells",
        "fuel_group": "renewable"
    }
)

photovoltaic_cell = client.create_node(
    node_type="energy_term",
    properties={
        "name": "Photovoltaic Cell",
        "definition": "The basic unit of a solar panel that converts light into electricity",
        "fuel_group": "renewable"
    }
)

# Create relationships manually
print("Creating relationships...")
client.create_relationship(
    start_node=solar_panel,
    end_node=photovoltaic_cell,
    type=RelationshipType.CONTAINS,
    properties={
        "confidence_score": 1.0,
        "source": "manual"
    }
)

# Find nodes by property
print("\nFinding renewable energy sources...")
renewable_sources = client.find_nodes(
    node_type="energy_source",
    properties={"renewable": True}
)

print(f"Found {len(renewable_sources)} renewable energy sources:")
for source in renewable_sources:
    print(f"- {source.properties.get('name')}")

# Find relationships by type
print("\nFinding IS_A relationships...")
is_a_relationships = client.find_relationships(
    relationship_type=RelationshipType.IS_A
)

print(f"Found {len(is_a_relationships)} IS_A relationships:")
for rel in is_a_relationships:
    start_node = client.get_node_by_id(rel.start_node_id)
    end_node = client.get_node_by_id(rel.end_node_id)
    print(f"- {start_node.properties.get('name')} IS_A {end_node.properties.get('name')}")

# Validate the knowledge graph
print("\nValidating knowledge graph...")
validation_result = client.validate_knowledge_graph()

print(f"Validation result: {validation_result.status}")
if validation_result.issues:
    print("Issues found:")
    for issue in validation_result.issues:
        print(f"- {issue.description}")

# Export the knowledge graph
print("\nExporting knowledge graph...")
export_path = "energy_taxonomy.json"
client.export_to_json(
    output_path=export_path,
    include_properties=True,
    pretty_print=True
)

print(f"Knowledge graph exported to {export_path}")

# Visualize the knowledge graph
print("\nGenerating visualization...")
client.visualize(
    output_path="energy_taxonomy.html",
    title="Energy Taxonomy",
    description="Comprehensive taxonomy of energy terms and sources"
)

print("Knowledge graph visualization saved to energy_taxonomy.html")
```

### Step 3: Run the Script

```bash
python energy_taxonomy.py
```

### Step 4: Explore the Results

- Open `energy_taxonomy.html` in your web browser to see the visualization
- Examine `energy_taxonomy.json` to see the exported data

## Advanced Usage

### Connecting to Neo4j

For advanced features, connect ATLAS Framework to a Neo4j database:

```python
from atlas import ATLASClient

# Connect to Neo4j
client = ATLASClient(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password"
)

# Now all operations will use Neo4j for storage
```

### Using Agentic LLMs

ATLAS Framework can use agentic LLMs for advanced extraction:

```python
from atlas import ATLASClient, ExtractionStrategy

# Initialize client with OpenAI API key
client = ATLASClient(
    openai_api_key="your-api-key"
)

# Extract knowledge using agentic LLMs
result = client.extract_from_url(
    url="https://www.eia.gov/tools/glossary/",
    domain="energy",
    extraction_strategy=ExtractionStrategy.AGENTIC_LLM,
    extraction_depth="comprehensive"
)
```

### Using FABRIC Patterns

ATLAS Framework supports FABRIC patterns for intelligent behavior:

```python
from atlas import ATLASClient, FabricPattern

# Initialize client
client = ATLASClient()

# Apply FABRIC pattern
result = client.apply_fabric_pattern(
    pattern=FabricPattern.EXTRACT_WISDOM,
    input_text="Solar energy is a renewable source that converts sunlight into electricity through photovoltaic cells.",
    domain="energy"
)

print("Extracted wisdom:")
for item in result.wisdom:
    print(f"- {item}")
```

### Creating a Custom Taxonomy

Create a custom taxonomy with specific node and relationship types:

```python
from atlas import ATLASClient, TaxonomyBuilder

# Initialize client
client = ATLASClient()

# Create taxonomy builder
builder = TaxonomyBuilder(client)

# Define node types
builder.add_node_type(
    name="technology",
    labels=["Technology", "TaxonomyNode"],
    properties={
        "name": {"type": "string", "required": True},
        "description": {"type": "string", "required": True},
        "maturity_level": {"type": "string", "enum": ["research", "development", "commercial", "mature"]}
    }
)

builder.add_node_type(
    name="application",
    labels=["Application", "TaxonomyNode"],
    properties={
        "name": {"type": "string", "required": True},
        "description": {"type": "string", "required": True},
        "sector": {"type": "string", "required": True}
    }
)

# Define relationship types
builder.add_relationship_type(
    name="ENABLES",
    description="Indicates that one technology enables an application"
)

builder.add_relationship_type(
    name="COMPETES_WITH",
    description="Indicates that one technology competes with another"
)

# Build the taxonomy
taxonomy = builder.build(name="Energy Technology Taxonomy")

# Use the taxonomy
solar_pv = taxonomy.create_node(
    node_type="technology",
    properties={
        "name": "Solar PV",
        "description": "Photovoltaic technology that converts sunlight into electricity",
        "maturity_level": "mature"
    }
)

residential_power = taxonomy.create_node(
    node_type="application",
    properties={
        "name": "Residential Power",
        "description": "Electricity for residential buildings",
        "sector": "residential"
    }
)

taxonomy.create_relationship(
    start_node=solar_pv,
    end_node=residential_power,
    type="ENABLES"
)
```

## Next Steps

Now that you've completed the quick start guide, you can:

- Learn about [Configuration Options](configuration.md) to customize ATLAS Framework
- Explore [First Steps](first-steps.md) for more detailed examples
- Read about [Knowledge Graphs](../features/knowledge-graph.md) to understand the core concept
- Check out [Examples](../examples/basic-usage.md) for more advanced usage

