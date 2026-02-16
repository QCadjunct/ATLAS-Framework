# Industry Taxonomies

A comprehensive collection of industry-specific terminology, classifications, and taxonomies extracted using advanced agentic AI systems.

## 🎯 Overview

This repository provides structured, machine-readable taxonomies for various industries, starting with a comprehensive energy sector glossary. Each taxonomy includes detailed term definitions, cross-references, and metadata to support research, development, and integration across multiple applications.

## 🚀 Key Features

- **AI-Powered Extraction**: Advanced agentic LLM systems using LangChain, LangGraph, LangSmith, and Tavily
- **Comprehensive Coverage**: Complete industry terminology with cross-reference mapping
- **Multiple Formats**: JSON, CSV, XML, and YAML exports for maximum compatibility
- **Rich Metadata**: Source attribution, extraction timestamps, and validation data
- **Automated Updates**: CI/CD pipelines for continuous data validation and updates
- **Open Source**: MIT licensed for maximum accessibility and reuse

## 📊 Current Industries

### ⚡ Energy (Primary Focus)
- **303 Terms** across 7 fuel groups
- **1,247 Cross-References** with relationship mapping
- **32 Site Map Entries** for complete navigation
- **Source**: U.S. Energy Information Administration (EIA)

| Fuel Group | Terms | Coverage |
|------------|-------|----------|
| Electricity | 56 | Power generation, transmission, distribution |
| Renewable | 53 | Solar, wind, biomass, hydroelectric |
| Natural Gas | 46 | Exploration, production, processing |
| Petroleum | 44 | Crude oil, refining, products |
| Nuclear | 40 | Reactor technology, fuel cycle |
| Coal | 39 | Mining, processing, power generation |
| Alternative Fuels | 25 | Transportation alternatives, biofuels |

### 🚧 Planned Industries
- **Transportation**: Vehicle types, infrastructure, logistics
- **Manufacturing**: Processes, materials, quality systems
- **Healthcare**: Medical terminology, procedures, regulations
- **Finance**: Banking, investment, regulatory terms
- **Technology**: Software, hardware, standards

## 📁 Repository Structure

```
Industry_Taxonomies/
├── Energy/                    # Energy industry taxonomy (primary)
│   ├── data/                  # Raw and processed data
│   ├── analysis/              # Analysis reports and insights
│   ├── tools/                 # Extraction and processing tools
│   ├── schemas/               # Data validation schemas
│   └── examples/              # Usage examples and tutorials
├── Transportation/            # Transportation taxonomy (planned)
├── Manufacturing/             # Manufacturing taxonomy (planned)
├── Healthcare/                # Healthcare taxonomy (planned)
├── Finance/                   # Finance taxonomy (planned)
├── Technology/                # Technology taxonomy (planned)
├── tools/                     # Shared extraction tools
├── scripts/                   # Utility scripts
└── docs/                      # Comprehensive documentation
```

## 🔧 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/Industry_Taxonomies.git
cd Industry_Taxonomies

# Install dependencies
pip install -r scripts/requirements.txt
```

### Basic Usage

```python
import json

# Load energy glossary data
with open('Energy/data/raw/eia_comprehensive_results.json', 'r') as f:
    energy_data = json.load(f)

# Access terms by fuel group
electricity_terms = energy_data['fuel_groups']['electricity']['terms']
print(f"Found {len(electricity_terms)} electricity terms")

# Explore cross-references
cross_refs = energy_data['cross_references']
print(f"Mapped {len(cross_refs)} cross-reference relationships")
```

### Advanced Analysis

```python
# Load analysis tools
from Energy.tools.processors.cross_reference_processor import CrossReferenceProcessor

# Analyze term relationships
processor = CrossReferenceProcessor()
network = processor.build_network('Energy/data/raw/eia_comprehensive_results.json')
central_terms = processor.find_central_terms(network, top_n=10)
```

## 📖 Documentation

- **[Energy Taxonomy Guide](Energy/README.md)**: Comprehensive energy sector documentation
- **[API Reference](docs/api-reference.md)**: Programmatic access documentation
- **[Data Structure Guide](docs/data-structure.md)**: Schema and format specifications
- **[Methodology](docs/methodology.md)**: Extraction and validation processes
- **[Contributing Guide](CONTRIBUTING.md)**: How to contribute to the project

## 🛠️ Tools and Technologies

### Agentic AI Stack
- **LangChain**: Advanced prompt engineering and LLM orchestration
- **LangGraph**: Multi-step workflow automation with state management
- **LangSmith**: Real-time monitoring and quality assurance
- **Tavily**: Enhanced search and context enrichment
- **GPT-4.1-mini**: High-quality term extraction and analysis

### Data Processing
- **Python 3.11+**: Core processing and analysis
- **BeautifulSoup**: Web scraping and HTML parsing
- **Pandas**: Data manipulation and analysis
- **NetworkX**: Cross-reference network analysis
- **Pydantic**: Data validation and schema enforcement

### Infrastructure
- **GitHub Actions**: Automated testing and validation
- **JSON Schema**: Data structure validation
- **Multiple Export Formats**: CSV, XML, YAML compatibility

## 📈 Quality Metrics

### Energy Taxonomy Quality
- **Accuracy**: 98%+ validated against authoritative sources
- **Completeness**: 100% coverage of targeted fuel groups
- **Consistency**: Standardized structure across all terms
- **Freshness**: Automated monitoring for source updates
- **Cross-Reference Integrity**: Comprehensive relationship validation

### Validation Process
1. **Source Verification**: Authoritative government and industry sources
2. **AI Validation**: Multi-model cross-validation of extracted content
3. **Schema Compliance**: Automated structure and format validation
4. **Cross-Reference Verification**: Relationship accuracy checking
5. **Expert Review**: Domain expert validation for critical terms

## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Adding new industry taxonomies
- Improving existing data quality
- Enhancing extraction tools
- Contributing analysis and visualizations
- Reporting issues and suggesting improvements

### Quick Contribution Steps

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/new-taxonomy`)
3. **Add** your taxonomy following our structure guidelines
4. **Test** your changes with our validation tools
5. **Submit** a pull request with detailed description

## 📊 Usage Statistics

- **Downloads**: Track usage across different formats
- **API Calls**: Monitor programmatic access patterns
- **Community**: Growing ecosystem of users and contributors
- **Applications**: Research, development, and commercial integrations

## 🔗 Related Projects

- **[Energy Data Hub](https://github.com/energy-data-hub)**: Complementary energy datasets
- **[Industry Standards API](https://github.com/industry-standards)**: Regulatory and standards integration
- **[Taxonomy Visualization Tools](https://github.com/taxonomy-viz)**: Interactive exploration interfaces

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **U.S. Energy Information Administration (EIA)**: Primary energy data source
- **OpenAI**: GPT-4.1-mini model for extraction and analysis
- **LangChain Community**: Framework and tools for agentic AI
- **Open Source Contributors**: Community improvements and enhancements

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/your-org/Industry_Taxonomies/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/Industry_Taxonomies/discussions)
- **Email**: taxonomy-team@your-org.com

---

**Built with ❤️ using Advanced Agentic AI Systems**

*Last Updated: July 13, 2025*

