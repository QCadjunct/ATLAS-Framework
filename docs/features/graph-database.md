# Graph Database Integration

The ATLAS Framework uses graph databases to store and query knowledge graphs. This page explains how graph databases are integrated into the framework and how they are used to represent taxonomies.

## Graph Database Architecture

The ATLAS Framework uses Neo4j as its primary graph database, but it's designed to be database-agnostic with adapters for different graph database systems.

```mermaid
flowchart TB
    classDef core fill:#e3f2fd,stroke:#1565c0,color:#1565c0,stroke-width:2px
    classDef adapter fill:#e8f5e9,stroke:#2e7d32,color:#2e7d32,stroke-width:2px
    classDef db fill:#fff3e0,stroke:#e65100,color:#e65100,stroke-width:2px
    
    A[ATLAS Core]:::core --> B[Graph Database Adapter]:::core
    
    B --> C[Neo4j Adapter]:::adapter
    B --> D[TigerGraph Adapter]:::adapter
    B --> E[Amazon Neptune Adapter]:::adapter
    B --> F[Custom Adapter]:::adapter
    
    C --> G[Neo4j Database]:::db
    D --> H[TigerGraph Database]:::db
    E --> I[Amazon Neptune]:::db
    F --> J[Custom Graph Database]:::db
    
    class A,B core
    class C,D,E,F adapter
    class G,H,I,J db
```

## Data Model

The ATLAS Framework uses a flexible data model that can represent complex taxonomies and their relationships.

```mermaid
erDiagram
    NODE ||--o{ RELATIONSHIP : has
    NODE {
        string id PK
        string[] labels
        json properties
    }
    RELATIONSHIP {
        string id PK
        string type
        string startNodeId FK
        string endNodeId FK
        json properties
    }
    NODE ||--o{ PROPERTY : has
    PROPERTY {
        string key
        string value
        string dataType
    }
    RELATIONSHIP ||--o{ PROPERTY : has
```

## Node and Relationship Types

The ATLAS Framework defines a set of standard node and relationship types for representing taxonomies.

```mermaid
classDiagram
    class Node {
        +String id
        +String[] labels
        +Map~String,Any~ properties
    }
    
    class Relationship {
        +String id
        +String type
        +String startNodeId
        +String endNodeId
        +Map~String,Any~ properties
    }
    
    class EnergyTerm {
        +String name
        +String definition
        +String fuelGroup
    }
    
    class EnergySource {
        +String name
        +String type
        +Number capacity
    }
    
    class EnergyTechnology {
        +String name
        +String description
        +Number efficiencyRating
    }
    
    Node <|-- EnergyTerm
    Node <|-- EnergySource
    Node <|-- EnergyTechnology
    
    Node "1" -- "0..*" Relationship : participates in
    Relationship "0..*" -- "1" Node : connects to
```

## Query Patterns

The ATLAS Framework provides a set of standard query patterns for interacting with the graph database.

```mermaid
graph TD
    classDef query fill:#e1bee7,stroke:#8e24aa,color:#8e24aa,stroke-width:2px
    
    A[Query Builder] --> B{Query Type}
    
    B -->|Find Node| C[Find By ID]:::query
    B -->|Find Node| D[Find By Label]:::query
    B -->|Find Node| E[Find By Property]:::query
    
    B -->|Find Relationship| F[Find By Type]:::query
    B -->|Find Relationship| G[Find Between Nodes]:::query
    
    B -->|Path Finding| H[Shortest Path]:::query
    B -->|Path Finding| I[All Paths]:::query
    
    B -->|Graph Analytics| J[Community Detection]:::query
    B -->|Graph Analytics| K[Centrality Analysis]:::query
    
    class C,D,E,F,G,H,I,J,K query
```

## Cypher Query Examples

The ATLAS Framework generates Cypher queries for Neo4j based on high-level query specifications.

```mermaid
sequenceDiagram
    participant App as Application
    participant QB as Query Builder
    participant Adapter as Neo4j Adapter
    participant DB as Neo4j Database
    
    App->>QB: Find nodes with label "EnergyTerm"
    QB->>Adapter: Generate Cypher query
    Adapter->>DB: MATCH (n:EnergyTerm) RETURN n
    DB-->>Adapter: Return nodes
    Adapter-->>QB: Parse results
    QB-->>App: Return typed objects
```

## Graph Schema

The ATLAS Framework uses a flexible schema that can be extended for different domains.

```mermaid
classDiagram
    class EnergyTerm {
        +String name
        +String definition
        +String fuelGroup
    }
    
    class RenewableSource {
        +String name
        +String type
        +Number capacity
    }
    
    class FossilFuelSource {
        +String name
        +String type
        +Number carbonIntensity
    }
    
    class EnergyTechnology {
        +String name
        +String description
        +Number efficiencyRating
    }
    
    class IS_A {
        +Number confidence
    }
    
    class PART_OF {
        +Number confidence
    }
    
    class USES {
        +Number confidence
    }
    
    class PRODUCES {
        +Number confidence
    }
    
    EnergyTerm <|-- RenewableSource : IS_A
    EnergyTerm <|-- FossilFuelSource : IS_A
    EnergyTechnology -- RenewableSource : USES
    EnergyTechnology -- FossilFuelSource : USES
    EnergyTechnology -- EnergyTerm : PRODUCES
```

## Graph Visualization

The ATLAS Framework provides tools for visualizing the knowledge graph.

```mermaid
graph TD
    classDef term fill:#bbdefb,stroke:#1976d2,color:#1976d2,stroke-width:2px
    classDef renewable fill:#c8e6c9,stroke:#388e3c,color:#388e3c,stroke-width:2px
    classDef fossil fill:#ffcdd2,stroke:#d32f2f,color:#d32f2f,stroke-width:2px
    classDef tech fill:#e1bee7,stroke:#8e24aa,color:#8e24aa,stroke-width:2px
    
    A[Energy]:::term
    B[Renewable]:::renewable
    C[Fossil Fuels]:::fossil
    D[Solar]:::renewable
    E[Wind]:::renewable
    F[Coal]:::fossil
    G[Natural Gas]:::fossil
    H[Solar Panel]:::tech
    I[Wind Turbine]:::tech
    
    A --> B
    A --> C
    B --> D
    B --> E
    C --> F
    C --> G
    D --> H
    E --> I
    
    class A term
    class B,D,E renewable
    class C,F,G fossil
    class H,I tech
```

## Graph Analytics

The ATLAS Framework provides tools for analyzing the knowledge graph to extract insights.

```mermaid
flowchart LR
    classDef analytics fill:#e1bee7,stroke:#8e24aa,color:#8e24aa,stroke-width:2px
    
    A[Knowledge Graph] --> B{Analytics}
    
    B -->|Community Detection| C[Communities]:::analytics
    B -->|Centrality Analysis| D[Central Nodes]:::analytics
    B -->|Path Analysis| E[Paths]:::analytics
    B -->|Similarity Analysis| F[Similar Nodes]:::analytics
    
    C --> G[Domain Clusters]
    D --> H[Key Concepts]
    E --> I[Concept Relationships]
    F --> J[Related Concepts]
    
    class C,D,E,F analytics
```

## Graph Database Performance

The ATLAS Framework is designed to handle large knowledge graphs efficiently.

```mermaid
xychart-beta
    title "Graph Database Performance"
    x-axis "Nodes (thousands)" [10, 50, 100, 500, 1000]
    y-axis "Query Time (ms)" [0, 50, 100, 150, 200, 250]
    line [15, 35, 60, 120, 220]
```

## Graph Database Deployment

The ATLAS Framework supports different deployment options for the graph database.

```mermaid
flowchart TB
    classDef local fill:#bbdefb,stroke:#1976d2,color:#1976d2,stroke-width:2px
    classDef cloud fill:#e1bee7,stroke:#8e24aa,color:#8e24aa,stroke-width:2px
    
    A[ATLAS Framework] --> B{Deployment}
    
    B -->|Local| C[Docker Container]:::local
    B -->|Local| D[Native Installation]:::local
    
    B -->|Cloud| E[AWS Neptune]:::cloud
    B -->|Cloud| F[Neo4j Aura]:::cloud
    B -->|Cloud| G[Azure Cosmos DB]:::cloud
    
    class C,D local
    class E,F,G cloud
```

## Data Import/Export

The ATLAS Framework provides tools for importing and exporting data from the graph database.

```mermaid
flowchart LR
    classDef import fill:#c8e6c9,stroke:#388e3c,color:#388e3c,stroke-width:2px
    classDef export fill:#ffcdd2,stroke:#d32f2f,color:#d32f2f,stroke-width:2px
    
    A[Graph Database] --> B{Import/Export}
    
    B -->|Import| C[CSV Import]:::import
    B -->|Import| D[JSON Import]:::import
    B -->|Import| E[RDF Import]:::import
    
    B -->|Export| F[CSV Export]:::export
    B -->|Export| G[JSON Export]:::export
    B -->|Export| H[RDF Export]:::export
    B -->|Export| I[GraphML Export]:::export
    
    class C,D,E import
    class F,G,H,I export
```

These diagrams provide a comprehensive view of how graph databases are integrated into the ATLAS Framework for storing and querying knowledge graphs.

