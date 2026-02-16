# EIA Glossary Analysis

## Website Structure
- Base URL: https://www.eia.gov/tools/glossary/index.php
- Fuel group categories are accessible via URL parameters: `?id=<fuel_group>`

## Target Fuel Groups and Term Counts
1. **Alternative fuels** (30 terms) - URL: `?id=alternative%20fuels`
2. **Coal** (31 terms) - URL: `?id=coal`
3. **Electricity** (32 terms) - URL: `?id=electricity`
4. **Natural gas** (35 terms) - URL: `?id=natural%20gas`
5. **Nuclear** (34 terms) - URL: `?id=nuclear`
6. **Petroleum** (35 terms) - URL: `?id=petroleum`
7. **Renewable** (36 terms) - URL: `?id=renewable`

## Data Structure
Each fuel group page contains:
- Multiple glossary terms in bold format
- Detailed definitions following each term
- Cross-references to other terms (linked)
- Some terms have sub-bullets or lists

## Sample Terms from Alternative Fuels
- Aftermarket converted vehicle
- Alternative fuel
- Alternative fuel vehicle (AFV)
- E85 (Flex Fuel)
- Ethanol (C2H5OH)
- Flexible fuel vehicle
- Methanol blend
- Wood and wood-derived fuels

## Scraping Strategy
1. Navigate to each fuel group URL
2. Extract all terms and definitions
3. Parse the HTML structure to identify term names and definitions
4. Organize data by fuel group
5. Use agentic LLMs to enhance extraction and categorization

