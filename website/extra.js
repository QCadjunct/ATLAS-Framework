// ATLAS Framework Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
  // Initialize interactive demo if on the demo page
  if (document.querySelector('.interactive-form')) {
    initializeDemo();
  }
  
  // Add smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href').substring(1);
      const targetElement = document.getElementById(targetId);
      
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 100,
          behavior: 'smooth'
        });
      }
    });
  });
  
  // Add copy button to code blocks
  document.querySelectorAll('pre > code').forEach(codeBlock => {
    const button = document.createElement('button');
    button.className = 'md-clipboard';
    button.title = 'Copy to clipboard';
    button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"></path></svg>';
    
    const pre = codeBlock.parentNode;
    pre.style.position = 'relative';
    pre.insertBefore(button, codeBlock);
    
    button.addEventListener('click', () => {
      const textToCopy = codeBlock.textContent;
      navigator.clipboard.writeText(textToCopy).then(() => {
        button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"></path></svg>';
        setTimeout(() => {
          button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z"></path></svg>';
        }, 2000);
      });
    });
  });
  
  // Add version selector if available
  const versionSelector = document.getElementById('version-selector');
  if (versionSelector) {
    versionSelector.addEventListener('change', function() {
      window.location.href = this.value;
    });
  }
});

// Interactive demo functionality
function initializeDemo() {
  // Mock ATLAS client for demo purposes
  window.ATLASClient = class {
    constructor() {
      this.nodes = [];
      this.relationships = [];
      this.nextNodeId = 1;
      this.nextRelationshipId = 1;
    }
    
    createNode(nodeType, properties) {
      const node = {
        id: this.nextNodeId++,
        type: nodeType,
        properties: properties,
        labels: this._getLabelsForNodeType(nodeType)
      };
      
      this.nodes.push(node);
      return Promise.resolve(node);
    }
    
    createRelationship(startNodeId, endNodeId, relationshipType) {
      const relationship = {
        id: this.nextRelationshipId++,
        type: relationshipType,
        startNodeId: parseInt(startNodeId),
        endNodeId: parseInt(endNodeId),
        properties: {}
      };
      
      this.relationships.push(relationship);
      return Promise.resolve(relationship);
    }
    
    getNodes() {
      return Promise.resolve(this.nodes);
    }
    
    getRelationships() {
      return Promise.resolve(this.relationships);
    }
    
    extractFromText(text, domain, depth) {
      // Simulate extraction process
      return new Promise(resolve => {
        setTimeout(() => {
          const extractedNodes = [];
          const extractedRelationships = [];
          
          // Generate some mock nodes based on text
          const keywords = this._extractKeywords(text);
          
          keywords.forEach((keyword, index) => {
            extractedNodes.push({
              id: this.nextNodeId + index,
              type: 'energy_term',
              properties: {
                name: keyword,
                definition: `Definition for ${keyword}`,
                confidence: Math.random().toFixed(2)
              },
              labels: ['EnergyTerm']
            });
            
            // Create some relationships between nodes
            if (index > 0) {
              extractedRelationships.push({
                id: this.nextRelationshipId + index - 1,
                type: this._getRandomRelationshipType(),
                startNodeId: this.nextNodeId + index - 1,
                endNodeId: this.nextNodeId + index,
                properties: {
                  confidence: Math.random().toFixed(2)
                }
              });
            }
          });
          
          resolve({
            nodes: extractedNodes,
            relationships: extractedRelationships
          });
        }, 1500);
      });
    }
    
    extractFromUrl(url, domain, depth) {
      // Similar to extractFromText but simulates URL extraction
      return new Promise(resolve => {
        setTimeout(() => {
          const extractedNodes = [];
          const extractedRelationships = [];
          
          // Generate some mock nodes based on URL
          const urlParts = url.split('/');
          const domainName = urlParts[2] || 'example.com';
          
          // Create 5-10 random nodes
          const nodeCount = 5 + Math.floor(Math.random() * 6);
          
          for (let i = 0; i < nodeCount; i++) {
            extractedNodes.push({
              id: this.nextNodeId + i,
              type: 'energy_term',
              properties: {
                name: `Term ${i + 1} from ${domainName}`,
                definition: `Definition extracted from ${url}`,
                source: url,
                confidence: Math.random().toFixed(2)
              },
              labels: ['EnergyTerm']
            });
            
            // Create some relationships between nodes
            if (i > 0) {
              extractedRelationships.push({
                id: this.nextRelationshipId + i - 1,
                type: this._getRandomRelationshipType(),
                startNodeId: this.nextNodeId + i - 1,
                endNodeId: this.nextNodeId + i,
                properties: {
                  confidence: Math.random().toFixed(2)
                }
              });
            }
          }
          
          resolve({
            nodes: extractedNodes,
            relationships: extractedRelationships
          });
        }, 2000);
      });
    }
    
    addNodes(nodes) {
      this.nextNodeId += nodes.length;
      this.nodes = this.nodes.concat(nodes);
      return Promise.resolve(true);
    }
    
    addRelationships(relationships) {
      this.nextRelationshipId += relationships.length;
      this.relationships = this.relationships.concat(relationships);
      return Promise.resolve(true);
    }
    
    findNodes(labels) {
      const matchingNodes = this.nodes.filter(node => {
        return labels.some(label => node.labels.includes(label));
      });
      
      return Promise.resolve(matchingNodes);
    }
    
    findRelationships(types) {
      const matchingRelationships = this.relationships.filter(rel => {
        return types.includes(rel.type);
      });
      
      return Promise.resolve(matchingRelationships);
    }
    
    findPaths(startNodeId, endNodeId, maxDepth) {
      // Simplified path finding for demo
      return Promise.resolve({
        paths: [{
          nodes: [
            this.nodes.find(n => n.id === parseInt(startNodeId)),
            this.nodes.find(n => n.id === parseInt(endNodeId))
          ],
          relationships: []
        }]
      });
    }
    
    findCommunities(algorithm, minSize) {
      // Mock community detection
      return Promise.resolve({
        communities: [
          { id: 1, nodes: this.nodes.slice(0, Math.min(3, this.nodes.length)) },
          { id: 2, nodes: this.nodes.slice(Math.min(3, this.nodes.length)) }
        ]
      });
    }
    
    exportToJson(includeProperties, prettyPrint) {
      const exportData = {
        nodes: includeProperties ? this.nodes : this.nodes.map(n => ({ id: n.id, type: n.type, labels: n.labels })),
        relationships: includeProperties ? this.relationships : this.relationships.map(r => ({ id: r.id, type: r.type, startNodeId: r.startNodeId, endNodeId: r.endNodeId }))
      };
      
      return Promise.resolve(prettyPrint ? JSON.stringify(exportData, null, 2) : JSON.stringify(exportData));
    }
    
    exportToCsv() {
      let csv = 'id,type,name,definition\n';
      
      this.nodes.forEach(node => {
        csv += `${node.id},${node.type},"${node.properties.name || ''}","${node.properties.definition || ''}"\n`;
      });
      
      return Promise.resolve(csv);
    }
    
    exportToRdf() {
      let rdf = '@prefix atlas: <http://atlas-framework.org/ontology/> .\n';
      rdf += '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\n';
      
      this.nodes.forEach(node => {
        rdf += `atlas:node${node.id} rdf:type atlas:${node.type} ;\n`;
        rdf += `  atlas:name "${node.properties.name || ''}" ;\n`;
        rdf += `  atlas:definition "${node.properties.definition || ''}" .\n\n`;
      });
      
      return Promise.resolve(rdf);
    }
    
    exportToCypher() {
      let cypher = '// Create nodes\n';
      
      this.nodes.forEach(node => {
        const labels = node.labels.map(l => `:${l}`).join('');
        const props = JSON.stringify(node.properties).replace(/"([^"]+)":/g, '$1:');
        cypher += `CREATE (n${node.id}${labels} ${props});\n`;
      });
      
      cypher += '\n// Create relationships\n';
      
      this.relationships.forEach(rel => {
        cypher += `CREATE (n${rel.startNodeId})-[:${rel.type}]->(n${rel.endNodeId});\n`;
      });
      
      return Promise.resolve(cypher);
    }
    
    exportToGraphml() {
      let graphml = '<?xml version="1.0" encoding="UTF-8"?>\n';
      graphml += '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">\n';
      graphml += '  <graph id="G" edgedefault="directed">\n';
      
      this.nodes.forEach(node => {
        graphml += `    <node id="n${node.id}">\n`;
        graphml += `      <data key="type">${node.type}</data>\n`;
        graphml += `      <data key="name">${node.properties.name || ''}</data>\n`;
        graphml += '    </node>\n';
      });
      
      this.relationships.forEach(rel => {
        graphml += `    <edge id="e${rel.id}" source="n${rel.startNodeId}" target="n${rel.endNodeId}">\n`;
        graphml += `      <data key="type">${rel.type}</data>\n`;
        graphml += '    </edge>\n';
      });
      
      graphml += '  </graph>\n';
      graphml += '</graphml>';
      
      return Promise.resolve(graphml);
    }
    
    loadSampleData(sampleName) {
      // Clear existing data
      this.nodes = [];
      this.relationships = [];
      this.nextNodeId = 1;
      this.nextRelationshipId = 1;
      
      if (sampleName === 'renewable-energy') {
        // Load renewable energy sample
        return this._loadRenewableEnergySample();
      } else if (sampleName === 'energy-storage') {
        // Load energy storage sample
        return this._loadEnergyStorageSample();
      } else if (sampleName === 'energy-policy') {
        // Load energy policy sample
        return this._loadEnergyPolicySample();
      } else if (sampleName === 'complete-taxonomy') {
        // Load complete taxonomy sample
        return this._loadCompleteTaxonomySample();
      }
      
      return Promise.resolve(false);
    }
    
    // Helper methods
    _getLabelsForNodeType(nodeType) {
      const labelMap = {
        'energy_term': ['EnergyTerm'],
        'energy_source': ['EnergySource'],
        'energy_technology': ['EnergyTechnology'],
        'energy_policy': ['EnergyPolicy']
      };
      
      return labelMap[nodeType] || ['Node'];
    }
    
    _getRandomRelationshipType() {
      const types = ['IS_A', 'PART_OF', 'USES', 'PRODUCES', 'REGULATES'];
      return types[Math.floor(Math.random() * types.length)];
    }
    
    _extractKeywords(text) {
      // Very simple keyword extraction for demo
      const words = text.split(/\s+/);
      const uniqueWords = [...new Set(words)];
      
      // Take up to 5 words with length > 3
      return uniqueWords
        .filter(word => word.length > 3)
        .slice(0, 5);
    }
    
    _loadRenewableEnergySample() {
      // Create nodes
      const solarNode = {
        id: 1,
        type: 'energy_source',
        properties: {
          name: 'Solar Energy',
          definition: 'Energy derived from the sun\'s radiation'
        },
        labels: ['EnergySource', 'RenewableSource']
      };
      
      const windNode = {
        id: 2,
        type: 'energy_source',
        properties: {
          name: 'Wind Energy',
          definition: 'Energy derived from wind'
        },
        labels: ['EnergySource', 'RenewableSource']
      };
      
      const renewableNode = {
        id: 3,
        type: 'energy_term',
        properties: {
          name: 'Renewable',
          definition: 'Energy from sources that are naturally replenished'
        },
        labels: ['EnergyTerm']
      };
      
      const solarPanelNode = {
        id: 4,
        type: 'energy_technology',
        properties: {
          name: 'Solar Panel',
          definition: 'Device that converts sunlight into electricity'
        },
        labels: ['EnergyTechnology']
      };
      
      const windTurbineNode = {
        id: 5,
        type: 'energy_technology',
        properties: {
          name: 'Wind Turbine',
          definition: 'Device that converts wind energy into electricity'
        },
        labels: ['EnergyTechnology']
      };
      
      // Create relationships
      const rel1 = {
        id: 1,
        type: 'IS_A',
        startNodeId: 1,
        endNodeId: 3,
        properties: {}
      };
      
      const rel2 = {
        id: 2,
        type: 'IS_A',
        startNodeId: 2,
        endNodeId: 3,
        properties: {}
      };
      
      const rel3 = {
        id: 3,
        type: 'USES',
        startNodeId: 4,
        endNodeId: 1,
        properties: {}
      };
      
      const rel4 = {
        id: 4,
        type: 'USES',
        startNodeId: 5,
        endNodeId: 2,
        properties: {}
      };
      
      this.nodes = [solarNode, windNode, renewableNode, solarPanelNode, windTurbineNode];
      this.relationships = [rel1, rel2, rel3, rel4];
      this.nextNodeId = 6;
      this.nextRelationshipId = 5;
      
      return Promise.resolve(true);
    }
    
    _loadEnergyStorageSample() {
      // Create nodes
      const storageNode = {
        id: 1,
        type: 'energy_term',
        properties: {
          name: 'Energy Storage',
          definition: 'Technologies that store energy for later use'
        },
        labels: ['EnergyTerm']
      };
      
      const batteryNode = {
        id: 2,
        type: 'energy_technology',
        properties: {
          name: 'Battery Storage',
          definition: 'Chemical storage of electrical energy'
        },
        labels: ['EnergyTechnology', 'StorageTechnology']
      };
      
      const pumpedHydroNode = {
        id: 3,
        type: 'energy_technology',
        properties: {
          name: 'Pumped Hydro Storage',
          definition: 'Storage of energy by pumping water to a higher elevation'
        },
        labels: ['EnergyTechnology', 'StorageTechnology']
      };
      
      const lithiumIonNode = {
        id: 4,
        type: 'energy_technology',
        properties: {
          name: 'Lithium-Ion Battery',
          definition: 'Rechargeable battery using lithium ions'
        },
        labels: ['EnergyTechnology', 'BatteryTechnology']
      };
      
      const gridStabilityNode = {
        id: 5,
        type: 'energy_term',
        properties: {
          name: 'Grid Stability',
          definition: 'Maintaining reliable electrical grid operation'
        },
        labels: ['EnergyTerm']
      };
      
      // Create relationships
      const rel1 = {
        id: 1,
        type: 'IS_A',
        startNodeId: 2,
        endNodeId: 1,
        properties: {}
      };
      
      const rel2 = {
        id: 2,
        type: 'IS_A',
        startNodeId: 3,
        endNodeId: 1,
        properties: {}
      };
      
      const rel3 = {
        id: 3,
        type: 'IS_A',
        startNodeId: 4,
        endNodeId: 2,
        properties: {}
      };
      
      const rel4 = {
        id: 4,
        type: 'CONTRIBUTES_TO',
        startNodeId: 1,
        endNodeId: 5,
        properties: {}
      };
      
      this.nodes = [storageNode, batteryNode, pumpedHydroNode, lithiumIonNode, gridStabilityNode];
      this.relationships = [rel1, rel2, rel3, rel4];
      this.nextNodeId = 6;
      this.nextRelationshipId = 5;
      
      return Promise.resolve(true);
    }
    
    _loadEnergyPolicySample() {
      // Create nodes
      const policyNode = {
        id: 1,
        type: 'energy_policy',
        properties: {
          name: 'Energy Policy',
          definition: 'Government actions that affect energy production and consumption'
        },
        labels: ['EnergyPolicy']
      };
      
      const carbonTaxNode = {
        id: 2,
        type: 'energy_policy',
        properties: {
          name: 'Carbon Tax',
          definition: 'Tax on carbon dioxide emissions'
        },
        labels: ['EnergyPolicy', 'TaxPolicy']
      };
      
      const renewableSubsidyNode = {
        id: 3,
        type: 'energy_policy',
        properties: {
          name: 'Renewable Energy Subsidy',
          definition: 'Financial support for renewable energy development'
        },
        labels: ['EnergyPolicy', 'SubsidyPolicy']
      };
      
      const emissionsNode = {
        id: 4,
        type: 'energy_term',
        properties: {
          name: 'Greenhouse Gas Emissions',
          definition: 'Release of gases that trap heat in the atmosphere'
        },
        labels: ['EnergyTerm', 'EnvironmentalTerm']
      };
      
      const renewableNode = {
        id: 5,
        type: 'energy_term',
        properties: {
          name: 'Renewable Energy',
          definition: 'Energy from sources that are naturally replenished'
        },
        labels: ['EnergyTerm']
      };
      
      // Create relationships
      const rel1 = {
        id: 1,
        type: 'IS_A',
        startNodeId: 2,
        endNodeId: 1,
        properties: {}
      };
      
      const rel2 = {
        id: 2,
        type: 'IS_A',
        startNodeId: 3,
        endNodeId: 1,
        properties: {}
      };
      
      const rel3 = {
        id: 3,
        type: 'REGULATES',
        startNodeId: 2,
        endNodeId: 4,
        properties: {}
      };
      
      const rel4 = {
        id: 4,
        type: 'PROMOTES',
        startNodeId: 3,
        endNodeId: 5,
        properties: {}
      };
      
      this.nodes = [policyNode, carbonTaxNode, renewableSubsidyNode, emissionsNode, renewableNode];
      this.relationships = [rel1, rel2, rel3, rel4];
      this.nextNodeId = 6;
      this.nextRelationshipId = 5;
      
      return Promise.resolve(true);
    }
    
    _loadCompleteTaxonomySample() {
      // This would load a more comprehensive sample
      // For demo purposes, we'll combine the previous samples
      return this._loadRenewableEnergySample()
        .then(() => {
          const offset = this.nextNodeId - 1;
          
          return this._loadEnergyStorageSample()
            .then(() => {
              // Adjust IDs for the second sample
              this.nodes.slice(5).forEach(node => {
                node.id += offset;
              });
              
              this.relationships.slice(4).forEach(rel => {
                rel.id += offset;
                rel.startNodeId += offset;
                rel.endNodeId += offset;
              });
              
              return this._loadEnergyPolicySample();
            })
            .then(() => {
              // Adjust IDs for the third sample
              const offset2 = offset + 5;
              
              this.nodes.slice(10).forEach(node => {
                node.id += offset2;
              });
              
              this.relationships.slice(8).forEach(rel => {
                rel.id += offset2;
                rel.startNodeId += offset2;
                rel.endNodeId += offset2;
              });
              
              // Add some cross-sample relationships
              const rel1 = {
                id: this.nextRelationshipId++,
                type: 'SUPPORTS',
                startNodeId: 6, // Energy Storage
                endNodeId: 3, // Renewable
                properties: {}
              };
              
              const rel2 = {
                id: this.nextRelationshipId++,
                type: 'PROMOTES',
                startNodeId: 13, // Renewable Energy Subsidy
                endNodeId: 3, // Renewable
                properties: {}
              };
              
              this.relationships.push(rel1, rel2);
              
              return Promise.resolve(true);
            });
        });
    }
  };
  
  // Initialize the client
  const atlasClient = new ATLASClient();
  
  // Set up event handlers for the demo
  window.createNode = function() {
    const nodeType = document.getElementById('node-type').value;
    const name = document.getElementById('node-name').value;
    const definition = document.getElementById('node-definition').value;
    
    if (!name) {
      alert('Please enter a name for the node');
      return;
    }
    
    let properties = {
      name: name,
      definition: definition
    };
    
    if (nodeType === 'energy_term') {
      properties.fuel_group = document.getElementById('fuel-group').value;
    }
    
    atlasClient.createNode(nodeType, properties)
      .then(() => {
        document.getElementById('node-name').value = '';
        document.getElementById('node-definition').value = '';
        updateKnowledgeGraph();
        updateNodeSelects();
      });
  };
  
  window.createRelationship = function() {
    const startNodeId = document.getElementById('start-node').value;
    const endNodeId = document.getElementById('end-node').value;
    const relationshipType = document.getElementById('relationship-type').value;
    
    if (startNodeId === endNodeId) {
      alert('Start and end nodes must be different');
      return;
    }
    
    atlasClient.createRelationship(startNodeId, endNodeId, relationshipType)
      .then(() => {
        updateKnowledgeGraph();
      });
  };
  
  window.extractKnowledge = function() {
    const sourceType = document.getElementById('extraction-source').value;
    const extractionDepth = document.getElementById('extraction-depth').value;
    
    let extractionPromise;
    
    if (sourceType === 'text') {
      const text = document.getElementById('text-input').value;
      if (!text) {
        alert('Please enter text to extract from');
        return;
      }
      extractionPromise = atlasClient.extractFromText(text, 'energy', extractionDepth);
    } else {
      const url = document.getElementById('url-input').value;
      if (!url) {
        alert('Please enter a URL to extract from');
        return;
      }
      extractionPromise = atlasClient.extractFromUrl(url, 'energy', extractionDepth);
    }
    
    // Show loading indicator
    document.getElementById('extraction-visualization').innerHTML = 'Extracting knowledge...';
    
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
  };
  
  window.updateVisualization = function() {
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
  };
  
  window.executeQuery = function() {
    const queryType = document.getElementById('query-type').value;
    
    let queryPromise;
    
    if (queryType === 'find-nodes') {
      const labels = Array.from(document.getElementById('node-labels').selectedOptions).map(option => option.value);
      if (labels.length === 0) {
        alert('Please select at least one node label');
        return;
      }
      queryPromise = atlasClient.findNodes(labels);
    } else if (queryType === 'find-relationships') {
      const types = Array.from(document.getElementById('relationship-types').selectedOptions).map(option => option.value);
      if (types.length === 0) {
        alert('Please select at least one relationship type');
        return;
      }
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
    
    // Show loading indicator
    document.getElementById('query-results').innerHTML = 'Executing query...';
    
    queryPromise.then(results => {
      displayQueryResults(results, queryType);
    });
  };
  
  window.exportKnowledgeGraph = function() {
    const format = document.getElementById('export-format').value;
    const includeProperties = document.getElementById('include-properties').checked;
    const prettyPrint = document.getElementById('pretty-print').checked;
    
    let exportPromise;
    
    if (format === 'json') {
      exportPromise = atlasClient.exportToJson(includeProperties, prettyPrint);
    } else if (format === 'csv') {
      exportPromise = atlasClient.exportToCsv();
    } else if (format === 'rdf') {
      exportPromise = atlasClient.exportToRdf();
    } else if (format === 'cypher') {
      exportPromise = atlasClient.exportToCypher();
    } else if (format === 'graphml') {
      exportPromise = atlasClient.exportToGraphml();
    }
    
    exportPromise.then(exportData => {
      document.getElementById('export-preview').textContent = exportData;
    });
  };
  
  window.downloadExport = function() {
    const format = document.getElementById('export-format').value;
    const exportData = document.getElementById('export-preview').textContent;
    
    if (!exportData) {
      alert('No export data available');
      return;
    }
    
    const blob = new Blob([exportData], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `atlas_knowledge_graph.${format}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };
  
  window.loadSampleData = function(sampleName) {
    atlasClient.loadSampleData(sampleName)
      .then(() => {
        updateKnowledgeGraph();
        updateNodeSelects();
      });
  };
  
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
      
      if (!startNodeSelect || !endNodeSelect) return;
      
      // Clear existing options
      startNodeSelect.innerHTML = '';
      endNodeSelect.innerHTML = '';
      
      if (startNodePathSelect) startNodePathSelect.innerHTML = '';
      if (endNodePathSelect) endNodePathSelect.innerHTML = '';
      
      // Add options for each node
      nodes.forEach(node => {
        const option1 = document.createElement('option');
        option1.value = node.id;
        option1.textContent = node.properties.name || `Node ${node.id}`;
        
        const option2 = document.createElement('option');
        option2.value = node.id;
        option2.textContent = node.properties.name || `Node ${node.id}`;
        
        startNodeSelect.appendChild(option1);
        endNodeSelect.appendChild(option2);
        
        if (startNodePathSelect && endNodePathSelect) {
          const option3 = document.createElement('option');
          option3.value = node.id;
          option3.textContent = node.properties.name || `Node ${node.id}`;
          
          const option4 = document.createElement('option');
          option4.value = node.id;
          option4.textContent = node.properties.name || `Node ${node.id}`;
          
          startNodePathSelect.appendChild(option3);
          endNodePathSelect.appendChild(option4);
        }
      });
    });
  }
  
  function visualizeKnowledgeGraph(nodes, relationships, options = {}) {
    const container = document.getElementById('knowledge-graph-visualization');
    if (!container) return;
    
    if (nodes.length === 0) {
      container.innerHTML = 'No nodes in the knowledge graph yet. Create some nodes or load a sample.';
      return;
    }
    
    container.innerHTML = `
      <div style="text-align: center; padding: 20px;">
        <div style="font-weight: bold; margin-bottom: 10px;">Knowledge Graph Visualization</div>
        <div style="color: #666;">
          ${nodes.length} nodes and ${relationships.length} relationships
        </div>
        <div style="margin-top: 20px; font-style: italic; color: #666;">
          (In a real implementation, this would be an interactive visualization)
        </div>
      </div>
    `;
  }
  
  function visualizeExtraction(nodes, relationships) {
    const container = document.getElementById('extraction-visualization');
    if (!container) return;
    
    if (nodes.length === 0) {
      container.innerHTML = 'No nodes extracted. Try a different text or URL.';
      return;
    }
    
    container.innerHTML = `
      <div style="text-align: center; padding: 20px;">
        <div style="font-weight: bold; margin-bottom: 10px;">Extraction Results</div>
        <div style="color: #666;">
          ${nodes.length} nodes and ${relationships.length} relationships extracted
        </div>
        <div style="margin-top: 20px; font-style: italic; color: #666;">
          (In a real implementation, this would be an interactive visualization)
        </div>
      </div>
    `;
  }
  
  function displayQueryResults(results, queryType) {
    const container = document.getElementById('query-results');
    if (!container) return;
    
    const visualization = document.getElementById('query-visualization');
    
    if (queryType === 'find-nodes') {
      if (results.length === 0) {
        container.innerHTML = 'No nodes found matching the selected labels.';
        visualization.innerHTML = '';
        return;
      }
      
      let html = '<h4>Matching Nodes</h4>';
      html += '<table>';
      html += '<tr><th>ID</th><th>Name</th><th>Type</th><th>Labels</th></tr>';
      
      results.forEach(node => {
        html += `<tr>
          <td>${node.id}</td>
          <td>${node.properties.name || ''}</td>
          <td>${node.type}</td>
          <td>${node.labels.join(', ')}</td>
        </tr>`;
      });
      
      html += '</table>';
      container.innerHTML = html;
      
      visualization.innerHTML = `
        <div style="text-align: center; padding: 20px;">
          <div style="font-weight: bold; margin-bottom: 10px;">Query Results Visualization</div>
          <div style="color: #666;">
            ${results.length} nodes found
          </div>
          <div style="margin-top: 20px; font-style: italic; color: #666;">
            (In a real implementation, this would be an interactive visualization)
          </div>
        </div>
      `;
    } else if (queryType === 'find-relationships') {
      if (results.length === 0) {
        container.innerHTML = 'No relationships found matching the selected types.';
        visualization.innerHTML = '';
        return;
      }
      
      let html = '<h4>Matching Relationships</h4>';
      html += '<table>';
      html += '<tr><th>ID</th><th>Type</th><th>Start Node</th><th>End Node</th></tr>';
      
      results.forEach(rel => {
        html += `<tr>
          <td>${rel.id}</td>
          <td>${rel.type}</td>
          <td>${rel.startNodeId}</td>
          <td>${rel.endNodeId}</td>
        </tr>`;
      });
      
      html += '</table>';
      container.innerHTML = html;
      
      visualization.innerHTML = `
        <div style="text-align: center; padding: 20px;">
          <div style="font-weight: bold; margin-bottom: 10px;">Query Results Visualization</div>
          <div style="color: #666;">
            ${results.length} relationships found
          </div>
          <div style="margin-top: 20px; font-style: italic; color: #666;">
            (In a real implementation, this would be an interactive visualization)
          </div>
        </div>
      `;
    } else if (queryType === 'find-paths') {
      if (!results.paths || results.paths.length === 0) {
        container.innerHTML = 'No paths found between the selected nodes.';
        visualization.innerHTML = '';
        return;
      }
      
      let html = '<h4>Paths Found</h4>';
      
      results.paths.forEach((path, index) => {
        html += `<div><strong>Path ${index + 1}</strong>: `;
        
        path.nodes.forEach((node, i) => {
          if (i > 0) {
            html += ' → ';
          }
          html += node.properties.name || `Node ${node.id}`;
        });
        
        html += '</div>';
      });
      
      container.innerHTML = html;
      
      visualization.innerHTML = `
        <div style="text-align: center; padding: 20px;">
          <div style="font-weight: bold; margin-bottom: 10px;">Path Visualization</div>
          <div style="color: #666;">
            ${results.paths.length} paths found
          </div>
          <div style="margin-top: 20px; font-style: italic; color: #666;">
            (In a real implementation, this would be an interactive visualization)
          </div>
        </div>
      `;
    } else if (queryType === 'find-communities') {
      if (!results.communities || results.communities.length === 0) {
        container.innerHTML = 'No communities found in the knowledge graph.';
        visualization.innerHTML = '';
        return;
      }
      
      let html = '<h4>Communities Found</h4>';
      
      results.communities.forEach((community, index) => {
        html += `<div><strong>Community ${index + 1}</strong> (${community.nodes.length} nodes): `;
        
        community.nodes.forEach((node, i) => {
          if (i > 0) {
            html += ', ';
          }
          html += node.properties.name || `Node ${node.id}`;
        });
        
        html += '</div>';
      });
      
      container.innerHTML = html;
      
      visualization.innerHTML = `
        <div style="text-align: center; padding: 20px;">
          <div style="font-weight: bold; margin-bottom: 10px;">Community Visualization</div>
          <div style="color: #666;">
            ${results.communities.length} communities found
          </div>
          <div style="margin-top: 20px; font-style: italic; color: #666;">
            (In a real implementation, this would be an interactive visualization)
          </div>
        </div>
      `;
    }
  }
  
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
  
  // Initialize the demo
  updateKnowledgeGraph();
  updateNodeSelects();
}

