"""
Configuration settings for EIA Glossary Extractor
"""

import os
from typing import List

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")

# LLM Configuration
LLM_MODEL = "gpt-4o-mini"
LLM_TEMPERATURE = 0
LLM_MAX_TOKENS = 4000

# EIA Website Configuration
EIA_BASE_URL = "https://www.eia.gov/tools/glossary/index.php"
FUEL_GROUPS = [
    "alternative fuels",
    "coal", 
    "electricity",
    "natural gas",
    "nuclear",
    "petroleum",
    "renewable"
]

# Request Configuration
REQUEST_TIMEOUT = 30
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Output Configuration
OUTPUT_FILENAME = "eia_glossary_extracted.json"
MARKDOWN_OUTPUT = "eia_glossary_report.md"

# Processing Configuration
ENABLE_TAVILY_ENHANCEMENT = True
ENABLE_LANGSMITH_TRACING = True
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

