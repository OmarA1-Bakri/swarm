# tavily_api.py

# tavily_api.py

import os
import requests
import logging

# Retrieve the Tavily API key from environment variables
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_API_URL = "https://api.tavily.com/search"


def tavily_search(query):
    if not TAVILY_API_KEY:
        logging.error("TAVILY_API_KEY is not set in the environment variables.")
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
        logging.error(f"Failed to connect to Tavily API: {e}")
        raise requests.exceptions.RequestException(
            f"Failed to connect to Tavily API: {e}"
        )

    try:
        return response.json()["results"][0]["content"]
    except KeyError as e:
        logging.error(f"Unexpected response format from Tavily API: {e}")
        raise KeyError(f"Unexpected response format from Tavily API: {e}")
