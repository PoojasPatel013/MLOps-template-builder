# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Project Structure
```
.
├── src/              # Source code
│   ├── __init__.py
│   ├── data/         # Data processing
│   ├── models/       # ML models
│   └── utils/        # Utility functions
├── tests/           # Test files
├── notebooks/       # Jupyter notebooks
├── config/          # Configuration files
├── requirements.txt # Project dependencies
└── .gitignore      # Git ignore file
```

## Setup
1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
venv\Scripts\activate     # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Train models:
```bash
python src/train.py
```

2. Run tests:
```bash
pytest tests/
```

## License
{{ cookiecutter.open_source_license }}
