# Interactive Demo

This page provides an interactive demo of ATLAS Framework. You can use this demo to explore the framework's capabilities without writing any code.

## Demo Overview

The interactive demo allows you to:

1. **Create a Knowledge Graph**: Create nodes and relationships
2. **Extract Knowledge**: Extract knowledge from text or URLs
3. **Visualize the Knowledge Graph**: See the knowledge graph in action
4. **Query the Knowledge Graph**: Find nodes and relationships
5. **Export the Knowledge Graph**: Export to various formats

## Getting Started

To use the interactive demo, simply follow the steps below. Each step includes interactive elements that allow you to experiment with ATLAS Framework.

### Step 1: Create a Knowledge Graph

Use the form below to create nodes and relationships in your knowledge graph:

<div class="interactive-form" id="create-node-form">
    <h3>Create Node</h3>
    <form>
        <div class="form-group">
            <label for="node-type">Node Type:</label>
            <select id="node-type">
                <option value="energy_term">Energy Term</option>
                <option value="energy_source">Energy Source</option>
                <option value="energy_technology">Energy Technology</option>
                <option value="energy_policy">Energy Policy</option>
            </select>
        </div>
        <div class="form-group">
            <label for="node-name">Name:</label>
            <input type="text" id="node-name" placeholder="e.g., Solar PV">
        </div>
        <div class="form-group">
            <label for="node-definition">Definition:</label>
            <textarea id="node-definition" placeholder="e.g., Photovoltaic technology that converts sunlight into electricity"></textarea>
        </div>
        <div class="form-group" id="fuel-group-field">
            <label for="fuel-group">Fuel Group:</label>
            <select id="fuel-group">
                <option value="renewable">Renewable</option>
                <option value="fossil">Fossil</option>
                <option value="nuclear">Nuclear</option>
                <option value="alternative">Alternative</option>
            </select>
        </div>
        <button type="button" onclick="createNode()">Create Node</button>
    </form>
</div>

<div class="interactive-form" id="create-relationship-form">
    <h3>Create Relationship</h3>
    <form>
        <div class="form-group">
            <label for="start-node">Start Node:</label>
            <select id="start-node">
                <!-- Options will be populated dynamically -->
            </select>
        </div>
        <div class="form-group">
            <label for="relationship-type">Relationship Type:</label>
            <select id="relationship-type">
                <option value="IS_A">IS_A</option>
                <option value="PART_OF">PART_OF</option>
                <option value="USES">USES</option>
                <option value="PRODUCES">PRODUCES</option>
                <option value="REGULATES">REGULATES</option>
            </select>
        </div>
        <div class="form-group">
            <label for="end-node">End Node:</label>
            <select id="end-node">
                <!-- Options will be populated dynamically -->
            </select>
        </div>
        <button type="button" onclick="createRelationship()">Create Relationship</button>
    </form>
</div>

<div class="demo-output" id="knowledge-graph-output">
    <h3>Knowledge Graph</h3>
    <div id="knowledge-graph-visualization"></div>
    <div id="knowledge-graph-stats">
        <p>Nodes: <span id="node-count">0</span></p>
        <p>Relationships: <span id="relationship-count">0</span></p>
    </div>
</div>

### Step 2: Extract Knowledge

Use the form below to extract knowledge from text or URLs:

<div class="interactive-form" id="extract-knowledge-form">
    <h3>Extract Knowledge</h3>
    <form>
        <div class="form-group">
            <label for="extraction-source">Source Type:</label>
            <select id="extraction-source">
                <option value="text">Text</option>
                <option value="url">URL</option>
            </select>
        </div>
        <div class="form-group" id="text-input-field">
            <label for="text-input">Text:</label>
            <textarea id="text-input" placeholder="Enter text about energy..."></textarea>
        </div>
        <div class="form-group" id="url-input-field" style="display: none;">
            <label for="url-input">URL:</label>
            <input type="text" id="url-input" placeholder="e.g., https://www.eia.gov/tools/glossary/">
        </div>
        <div class="form-group">
            <label for="extraction-depth">Extraction Depth:</label>
            <select id="extraction-depth">
                <option value="basic">Basic</option>
                <option value="comprehensive" selected>Comprehensive</option>
                <option value="expert">Expert</option>
            </select>
        </div>
        <button type="button" onclick="extractKnowledge()">Extract Knowledge</button>
    </form>
</div>

<div class="demo-output" id="extraction-output">
    <h3>Extraction Results</h3>
    <div id="extraction-visualization"></div>
    <div id="extraction-stats">
        <p>Extracted Nodes: <span id="extracted-node-count">0</span></p>
        <p>Extracted Relationships: <span id="extracted-relationship-count">0</span></p>
    </div>
</div>

### Step 3: Visualize the Knowledge Graph

Use the options below to customize the visualization of your knowledge graph:

<div class="interactive-form" id="visualization-options-form">
    <h3>Visualization Options</h3>
    <form>
        <div class="form-group">
            <label for="visualization-layout">Layout:</label>
            <select id="visualization-layout">
                <option value="force">Force-Directed</option>
                <option value="hierarchical">Hierarchical</option>
                <option value="circular">Circular</option>
                <option value="grid">Grid</option>
            </select>
        </div>
        <div class="form-group">
            <label for="node-size">Node Size:</label>
            <input type="range" id="node-size" min="10" max="50" value="30">
        </div>
        <div class="form-group">
            <label for="node-color-scheme">Node Color Scheme:</label>
            <select id="node-color-scheme">
                <option value="category">By Category</option>
                <option value="fuel-group">By Fuel Group</option>
                <option value="centrality">By Centrality</option>
            </select>
        </div>
        <div class="form-group">
            <label for="show-labels">Show Labels:</label>
            <input type="checkbox" id="show-labels" checked>
        </div>
        <button type="button" onclick="updateVisualization()">Update Visualization</button>
    </form>
</div>

<div class="demo-output" id="visualization-output">
    <h3>Knowledge Graph Visualization</h3>
    <div id="full-visualization"></div>
    <button type="button" onclick="downloadVisualization()">Download Visualization</button>
</div>

### Step 4: Query the Knowledge Graph

Use the form below to query your knowledge graph:

<div class="interactive-form" id="query-form">
    <h3>Query Knowledge Graph</h3>
    <form>
        <div class="form-group">
            <label for="query-type">Query Type:</label>
            <select id="query-type">
                <option value="find-nodes">Find Nodes</option>
                <option value="find-relationships">Find Relationships</option>
                <option value="find-paths">Find Paths</option>
                <option value="find-communities">Find Communities</option>
            </select>
        </div>
        <div class="form-group" id="node-query-fields">
            <label for="node-labels">Node Labels:</label>
            <select id="node-labels" multiple>
                <option value="EnergyTerm">Energy Term</option>
                <option value="EnergySource">Energy Source</option>
                <option value="EnergyTechnology">Energy Technology</option>
                <option value="EnergyPolicy">Energy Policy</option>
            </select>
        </div>
        <div class="form-group" id="relationship-query-fields" style="display: none;">
            <label for="relationship-types">Relationship Types:</label>
            <select id="relationship-types" multiple>
                <option value="IS_A">IS_A</option>
                <option value="PART_OF">PART_OF</option>
                <option value="USES">USES</option>
                <option value="PRODUCES">PRODUCES</option>
                <option value="REGULATES">REGULATES</option>
            </select>
        </div>
        <div class="form-group" id="path-query-fields" style="display: none;">
            <label for="start-node-path">Start Node:</label>
            <select id="start-node-path">
                <!-- Options will be populated dynamically -->
            </select>
            <label for="end-node-path">End Node:</label>
            <select id="end-node-path">
                <!-- Options will be populated dynamically -->
            </select>
            <label for="max-depth">Max Depth:</label>
            <input type="number" id="max-depth" min="1" max="10" value="3">
        </div>
        <div class="form-group" id="community-query-fields" style="display: none;">
            <label for="community-algorithm">Algorithm:</label>
            <select id="community-algorithm">
                <option value="louvain">Louvain</option>
                <option value="label-propagation">Label Propagation</option>
                <option value="connected-components">Connected Components</option>
            </select>
            <label for="min-community-size">Min Community Size:</label>
            <input type="number" id="min-community-size" min="2" max="20" value="3">
        </div>
        <button type="button" onclick="executeQuery()">Execute Query</button>
    </form>
</div>

<div class="demo-output" id="query-output">
    <h3>Query Results</h3>
    <div id="query-visualization"></div>
    <div id="query-results">
        <p>Results will appear here...</p>
    </div>
</div>

### Step 5: Export the Knowledge Graph

Use the form below to export your knowledge graph:

<div class="interactive-form" id="export-form">
    <h3>Export Knowledge Graph</h3>
    <form>
        <div class="form-group">
            <label for="export-format">Export Format:</label>
            <select id="export-format">
                <option value="json">JSON</option>
                <option value="csv">CSV</option>
                <option value="rdf">RDF (Turtle)</option>
                <option value="cypher">Neo4j Cypher</option>
                <option value="graphml">GraphML</option>
            </select>
        </div>
        <div class="form-group">
            <label for="include-properties">Include Properties:</label>
            <input type="checkbox" id="include-properties" checked>
        </div>
        <div class="form-group" id="pretty-print-field">
            <label for="pretty-print">Pretty Print:</label>
            <input type="checkbox" id="pretty-print" checked>
        </div>
        <button type="button" onclick="exportKnowledgeGraph()">Export</button>
    </form>
</div>

<div class="demo-output" id="export-output">
    <h3>Export Preview</h3>
    <pre id="export-preview"></pre>
    <button type="button" onclick="downloadExport()">Download Export</button>
</div>

## Sample Data

To get started quickly, you can load sample data into the demo:

<div class="sample-data">
    <h3>Sample Data</h3>
    <button type="button" onclick="loadSampleData('renewable-energy')">Load Renewable Energy Sample</button>
    <button type="button" onclick="loadSampleData('energy-storage')">Load Energy Storage Sample</button>
    <button type="button" onclick="loadSampleData('energy-policy')">Load Energy Policy Sample</button>
    <button type="button" onclick="loadSampleData('complete-taxonomy')">Load Complete Taxonomy Sample</button>
</div>

## Demo Code

The interactive demo is powered by ATLAS Framework. Here's a simplified version of the code that powers this demo:

```javascript
// Initialize ATLAS client
const atlasClient = new ATLASClient();

// Create node
function createNode() {
    const nodeType = document.getElementById('node-type').value;
    const name = document.getElementById('node-name').value;
    const definition = document.getElementById('node-definition').value;
    
    let properties = {
        name: name,
        definition: definition
    };
    
    if (nodeType === 'energy_term') {
        properties.fuel_group = document.getElementById('fuel-group').value;
    }
    
    atlasClient.createNode(nodeType, properties)
        .then(node => {
            updateKnowledgeGraph();
            updateNodeSelects();
        });
}

// Create relationship
function createRelationship() {
    const startNodeId = document.getElementById('start-node').value;
    const endNodeId = document.getElementById('end-node').value;
    const relationshipType = document.getElementById('relationship-type').value;
    
    atlasClient.createRelationship(startNodeId, endNodeId, relationshipType)
        .then(relationship => {
            updateKnowledgeGraph();
        });
}

// Extract knowledge
function extractKnowledge() {
    const sourceType = document.getElementById('extraction-source').value;
    const extractionDepth = document.getElementById('extraction-depth').value;
    
    let extractionPromise;
    
    if (sourceType === 'text') {
        const text = document.getElementById('text-input').value;
        extractionPromise = atlasClient.extractFromText(text, 'energy', extractionDepth);
    } else {
        const url = document.getElementById('url-input').value;
        extractionPromise = atlasClient.extractFromUrl(url, 'energy', extractionDepth);
    }
    
    extractionPromise.then(result => {
        document.getElementById('extracted-node-count').textContent = result.nodes.length;
        document.getElementById('extracted-relationship-count').textContent = result.relationships.length;
        
        visualizeExtraction(result.nodes, result.relationships);
        
        // Option to add extracted knowledge to the main knowledge graph
        if (confirm('Add extracted knowledge to the main knowledge graph?')) {
            atlasClient.addNodes(result.nodes);
            atlasClient.addRelationships(result.relationships);
            updateKnowledgeGraph();
            updateNodeSelects();
        }
    });
}

// Update visualization
function updateVisualization() {
    const layout = document.getElementById('visualization-layout').value;
    const nodeSize = document.getElementById('node-size').value;
    const colorScheme = document.getElementById('node-color-scheme').value;
    const showLabels = document.getElementById('show-labels').checked;
    
    atlasClient.getNodes().then(nodes => {
        atlasClient.getRelationships().then(relationships => {
            visualizeKnowledgeGraph(nodes, relationships, {
                layout: layout,
                nodeSize: nodeSize,
                colorScheme: colorScheme,
                showLabels: showLabels
            });
        });
    });
}

// Execute query
function executeQuery() {
    const queryType = document.getElementById('query-type').value;
    
    let queryPromise;
    
    if (queryType === 'find-nodes') {
        const labels = Array.from(document.getElementById('node-labels').selectedOptions).map(option => option.value);
        queryPromise = atlasClient.findNodes(labels);
    } else if (queryType === 'find-relationships') {
        const types = Array.from(document.getElementById('relationship-types').selectedOptions).map(option => option.value);
        queryPromise = atlasClient.findRelationships(types);
    } else if (queryType === 'find-paths') {
        const startNodeId = document.getElementById('start-node-path').value;
        const endNodeId = document.getElementById('end-node-path').value;
        const maxDepth = document.getElementById('max-depth').value;
        queryPromise = atlasClient.findPaths(startNodeId, endNodeId, maxDepth);
    } else if (queryType === 'find-communities') {
        const algorithm = document.getElementById('community-algorithm').value;
        const minSize = document.getElementById('min-community-size').value;
        queryPromise = atlasClient.findCommunities(algorithm, minSize);
    }
    
    queryPromise.then(results => {
        displayQueryResults(results, queryType);
    });
}

// Export knowledge graph
function exportKnowledgeGraph() {
    const format = document.getElementById('export-format').value;
    const includeProperties = document.getElementById('include-properties').checked;
    const prettyPrint = document.getElementById('pretty-print').checked;
    
    let exportPromise;
    
    if (format === 'json') {
        exportPromise = atlasClient.exportToJson(includeProperties, prettyPrint);
    } else if (format === 'csv') {
        exportPromise = atlasClient.exportToCsv();
    } else if (format === 'rdf') {
        exportPromise = atlasClient.exportToRdf('turtle');
    } else if (format === 'cypher') {
        exportPromise = atlasClient.exportToCypher();
    } else if (format === 'graphml') {
        exportPromise = atlasClient.exportToGraphml();
    }
    
    exportPromise.then(exportData => {
        document.getElementById('export-preview').textContent = exportData;
    });
}

// Load sample data
function loadSampleData(sampleName) {
    atlasClient.loadSampleData(sampleName)
        .then(() => {
            updateKnowledgeGraph();
            updateNodeSelects();
        });
}

// Helper functions
function updateKnowledgeGraph() {
    atlasClient.getNodes().then(nodes => {
        document.getElementById('node-count').textContent = nodes.length;
        
        atlasClient.getRelationships().then(relationships => {
            document.getElementById('relationship-count').textContent = relationships.length;
            
            visualizeKnowledgeGraph(nodes, relationships);
        });
    });
}

function updateNodeSelects() {
    atlasClient.getNodes().then(nodes => {
        const startNodeSelect = document.getElementById('start-node');
        const endNodeSelect = document.getElementById('end-node');
        const startNodePathSelect = document.getElementById('start-node-path');
        const endNodePathSelect = document.getElementById('end-node-path');
        
        // Clear existing options
        startNodeSelect.innerHTML = '';
        endNodeSelect.innerHTML = '';
        startNodePathSelect.innerHTML = '';
        endNodePathSelect.innerHTML = '';
        
        // Add options for each node
        nodes.forEach(node => {
            const option1 = document.createElement('option');
            option1.value = node.id;
            option1.textContent = node.properties.name;
            
            const option2 = document.createElement('option');
            option2.value = node.id;
            option2.textContent = node.properties.name;
            
            const option3 = document.createElement('option');
            option3.value = node.id;
            option3.textContent = node.properties.name;
            
            const option4 = document.createElement('option');
            option4.value = node.id;
            option4.textContent = node.properties.name;
            
            startNodeSelect.appendChild(option1);
            endNodeSelect.appendChild(option2);
            startNodePathSelect.appendChild(option3);
            endNodePathSelect.appendChild(option4);
        });
    });
}

function visualizeKnowledgeGraph(nodes, relationships, options = {}) {
    // Visualization code using D3.js or similar library
    // ...
}

function visualizeExtraction(nodes, relationships) {
    // Visualization code for extraction results
    // ...
}

function displayQueryResults(results, queryType) {
    // Display query results
    // ...
}

// Initialize the demo
document.addEventListener('DOMContentLoaded', () => {
    updateKnowledgeGraph();
    updateNodeSelects();
    
    // Set up event listeners for form changes
    document.getElementById('extraction-source').addEventListener('change', event => {
        if (event.target.value === 'text') {
            document.getElementById('text-input-field').style.display = 'block';
            document.getElementById('url-input-field').style.display = 'none';
        } else {
            document.getElementById('text-input-field').style.display = 'none';
            document.getElementById('url-input-field').style.display = 'block';
        }
    });
    
    document.getElementById('query-type').addEventListener('change', event => {
        document.getElementById('node-query-fields').style.display = 'none';
        document.getElementById('relationship-query-fields').style.display = 'none';
        document.getElementById('path-query-fields').style.display = 'none';
        document.getElementById('community-query-fields').style.display = 'none';
        
        if (event.target.value === 'find-nodes') {
            document.getElementById('node-query-fields').style.display = 'block';
        } else if (event.target.value === 'find-relationships') {
            document.getElementById('relationship-query-fields').style.display = 'block';
        } else if (event.target.value === 'find-paths') {
            document.getElementById('path-query-fields').style.display = 'block';
        } else if (event.target.value === 'find-communities') {
            document.getElementById('community-query-fields').style.display = 'block';
        }
    });
    
    document.getElementById('export-format').addEventListener('change', event => {
        if (event.target.value === 'json') {
            document.getElementById('pretty-print-field').style.display = 'block';
        } else {
            document.getElementById('pretty-print-field').style.display = 'none';
        }
    });
});
```

## Next Steps

After exploring the interactive demo, you can:

- Install ATLAS Framework using the [Installation Guide](../getting-started/installation.md)
- Try the [Quick Start Guide](../getting-started/quick-start.md) to create your own knowledge graph
- Explore the [API Reference](../api/core.md) for detailed documentation
- Check out the [Examples](../examples/basic-usage.md) for more usage scenarios

