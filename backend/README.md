# Backend

Small README for the `backend` service (FastAPI + Uvicorn).

Overview
- FastAPI application located in `backend/app`.
- Uses PostgreSQL (SQLAlchemy / asyncpg) and Neo4j (bolt driver) plus optional OpenAI integration.

Requirements
- Python 3.11+ (match your environment)
- Dependencies in `backend/requirements.txt`
- Postgres and Neo4j instances available (or use the included docker compose files)

Environment variables
- DATABASE_URL: e.g. `postgresql+asyncpg://user:pass@localhost:5432/dbname`
- NEO4J_URI: e.g. `bolt://localhost:7687`
- NEO4J_USER
- NEO4J_PASSWORD
- OPENAI_API_KEY (optional)

Local setup
1. Create and activate a virtual environment:

   python -m venv .venv
   source .venv/bin/activate

2. Install dependencies:

   pip install -r requirements.txt

3. Prepare databases (example using alembic migrations):
```
   # run from repository root
   cd backend
   alembic -c alembic.ini upgrade head
```
Run (development)
- Preferred (from repository root):
```
  # ensure PYTHONPATH includes backend so `app` package is importable
  export PYTHONPATH="$PWD/backend"
  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Or run from inside `backend` dir:
```
  cd backend
  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
VS Code debugging
- There is a launch configuration: `Python: Uvicorn (FastAPI)` in `.vscode/launch.json` that runs uvicorn as a module with cwd set so relative imports work. Use that for breakpoints and step-through debugging.

Docker / Production
- See `docker-compose.yml` and `docker-compose-prod.yml` in the repository root. They can start dependent services (Postgres, Neo4j) and the backend.

Troubleshooting
- ImportError: "attempted relative import with no known parent package": This usually means the app wasn't run as a package. Ensure you either:
  - Run uvicorn as a module from the project root (with `PYTHONPATH` set to include `backend`), e.g. `python -m uvicorn app.main:app`, or
  - Set your working directory to `backend` when launching.

- Database connection issues: verify `DATABASE_URL` and that Postgres is reachable.

Notes
- Secrets and credentials should be stored securely. See the `secrets/README.md` in the repo for guidance.

```
# This should return "Not authenticate"
http://localhost:8000/api/context/one

# Should pop up Google Login
http://localhost:8000/api/auth/login/google

# Should pop up GitHub Login
http://localhost:8000/api/auth/login/github