# perplexity_api.py

# perplexity_api.py

import os
import requests
import logging

# Retrieve the Perplexity API key from environment variables
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"


def perplexity_search(query):
    if not PERPLEXITY_API_KEY:
        logging.error("PERPLEXITY_API_KEY is not set in the environment variables.")
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
        logging.error(f"Failed to connect to Perplexity API: {e}")
        raise requests.exceptions.RequestException(
            f"Failed to connect to Perplexity API: {e}"
        )

    try:
        return response.json()["choices"][0]["message"]["content"]
    except KeyError as e:
        logging.error(f"Unexpected response format from Perplexity API: {e}")
        raise KeyError(f"Unexpected response format from Perplexity API: {e}")
