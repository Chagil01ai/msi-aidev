# tools/web_search.py

import requests
import os

def web_search(query):
    """Search Google or SerpAPI for live info."""
    api_key = os.getenv("SERPAPI_API_KEY")  # Secure in .env
    url = "https://serpapi.com/search.json"

    params = {
        "q": query,
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "organic_results" in data:
        # Return top 3 results
        return "\n".join([f"{r['title']}: {r['link']}" for r in data["organic_results"][:3]])
    else:
        return "No search results found."
