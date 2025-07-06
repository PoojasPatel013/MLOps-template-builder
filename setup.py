from setuptools import setup, find_packages
import subprocess
import sys
import os

def install_ml_packages():
    ml_requirements = [
        "numpy==1.26.4",
        "pandas==2.1.4",
        "scikit-learn==1.3.2",
        "matplotlib==3.8.2"
    ]
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--no-cache-dir'] + ml_requirements)

def install_basic_packages():
    basic_requirements = [
        "cookiecutter>=2.3.0",
        "pyyaml>=6.0.1",
        "jinja2>=3.1.2",
        "python-dotenv>=1.0.0",
        "black>=23.7.0",
        "pytest>=7.4.0",
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "bentoml>=1.0.22",
        "python-multipart>=0.0.6",
        "requests>=2.31.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4"
    ]
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--no-cache-dir'] + basic_requirements)

class CustomInstallCommand(install):
    def run(self):
        install_ml_packages()
        install_basic_packages()
        install.run(self)

setup(
    name="mlops-template-builder",
    version="0.1.0",
    packages=find_packages(),
    cmdclass={'install': CustomInstallCommand},
    install_requires=[
        # These will be handled by our custom install
        "cookiecutter>=2.3.0",
        "pyyaml>=6.0.1",
        "jinja2>=3.1.2",
        "python-dotenv>=1.0.0",
        "black>=23.7.0",
        "pytest>=7.4.0",
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "bentoml>=1.0.22",
        "python-multipart>=0.0.6",
        "requests>=2.31.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4"
    ],
    entry_points={
        'console_scripts': [
            'mlops-template-builder=template_builder:main'
        ]
    },
    python_requires='>=3.11',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)