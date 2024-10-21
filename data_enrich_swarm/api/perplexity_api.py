# perplexity_api.py

import os
import requests

# Retrieve the Perplexity API key from environment variables
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"


def perplexity_search(query):
    """
    Performs a search using the Perplexity API with the given query.

    Args:
        query (str): The search query to be sent to the Perplexity API.

    Returns:
        str: The content of the response message from the Perplexity API.

    Raises:
        ValueError: If the API key is not set.
        requests.exceptions.RequestException: If the request to the API fails.
        KeyError: If the expected data is not found in the API response.
    """
    if not PERPLEXITY_API_KEY:
        raise ValueError("PERPLEXITY_API_KEY is not set in the environment variables.")

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": query}],
    }

    try:
        response = requests.post(PERPLEXITY_API_URL, json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"Failed to connect to Perplexity API: {e}"
        )

    try:
        return response.json()["choices"][0]["message"]["content"]
    except KeyError as e:
        raise KeyError(f"Unexpected response format from Perplexity API: {e}")
