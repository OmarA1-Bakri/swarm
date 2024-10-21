# config.py

# API Keys
TAVILY_API_KEY = "your_tavily_api_key"
PERPLEXITY_API_KEY = "your_perplexity_api_key"

# CSV Files
INPUT_CSV = "data/Fintechs.csv"
OUTPUT_CSV = "Fintechs_enriched.csv"

# Rate Limiting
TAVILY_RATE_LIMIT = 60  # requests per minute
PERPLEXITY_RATE_LIMIT = 60  # requests per minute

# Chunk size for processing companies
CHUNK_SIZE = 10

# LLM Model Configuration
DEFAULT_MANAGER_MODEL = "o1-mini"
DEFAULT_WORKER_MODEL = "gpt-4o-mini"
