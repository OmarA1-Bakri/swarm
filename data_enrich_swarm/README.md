# readme.md

# Fintech Data Enrichment Application

This application uses OpenAI's SWARM platform to enrich data from a CSV file containing information about fintech companies. It leverages the Tavily and Perplexity APIs for web data retrieval and enrichment, implementing a multi-agent framework for efficient data processing.

## Features

- Multi-agent architecture using OpenAI's SWARM platform
- Data enrichment using Tavily and Perplexity APIs
- Configurable manager and worker models
- Rate limiting for API calls
- Chunk-based processing for large datasets

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fintech-data-enrichment.git
   cd fintech-data-enrichment
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your API keys in the `config.py` file:
   - TAVILY_API_KEY
   - PERPLEXITY_API_KEY

4. Configure the input and output CSV files in `config.py`:
   - INPUT_CSV: Path to your input CSV file
   - OUTPUT_CSV: Path where the enriched CSV will be saved

5. Adjust other configuration settings in `config.py` as needed:
   - CHUNK_SIZE: Number of companies to process in each batch
   - DEFAULT_MANAGER_MODEL: The model to use for the manager agent
   - DEFAULT_WORKER_MODEL: The model to use for worker agents

## Running the Application

To run the application, execute the following command:

