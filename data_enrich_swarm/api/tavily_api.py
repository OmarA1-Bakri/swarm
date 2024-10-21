# tavily_api.py

import os
import requests

# Retrieve the Tavily API key from environment variables
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_API_URL = "https://api.tavily.com/search"


def tavily_search(query):
    """
    Performs a search using the Tavily API with the given query.

    Args:
        query (str): The search query to be sent to the Tavily API.

    Returns:
        str: The content of the response message from the Tavily API.

    Raises:
        ValueError: If the API key is not set.
        requests.exceptions.RequestException: If the request to the API fails.
        KeyError: If the expected data is not found in the API response.
    """
    if not TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY is not set in the environment variables.")

    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"query": query, "max_results": 1}

    try:
        response = requests.post(TAVILY_API_URL, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"Failed to connect to Tavily API: {e}"
        )

    try:
        return response.json()["results"][0]["content"]
    except KeyError as e:
        raise KeyError(f"Unexpected response format from Tavily API: {e}")
