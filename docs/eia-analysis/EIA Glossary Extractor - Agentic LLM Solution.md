# EIA Glossary Extractor - Agentic LLM Solution

This project extracts energy industry glossary terms from the U.S. Energy Information Administration (EIA) website using advanced agentic LLM techniques with LangChain, LangGraph, LangSmith, and Tavily.

## Features

- **Agentic LLM Architecture**: Uses LangGraph to create a multi-step workflow for intelligent data extraction
- **Advanced NLP**: Leverages GPT-4 for accurate term identification and definition extraction
- **Web Scraping**: Automated extraction from EIA's online glossary
- **Structured Output**: Organizes terms by fuel groups with cross-references
- **Enhanced Context**: Optional integration with Tavily for additional context
- **Tracing & Monitoring**: LangSmith integration for workflow observability

## Target Fuel Groups

The extractor focuses on these seven key energy sectors:

1. **Alternative Fuels** (~30 terms)
2. **Coal** (~31 terms)
3. **Electricity** (~32 terms)
4. **Natural Gas** (~35 terms)
5. **Nuclear** (~34 terms)
6. **Petroleum** (~35 terms)
7. **Renewable** (~36 terms)

## Architecture

### Agentic LLM Components

1. **LangChain**: Core framework for LLM interactions and prompt engineering
2. **LangGraph**: Workflow orchestration with state management
3. **LangSmith**: Tracing and monitoring of LLM operations
4. **Tavily**: Optional web search enhancement for additional context

### Workflow Design

```
Start → Fetch Content → Extract Terms → Enhance with AI → Next Group → Complete
  ↑                                                           ↓
  └─────────────────── Continue Processing ←─────────────────┘
```

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export TAVILY_API_KEY="your-tavily-api-key"  # Optional
   export LANGSMITH_API_KEY="your-langsmith-api-key"  # Optional
   ```

## Usage

### Basic Execution

```bash
python eia_glossary_extractor.py
```

### Programmatic Usage

```python
from eia_glossary_extractor import EIAGlossaryExtractor

# Initialize extractor
extractor = EIAGlossaryExtractor()

# Run extraction
results = extractor.run_extraction()

# Save results
output_file = extractor.save_results(results)
```

## Output Format

The extractor generates a structured JSON file with the following format:

```json
{
  "alternative fuels": [
    {
      "term": "Alternative fuel",
      "definition": "Alternative fuels, for transportation applications, include...",
      "fuel_group": "alternative fuels",
      "cross_references": ["Biomass", "Fuel Ethanol"]
    }
  ],
  "coal": [...],
  "electricity": [...],
  ...
}
```

## Key Classes and Methods

### `EIAGlossaryExtractor`

Main extractor class implementing the agentic LLM workflow.

**Key Methods:**
- `fetch_page_content(fuel_group)`: Retrieves HTML content for a fuel group
- `extract_terms_with_llm(content, fuel_group)`: Uses LLM to extract structured terms
- `create_langgraph_workflow()`: Builds the LangGraph workflow
- `run_extraction()`: Executes the complete extraction process

### `GlossaryTerm`

Data class representing an extracted glossary term.

**Attributes:**
- `term`: The glossary term name
- `definition`: Complete definition text
- `fuel_group`: Associated fuel group category
- `cross_references`: List of referenced terms

### `AgentState`

TypedDict defining the state for the LangGraph workflow.

**State Variables:**
- `fuel_groups`: List of fuel groups to process
- `current_group`: Currently processing fuel group
- `extracted_terms`: Accumulated extracted terms
- `processed_count`: Number of completed fuel groups

## Advanced Features

### LangGraph Workflow

The solution uses LangGraph to create a sophisticated workflow with:

- **State Management**: Tracks progress across fuel groups
- **Conditional Logic**: Determines when to continue or complete
- **Error Handling**: Robust error recovery mechanisms
- **Parallel Processing**: Potential for concurrent term extraction

### LLM Prompt Engineering

Sophisticated prompts ensure:

- **Complete Extraction**: Captures all terms without omission
- **Accurate Parsing**: Maintains definition integrity
- **Cross-Reference Detection**: Identifies term relationships
- **Structured Output**: Consistent JSON formatting

### Optional Enhancements

- **Tavily Integration**: Additional web context for terms
- **LangSmith Tracing**: Detailed workflow monitoring
- **Retry Logic**: Handles temporary failures gracefully

## Configuration

Modify `config.py` to customize:

- LLM model and parameters
- Request timeouts and headers
- Output file names and formats
- Feature toggles for optional components

## Error Handling

The solution includes comprehensive error handling:

- **Network Failures**: Automatic retries with exponential backoff
- **LLM Errors**: Graceful degradation and alternative approaches
- **Parsing Issues**: Robust HTML parsing with fallbacks
- **State Recovery**: Workflow continuation from interruptions

## Performance Considerations

- **Rate Limiting**: Respects API rate limits
- **Caching**: Avoids redundant requests
- **Memory Management**: Efficient handling of large datasets
- **Concurrent Processing**: Potential for parallel execution

## Monitoring and Debugging

With LangSmith integration:

- **Trace Workflows**: Monitor each step execution
- **Performance Metrics**: Track extraction efficiency
- **Error Analysis**: Detailed failure investigation
- **Cost Tracking**: Monitor API usage and costs

## Future Enhancements

Potential improvements:

1. **Multi-language Support**: Extract terms in multiple languages
2. **Real-time Updates**: Monitor EIA website for changes
3. **Semantic Analysis**: Advanced term relationship mapping
4. **Export Formats**: Additional output formats (CSV, XML, etc.)
5. **Web Interface**: User-friendly web application
6. **API Service**: RESTful API for programmatic access

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgments

- U.S. Energy Information Administration for providing comprehensive energy glossaries
- OpenAI for advanced language model capabilities
- LangChain team for the excellent framework ecosystem
- Tavily for web search enhancement capabilities

