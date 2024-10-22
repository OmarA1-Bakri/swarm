# config.py

import os

# API Keys
# Retrieve API keys from environment variables for security and flexibility.
OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)  # OpenAI API key for accessing OpenAI services
TAVILY_API_KEY = os.getenv(
    "TAVILY_API_KEY"
)  # Tavily API key for accessing Tavily services
PERPLEXITY_API_KEY = os.getenv(
    "PERPLEXITY_API_KEY"
)  # Perplexity API key for accessing Perplexity services

# CSV Files
# Define file paths for input and output CSV files used in data processing.
INPUT_CSV = "data/Fintechs.csv"  # Path to the input CSV file containing raw data
OUTPUT_CSV = "Fintechs_enriched.csv"  # Path to the output CSV file for enriched data

# Rate Limiting
# Set rate limits for API requests to prevent exceeding service quotas.
OPENAI_RATE_LIMIT = 60  # Maximum number of OpenAI API requests per minute
TAVILY_RATE_LIMIT = 60  # Maximum number of Tavily API requests per minute
PERPLEXITY_RATE_LIMIT = 60  # Maximum number of Perplexity API requests per minute

# Chunk size for processing companies
# Specify the number of companies to process in each batch.
CHUNK_SIZE = 10  # Number of companies to process in each chunk

# LLM Model Configuration
# Define default models for manager and worker agents in the data enrichment process.
DEFAULT_MANAGER_MODEL = "o1-mini"  # Default model for the ManagerAgent
DEFAULT_WORKER_MODEL = "gpt-4o-mini"  # Default model for the WorkerAgent
