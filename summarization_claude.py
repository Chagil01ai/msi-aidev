import os
import re
import anthropic
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple
import json
import seaborn as sns

# Set up Anthropic client
# You can set up a .env file with your API key to keep it private, and import it like so:
from dotenv import load_dotenv
load_dotenv()

my_api_key = os.getenv("ANTHROPIC_API_KEY")

if not my_api_key:
    raise ValueError("ANTHROPIC_API_KEY is not set in the environment variables.")

#Initialize Anthropic event
client = anthropic.Anthropic(
    api_key=my_api_key
)

import pypdf
import re

pdf_path = "c:/Users/cgilb/ai-projects/Claudy/data/Sample Sublease Agreement.pdf"

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def clean_text(text):
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove page numbers
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    return text.strip()

def prepare_for_llm(text, max_tokens=180000):
    # Truncate text to fit within token limit (approximate)
    return text[:max_tokens * 4]  # Assuming average of 4 characters per token

def get_llm_text(path):
    extracted_text = extract_text_from_pdf(path)
    cleaned_text = clean_text(extracted_text)
    llm_ready_text = prepare_for_llm(cleaned_text)
    return llm_ready_text

# You can now use get_llm_text in your LLM prompt
text = get_llm_text(pdf_path)

def basic_summarize(text, max_tokens=1000):

    # Prompt the model to summarize the text
    prompt = f"""Summarize the following text in bullet points. Focus on the main ideas and key details:
    {text}
    """

    response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            system="You are a legal analyst known for highly accurate and detailed summaries of legal documents.",
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                },
                {
                    "role": "assistant",
                    "content": "Here is the summary of the legal document: <summary>" 
                }
            ],
            stop_sequences=["</summary>"]
        )

    return response.content[0].text

basic_response = basic_summarize(text, max_tokens=1000)

print(basic_response)

