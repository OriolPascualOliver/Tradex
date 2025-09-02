# Tradex

## Backend Architecture

The backend is built with [FastAPI](https://fastapi.tiangolo.com/) and
[SQLAlchemy](https://www.sqlalchemy.org/) for database interactions.
Configuration is handled via `pydantic-settings`, and Alembic manages
database migrations. The application is structured into modular routers
(`backend/api/routers`) for features such as authentication, tasks,
contact, and health checks. Models and schemas live under
`backend/api/models` and `backend/api/schemas` respectively, while core
configuration and database setup are in `backend/core`.

## Environment variables

The API reads configuration from environment variables or a `.env` file:

- `DATABASE_URL` – SQLAlchemy database URL. Defaults to
  `sqlite:///./sql_app.db` for local development.
- `SECRET_KEY` – secret used to sign JWT access tokens.

Additional variables such as `POSTGRES_USER`, `POSTGRES_PASSWORD`, and
`POSTGRES_DB` are used when running via Docker.

## Running the API locally (without Docker)

1. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```

2. **Configure environment variables**

   Create a `.env` file or export variables in your shell. At minimum
   set `DATABASE_URL` (e.g. `sqlite:///./sql_app.db`) and `SECRET_KEY`.

3. **Run database migrations**

   ```bash
   alembic -c backend/alembic.ini upgrade head
   ```

4. **Start the development server**

   ```bash
   uvicorn main:app --reload
   ```

The API will now be available at http://localhost:8000.

## API Documentation

FastAPI automatically provides interactive API docs at
`http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc`.

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
