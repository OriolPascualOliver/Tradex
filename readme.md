# Tradex

## Running with Docker

The project uses `docker-compose` to start the API and database services. Ensure the `.env` file is present, then start everything with:

```bash
docker-compose up --build
```

The API will be available at http://localhost:8000 and a PostgreSQL database will be created with the credentials defined in `.env`.

To stop and remove containers:

```bash
docker-compose down
```

## Running tests

Install the application and development dependencies:

```bash
pip install -r backend/requirements.txt -r requirements-dev.txt
```

Then execute the test suite:

```bash
pytest backend/tests
```
