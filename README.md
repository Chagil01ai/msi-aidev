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

## 🚀 Roadmap

This project is my AI Playground using Claude API.

**Current Capabilities:**

- ✅ Terminal-based chatbot (`chatbot_v1.py`)
- ✅ PDF text extraction and summarization (`summarization_claude.py`)

**Planned Enhancements:**

- [ ] Build a simple web app interface using Flask or FastAPI.
- [ ] Add file upload capability for summarization.
- [ ] Improve prompt engineering for more accurate summaries.
- [ ] Save chat or summary history to a local file or database.
- [ ] Deploy the web app online (using Heroku, Render, or similar).
- [ ] Add unit tests and basic error handling.

---

**Want to contribute ideas or features?**  
Create an [issue][def] or submit a pull request!

[def]: https://github.com/Chagil01ai/msi-aidev/issues
