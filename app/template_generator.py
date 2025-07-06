import os
import json
import shutil
from pathlib import Path
from typing import Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_template(config: Dict) -> str:
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
    
    Returns:
        str: Path to the generated project directory
    
    Raises:
        ValueError: If required configuration is missing
        OSError: If file operations fail
    """
    try:
        # Validate required fields
        required_fields = [
            'project_name', 'project_description', 'open_source_license',
            'cloud_provider', 'experiment_tracker', 'python_version',
            'include_docker', 'include_ci', 'include_tests', 'include_notebooks'
        ]
        
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required configuration: {field}")

        # Create project directory
        project_name = config['project_name']
        project_dir = Path(project_name)
        
        if project_dir.exists():
            raise OSError(f"Project directory '{project_name}' already exists")
            
        project_dir.mkdir(exist_ok=True)
        logger.info(f"Creating project directory at {project_dir}")

        # Copy base template structure
        # Get the absolute path of the current file
        current_file = Path(__file__).resolve()
        # Go up to the project root (where templates folder is located)
        project_root = current_file.parent.parent
        template_dir = project_root / 'templates' / 'project_template'
        
        if not template_dir.exists():
            raise OSError(f"Template directory not found: {template_dir}")
            
        # Copy all files from template directory
        for item in template_dir.iterdir():
            if item.name == '{{cookiecutter.project_name}}':
                # Copy the contents of the project_name directory
                # Create a temporary directory with the actual project name
                temp_dir = template_dir / project_name
                temp_dir.mkdir(exist_ok=True)
                
                # Copy all files from the template directory
                for subitem in (item / '{{cookiecutter.project_name}}').iterdir():
                    if subitem.is_dir():
                        shutil.copytree(subitem, temp_dir / subitem.name, dirs_exist_ok=True)
                    else:
                        # Replace placeholder in file content
                        with open(subitem, 'r') as f:
                            content = f.read()
                        content = content.replace('{{cookiecutter.project_name}}', project_name)
                        with open(temp_dir / subitem.name, 'w') as f:
                            f.write(content)
                
                # Copy from temp directory to project
                for subitem in temp_dir.iterdir():
                    if subitem.is_dir():
                        shutil.copytree(subitem, project_dir / subitem.name, dirs_exist_ok=True)
                    else:
                        shutil.copy2(subitem, project_dir / subitem.name)
                
                # Clean up temp directory
                shutil.rmtree(temp_dir)
            elif item.is_dir():
                shutil.copytree(item, project_dir / item.name, dirs_exist_ok=True)
            else:
                # Replace placeholder in file content if it exists
                if '{{cookiecutter.project_name}}' in item.name:
                    new_name = item.name.replace('{{cookiecutter.project_name}}', project_name)
                    shutil.copy2(item, project_dir / new_name)
                else:
                    shutil.copy2(item, project_dir / item.name)
        logger.info("Copied base template structure")

        # Generate README.md
        with open(project_dir / 'README.md', 'w') as f:
            f.write(f"# {project_name}\n\n")
            f.write(f"{config['project_description']}\n\n")
            f.write("""## Project Structure
```
.
├── src/              # Source code
│   ├── __init__.py
│   ├── data/         # Data processing
│   ├── models/       # ML models
│   └── utils/        # Utility functions
├── tests/           # Test files
└── requirements.txt # Project dependencies
```
""")
        logger.info("Generated README.md")

        # Generate requirements.txt
        with open(project_dir / 'requirements.txt', 'w') as f:
            base_requirements = [
                "numpy>=1.26.0",
                "pandas>=2.0.0",
                "scikit-learn>=1.3.0",
                "mlflow>=2.5.0",
                "pytest>=7.0.0",
                "black>=23.0.0",
                "isort>=5.10.0",
                "flake8>=6.0.0",
            ]
            
            # Add additional requirements based on configuration
            if config['experiment_tracker'] == 'TensorBoard':
                base_requirements.append("tensorboard>=2.13.0")
            elif config['experiment_tracker'] == 'WandB':
                base_requirements.append("wandb>=0.15.0")
                
            if config['include_notebooks'] == 'yes':
                base_requirements.extend([
                    "jupyter>=1.0.0",
                    "ipykernel>=6.0.0"
                ])
                
            f.write("\n".join(base_requirements))
        logger.info("Generated requirements.txt")

        # Generate .gitignore
        with open(project_dir / '.gitignore', 'w') as f:
            gitignore_content = [
                "__pycache__/*",
                "*.pyc",
                ".env",
                ".venv/*",
                "venv/*",
                "*.log",
                "mlruns/*",
                "*.ipynb_checkpoints/*",
                ".pytest_cache/*",
                ".coverage",
                "htmlcov/*",
                "dist/*",
                "build/*",
                "*.egg-info/*"
            ]
            f.write("\n".join(gitignore_content))
        logger.info("Generated .gitignore")

        # Generate .env file if needed
        if config['cloud_provider'] != 'None':
            with open(project_dir / '.env', 'w') as f:
                f.write("# Cloud Provider Configuration\n")
                if config['cloud_provider'] == 'AWS':
                    f.write("AWS_ACCESS_KEY_ID=your_access_key\n")
                    f.write("AWS_SECRET_ACCESS_KEY=your_secret_key\n")
                elif config['cloud_provider'] == 'GCP':
                    f.write("GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json\n")
                elif config['cloud_provider'] == 'Azure':
                    f.write("AZURE_STORAGE_CONNECTION_STRING=your_connection_string\n")
            logger.info("Generated .env file")

        # Generate Dockerfile if requested
        if config['include_docker'] == 'yes':
            docker_content = [
                "FROM python:3.11-slim",
                "",
                "WORKDIR /app",
                "",
                "COPY requirements.txt .",
                "RUN pip install --no-cache-dir -r requirements.txt",
                "",
                "COPY . .",
                "",
                "CMD [\"python\", \"src/train.py\"]"
            ]
            with open(project_dir / 'Dockerfile', 'w') as f:
                f.write("\n".join(docker_content))
            logger.info("Generated Dockerfile")

        logger.info(f"Template generation completed successfully for {project_name}")
        return str(project_dir.absolute())

    except Exception as e:
        logger.error(f"Error generating template: {str(e)}")
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