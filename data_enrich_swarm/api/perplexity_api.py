# perplexity_api.py

import os
import requests
import logging

# Retrieve the Perplexity API key from environment variables
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
# Define the Perplexity API URL
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"


def perplexity_search(query):
    """
    Sends a query to the Perplexity API and retrieves the response.

    Args:
        query (str): The query string to be sent to the Perplexity API.

    Returns:
        str: The content of the response message from the Perplexity API.

    Raises:
        ValueError: If the PERPLEXITY_API_KEY is not set in the environment variables.
        requests.exceptions.RequestException: If there is a network-related error or
                                              an invalid response from the API.
        KeyError: If the response format from the API is not as expected.
    """
    # Check if the API key is available
    if not PERPLEXITY_API_KEY:
        logging.error("PERPLEXITY_API_KEY is not set in the environment variables.")
        raise ValueError("PERPLEXITY_API_KEY is not set in the environment variables.")

    # Set up the headers for the API request
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",  # Use the API key for authorization
        "Content-Type": "application/json",  # Specify the content type as JSON
    }

    # Prepare the payload with the query and model information
    payload = {
        "model": "gpt-3.5-turbo",  # Specify the model to be used
        "messages": [{"role": "user", "content": query}],  # Include the user query
    }

    try:
        # Make a POST request to the Perplexity API
        response = requests.post(PERPLEXITY_API_URL, json=payload, headers=headers)
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to connect to Perplexity API: {e}")
        raise requests.exceptions.RequestException(
            f"Failed to connect to Perplexity API: {e}"
        )

    try:
        # Extract and return the content of the response message
        return response.json()["choices"][0]["message"]["content"]
    except KeyError as e:
        logging.error(f"Unexpected response format from Perplexity API: {e}")
        raise KeyError(f"Unexpected response format from Perplexity API: {e}")
