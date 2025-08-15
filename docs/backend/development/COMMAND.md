## Development Commands

### Start venv
.\backend\venv\Scripts\activate

### Start Server
```bash
python -m app.main
```
Server runs on: http://localhost:8000

### Install Dependencies
```bash
# First activate the virtual environment
cd backend
./venv/Scripts/activate

# Then install dependencies
pip install -r requirements.txt
```

### Install Individual Packages
```bash
# Activate virtual environment first
cd backend
./venv/Scripts/activate

# Install specific package (e.g., pytest)
pip install pytest
```