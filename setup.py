from setuptools import setup, find_packages

setup(
    name="mlops-template-builder",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "cookiecutter>=2.3.0",
        "pyyaml>=6.0.1",
        "jinja2>=3.1.2",
        "python-dotenv>=1.0.0",
        "black>=23.7.0",
        "pytest>=7.4.0",
        "great_expectations>=0.17.18",
        "mlflow>=2.5.0",
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "bentoml>=1.0.22",
        "python-multipart>=0.0.6",
        "requests>=2.31.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "pydantic>=2.4.2",
        "httpx>=0.25.1",
        "numpy>=1.24.3",
        "pandas>=2.0.0",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.7.0"
    ],
    entry_points={
        'console_scripts': [
            'mlops-template-builder=template_builder:main'
        ]
    },
    python_requires='>=3.9',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
