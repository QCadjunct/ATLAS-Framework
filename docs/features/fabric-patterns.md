# FABRIC Patterns

The ATLAS Framework leverages Daniel Meissler's FABRIC patterns for agentic LLM orchestration. This page explains the patterns and how they are implemented in the framework.

## What are FABRIC Patterns?

FABRIC patterns are a collection of prompt engineering patterns that enable LLMs to perform complex reasoning tasks. They provide a structured approach to decomposing complex problems into manageable steps.

```mermaid
flowchart LR
    classDef pattern fill:#e8f5e9,stroke:#2e7d32,color:#2e7d32,stroke-width:2px
    
    A[Input] --> B[FABRIC Pattern]
    B --> C[Output]
    
    subgraph Patterns
        D[Extract Wisdom]:::pattern
        E[Find Patterns]:::pattern
        F[Analyze Claims]:::pattern
        G[Create Summary]:::pattern
        H[Create Network Threat Landscape]:::pattern
    end
    
    B --- Patterns
    
    class D,E,F,G,H pattern
```

## Pattern Composition

FABRIC patterns can be composed to create complex workflows. The ATLAS Framework uses this composition to create sophisticated knowledge extraction and analysis pipelines.

```mermaid
flowchart TD
    classDef input fill:#e3f2fd,stroke:#1565c0,color:#1565c0,stroke-width:2px
    classDef pattern fill:#e8f5e9,stroke:#2e7d32,color:#2e7d32,stroke-width:2px
    classDef output fill:#fff3e0,stroke:#e65100,color:#e65100,stroke-width:2px
    
    A[Raw Text]:::input --> B[Extract Wisdom]:::pattern
    B --> C[Entities & Concepts]:::output
    
    C --> D[Find Patterns]:::pattern
    D --> E[Relationships & Structures]:::output
    
    E --> F[Analyze Claims]:::pattern
    F --> G[Validated Knowledge]:::output
    
    G --> H[Create Summary]:::pattern
    H --> I[Knowledge Graph]:::output
    
    class A input
    class B,D,F,H pattern
    class C,E,G,I output
```

## Pattern Implementation

The ATLAS Framework implements FABRIC patterns as decorators that can be applied to functions. This allows for flexible composition and reuse of patterns.

```mermaid
classDiagram
    class FabricPattern {
        +String name
        +Dict parameters
        +apply(func)
        +process(input)
    }
    
    class ExtractWisdom {
        +process(text)
    }
    
    class FindPatterns {
        +process(entities)
    }
    
    class AnalyzeClaims {
        +process(relationships)
    }
    
    class CreateSummary {
        +process(knowledge)
    }
    
    FabricPattern <|-- ExtractWisdom
    FabricPattern <|-- FindPatterns
    FabricPattern <|-- AnalyzeClaims
    FabricPattern <|-- CreateSummary
```

## Pattern Orchestration

The ATLAS Framework uses a pattern orchestrator to manage the execution of FABRIC patterns. The orchestrator selects the appropriate patterns based on the input and desired output.

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator as Pattern Orchestrator
    participant Registry as Pattern Registry
    participant LLM as LLM Service
    
    User->>Orchestrator: Process input
    Orchestrator->>Registry: Get appropriate patterns
    Registry-->>Orchestrator: Return patterns
    
    loop For each pattern
        Orchestrator->>LLM: Apply pattern
        LLM-->>Orchestrator: Return result
    end
    
    Orchestrator-->>User: Return final result
```

## Pattern Selection

The ATLAS Framework uses a decision tree to select the appropriate patterns for a given task. This ensures that the most effective patterns are used for each specific use case.

```mermaid
graph TD
    A[Input Task] --> B{Task Type?}
    B -->|Extraction| C[Extract Wisdom]
    B -->|Analysis| D[Find Patterns]
    B -->|Validation| E[Analyze Claims]
    B -->|Summarization| F[Create Summary]
    
    C --> G{Need Relationships?}
    G -->|Yes| D
    G -->|No| H{Need Validation?}
    
    D --> H
    
    H -->|Yes| E
    H -->|No| I{Need Summary?}
    
    E --> I
    
    I -->|Yes| F
    I -->|No| J[Final Output]
    
    F --> J
```

## Pattern Configuration

Each FABRIC pattern in the ATLAS Framework can be configured with specific parameters to customize its behavior. This allows for fine-tuning of the patterns for specific domains and use cases.

```mermaid
erDiagram
    PATTERN ||--o{ PARAMETER : has
    PATTERN {
        string name
        string description
        function apply
    }
    PARAMETER {
        string name
        string type
        any default_value
        boolean required
    }
    PATTERN ||--o{ EXAMPLE : has
    EXAMPLE {
        string input
        string output
        json parameters
    }
```

## Energy Domain Patterns

The ATLAS Framework includes specialized FABRIC patterns for the energy domain. These patterns are designed to extract and analyze energy-specific concepts and relationships.

```mermaid
mindmap
  root((Energy Domain Patterns))
    Extract Energy Terms
      Fuel Types
      Technologies
      Regulations
      Markets
    Find Energy Relationships
      Generation Methods
      Distribution Networks
      Consumption Patterns
      Environmental Impact
    Analyze Energy Claims
      Efficiency Claims
      Environmental Claims
      Cost Claims
      Policy Claims
    Create Energy Taxonomy
      Hierarchical Classification
      Cross-Domain Relationships
      Regulatory Framework
      Technology Roadmap
```

## Pattern Usage Example

Here's an example of how FABRIC patterns are used in the ATLAS Framework to extract and analyze energy taxonomy from text.

```mermaid
sequenceDiagram
    participant User
    participant ATLAS
    participant ExtractWisdom
    participant FindPatterns
    participant AnalyzeClaims
    participant CreateSummary
    participant Graph
    
    User->>ATLAS: Extract energy taxonomy from text
    ATLAS->>ExtractWisdom: Process text
    ExtractWisdom-->>ATLAS: Return energy terms
    
    ATLAS->>FindPatterns: Process energy terms
    FindPatterns-->>ATLAS: Return energy relationships
    
    ATLAS->>AnalyzeClaims: Validate relationships
    AnalyzeClaims-->>ATLAS: Return validated knowledge
    
    ATLAS->>CreateSummary: Create taxonomy
    CreateSummary-->>ATLAS: Return taxonomy structure
    
    ATLAS->>Graph: Store taxonomy
    Graph-->>ATLAS: Confirm storage
    
    ATLAS-->>User: Return energy taxonomy
```

## Pattern Performance Metrics

The ATLAS Framework tracks performance metrics for each FABRIC pattern to optimize their usage and improve results over time.

```mermaid
xychart-beta
    title "FABRIC Pattern Performance"
    x-axis "Pattern" ["Extract Wisdom", "Find Patterns", "Analyze Claims", "Create Summary"]
    y-axis "Accuracy (%)" [0, 20, 40, 60, 80, 100]
    bar [85, 78, 92, 88]
```

These diagrams provide a comprehensive view of how FABRIC patterns are implemented and used in the ATLAS Framework for knowledge extraction and analysis.

