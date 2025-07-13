from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
import json
import shutil
import logging
from typing import Dict, Any
from .template_generator import generate_template

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MLOps Template Builder")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add favicon route
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

# Templates
templates = Jinja2Templates(directory="templates")

# Load cookiecutter.json
try:
    with open(Path(__file__).parent.parent / "templates" / "cookiecutter.json", "r") as f:
        config = json.load(f)
except Exception as e:
    logger.error(f"Error loading cookiecutter.json: {str(e)}")
    raise HTTPException(
        status_code=500,
        detail={"error": f"Failed to load configuration: {str(e)}"}
    )

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "config": config})

@app.post("/generate")
async def handle_template_generation(request: Request):
    try:
        logger.info("Received template generation request")
        data = await request.json()
        logger.info(f"Request data: {json.dumps(data, indent=2)}")
        
        # Validate required fields
        required_fields = [
            'project_name', 'project_description', 'open_source_license',
            'cloud_provider', 'experiment_tracker', 'python_version',
            'include_docker', 'include_ci', 'include_tests', 'include_notebooks',
            'target_directory'
        ]
        
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field: {field}")
                raise HTTPException(
                    status_code=400,
                    detail={"error": f"Missing required field: {field}"}
                )

        # Validate target directory
        target_directory = data['target_directory']
        if not target_directory:
            raise HTTPException(
                status_code=400,
                detail={"error": "Target directory not specified"}
            )

        try:
            # Generate the template
            project_path = await generate_template(data, target_directory)
            logger.info(f"Template generated successfully at: {project_path}")
            
            return {
                "message": "Template generated successfully",
                "project_path": str(project_path),
                "success": True
            }
        except Exception as e:
            logger.error(f"Error generating template: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail={
                    "error": f"Failed to generate template: {str(e)}",
                    "details": str(e)
                }
            )

    except HTTPException as e:
        logger.error(f"HTTP error: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "An unexpected error occurred",
                "details": str(e)
            }
        )
