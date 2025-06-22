from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from summarization_claude import basic_summarize, get_llm_text
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# FastAPI can serve static files if needed
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "summary": ""})

@app.post("/", response_class=HTMLResponse)
async def summarize(request: Request, pdf_path: str = Form(...)):
    text = get_llm_text(pdf_path)
    summary = basic_summarize(text)
    return templates.TemplateResponse("index.html", {"request": request, "summary": summary})
