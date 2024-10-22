# worker_agent.py

from swarm import Agent
from utils.rate_limiter import RateLimiter
from config import (
    TAVILY_API_KEY,
    PERPLEXITY_API_KEY,
    TAVILY_RATE_LIMIT,
    PERPLEXITY_RATE_LIMIT,
)
import logging
import requests


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
        super().__init__(name=name, swarm=swarm)
        self.column = column
        self.model = model
        # Initialize rate limiters for Tavily and Perplexity APIs
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
                # Enrich data for each company
                value = self.enrich_company(company)
                results.append((company, value))
            except Exception as e:
                logging.error(f"Error enriching data for {company}: {e}")
                results.append((company, f"Error: {str(e)}"))
        return str(results)

    def enrich_company(self, company):
        """
        Enriches data for a single company by querying relevant information.

        Args:
            company (str): The name of the company to enrich data for.

        Returns:
            str: A summary of the enriched data for the company.
        """
        query = f"{company} {self.column}"

        try:
            # Determine which API to use based on the column
            if self.column in [
                "API yes/no",
                "Core business focus",
                "Headquaters",
                "Currencies",
            ]:
                data = self.tavily_search(query)
            else:
                data = self.perplexity_search(query)

            # Use the swarm to process the data and generate a summary
            response = self.swarm.run(
                agent=self,
                messages=[
                    {
                        "role": "user",
                        "content": f"Summarize the following information about {company} for the {self.column} category:\n\n{data}",
                    }
                ],
                model=self.model,
            )
            summary = response.messages[-1]["content"]
            logging.info(f"Enriched data for {company} in column {self.column}")
            return summary
        except Exception as e:
            logging.error(
                f"Error in enrich_company for {company} in column {self.column}: {e}"
            )
            raise

    def tavily_search(self, query):
        """
        Performs a search using the Tavily API.

        Args:
            query (str): The search query.

        Returns:
            str: The content of the first result from the Tavily API.
        """
        url = "https://api.tavily.com/search"
        headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}
        params = {"query": query, "max_results": 1}

        with self.tavily_limiter:
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                return response.json()["results"][0]["content"]
            except Exception as e:
                logging.error(f"Error in Tavily search: {e}")
                raise

    def perplexity_search(self, query):
        """
        Performs a search using the Perplexity API.

        Args:
            query (str): The search query.

        Returns:
            str: The content of the first message from the Perplexity API.
        """
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": query}],
        }

        with self.perplexity_limiter:
            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                logging.error(f"Error in Perplexity search: {e}")
                raise

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
