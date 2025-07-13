import os
import json
from pathlib import Path
from cookiecutter.main import cookiecutter
from cookiecutter.generate import generate_context
from cookiecutter.prompt import read_user_variable
from typing import Dict, Any

class MLOpsTemplateBuilder:
    def __init__(self):
        self.template_dir = Path.cwd() / "templates"
        self.context = {
            "project_name": "",
            "project_description": "",
            "author_name": "",
            "author_email": "",
            "cloud_provider": "", 
            "experiment_tracker": "", 
            "ci_provider": "", 
            "python_version": "3.9",
            "license": "MIT",
        }

    def prompt_user(self) -> Dict[str, Any]:
        print("\nWelcome to the MLOps Project Template Builder!\n")
        
        for key in self.context:
            prompt = f"Please enter {key.replace('_', ' ')}: "
            if key in ["cloud_provider", "experiment_tracker", "ci_provider"]:
                choices = self.get_choices(key)
                prompt += f" ({', '.join(choices)})"
            
            self.context[key] = read_user_variable(key, prompt)

        return self.context

    def get_choices(self, field: str) -> list:
        choices = {
            "cloud_provider": ["aws", "azure", "gcp", "local"],
            "experiment_tracker": ["mlflow", "wandb", "neptune"],
            "ci_provider": ["github", "gitlab"],
        }
        return choices.get(field, [])

    def create_template(self, output_dir: str = "."):
        self.template_dir.mkdir(exist_ok=True)
        cookiecutter(
            str(self.template_dir),
            no_input=True,
            extra_context=self.context,
            output_dir=output_dir
        )

    def generate(self):
        self.context = self.prompt_user()
        self.create_template()

if __name__ == "__main__":
    builder = MLOpsTemplateBuilder()
    builder.generate()
