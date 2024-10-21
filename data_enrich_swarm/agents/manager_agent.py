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
    It reads input data, creates worker agents, distributes work among them,
    and saves the enriched data to an output file.

    Attributes:
        input_csv (str): Path to the input CSV file.
        output_csv (str): Path to the output CSV file.
        data (DataFrame): Data read from the input CSV.
        workers (dict): Dictionary of worker agents for each data column.
        worker_model (str): Model to be used by worker agents.
    """

    def __init__(self, name, swarm, input_csv, output_csv, worker_model):
        """
        Initializes the ManagerAgent with the given parameters.

        Args:
            name (str): Name of the manager agent.
            swarm (Swarm): The swarm instance to manage agents.
            input_csv (str): Path to the input CSV file.
            output_csv (str): Path to the output CSV file.
            worker_model (str): Model to be used by worker agents.
        """
        super().__init__(name=name, swarm=swarm)
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
        Executes the data enrichment process by reading input data,
        creating worker agents, distributing work, and saving results.
        """
        try:
            self.data = read_csv(self.input_csv)
            self.create_worker_agents()
            self.distribute_work()
            self.save_results()
            logging.info("Data enrichment process completed successfully")
        except Exception as e:
            logging.error(f"Error during the run process: {e}")
            raise

    def create_worker_agents(self):
        """
        Creates worker agents for each column in the data, except the 'Company Name' column.
        """
        try:
            columns = self.data.columns[1:]  # Skip the 'Company Name' column
            for column in columns:
                worker = WorkerAgent(
                    f"Worker_{column}", self.swarm, column, self.worker_model
                )
                self.workers[column] = lambda chunk: self.swarm.run(
                    agent=worker,
                    messages=[
                        {"role": "user", "content": f"Process chunk for {column}"}
                    ],
                    context_variables={"chunk": chunk},
                )
            logging.info(f"Created {len(self.workers)} worker agents")
        except Exception as e:
            logging.error(f"Error creating worker agents: {e}")
            raise

    def distribute_work(self):
        """
        Distributes chunks of companies to worker agents for processing.
        """
        try:
            companies = self.data["Company Name"].tolist()
            for i in range(0, len(companies), CHUNK_SIZE):
                chunk = companies[i : i + CHUNK_SIZE]
                logging.info(
                    f"Processing chunk {i//CHUNK_SIZE + 1} of {len(companies)//CHUNK_SIZE + 1}"
                )
                for column, worker_function in self.workers.items():
                    results = worker_function(chunk)
                    self.update_data(results.messages[-1]["content"], column)
        except Exception as e:
            logging.error(f"Error distributing work: {e}")
            raise

    def update_data(self, results, column):
        """
        Updates the data with the results from worker agents.

        Args:
            results (str): The results returned by the worker agents.
            column (str): The column to update in the data.
        """
        try:
            for company, value in eval(results):
                self.data.loc[self.data["Company Name"] == company, column] = value
            logging.info(f"Updated data for column: {column}")
        except Exception as e:
            logging.error(f"Error updating data for column {column}: {e}")
            raise

    def save_results(self):
        """
        Saves the enriched data to the output CSV file.
        """
        try:
            write_csv(self.data, self.output_csv)
            logging.info(f"Results saved to {self.output_csv}")
        except Exception as e:
            logging.error(f"Error saving results to {self.output_csv}: {e}")
            raise

    def handle_error(self, error):
        """
        Handles errors that occur during the management process.

        Args:
            error (Exception): The error that occurred.

        Returns:
            dict: A dictionary containing error information.
        """
        logging.error(f"Error in ManagerAgent: {error}")
        return {"error": str(error), "stage": "management"}
