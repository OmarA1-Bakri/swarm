# main.py

import os
import logging
from swarm import Swarm
from config import (
    OPENAI_API_KEY,
    TAVILY_API_KEY,
    PERPLEXITY_API_KEY,
    INPUT_CSV,
    OUTPUT_CSV,
    DEFAULT_MANAGER_MODEL,
    DEFAULT_WORKER_MODEL,
    OPENAI_RATE_LIMIT,
)
from agents.manager_agent import ManagerAgent
from utils.rate_limiter import RateLimiter


def setup_logging():
    """
    Configures the logging settings for the application.
    Logs are written to 'data_enrichment.log' with INFO level and above.
    The log format includes the timestamp, logger name, log level, and message.
    Log files are rotated when they reach 1MB in size, keeping 5 backup files.
    """
    from logging.handlers import RotatingFileHandler

    handler = RotatingFileHandler(
        "data_enrichment.log", maxBytes=1_000_000, backupCount=5  # 1MB
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[handler],
    )


def main():
    """
    Main function to execute the data enrichment process.
    It sets up logging, checks for API key availability, initializes the Swarm,
    and runs the ManagerAgent to process the data.
    """
    setup_logging()  # Initialize logging configuration

    try:
        # Ensure all necessary API keys are set
        if not OPENAI_API_KEY or not TAVILY_API_KEY or not PERPLEXITY_API_KEY:
            raise ValueError("All API keys must be set in the configuration file.")

        # Set environment variables for API keys
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
        os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
        os.environ["PERPLEXITY_API_KEY"] = PERPLEXITY_API_KEY

        logging.info("Initializing Swarm and starting data enrichment process")

        # Initialize a rate limiter for the Swarm with the OpenAI rate limit
        rate_limiter = RateLimiter(OPENAI_RATE_LIMIT)
        # Create a Swarm instance with the default manager model and rate limiter
        swarm = Swarm(model=DEFAULT_MANAGER_MODEL, rate_limiter=rate_limiter)

        # Instantiate the ManagerAgent with the necessary parameters
        manager = ManagerAgent(
            "ManagerAgent", swarm, INPUT_CSV, OUTPUT_CSV, DEFAULT_WORKER_MODEL
        )
        # Run the data enrichment process
        manager.run()

        logging.info("Data enrichment process completed successfully")

    except ValueError as ve:
        # Log and print configuration errors
        logging.error(f"Configuration Error: {ve}")
        print(f"Configuration Error: {ve}")
    except Exception as e:
        # Log and print any unexpected errors
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
    finally:
        # Notify the user that the process is complete and logs are available
        print("Data enrichment process completed. Check the log file for details.")


if __name__ == "__main__":
    main()  # Execute the main function if the script is run directly
