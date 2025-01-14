# main.py

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
)
from agents.manager_agent import ManagerAgent
from utils.rate_limiter import RateLimiter


def setup_logging():
    """
    Configures the logging settings for the application.

    This function sets up logging to write logs to 'data_enrichment.log' with a level of INFO and above.
    The log format includes the timestamp, logger name, log level, and message.
    Log files are rotated when they reach 1MB in size, keeping 5 backup files.
    """
    from logging.handlers import RotatingFileHandler

    # Create a rotating file handler that writes to 'data_enrichment.log'
    handler = RotatingFileHandler(
        "data_enrichment.log", maxBytes=1_000_000, backupCount=5  # 1MB
    )
    # Configure the basic logging settings
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[handler],
    )


def main():
    """
    Main function to execute the data enrichment process.

    This function sets up logging, checks for the availability of API keys, initializes the Swarm,
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

        # Create a Swarm instance
        swarm = Swarm()

        # Instantiate the ManagerAgent with the necessary parameters
        manager = ManagerAgent(
            name="ManagerAgent",
            swarm=swarm,
            model=DEFAULT_MANAGER_MODEL,
            input_csv=INPUT_CSV,
            output_csv=OUTPUT_CSV,
            worker_model=DEFAULT_WORKER_MODEL,
        )
        # Run the data enrichment process
        try:
            manager.run()
        except Exception as e:
            logging.error(f"Error during manager execution: {e}")
            print(f"Error during manager execution: {e}")
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
