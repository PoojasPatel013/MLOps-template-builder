import json
import os
import shutil
from pathlib import Path
from typing import Dict
import aiofiles
import logging
from aiofiles import os as aio_os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def generate_template(config: Dict, target_directory: str) -> str:
    """
    Generate a new MLOps project template based on the provided configuration.
    
    Args:
        config: Dictionary containing template configuration
            - project_name: Name of the project
            - project_description: Project description
            - open_source_license: License type
            - cloud_provider: Cloud provider
            - experiment_tracker: Experiment tracking tool
            - python_version: Python version
            - include_docker: Include Docker support
            - include_ci: Include CI/CD
            - include_tests: Include tests
            - include_notebooks: Include notebooks
        target_directory: Path to the directory where the project should be created
    
    Returns:
        str: Path to the generated project directory
    
    Raises:
        ValueError: If required configuration is missing or invalid
        OSError: If file operations fail
        PermissionError: If insufficient permissions
    """
    try:
        logger.info(f"Starting template generation with config: {json.dumps(config, indent=2)}")
        
        # Validate required fields
        required_fields = [
            'project_name', 'project_description', 'open_source_license',
            'cloud_provider', 'experiment_tracker', 'python_version',
            'include_docker', 'include_ci', 'include_tests', 'include_notebooks'
        ]
        
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")

        # Validate and prepare target directory
        target_path = Path(target_directory)
        if not target_path.exists():
            raise OSError(f"Target directory does not exist: {target_directory}")
        if not target_path.is_dir():
            raise OSError(f"Target path is not a directory: {target_directory}")
        
        # Create project directory
        project_name = config['project_name'].strip()
        if not project_name:
            raise ValueError("Project name cannot be empty")
            
        project_dir = target_path / project_name
        if project_dir.exists():
            raise OSError(f"Project directory '{project_name}' already exists in {target_directory}")

        try:
            project_dir.mkdir(parents=True, exist_ok=False)
            logger.info(f"Successfully created project directory at {project_dir}")
            
            # Copy template files
            template_dir = Path(__file__).parent / "templates"
            if not template_dir.exists():
                raise OSError("Template directory not found")

            # Copy files from template directory
            for item in template_dir.iterdir():
                if item.is_dir():
                    shutil.copytree(item, project_dir / item.name, dirs_exist_ok=True)
                else:
                    # Process template files
                    content = await aiofiles.open(item, 'r').read()
                    content = content.replace('{{cookiecutter.project_name}}', project_name)
                    await aiofiles.open(project_dir / item.name, 'w').write(content)

            # Generate additional files
            await generate_additional_files(project_dir, config)
            
            return str(project_dir)
        except Exception as e:
            logger.error(f"Error creating project files: {str(e)}")
            if project_dir.exists():
                try:
                    shutil.rmtree(str(project_dir))
                except:
                    logger.error("Failed to clean up project directory")
            raise
    except Exception as e:
        logger.error(f"Template generation failed: {str(e)}", exc_info=True)
        raise

async def generate_additional_files(project_dir: Path, config: Dict):
    """Generate additional project files based on configuration."""
    try:
        # Generate README.md
        readme_content = f"""# {config['project_name']}

{config['project_description']}

## Project Structure
- src/: Source code
- tests/: Test files
- notebooks/: Jupyter notebooks
- .github/: GitHub Actions CI/CD
"""
        await aiofiles.open(project_dir / 'README.md', 'w').write(readme_content)

        # Generate requirements.txt
        requirements = [
            'numpy',
            'pandas',
            'scikit-learn',
            'fastapi',
            'uvicorn'
        ]
        if config['include_docker']:
            requirements.append('docker')
        if config['experiment_tracker'] == 'mlflow':
            requirements.append('mlflow')
        
        await aiofiles.open(project_dir / 'requirements.txt', 'w').write('\n'.join(requirements))

        # Generate .gitignore
        gitignore_content = """__pycache__/
*.py[cod]
*$py.class
.DS_Store
.env
.venv/
venv/
"""
        await aiofiles.open(project_dir / '.gitignore', 'w').write(gitignore_content)

        # Generate .env
        env_content = """# Environment variables
PYTHONPATH=${PYTHONPATH}:${PWD}
"""
        await aiofiles.open(project_dir / '.env', 'w').write(env_content)

        # Generate Dockerfile if requested
        if config['include_docker']:
            docker_content = """FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
            await aiofiles.open(project_dir / 'Dockerfile', 'w').write(docker_content)

    except Exception as e:
        logger.error(f"Error generating additional files: {str(e)}")
        raise

if __name__ == "__main__":
    # Example usage
    config = {
        "project_name": "test_project",
        "project_description": "Test MLOps project",
        "open_source_license": "MIT",
        "cloud_provider": "None",
        "experiment_tracker": "MLflow",
        "python_version": "3.11",
        "include_docker": "yes",
        "include_ci": "no",
        "include_tests": "yes",
        "include_notebooks": "yes"
    }
    
    try:
        project_path = generate_template(config)
        print(f"Project generated at: {project_path}")
    except Exception as e:
        print(f"Error: {str(e)}")