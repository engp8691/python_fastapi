# python_fastapi

## Python fast API

### Steps to check

**_NOTE:_**
My codes tested on my local machine under Python 3.13.2
The backend Database is PostgreSQL of postgres:latest in Docker
the .env file is changed to env.sample file. Change the values according to your DB.
Follow the following steps and run the script to create the DB and tables.

- Step 1: `python -m venv venv`
- step 2: `source venv/bin/activate`
- Step 3: go inside the `fastapi_python` folder and install all the packages required with command of `pip install -r requirements.txt`
- Step 4: initiate the database by `python -m app.db.create_tables`
- Step 5: run the server by `uvicorn app.main:app --reload`
- Step 6: run unit tests by `pytest --cov=app --cov-report=html`
- Step 7: check the coverate under `htmlcov/index.html`
- Step 8: swagger docs under `http://localhost:8000/docs`
