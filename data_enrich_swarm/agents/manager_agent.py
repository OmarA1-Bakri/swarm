# manager_agent.py

from swarm import Agent
from agents.worker_agent import WorkerAgent
from utils.csv_handler import read_csv, write_csv
from config import CHUNK_SIZE
import logging
import pandas as pd


class ManagerAgent(Agent):
    """
    ManagerAgent is responsible for orchestrating the data enrichment process.
    It reads input data, creates worker agents for each data column, distributes
    work among these agents, and saves the enriched data to an output file.

    Attributes:
        input_csv (str): Path to the input CSV file.
        output_csv (str): Path to the output CSV file.
        data (pd.DataFrame): DataFrame holding the input data.
        workers (dict): Dictionary mapping column names to WorkerAgent instances.
        worker_model (str): Model used by worker agents for processing.
    """

    def __init__(self, name, swarm, model, input_csv, output_csv, worker_model):
        """
        Initializes the ManagerAgent with the given parameters.

        Args:
            name (str): Name of the manager agent.
            swarm (Swarm): Swarm instance for managing agents.
            model (str): Model to be used by the manager agent.
            input_csv (str): Path to the input CSV file.
            output_csv (str): Path to the output CSV file.
            worker_model (str): Model used by worker agents for processing.
        """
        super().__init__(name=name, swarm=swarm, model=model)
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.data = None
        self.workers = {}
        self.worker_model = worker_model
        logging.info(
            f"Initialized ManagerAgent with input: {input_csv}, output: {output_csv}"
        )

    def run(self):
        """
        Executes the data enrichment process. It reads the input data, creates
        worker agents, distributes work among them, and saves the results.
        """
        try:
            self.data = read_csv(self.input_csv)  # Read input CSV into a DataFrame
            self.create_worker_agents()  # Create worker agents for each column
            self.distribute_work()  # Distribute work to worker agents
            self.save_results()  # Save the enriched data to the output CSV
            logging.info("Data enrichment process completed successfully")
        except Exception as e:
            logging.error(f"Error during the run process: {e}")
            raise

    def create_worker_agents(self):
        """
        Creates a WorkerAgent for each column in the data (excluding the first column).
        Each WorkerAgent is responsible for processing data in its respective column.
        """
        try:
            columns = self.data.columns[1:]  # Skip the 'Company Name' column
            for column in columns:
                worker = WorkerAgent(
                    name=f"Worker_{column}",
                    swarm=self.swarm,
                    model=self.worker_model,
                    column=column,
                )
                self.workers[column] = (
                    worker  # Store the worker agent in the dictionary
                )
            logging.info(f"Created {len(self.workers)} worker agents")
        except Exception as e:
            logging.error(f"Error creating worker agents: {e}")
            raise

    def distribute_work(self):
        """
        Distributes chunks of companies to each worker agent for processing.
        Each chunk is processed by all worker agents, and results are collected.
        """
        try:
            companies = self.data.index.tolist()  # List of company indices
            for i in range(0, len(companies), CHUNK_SIZE):
                chunk = companies[i : i + CHUNK_SIZE]  # Create a chunk of companies
                logging.info(
                    f"Processing chunk {i//CHUNK_SIZE + 1} of {len(companies)//CHUNK_SIZE + 1}"
                )
                for column, worker in self.workers.items():
                    try:
                        results = worker.process_chunk(
                            chunk
                        )  # Process chunk with worker
                        self.update_data(results, column)  # Update data with results
                    except Exception as e:
                        logging.error(f"Error processing column {column}: {e}")
                        self.handle_worker_failure(column)
        except Exception as e:
            logging.error(f"Error distributing work: {e}")
            raise

    def update_data(self, results, column):
        """
        Updates the DataFrame with the results from a worker agent.

        Args:
            results (str): String representation of the results from a worker agent.
            column (str): The column name to update in the DataFrame.
        """
        try:
            for company, value in eval(results):  # Convert string results to a list
                self.data.loc[company, column] = value  # Update DataFrame with results
            logging.info(f"Updated data for column: {column}")
        except Exception as e:
            logging.error(f"Error updating data for column {column}: {e}")
            raise

    def save_results(self):
        """
        Saves the enriched data to the output CSV file.
        """
        try:
            write_csv(self.data, self.output_csv)  # Write DataFrame to CSV
            logging.info(f"Results saved to {self.output_csv}")
        except Exception as e:
            logging.error(f"Error saving results to {self.output_csv}: {e}")
            raise

    def handle_error(self, error):
        """
        Handles errors that occur within the ManagerAgent.

        Args:
            error (Exception): The error that occurred.

        Returns:
            dict: A dictionary containing error information.
        """
        logging.error(f"Error in ManagerAgent: {error}")
        return {"error": str(error), "stage": "management"}

    def handle_worker_failure(self, column):
        """
        Handles the case when a worker agent fails to process a column.

        Args:
            column (str): The column that failed to process.
        """
        logging.warning(
            f"Worker agent for column {column} failed. Skipping this column."
        )
        self.data[column] = "Failed to process"
