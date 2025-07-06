@echo off
echo Installing Project Dependencies...

:: Step 1: Create virtual environment
echo 1. Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

:: Step 2: Upgrade pip
echo 2. Upgrading pip...
pip install --upgrade pip --only-binary :all:

:: Step 3: Install pre-built wheels
echo 3. Installing pre-built packages...
pip install --only-binary :all: numpy pandas scikit-learn matplotlib

:: Step 4: Install basic packages
echo 4. Installing basic packages...
pip install cookiecutter pyyaml jinja2 python-dotenv black pytest

:: Step 5: Install remaining packages
echo 5. Installing remaining packages...
pip install fastapi uvicorn bentoml python-multipart requests python-jose[cryptography] passlib[bcrypt]

echo Installation complete!
pause


