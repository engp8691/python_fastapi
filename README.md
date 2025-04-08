# python_fastapi
Python fast API


Step 1: `python -m venv venv`
step 2: `source venv/bin/activate`
Step 3: install all the packages required
Step 4: run the server by `uvicorn app.main:app --reload`
Step 5: run unit tests by `pytest --cov=app --cov-report=html`
Step 6: check the coverate under `htmlcov/index.html`
Step 7: python -m app.db.create_tables