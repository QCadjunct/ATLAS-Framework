# Mermaid.js Examples

This page demonstrates the various types of diagrams you can create with Mermaid.js in the ATLAS Framework documentation.

## Flowchart

```mermaid
graph TD
    A[Client] --> B[Load Balancer]
    B --> C[Server01]
    B --> D[Server02]
```

## ATLAS Framework Architecture

```mermaid
graph TB
    subgraph "Data Layer"
        A[Data Sources] --> B[Extraction Engine]
        B --> C[Data Processing]
        C --> D[Knowledge Graph]
    end
    
    subgraph "Framework Layer"
        E[LangChain] --- F[LangGraph]
        F --- G[LangSmith]
        G --- H[Tavily]
    end
    
    subgraph "Intelligence Layer"
        I[FABRIC Patterns] --> J[Orchestration]
        J --> K[Composition]
    end
    
    D --> E
    H --> I
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant ATLAS
    participant LLM
    participant Graph
    
    User->>ATLAS: Extract taxonomy
    ATLAS->>LLM: Process text
    LLM-->>ATLAS: Return entities
    ATLAS->>Graph: Create nodes
    Graph-->>ATLAS: Confirm creation
    ATLAS->>LLM: Process relationships
    LLM-->>ATLAS: Return relationships
    ATLAS->>Graph: Create relationships
    Graph-->>ATLAS: Confirm creation
    ATLAS-->>User: Return knowledge graph
```

## Class Diagram

```mermaid
classDiagram
    class ATLASNode {
        +String id
        +List~String~ labels
        +Dict properties
        +create()
        +update()
        +delete()
    }
    
    class EnergyTerm {
        +String name
        +String definition
        +FuelGroupType fuel_group
    }
    
    class RelationshipType {
        +IS_A
        +PART_OF
        +USES
        +PRODUCES
        +bool is_hierarchical()
    }
    
    ATLASNode <|-- EnergyTerm
    ATLASNode -- RelationshipType
```

## Entity Relationship Diagram

```mermaid
erDiagram
    NODE ||--o{ RELATIONSHIP : has
    NODE {
        string id
        string type
        json properties
    }
    RELATIONSHIP {
        string id
        string type
        string startNodeId
        string endNodeId
    }
    NODE ||--o{ LABEL : tagged_with
    LABEL {
        string name
    }
```

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Initialized
    Initialized --> Extracting: start_extraction
    Extracting --> Processing: raw_data
    Processing --> Validating: processed_data
    Validating --> Complete: validated_data
    Validating --> Failed: validation_error
    Failed --> [*]
    Complete --> [*]
```

## Gantt Chart

```mermaid
gantt
    title ATLAS Framework Development Roadmap
    dateFormat  YYYY-MM-DD
    
    section Core Framework
    Design Architecture       :done,    des1, 2025-01-01, 2025-01-15
    Implement Core Components :active,  des2, 2025-01-16, 2025-02-28
    
    section Knowledge Graph
    Design Schema             :done,    des3, 2025-01-10, 2025-01-20
    Implement Graph Database  :active,  des4, 2025-01-25, 2025-02-15
    
    section Agentic LLMs
    Research LLM Integration  :done,    des5, 2025-01-05, 2025-01-25
    Implement FABRIC Patterns :         des6, 2025-02-01, 2025-03-15
    
    section Documentation
    Create Website            :         des7, 2025-03-01, 2025-03-15
    Write Documentation       :         des8, 2025-03-15, 2025-04-01
```

## Pie Chart

```mermaid
pie title Energy Source Distribution
    "Renewable" : 42.7
    "Fossil" : 30.6
    "Nuclear" : 18.9
    "Other" : 7.8
```

## User Journey

```mermaid
journey
    title User Journey with ATLAS Framework
    section Installation
      Download package: 5
      Install dependencies: 3
      Configure settings: 3
    section First Use
      Create project: 5
      Extract taxonomy: 4
      Visualize results: 5
    section Advanced Use
      Customize extraction: 4
      Integrate with systems: 3
      Deploy to production: 4
```

## Git Graph

```mermaid
gitGraph
   commit
   commit
   branch develop
   checkout develop
   commit
   commit
   checkout main
   merge develop
   commit
   commit
   branch feature
   checkout feature
   commit
   checkout develop
   merge feature
   checkout main
   merge develop
   commit
```

## Requirement Diagram

```mermaid
requirementDiagram
    requirement ATLAS_Framework {
        id: 1
        text: ATLAS Framework must extract and organize taxonomies
        risk: high
        verifymethod: test
    }
    
    element ATLASCore {
        type: system
        docref: architecture/overview.md
    }
    
    ATLASCore - satisfies -> ATLAS_Framework
    
    requirement Knowledge_Graph {
        id: 1.1
        text: System must generate knowledge graphs
        risk: medium
        verifymethod: test
    }
    
    requirement Agentic_LLMs {
        id: 1.2
        text: System must use agentic LLMs
        risk: medium
        verifymethod: test
    }
    
    ATLAS_Framework - contains -> Knowledge_Graph
    ATLAS_Framework - contains -> Agentic_LLMs
```

## C4 Diagram

```mermaid
C4Context
    title System Context diagram for ATLAS Framework
    
    Person(user, "User", "A user of the ATLAS Framework")
    
    System(atlas, "ATLAS Framework", "Extracts and organizes taxonomies using agentic LLMs and knowledge graphs")
    
    System_Ext(llm, "LLM Service", "Provides natural language processing capabilities")
    System_Ext(db, "Graph Database", "Stores and queries knowledge graphs")
    
    Rel(user, atlas, "Uses")
    Rel(atlas, llm, "Sends prompts to")
    Rel(atlas, db, "Stores data in")
```

## Mindmap

```mermaid
mindmap
  root((ATLAS Framework))
    Data Layer
      Data Sources
      Extraction Engine
      Data Processing
      Knowledge Graph
    Framework Layer
      LangChain
      LangGraph
      LangSmith
      Tavily
    Intelligence Layer
      FABRIC Patterns
      Orchestration
      Composition
```

## Timeline

```mermaid
timeline
    title ATLAS Framework Development Timeline
    section 2025 Q1
        Design Architecture : Core components design
        : Schema design
        : Research LLM integration
    section 2025 Q2
        Implementation : Core implementation
        : Graph database integration
        : FABRIC patterns implementation
    section 2025 Q3
        Testing & Documentation : System testing
        : Documentation
        : Website creation
    section 2025 Q4
        Release & Expansion : Initial release
        : Community building
        : Additional industry support
```

## Quadrant Chart

```mermaid
quadrantChart
    title Taxonomy Management Solutions Comparison
    x-axis Low Capability --> High Capability
    y-axis Low Flexibility --> High Flexibility
    quadrant-1 High Flexibility, Low Capability
    quadrant-2 High Flexibility, High Capability
    quadrant-3 Low Flexibility, Low Capability
    quadrant-4 Low Flexibility, High Capability
    ATLAS Framework: [0.9, 0.8]
    Traditional Taxonomies: [0.3, 0.2]
    Custom Solutions: [0.5, 0.6]
    Enterprise Tools: [0.7, 0.4]
```

## XY Chart

```mermaid
xychart-beta
    title "ATLAS Framework Performance"
    x-axis "Number of Terms" [100, 500, 1000, 5000, 10000]
    y-axis "Processing Time (s)" [0, 10, 20, 30, 40, 50]
    line [5, 12, 18, 25, 30]
    line [8, 15, 25, 35, 45]
```

## Block Diagram

```mermaid
block-beta
    columns 3
    
    block:app["ATLAS Framework"]
    block:data["Data Sources"]
    block:llm["LLM Services"]
    block:graph["Graph Database"]
    block:ui["User Interface"]
    
    data --> app
    app --> llm
    llm --> app
    app --> graph
    graph --> app
    app --> ui
```

These examples demonstrate the power and flexibility of Mermaid.js for creating various types of diagrams in the ATLAS Framework documentation.

