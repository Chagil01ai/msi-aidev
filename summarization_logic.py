import pypdf
import re
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract_text_from_pdf(file):
    reader = pypdf.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    return text.strip()

def summarize_pdf(file):
    raw = extract_text_from_pdf(file)
    clean = clean_text(raw)
    prompt = f"Summarize this: {clean[:2000]}"  # limit tokens
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
