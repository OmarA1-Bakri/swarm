# config.py

import os

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# CSV Files
INPUT_CSV = "data/Fintechs.csv"
OUTPUT_CSV = "Fintechs_enriched.csv"

# Rate Limiting
OPENAI_RATE_LIMIT = 60  # requests per minute
TAVILY_RATE_LIMIT = 60  # requests per minute
PERPLEXITY_RATE_LIMIT = 60  # requests per minute

# Chunk size for processing companies
CHUNK_SIZE = 10

# LLM Model Configuration
DEFAULT_MANAGER_MODEL = "o1-mini"
DEFAULT_WORKER_MODEL = "gpt-4o-mini"
