# Basic Usage Examples

This page provides basic usage examples for ATLAS Framework. These examples demonstrate the core functionality and are designed to help you get started quickly.

## Example 1: Creating a Simple Knowledge Graph

This example shows how to create a simple knowledge graph with nodes and relationships:

```python
from atlas import ATLASClient, RelationshipType

# Initialize client
client = ATLASClient()

# Create nodes
solar_pv = client.create_node(
    labels=["EnergyTerm", "RenewableSource"],
    properties={
        "name": "Solar PV",
        "definition": "Photovoltaic technology that converts sunlight into electricity",
        "fuel_group": "renewable"
    }
)

photovoltaic_cell = client.create_node(
    labels=["EnergyTerm", "Component"],
    properties={
        "name": "Photovoltaic Cell",
        "definition": "The basic unit of a solar panel that converts light into electricity",
        "fuel_group": "renewable"
    }
)

renewable_energy = client.create_node(
    labels=["EnergyTerm", "Category"],
    properties={
        "name": "Renewable Energy",
        "definition": "Energy derived from natural processes that are replenished constantly",
        "fuel_group": "renewable"
    }
)

# Create relationships
client.create_relationship(
    start_node=solar_pv,
    end_node=photovoltaic_cell,
    type=RelationshipType.CONTAINS,
    properties={
        "confidence_score": 1.0,
        "source": "manual"
    }
)

client.create_relationship(
    start_node=solar_pv,
    end_node=renewable_energy,
    type=RelationshipType.IS_A,
    properties={
        "confidence_score": 1.0,
        "source": "manual"
    }
)

# Visualize the knowledge graph
client.visualize(
    nodes=[solar_pv, photovoltaic_cell, renewable_energy],
    output_path="simple_knowledge_graph.html"
)

print("Knowledge graph visualization saved to simple_knowledge_graph.html")
```

<div class="result-preview">
    <h3>Result Preview</h3>
    <p>This example creates a simple knowledge graph with three nodes and two relationships:</p>
    <ul>
        <li>Nodes: Solar PV, Photovoltaic Cell, Renewable Energy</li>
        <li>Relationships: Solar PV CONTAINS Photovoltaic Cell, Solar PV IS_A Renewable Energy</li>
    </ul>
    <p>The visualization shows the nodes and relationships in an interactive graph.</p>
</div>

## Example 2: Extracting Knowledge from Text

This example demonstrates how to extract knowledge from text:

```python
from atlas import ATLASClient

# Initialize client
client = ATLASClient()

# Sample text about energy sources
text = """
Renewable energy sources include solar, wind, hydro, geothermal, and biomass.
Solar energy is captured through photovoltaic panels and concentrated solar power systems.
Wind energy is harvested by wind turbines, which convert kinetic energy into electricity.
Hydroelectric power uses the energy of flowing water to generate electricity through turbines.
"""

# Extract knowledge from text
result = client.extract_from_text(
    text=text,
    domain="energy",
    extraction_depth="comprehensive"
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

# Visualize the extracted knowledge graph
client.visualize(
    nodes=result.nodes,
    relationships=result.relationships,
    output_path="extracted_knowledge_graph.html"
)

print("\nKnowledge graph visualization saved to extracted_knowledge_graph.html")
```

<div class="result-preview">
    <h3>Result Preview</h3>
    <p>This example extracts knowledge from text about renewable energy sources:</p>
    <ul>
        <li>Extracted nodes include: Renewable Energy, Solar Energy, Wind Energy, Hydroelectric Power, etc.</li>
        <li>Extracted relationships include: Solar Energy IS_A Renewable Energy, Wind Energy IS_A Renewable Energy, etc.</li>
    </ul>
    <p>The visualization shows the extracted knowledge graph with all nodes and relationships.</p>
</div>

## Example 3: Querying a Knowledge Graph

This example shows how to query a knowledge graph:

```python
from atlas import ATLASClient

# Initialize client
client = ATLASClient()

# Find nodes by label
renewable_sources = client.find_nodes(
    labels=["RenewableSource"],
    limit=10
)

print(f"Found {len(renewable_sources)} renewable sources:")
for source in renewable_sources:
    print(f"- {source.properties.get('name')}")

# Find nodes by property
solar_nodes = client.find_nodes(
    properties={"name": "Solar PV"}
)

print(f"\nFound {len(solar_nodes)} nodes with name 'Solar PV':")
for node in solar_nodes:
    print(f"- {node.id}: {node.properties.get('definition')}")

# Find relationships by type
is_a_relationships = client.find_relationships(
    relationship_type="IS_A",
    start_node_labels=["EnergyTerm"],
    end_node_labels=["Category"]
)

print(f"\nFound {len(is_a_relationships)} IS_A relationships:")
for rel in is_a_relationships:
    start_node = client.get_node_by_id(rel.start_node_id)
    end_node = client.get_node_by_id(rel.end_node_id)
    print(f"- {start_node.properties.get('name')} IS_A {end_node.properties.get('name')}")

# Find paths between nodes
paths = client.find_paths(
    start_node_properties={"name": "Photovoltaic Cell"},
    end_node_properties={"name": "Renewable Energy"},
    max_depth=3
)

print(f"\nFound {len(paths)} paths from 'Photovoltaic Cell' to 'Renewable Energy':")
for path in paths:
    path_str = " -> ".join([client.get_node_by_id(node_id).properties.get('name') for node_id in path.node_ids])
    print(f"- {path_str}")
```

<div class="result-preview">
    <h3>Result Preview</h3>
    <p>This example demonstrates various ways to query a knowledge graph:</p>
    <ul>
        <li>Finding nodes by label (e.g., RenewableSource)</li>
        <li>Finding nodes by property (e.g., name="Solar PV")</li>
        <li>Finding relationships by type (e.g., IS_A relationships)</li>
        <li>Finding paths between nodes (e.g., from Photovoltaic Cell to Renewable Energy)</li>
    </ul>
    <p>The results show the matching nodes, relationships, and paths.</p>
</div>

## Example 4: Using Agentic LLMs

This example demonstrates how to use agentic LLMs for knowledge extraction:

```python
from atlas import ATLASClient, ExtractionStrategy

# Initialize client
client = ATLASClient()

# Sample text about energy storage
text = """
Energy storage systems are crucial for integrating renewable energy sources into the grid.
Battery storage, including lithium-ion, lead-acid, and flow batteries, stores electricity for later use.
Pumped hydro storage uses excess electricity to pump water uphill, then releases it to generate electricity when needed.
Thermal energy storage stores heat or cold for later use in heating or cooling systems.
"""

# Extract knowledge using agentic LLMs
result = client.extract_from_text(
    text=text,
    domain="energy",
    extraction_strategy=ExtractionStrategy.AGENTIC_LLM,
    extraction_depth="comprehensive"
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

# Visualize the extracted knowledge graph
client.visualize(
    nodes=result.nodes,
    relationships=result.relationships,
    output_path="agentic_extraction.html"
)

print("\nKnowledge graph visualization saved to agentic_extraction.html")
```

<div class="result-preview">
    <h3>Result Preview</h3>
    <p>This example uses agentic LLMs to extract knowledge about energy storage systems:</p>
    <ul>
        <li>Extracted nodes include: Energy Storage, Battery Storage, Lithium-ion Battery, Pumped Hydro Storage, etc.</li>
        <li>Extracted relationships include: Battery Storage IS_A Energy Storage, Lithium-ion Battery IS_A Battery Storage, etc.</li>
    </ul>
    <p>The agentic LLM approach provides more comprehensive and accurate extraction compared to traditional methods.</p>
</div>

## Example 5: Validating a Knowledge Graph

This example shows how to validate a knowledge graph:

```python
from atlas import ATLASClient, ValidationStrategy

# Initialize client
client = ATLASClient()

# Validate nodes
node_validation = client.validate_nodes(
    labels=["EnergyTerm"],
    validation_strategy=ValidationStrategy.AGENTIC_LLM,
    confidence_threshold=0.8
)

print(f"Node validation results:")
print(f"- Validated: {node_validation.validated_count}")
print(f"- Rejected: {node_validation.rejected_count}")
print(f"- Needs review: {node_validation.needs_review_count}")

# Validate relationships
relationship_validation = client.validate_relationships(
    relationship_type="IS_A",
    validation_strategy=ValidationStrategy.AGENTIC_LLM,
    confidence_threshold=0.8
)

print(f"\nRelationship validation results:")
print(f"- Validated: {relationship_validation.validated_count}")
print(f"- Rejected: {relationship_validation.rejected_count}")
print(f"- Needs review: {relationship_validation.needs_review_count}")

# Validate schema
schema_validation = client.validate_schema(
    node_types=["EnergyTerm", "Category"],
    relationship_types=["IS_A", "PART_OF"]
)

print(f"\nSchema validation results:")
print(f"- Valid: {schema_validation.valid}")
print(f"- Violations: {len(schema_validation.violations)}")

# Validate consistency
consistency_validation = client.validate_consistency(
    rules=["no_cycles", "no_orphans", "no_contradictions"]
)

print(f"\nConsistency validation results:")
print(f"- Valid: {consistency_validation.valid}")
print(f"- Inconsistencies: {len(consistency_validation.inconsistencies)}")
```

<div class="result-preview">
    <h3>Result Preview</h3>
    <p>This example demonstrates various validation methods for knowledge graphs:</p>
    <ul>
        <li>Node validation: Validates the accuracy and completeness of nodes</li>
        <li>Relationship validation: Validates the accuracy and completeness of relationships</li>
        <li>Schema validation: Validates that nodes and relationships conform to the schema</li>
        <li>Consistency validation: Validates the logical consistency of the knowledge graph</li>
    </ul>
    <p>The results show the validation status and any issues that need to be addressed.</p>
</div>

## Example 6: Exporting a Knowledge Graph

This example demonstrates how to export a knowledge graph in various formats:

```python
from atlas import ATLASClient

# Initialize client
client = ATLASClient()

# Export to JSON
client.export_to_json(
    output_path="energy_taxonomy.json",
    include_properties=True,
    pretty_print=True
)

print("Knowledge graph exported to energy_taxonomy.json")

# Export to CSV
client.export_to_csv(
    output_directory="energy_taxonomy_csv",
    separate_files=True
)

print("Knowledge graph exported to CSV files in energy_taxonomy_csv directory")

# Export to RDF
client.export_to_rdf(
    output_path="energy_taxonomy.rdf",
    format="turtle"
)

print("Knowledge graph exported to energy_taxonomy.rdf")

# Export to Neo4j Cypher script
client.export_to_cypher(
    output_path="energy_taxonomy.cypher"
)

print("Knowledge graph exported to energy_taxonomy.cypher")
```

<div class="result-preview">
    <h3>Result Preview</h3>
    <p>This example exports a knowledge graph in various formats:</p>
    <ul>
        <li>JSON: A single JSON file with all nodes and relationships</li>
        <li>CSV: Separate CSV files for nodes and relationships</li>
        <li>RDF: Resource Description Framework format (Turtle syntax)</li>
        <li>Cypher: Neo4j Cypher script for importing into Neo4j</li>
    </ul>
    <p>These exports can be used for backup, sharing, or importing into other systems.</p>
</div>

## Example 7: Using FABRIC Patterns

This example shows how to use FABRIC patterns for intelligent behavior:

```python
from atlas import ATLASClient, FabricPattern

# Initialize client
client = ATLASClient()

# Sample text about energy policy
text = """
Renewable Portfolio Standards (RPS) are policies designed to increase the use of renewable energy sources.
These standards require electricity suppliers to produce a specified percentage of their electricity from renewable sources.
As of 2025, 30 states and Washington, D.C. have established RPS policies, with targets ranging from 10% to 100% renewable energy.
Studies show that RPS policies have been effective in increasing renewable energy deployment and reducing greenhouse gas emissions.
"""

# Apply EXTRACT_WISDOM pattern
wisdom_result = client.apply_fabric_pattern(
    pattern=FabricPattern.EXTRACT_WISDOM,
    input_text=text,
    domain="energy_policy"
)

print("Extracted wisdom:")
for item in wisdom_result.wisdom:
    print(f"- {item}")

# Apply FIND_PATTERNS pattern
patterns_result = client.apply_fabric_pattern(
    pattern=FabricPattern.FIND_PATTERNS,
    input_text=text,
    domain="energy_policy"
)

print("\nIdentified patterns:")
for pattern in patterns_result.patterns:
    print(f"- {pattern}")

# Apply CREATE_SUMMARY pattern
summary_result = client.apply_fabric_pattern(
    pattern=FabricPattern.CREATE_SUMMARY,
    input_text=text,
    domain="energy_policy"
)

print("\nSummary:")
print(summary_result.summary)

# Apply pattern sequence
sequence_result = client.apply_fabric_pattern_sequence(
    patterns=[
        FabricPattern.EXTRACT_WISDOM,
        FabricPattern.FIND_PATTERNS,
        FabricPattern.CREATE_SUMMARY
    ],
    input_text=text,
    domain="energy_policy"
)

print("\nSequence result:")
print(f"- Wisdom count: {len(sequence_result.wisdom)}")
print(f"- Patterns count: {len(sequence_result.patterns)}")
print(f"- Summary length: {len(sequence_result.summary)}")
```

<div class="result-preview">
    <h3>Result Preview</h3>
    <p>This example demonstrates using FABRIC patterns for intelligent behavior:</p>
    <ul>
        <li>EXTRACT_WISDOM: Extracts key insights and wisdom from the text</li>
        <li>FIND_PATTERNS: Identifies patterns and trends in the text</li>
        <li>CREATE_SUMMARY: Creates a concise summary of the text</li>
        <li>Pattern sequence: Applies multiple patterns in sequence for comprehensive analysis</li>
    </ul>
    <p>The results show the extracted wisdom, identified patterns, and generated summary.</p>
</div>

## Example 8: Using Configuration

This example demonstrates how to use configuration to customize ATLAS Framework:

```python
from atlas import ATLASClient, ConfigBuilder

# Create configuration builder
config_builder = ConfigBuilder()

# Define node types
config_builder.add_node_type(
    name="energy_term",
    labels=["EnergyTerm", "TaxonomyNode"],
    properties={
        "name": {"type": "string", "required": True},
        "definition": {"type": "string", "required": True},
        "fuel_group": {"type": "string", "required": False, "enum": ["renewable", "fossil", "nuclear", "alternative"]}
    }
)

config_builder.add_node_type(
    name="energy_source",
    labels=["EnergySource", "TaxonomyNode"],
    properties={
        "name": {"type": "string", "required": True},
        "description": {"type": "string", "required": True},
        "renewable": {"type": "boolean", "required": True}
    }
)

# Define relationship types
config_builder.add_relationship_type(
    name="IS_A",
    description="Indicates that one node is a type or subclass of another"
)

config_builder.add_relationship_type(
    name="PART_OF",
    description="Indicates that one node is a part or component of another"
)

# Define global settings
config_builder.set_global_settings(
    default_cache_ttl=300,
    max_behavior_execution_time=60,
    validation_strictness="medium"
)

# Build configuration
config = config_builder.build()

# Save configuration to file
config_path = "atlas_config.json"
config_builder.save(config_path)

print(f"Configuration saved to {config_path}")

# Initialize client with configuration
client = ATLASClient(config_path=config_path)

# Create node using configuration
solar_pv = client.create_node(
    node_type="energy_term",
    properties={
        "name": "Solar PV",
        "definition": "Photovoltaic technology that converts sunlight into electricity",
        "fuel_group": "renewable"
    }
)

print(f"Created node: {solar_pv.properties.get('name')}")
```

<div class="result-preview">
    <h3>Result Preview</h3>
    <p>This example demonstrates how to use configuration to customize ATLAS Framework:</p>
    <ul>
        <li>Creating a configuration with node types, relationship types, and global settings</li>
        <li>Saving the configuration to a file</li>
        <li>Initializing the client with the configuration</li>
        <li>Creating nodes using the configured node types</li>
    </ul>
    <p>The configuration provides a flexible way to define the structure of your knowledge graph.</p>
</div>

## Interactive Examples

Try these interactive examples to see ATLAS Framework in action:

<div class="interactive-example">
    <h3>Interactive Example: Create a Simple Knowledge Graph</h3>
    <p>This example allows you to create a simple knowledge graph with custom nodes and relationships.</p>
    <div class="code-editor" id="example1-editor">
        <pre><code class="python">
from atlas import ATLASClient, RelationshipType

# Initialize client
client = ATLASClient()

# Create nodes
node1 = client.create_node(
    labels=["EnergyTerm"],
    properties={
        "name": "Solar PV",
        "definition": "Photovoltaic technology that converts sunlight into electricity"
    }
)

node2 = client.create_node(
    labels=["EnergyTerm"],
    properties={
        "name": "Renewable Energy",
        "definition": "Energy derived from natural processes that are replenished constantly"
    }
)

# Create relationship
client.create_relationship(
    start_node=node1,
    end_node=node2,
    type=RelationshipType.IS_A
)

# Visualize the knowledge graph
client.visualize(
    nodes=[node1, node2],
    output_path="interactive_example.html"
)
        </code></pre>
    </div>
    <button class="run-button" onclick="runExample('example1')">Run Example</button>
    <div class="example-output" id="example1-output"></div>
</div>

<div class="interactive-example">
    <h3>Interactive Example: Extract Knowledge from Text</h3>
    <p>This example allows you to extract knowledge from custom text.</p>
    <div class="code-editor" id="example2-editor">
        <pre><code class="python">
from atlas import ATLASClient

# Initialize client
client = ATLASClient()

# Sample text (you can modify this)
text = """
Solar photovoltaic (PV) is a technology that converts sunlight directly into electricity.
Solar PV cells are made from silicon and other materials that exhibit the photovoltaic effect.
"""

# Extract knowledge from text
result = client.extract_from_text(
    text=text,
    domain="energy",
    extraction_depth="comprehensive"
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
        </code></pre>
    </div>
    <button class="run-button" onclick="runExample('example2')">Run Example</button>
    <div class="example-output" id="example2-output"></div>
</div>

## Next Steps

Now that you've seen basic usage examples, you can:

- Try the [Energy Taxonomy](energy-taxonomy.md) example for a more comprehensive use case
- Explore [Enterprise Integration](enterprise-integration.md) for advanced usage
- Learn about [Custom Extensions](custom-extensions.md) to extend ATLAS Framework
- Read the [API Reference](../api/core.md) for detailed documentation

