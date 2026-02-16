# Industry_Taxonomies GitHub Repository Structure

## Repository Overview

**Repository Name**: `Industry_Taxonomies`  
**Primary Focus**: Comprehensive industry-specific terminology and classification systems  
**Energy Subdirectory**: `Industry_Taxonomies/Energy/` (primary focus area)

## Complete Directory Structure

```
Industry_Taxonomies/
├── README.md                           # Main repository overview
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # Contribution guidelines
├── .gitignore                        # Git ignore patterns
├── .github/                          # GitHub-specific files
│   ├── workflows/                    # GitHub Actions
│   │   ├── validate-data.yml         # Data validation workflow
│   │   └── update-glossaries.yml     # Automated update workflow
│   ├── ISSUE_TEMPLATE/               # Issue templates
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── data_update.md
│   └── PULL_REQUEST_TEMPLATE.md      # PR template
├── docs/                             # Documentation
│   ├── README.md                     # Documentation index
│   ├── methodology.md                # Extraction methodology
│   ├── data-structure.md             # Data format specifications
│   ├── api-reference.md              # API documentation
│   └── contributing-guide.md         # Detailed contribution guide
├── scripts/                          # Utility scripts
│   ├── README.md                     # Scripts documentation
│   ├── validate_data.py              # Data validation script
│   ├── update_glossary.py            # Update automation script
│   ├── export_formats.py             # Format conversion utilities
│   └── requirements.txt              # Script dependencies
├── tools/                            # Extraction and analysis tools
│   ├── README.md                     # Tools documentation
│   ├── agentic_extractors/           # AI-powered extraction tools
│   │   ├── __init__.py
│   │   ├── base_extractor.py         # Base extractor class
│   │   ├── eia_extractor.py          # EIA-specific extractor
│   │   └── requirements.txt          # Tool dependencies
│   ├── analyzers/                    # Analysis tools
│   │   ├── __init__.py
│   │   ├── cross_reference_analyzer.py
│   │   ├── network_analyzer.py
│   │   └── site_map_generator.py
│   └── validators/                   # Data validation tools
│       ├── __init__.py
│       ├── schema_validator.py
│       └── content_validator.py
├── Energy/                           # MAIN ENERGY DIRECTORY
│   ├── README.md                     # Energy taxonomy overview
│   ├── data/                         # Raw and processed data
│   │   ├── raw/                      # Original extracted data
│   │   │   ├── eia_comprehensive_results.json
│   │   │   ├── eia_glossary_simple.json
│   │   │   └── extraction_metadata.json
│   │   ├── processed/                # Cleaned and structured data
│   │   │   ├── fuel_groups/          # Data organized by fuel group
│   │   │   │   ├── alternative_fuels.json
│   │   │   │   ├── coal.json
│   │   │   │   ├── electricity.json
│   │   │   │   ├── natural_gas.json
│   │   │   │   ├── nuclear.json
│   │   │   │   ├── petroleum.json
│   │   │   │   └── renewable.json
│   │   │   ├── alphabetical/         # Data organized alphabetically
│   │   │   │   ├── a-d.json
│   │   │   │   ├── e-h.json
│   │   │   │   ├── i-l.json
│   │   │   │   ├── m-p.json
│   │   │   │   ├── q-t.json
│   │   │   │   └── u-z.json
│   │   │   ├── cross_references.json # Complete cross-reference mapping
│   │   │   ├── site_map.json         # Site navigation structure
│   │   │   └── unified_glossary.json # Complete unified dataset
│   │   └── exports/                  # Export formats
│   │       ├── csv/                  # CSV exports
│   │       │   ├── all_terms.csv
│   │       │   ├── fuel_groups_summary.csv
│   │       │   └── cross_references.csv
│   │       ├── xml/                  # XML exports
│   │       │   ├── energy_glossary.xml
│   │       │   └── cross_references.xml
│   │       └── yaml/                 # YAML exports
│   │           ├── energy_glossary.yaml
│   │           └── fuel_groups.yaml
│   ├── analysis/                     # Analysis reports and insights
│   │   ├── README.md                 # Analysis documentation
│   │   ├── comprehensive_analysis_report.md
│   │   ├── site_map_cross_reference_analysis.md
│   │   ├── baseline_comparison.md
│   │   ├── network_analysis/         # Network analysis results
│   │   │   ├── term_connectivity.json
│   │   │   ├── cluster_analysis.json
│   │   │   └── relationship_strength.json
│   │   └── visualizations/           # Charts and graphs
│   │       ├── fuel_group_distribution.png
│   │       ├── cross_reference_network.png
│   │       └── term_complexity_analysis.png
│   ├── sources/                      # Source information and metadata
│   │   ├── README.md                 # Sources documentation
│   │   ├── eia/                      # EIA-specific sources
│   │   │   ├── source_metadata.json
│   │   │   ├── extraction_log.json
│   │   │   └── baseline_comparison.json
│   │   └── validation/               # Validation data
│   │       ├── baseline_electricity_glossary.txt
│   │       └── validation_results.json
│   ├── tools/                        # Energy-specific tools
│   │   ├── README.md                 # Energy tools documentation
│   │   ├── extractors/               # Extraction tools
│   │   │   ├── focused_comprehensive_extractor.py
│   │   │   ├── comprehensive_eia_extractor.py
│   │   │   └── config.py
│   │   ├── processors/               # Data processing tools
│   │   │   ├── fuel_group_processor.py
│   │   │   ├── cross_reference_processor.py
│   │   │   └── export_generator.py
│   │   └── requirements.txt          # Energy tools dependencies
│   ├── schemas/                      # Data schemas and validation
│   │   ├── README.md                 # Schema documentation
│   │   ├── glossary_term.schema.json # Term schema definition
│   │   ├── cross_reference.schema.json # Cross-reference schema
│   │   ├── fuel_group.schema.json    # Fuel group schema
│   │   └── site_map.schema.json      # Site map schema
│   └── examples/                     # Usage examples and tutorials
│       ├── README.md                 # Examples documentation
│       ├── basic_usage.py            # Basic data access examples
│       ├── advanced_analysis.py      # Advanced analysis examples
│       ├── api_integration.py        # API integration examples
│       └── jupyter_notebooks/        # Interactive examples
│           ├── energy_glossary_exploration.ipynb
│           ├── cross_reference_analysis.ipynb
│           └── fuel_group_comparison.ipynb
├── Transportation/                   # Future expansion directory
│   └── README.md                     # Placeholder for transportation taxonomy
├── Manufacturing/                    # Future expansion directory
│   └── README.md                     # Placeholder for manufacturing taxonomy
├── Healthcare/                       # Future expansion directory
│   └── README.md                     # Placeholder for healthcare taxonomy
├── Finance/                          # Future expansion directory
│   └── README.md                     # Placeholder for finance taxonomy
└── Technology/                       # Future expansion directory
    └── README.md                     # Placeholder for technology taxonomy
```

## Directory Purpose and Organization

### Root Level Files
- **README.md**: Repository overview, quick start guide, and navigation
- **LICENSE**: Open source license (MIT recommended)
- **CONTRIBUTING.md**: Guidelines for contributors
- **.gitignore**: Ignore patterns for data files, logs, and temporary files

### .github/ Directory
- **workflows/**: Automated CI/CD pipelines for data validation and updates
- **ISSUE_TEMPLATE/**: Standardized issue reporting templates
- **PULL_REQUEST_TEMPLATE.md**: PR guidelines and checklist

### docs/ Directory
- Comprehensive documentation for the entire repository
- Methodology explanations and data structure specifications
- API reference and contribution guidelines

### scripts/ Directory
- Utility scripts for data validation, updates, and format conversion
- Standalone tools that can be used across different industry taxonomies

### tools/ Directory
- Reusable extraction and analysis tools
- Modular components for building new extractors
- Validation and quality assurance tools

### Energy/ Directory (Primary Focus)
- **data/**: Complete data organization with raw, processed, and export formats
- **analysis/**: Comprehensive analysis reports and visualizations
- **sources/**: Source metadata and validation information
- **tools/**: Energy-specific extraction and processing tools
- **schemas/**: JSON schemas for data validation
- **examples/**: Usage examples and tutorials

### Future Industry Directories
- Placeholder directories for expansion into other industries
- Consistent structure for scalability and maintainability

## Key Design Principles

### 1. Scalability
- Modular structure supports multiple industries
- Consistent organization patterns across directories
- Reusable tools and components

### 2. Data Organization
- Clear separation of raw, processed, and export data
- Multiple organization schemes (fuel groups, alphabetical)
- Comprehensive metadata and validation

### 3. Documentation
- Extensive README files at every level
- Clear methodology and usage documentation
- Examples and tutorials for different use cases

### 4. Automation
- GitHub Actions for continuous validation
- Automated update workflows
- Quality assurance pipelines

### 5. Accessibility
- Multiple export formats (JSON, CSV, XML, YAML)
- Clear schemas and validation
- Interactive examples and tutorials

## Repository Benefits

### For Developers
- Clear API and data structure documentation
- Ready-to-use extraction tools and examples
- Comprehensive validation and testing frameworks

### For Researchers
- Rich analysis reports and visualizations
- Cross-reference network data for academic study
- Baseline comparison data for validation

### For Industry Professionals
- Authoritative terminology references
- Multiple access formats and integration options
- Regular updates and quality assurance

### For Open Source Community
- Clear contribution guidelines and templates
- Modular architecture for easy extension
- Comprehensive documentation and examples

This structure provides a solid foundation for the Industry_Taxonomies repository with the Energy subdirectory as the primary focus, while maintaining scalability for future industry additions.

