import json
import os
import shutil
from pathlib import Path
from typing import Dict
import aiofiles
from aiofiles import os as aio_os
import logging

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
                raise ValueError(f"Missing required configuration: {field}")

        # Clean up project name (remove spaces, special characters)
        project_name = config['project_name'].strip()
        if not project_name:
            raise ValueError("Project name cannot be empty")
        
        # Clean up project name
        project_name = config['project_name'].strip()
        if not project_name:
            raise ValueError("Project name cannot be empty")
        
        # Validate target directory
        target_path = Path(target_directory)
        if not target_path.exists():
            raise OSError(f"Target directory does not exist: {target_directory}")
        if not target_path.is_dir():
            raise OSError(f"Target path is not a directory: {target_directory}")

        # Create project directory
        project_dir = target_path / project_name
        
        if project_dir.exists():
            raise OSError(f"Project directory '{project_name}' already exists in {target_directory}")
            
        try:
            # Create project directory with proper permissions
            project_dir.mkdir(parents=True, exist_ok=False)
            logger.info(f"Successfully created project directory at {project_dir}")
            
            # Get template directory
            template_dir = Path(__file__).parent / "templates"
            if not template_dir.exists():
                raise OSError("Template directory not found")
                
            # Copy template files
            for item in template_dir.iterdir():
                if item.name == '{{cookiecutter.project_name}}':
                    # Create temporary directory for processing
                    temp_dir = project_dir / "_temp"
                    temp_dir.mkdir(exist_ok=True)
                    
                    # Copy and process files
                    async with aiofiles.threadpool.wrap(os.scandir)(item / '{{cookiecutter.project_name}}') as entries:
                        async for subitem in entries:
                            if subitem.is_dir():
                                # Copy directories recursively
                                shutil.copytree(subitem.path, temp_dir / subitem.name, dirs_exist_ok=True)
                            else:
                                # Process and copy files
                                async with aiofiles.open(subitem.path, 'r') as f:
                                    content = await f.read()
                                content = content.replace('{{cookiecutter.project_name}}', project_name)
                                async with aiofiles.open(temp_dir / subitem.name, 'w') as f:
                                    await f.write(content)
                    
                    # Move processed files to project directory
                    for item in temp_dir.iterdir():
                        shutil.move(str(item), str(project_dir))
                    shutil.rmtree(str(temp_dir))
                    
            # Generate additional files
            await generate_additional_files(project_dir, config)
            
            return str(project_dir)
            
        except PermissionError as e:
            logger.error(f"Permission error: {str(e)}")
            raise PermissionError(f"Insufficient permissions to create project in {target_directory}")
            
        except Exception as e:
            logger.error(f"Error creating project directory: {str(e)}")
            if project_dir.exists():
                try:
                    shutil.rmtree(str(project_dir))
                except:
                    logger.error("Failed to clean up project directory")
            raise OSError(f"Failed to create project directory: {str(e)}")

        # Get the absolute path of the current file
        current_file = Path(__file__).resolve()
        # Go up to the project root (where templates folder is located)
        project_root = current_file.parent.parent
        template_dir = project_root / 'templates' / 'project_template'
        logger.info(f"Using template directory: {template_dir}")
        
        if not template_dir.exists():
            raise OSError(f"Template directory not found: {template_dir}")
            
        # Copy all files from template directory
        for item in template_dir.iterdir():
            if item.name == '{{cookiecutter.project_name}}':
                # Copy the contents of the project_name directory
                # Create a temporary directory with the actual project name
                temp_dir = template_dir / project_name
                logger.info(f"Creating temp directory: {temp_dir}")
                
                try:
                    temp_dir.mkdir(exist_ok=True)
                    
                    # Copy all files from the template directory
                    async with aiofiles.threadpool.wrap(os.scandir)(item / '{{cookiecutter.project_name}}') as entries:
                        async for subitem in entries:
                            if subitem.is_dir():
                                try:
                                    shutil.copytree(subitem.path, temp_dir / subitem.name, dirs_exist_ok=True)
                                    logger.info(f"Copied directory: {subitem.name}")
                                except Exception as e:
                                    logger.error(f"Error copying directory {subitem.name}: {str(e)}")
                                    raise
                            else:
                                # Replace placeholder in file content
                                try:
                                    async with aiofiles.open(subitem.path, 'r') as f:
                                        content = await f.read()
                                    content = content.replace('{{cookiecutter.project_name}}', project_name)
                                    async with aiofiles.open(temp_dir / subitem.name, 'w') as f:
                                        await f.write(content)
                                    logger.info(f"Processed file: {subitem.name}")
                                except Exception as e:
                                    logger.error(f"Error processing file {subitem.name}: {str(e)}")
                                    raise
                    
                    # Copy from temp directory to project
                    async with aiofiles.threadpool.wrap(os.scandir)(temp_dir) as entries:
                        async for subitem in entries:
                            if subitem.is_dir():
                                try:
                                    shutil.copytree(subitem.path, project_dir / subitem.name, dirs_exist_ok=True)
                                    logger.info(f"Copied directory to project: {subitem.name}")
                                except Exception as e:
                                    logger.error(f"Error copying directory to project {subitem.name}: {str(e)}")
                                    raise
                            else:
                                try:
                                    shutil.copy2(subitem.path, project_dir / subitem.name)
                                    logger.info(f"Copied file to project: {subitem.name}")
                                except Exception as e:
                                    logger.error(f"Error copying file to project {subitem.name}: {str(e)}")
                                    raise
                    
                    # Clean up temp directory
                    try:
                        shutil.rmtree(temp_dir)
                        logger.info(f"Cleaned up temp directory: {temp_dir}")
                    except Exception as e:
                        logger.error(f"Error cleaning up temp directory: {str(e)}")
                        raise
                except Exception as e:
                    logger.error(f"Error processing template directory: {str(e)}")
                    raise
            elif item.is_dir():
                try:
                    shutil.copytree(item, project_dir / item.name, dirs_exist_ok=True)
                    logger.info(f"Copied base directory: {item.name}")
                except Exception as e:
                    logger.error(f"Error copying base directory {item.name}: {str(e)}")
                    raise
            else:
                # Replace placeholder in file content if it exists
                try:
                    if '{{cookiecutter.project_name}}' in item.name:
                        new_name = item.name.replace('{{cookiecutter.project_name}}', project_name)
                        shutil.copy2(item, project_dir / new_name)
                        logger.info(f"Copied renamed file: {item.name} -> {new_name}")
                    else:
                        shutil.copy2(item, project_dir / item.name)
                        logger.info(f"Copied file: {item.name}")
                except Exception as e:
                    logger.error(f"Error copying file {item.name}: {str(e)}")
                    raise

        # Generate README.md
        async with aiofiles.open(project_dir / 'README.md', 'w') as f:
            await f.write(f"# {project_name}\n\n")
            await f.write(f"{config['project_description']}\n\n")
            await f.write("""## Project Structure
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
        async with aiofiles.open(project_dir / 'requirements.txt', 'w') as f:
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
                
            await f.write("\n".join(base_requirements))
        logger.info("Generated requirements.txt")

        # Generate .gitignore
        async with aiofiles.open(project_dir / '.gitignore', 'w') as f:
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
            await f.write("\n".join(gitignore_content))
        logger.info("Generated .gitignore")

        # Generate .env file if needed
        if config['cloud_provider'] != 'None':
            async with aiofiles.open(project_dir / '.env', 'w') as f:
                await f.write("# Cloud Provider Configuration\n")
                if config['cloud_provider'] == 'AWS':
                    await f.write("AWS_ACCESS_KEY_ID=your_access_key\n")
                    await f.write("AWS_SECRET_ACCESS_KEY=your_secret_key\n")
                elif config['cloud_provider'] == 'GCP':
                    await f.write("GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json\n")
                elif config['cloud_provider'] == 'Azure':
                    await f.write("AZURE_STORAGE_CONNECTION_STRING=your_connection_string\n")
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
            docker_content_str = "\n".join(docker_content)
            async with aiofiles.open(project_dir / 'Dockerfile', 'w') as f:
                await f.write(docker_content_str)
            logger.info("Generated Dockerfile")

        logger.info(f"Template generation completed successfully for {project_name}")
        return str(project_dir)

    except Exception as e:
        logger.error(f"Error generating template: {str(e)}")
        raise ValueError(f"Error generating template: {str(e)}")

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