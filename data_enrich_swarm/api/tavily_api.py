# tavily_api.py

import os
import requests
import logging

# Retrieve the Tavily API key from environment variables
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
# Define the Tavily API URL
TAVILY_API_URL = "https://api.tavily.com/search"


def tavily_search(query):
    """
    Performs a search query using the Tavily API.

    Args:
        query (str): The search query string.

    Returns:
        str: The content of the first result from the Tavily API response.

    Raises:
        ValueError: If the TAVILY_API_KEY is not set in the environment variables.
        requests.exceptions.RequestException: If there is an issue with the API request.
        KeyError: If the response format from the Tavily API is unexpected.
    """
    # Check if the API key is set
    if not TAVILY_API_KEY:
        logging.error("TAVILY_API_KEY is not set in the environment variables.")
        raise ValueError("TAVILY_API_KEY is not set in the environment variables.")

    # Set up the headers for the API request
    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json",
    }
    # Prepare the payload with the query and max_results
    payload = {"query": query, "max_results": 1}

    try:
        # Make a POST request to the Tavily API
        response = requests.post(TAVILY_API_URL, json=payload, headers=headers)
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to connect to Tavily API: {e}")
        raise requests.exceptions.RequestException(
            f"Failed to connect to Tavily API: {e}"
        )

    try:
        # Return the content of the first result from the API response
        return response.json()["results"][0]["content"]
    except KeyError as e:
        logging.error(f"Unexpected response format from Tavily API: {e}")
        raise KeyError(f"Unexpected response format from Tavily API: {e}")
