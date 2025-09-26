# Repository Guidelines

## Project Structure & Module Organization
The repository splits the product into a FastAPI backend and a React/Vite frontend. Backend application code sits in `backend/app` with feature modules under `api/`, `models/`, `schemas/`, and async database helpers in `db/`. Alembic migration scripts live in `backend/migrations`. Frontend code sits in `frontend/src`, with route components under `pages/` and assets in `src/assets/`. Reference materials and product specs reside in `docs/` and `specs.md`. Container assets are under `docker/`, while `logs/` and `secrets/` are reserved for local artifacts and never checked in.

## Build, Test, and Development Commands
Install backend dependencies with `python -m venv .venv && source .venv/bin/activate && pip install -r backend/requirements.txt`. Run the API during development via `PYTHONPATH="$PWD/backend" python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`. Apply database migrations with `alembic -c backend/alembic.ini upgrade head`. For the frontend, run `npm install` once, then `npm run dev` for local development, `npm run build` to create production assets, and `npm run lint` to enforce ESLint rules. Use `docker compose up` for an end-to-end stack when databases are needed.

## Coding Style & Naming Conventions
Write backend Python code with PEP 8 spacing (4-space indents), explicit type hints, and descriptive module names (`services/graph_service.py`). Prefer Pydantic models for request/response contracts and keep settings in `core/config.py`. Frontend TypeScript components use PascalCase filenames (`Home.tsx`), 2-space indents, and React function components. Keep CSS modules scoped inside `src/` and share constants via `src/assets/config`. Run ESLint before opening a PR; align imports using the default Vite/TypeScript ordering.

## Testing Guidelines
Add backend tests under `backend/tests` using `pytest`, mirroring the `app` package structure; name files `test_<feature>.py`. Frontend unit tests should live in `frontend/src/__tests__` and target hooks or pages with `*.test.tsx` files run by `vitest`. Until suites grow, smoke-test `/healthz` and OAuth flows locally before merging. Aim for coverage that exercises new endpoints, schema validation, and React routes.

## Commit & Pull Request Guidelines
Follow the existing history by writing short, imperative commit subjects (e.g., “Add Neo4j session helper”). Group related backend and frontend changes separately. PRs should explain the change, list manual test results, and link GitHub issues or spec sections. Include screenshots or curl output whenever the UI or API responses change.
