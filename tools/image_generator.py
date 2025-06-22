# tools/image_generator.py

import requests
import os

def generate_image(prompt):
    """Call DALL·E or other API to make an image."""

    # Example with OpenAI DALL·E API
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "512x512"
    }

    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=json_data
    )

    data = response.json()
    return data["data"][0]["url"]
