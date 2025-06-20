# MSI-AI Dev

This repo contains experiments and scripts for AI-powered tools and agents using the Claude API.

## Current scripts

- `chatbot_v1.py`: Terminal chatbot with Claude
- `summarization_claude.py`: PDF summarizer with Claude

## How to run

1. Create a `.env` file with your `ANTHROPIC_API_KEY`.
2. Activate your conda env: `conda activate ai-env`
3. Install requirements: `pip install -r requirements.txt` or manually install the basics: `pip install anthropic python-dotenv pypdf`
4. Run: `python chatbot_v1.py`
