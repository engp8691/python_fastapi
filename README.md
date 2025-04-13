# python_fastapi

## Python fast API

### Steps to check

- Step 1: `python -m venv venv`
- step 2: `source venv/bin/activate`
- Step 3: install all the packages required by `pip install -r requirements.txt`
- Step 4: initiate the database by `python -m app.db.create_tables`
- Step 5: run the server by `uvicorn app.main:app --reload`
- Step 6: run unit tests by `pytest --cov=app --cov-report=html`
- Step 7: check the coverate under `htmlcov/index.html`
- Step 8: swagger docs under `http://localhost:8000/docs`