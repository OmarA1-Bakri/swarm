# main.py

import os
import logging
from swarm import Swarm
from config import (
    TAVILY_API_KEY,
    PERPLEXITY_API_KEY,
    INPUT_CSV,
    OUTPUT_CSV,
    DEFAULT_MANAGER_MODEL,
    DEFAULT_WORKER_MODEL,
)
from agents.manager_agent import ManagerAgent


def setup_logging():
    """
    Sets up logging configuration for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename="data_enrichment.log",
    )


def main():
    """
    Main function to set up environment variables, initialize the Swarm, and run the data enrichment process.

    This function performs the following steps:
    1. Sets up logging.
    2. Sets up API keys as environment variables.
    3. Initializes the Swarm with the default manager model.
    4. Creates and runs the manager agent to start the data enrichment process.

    Raises:
        ValueError: If any of the required API keys are not set.
        Exception: If there is an error during the Swarm initialization or agent execution.
    """
    setup_logging()

    try:
        # Check if API keys are set, raise an error if not
        if not TAVILY_API_KEY or not PERPLEXITY_API_KEY:
            raise ValueError("API keys must be set in the configuration file.")

        # Set API keys as environment variables
        os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
        os.environ["PERPLEXITY_API_KEY"] = PERPLEXITY_API_KEY

        logging.info("Initializing Swarm and starting data enrichment process")

        # Initialize the Swarm with the default manager model
        swarm = Swarm(model=DEFAULT_MANAGER_MODEL)

        def manager_agent(input_csv, output_csv, worker_model):
            """
            Function to create and run the manager agent.

            Args:
                input_csv (str): Path to the input CSV file.
                output_csv (str): Path to the output CSV file.
                worker_model (str): Model to be used by the worker agents.
            """
            # Create a ManagerAgent instance and run it
            manager = ManagerAgent(
                "ManagerAgent", swarm, input_csv, output_csv, worker_model
            )
            manager.run()

        # Run the swarm with the manager agent function and context variables
        swarm.run(
            function=manager_agent,
            context_variables={
                "input_csv": INPUT_CSV,
                "output_csv": OUTPUT_CSV,
                "worker_model": DEFAULT_WORKER_MODEL,
            },
        )

        logging.info("Data enrichment process completed successfully")

    except ValueError as ve:
        # Handle configuration errors
        logging.error(f"Configuration Error: {ve}")
        print(f"Configuration Error: {ve}")
    except Exception as e:
        # Handle any unexpected errors
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
    finally:
        # Indicate completion of the data enrichment process
        print("Data enrichment process completed. Check the log file for details.")


if __name__ == "__main__":
    main()
