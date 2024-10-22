# worker_agent.py

from swarm import Agent
from utils.rate_limiter import RateLimiter
from config import (
    TAVILY_API_KEY,
    PERPLEXITY_API_KEY,
    TAVILY_RATE_LIMIT,
    PERPLEXITY_RATE_LIMIT,
)
from api.tavily_api import tavily_search
from api.perplexity_api import perplexity_search
import logging


class WorkerAgent(Agent):
    """
    WorkerAgent is responsible for processing data for a specific column in a dataset.
    It uses external APIs to enrich data and handles rate limiting for API requests.

    Attributes:
        column (str): The column name this agent is responsible for processing.
        model (str): The model used for processing data.
        tavily_limiter (RateLimiter): Rate limiter for Tavily API requests.
        perplexity_limiter (RateLimiter): Rate limiter for Perplexity API requests.
    """

    def __init__(self, name, swarm, column, model):
        """
        Initializes the WorkerAgent with the given parameters.

        Args:
            name (str): Name of the worker agent.
            swarm (Swarm): Swarm instance for managing agents.
            column (str): The column name this agent is responsible for processing.
            model (str): The model used for processing data.
        """
        super().__init__(name=name, swarm=swarm, model=model)
        self.column = column
        self.tavily_limiter = RateLimiter(TAVILY_RATE_LIMIT)
        self.perplexity_limiter = RateLimiter(PERPLEXITY_RATE_LIMIT)
        logging.info(f"Initialized WorkerAgent for column: {column}")

    def process_chunk(self, chunk):
        """
        Processes a chunk of companies, enriching data for each company in the chunk.

        Args:
            chunk (list): A list of company names to process.

        Returns:
            str: A string representation of the results for each company.
        """
        logging.info(
            f"Processing chunk of {len(chunk)} companies for column: {self.column}"
        )
        results = []
        for company in chunk:
            try:
                enriched_data = self.enrich_data(company)
                results.append((company, enriched_data))
            except Exception as e:
                logging.error(f"Error processing company {company}: {e}")
                results.append((company, f"Error: {str(e)}"))
        return str(results)

    def enrich_data(self, company):
        """
        Enriches data for a single company using Tavily and Perplexity APIs.

        Args:
            company (str): The name of the company to enrich data for.

        Returns:
            str: Enriched data for the company.
        """
        tavily_result = self.tavily_search(f"{company} {self.column}")
        perplexity_result = self.perplexity_search(
            f"Provide a concise summary about {company}'s {self.column}"
        )

        prompt = f"""
        Based on the following information about {company}'s {self.column}:
        
        Tavily search result: {tavily_result}
        
        Perplexity summary: {perplexity_result}
        
        Provide a brief, factual summary focusing on the most relevant and recent information.
        The summary should be no longer than 100 words.
        """

        return self.generate_summary(prompt)

    def tavily_search(self, query):
        """
        Performs a search using the Tavily API with rate limiting.

        Args:
            query (str): The search query.

        Returns:
            str: The content of the first result from the Tavily API.
        """
        with self.tavily_limiter:
            return tavily_search(query)

    def perplexity_search(self, query):
        """
        Performs a search using the Perplexity API with rate limiting.

        Args:
            query (str): The search query.

        Returns:
            str: The content of the first message from the Perplexity API.
        """
        with self.perplexity_limiter:
            return perplexity_search(query)

    def generate_summary(self, prompt):
        """
        Generates a summary using the agent's model.

        Args:
            prompt (str): The prompt for generating the summary.

        Returns:
            str: The generated summary.
        """
        response = self.swarm.run(
            agent=self, messages=[{"role": "user", "content": prompt}]
        )
        return response.messages[-1]["content"]

    def handle_error(self, error):
        """
        Handles errors that occur within the WorkerAgent.

        Args:
            error (Exception): The error that occurred.

        Returns:
            dict: A dictionary containing error information.
        """
        logging.error(f"Error in WorkerAgent: {error}")
        return {"error": str(error), "column": self.column}
