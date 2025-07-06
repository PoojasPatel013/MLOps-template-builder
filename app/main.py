from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json

app = FastAPI(title="MLOps Template Builder")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Load cookiecutter.json
with open("templates/template/cookiecutter.json", "r") as f:
    config = json.load(f)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "config": config
        }
    )

@app.post("/generate")
async def generate_template(request: Request):
    data = await request.json()
    # TODO: Implement template generation logic
    return {"status": "success", "message": "Template generated successfully!"}
