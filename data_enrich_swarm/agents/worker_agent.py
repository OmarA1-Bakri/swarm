# worker_agent.py

from swarm import Agent
from api.tavily_api import tavily_search
from api.perplexity_api import perplexity_search
from utils.rate_limiter import RateLimiter
from config import TAVILY_RATE_LIMIT, PERPLEXITY_RATE_LIMIT
import logging


class WorkerAgent(Agent):
    """
    WorkerAgent is responsible for enriching data for a specific column
    using either the Tavily or Perplexity API, depending on the column type.

    Attributes:
        column (str): The data column to enrich.
        model (str): The model to use for processing.
        tavily_limiter (RateLimiter): Rate limiter for Tavily API.
        perplexity_limiter (RateLimiter): Rate limiter for Perplexity API.
    """

    def __init__(self, name, swarm, column, model):
        """
        Initializes the WorkerAgent with the given parameters.

        Args:
            name (str): Name of the worker agent.
            swarm (Swarm): The swarm instance to manage agents.
            column (str): The data column to enrich.
            model (str): The model to use for processing.
        """
        super().__init__(name=name, swarm=swarm)
        self.column = column
        self.model = model
        self.tavily_limiter = RateLimiter(TAVILY_RATE_LIMIT)
        self.perplexity_limiter = RateLimiter(PERPLEXITY_RATE_LIMIT)
        logging.info(f"Initialized WorkerAgent for column: {column}")

    def process_chunk(self, chunk):
        """
        Processes a chunk of companies and returns the enriched data.

        Args:
            chunk (list): A list of company names to process.

        Returns:
            str: A string representation of the results.
        """
        logging.info(
            f"Processing chunk of {len(chunk)} companies for column: {self.column}"
        )
        results = []
        for company in chunk:
            try:
                value = self.enrich_company(company)
                results.append((company, value))
            except Exception as e:
                logging.error(f"Error enriching data for {company}: {e}")
                results.append((company, f"Error: {str(e)}"))
        return str(results)

    def enrich_company(self, company):
        """
        Enriches data for a given company using the appropriate API.

        Args:
            company (str): The name of the company to enrich data for.

        Returns:
            str: A summary of the enriched data for the company.
        """
        query = f"{company} {self.column}"

        try:
            if self.column in [
                "API yes/no",
                "Core business focus",
                "Headquaters",
                "Currencies",
            ]:
                with self.tavily_limiter:
                    data = tavily_search(query)
            else:
                with self.perplexity_limiter:
                    data = perplexity_search(query)

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

    def handle_error(self, error):
        """
        Handles errors that occur during the enrichment process.

        Args:
            error (Exception): The error that occurred.

        Returns:
            dict: A dictionary containing error information.
        """
        logging.error(f"Error in WorkerAgent: {error}")
        return {"error": str(error), "column": self.column}
