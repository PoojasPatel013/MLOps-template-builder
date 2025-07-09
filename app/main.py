from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import json
import shutil
from typing import Dict
from .template_generator import generate_template

app = FastAPI(title="MLOps Template Builder")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add favicon route
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

templates = Jinja2Templates(directory="templates")

# Load cookiecutter.json
with open(Path(__file__).parent.parent / "templates" / "project_template" / "{{cookiecutter.project_name}}" / "cookiecutter.json", "r") as f:
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
    try:
        data = await request.json()
        
        # Validate required fields
        required_fields = [
            'project_name', 'project_description', 'open_source_license',
            'cloud_provider', 'experiment_tracker', 'python_version',
            'include_docker', 'include_ci', 'include_tests', 'include_notebooks'
        ]
        
        for field in required_fields:
            if field not in data:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required field: {field}"
                )

        # Generate the template
        project_path = generate_template(data)
        
        return {
            "status": "success",
            "message": f"Template generated successfully at {project_path}",
            "project_path": project_path
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating template: {str(e)}"
        )
