# config.py

import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Check if all API keys are set
if not all([OPENAI_API_KEY, TAVILY_API_KEY, PERPLEXITY_API_KEY]):
    missing_keys = [
        key
        for key, value in {
            "OPENAI_API_KEY": OPENAI_API_KEY,
            "TAVILY_API_KEY": TAVILY_API_KEY,
            "PERPLEXITY_API_KEY": PERPLEXITY_API_KEY,
        }.items()
        if not value
    ]
    logging.error(f"Missing API keys: {', '.join(missing_keys)}")
    raise ValueError("All API keys must be set in the .env file.")

# CSV Files

INPUT_CSV = "data_enrich_swarm/data/fintechs.csv"
OUTPUT_CSV = "data_enrich_swarm/data/fintechs_enriched.csv"

# Rate Limiting
OPENAI_RATE_LIMIT = 60  # requests per minute
TAVILY_RATE_LIMIT = 60  # requests per minute
PERPLEXITY_RATE_LIMIT = 60  # requests per minute

# Chunk size for processing companies
CHUNK_SIZE = 10

# LLM Model Configuration
DEFAULT_MANAGER_MODEL = "o1-mini"
DEFAULT_WORKER_MODEL = "gpt-4o-mini"
