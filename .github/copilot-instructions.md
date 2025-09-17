# Relevantic Recall - GitHub Copilot Instructions

**ALWAYS follow these instructions first and fallback to additional search and context gathering only if the information here is incomplete or found to be in error.**

Relevantic Recall is a Python FastAPI application that provides a chat interface with PostgreSQL (vector storage) and Neo4j (graph database) backends. The system processes chat messages, extracts entities and relationships, and stores both conversation history and knowledge graph data.

## Working Effectively

### Prerequisites
- Python 3.12+ (tested with Python 3.12.3)
- Docker and Docker Compose for database services
- Environment variables configured in `.env` file

### Local Development Setup

1. **Clone and setup Python environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies (takes ~16 seconds):**
   ```bash
   pip install -r backend/requirements.txt
   ```
   **NEVER CANCEL** - Installation completes in under 30 seconds.

3. **Configure environment variables:**
   Create `.env` file in repository root:
   ```bash
   # Database Configuration
   DB_USER=relevantic_user
   DB_PASSWORD=relevantic_password
   DB_NAME=relevantic_recall
   DATABASE_URL=postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}
   SYNC_DATABASE_URL=postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}

   # Neo4j Configuration  
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=relevantic_password

   # Application Configuration
   SECRET_KEY=test-secret-key-for-development
   DEBUG=true

   # Optional OpenAI Configuration
   OPENAI_API_KEY=
   ```

4. **Start database services (takes ~7 seconds):**
   ```bash
   docker compose up postgres -d
   ```
   **NEVER CANCEL** - Database startup completes in under 15 seconds. Set timeout to 5+ minutes for safety.

5. **Run database migrations:**
   ```bash
   cd backend
   alembic upgrade head
   ```

6. **Set environment for application:**
   ```bash
   export PYTHONPATH="$PWD/backend"
   export DATABASE_URL="postgresql+asyncpg://relevantic_user:relevantic_password@localhost:5432/relevantic_recall"
   export NEO4J_URI="bolt://localhost:7687"
   export NEO4J_USER="neo4j"  
   export NEO4J_PASSWORD="relevantic_password"
   ```

7. **Start the application:**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Docker Build Issues
**CRITICAL**: Docker builds currently fail due to SSL certificate verification issues with PyPI in the sandboxed environment. Use local development setup instead.

The docker-compose.yml file has been corrected to use `context: ./backend` but pip installation fails with SSL errors.

## Validation

### Manual Testing Steps
1. **Verify health endpoint:**
   ```bash
   curl http://localhost:8000/healthz
   # Expected: {"status":"ok"}
   ```

2. **Test API documentation:**
   - Visit http://localhost:8000/docs for Swagger UI
   - Visit http://localhost:8000/openapi.json for OpenAPI spec

3. **Test chat endpoint:**
   ```bash
   curl -X POST http://localhost:8000/api/chat/ \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello test", "session_id": "550e8400-e29b-41d4-a716-446655440000", "user_id": "550e8400-e29b-41d4-a716-446655440001"}'
   # Expected: {"status":"processing","llm_response":"pending"}
   ```

4. **Verify database tables:**
   ```bash
   docker exec relevantic_postgres psql -U relevantic_user -d relevantic_recall -c "\\dt"
   # Expected tables: alembic_version, chat_history, entity_dictionary
   ```

### Build and Test Times
- **Python dependencies install**: ~16 seconds (NEVER CANCEL - set 5+ minute timeout)
- **Database startup**: ~7 seconds (NEVER CANCEL - set 5+ minute timeout)  
- **Application startup**: ~3 seconds
- **Database migration**: ~2 seconds

### Data Formats
- **User IDs and Session IDs**: Must be valid UUIDs (e.g., "550e8400-e29b-41d4-a716-446655440000")
- **Chat messages**: Text strings in JSON format
- **Database**: PostgreSQL with UUID primary keys and JSONB metadata columns

## Database Management

### Alembic Migrations
- **Location**: `backend/scripts/` and `backend/migrations/`
- **Models**: Defined in `backend/app/db/models.py`
- **Migration models**: Import from app models in `backend/migrations/models.py`

**Generate new migration:**
```bash
cd backend
alembic revision --autogenerate -m "Description"
```

**Apply migrations:**
```bash
cd backend  
alembic upgrade head
```

### Database Schema
- **chat_history**: Stores conversation messages with embeddings
- **entity_dictionary**: Stores extracted entities and canonical forms
- **Primary keys**: UUID format with auto-generation

## Architecture Overview

### Key Components
- **FastAPI application**: `backend/app/main.py`
- **API routes**: `backend/app/api/` (chat, context, entity endpoints)
- **Database models**: `backend/app/db/models.py`
- **Database operations**: `backend/app/db/crud.py`
- **Services**: `backend/app/services/` (Neo4j client)

### Environment Requirements
- **PYTHONPATH**: Must include `backend` directory for proper imports
- **DATABASE_URL**: PostgreSQL connection string with asyncpg driver
- **NEO4J_***: Neo4j connection parameters (optional for basic testing)

### Docker Compose Services
- **postgres**: pgvector/pgvector:pg16 with vector extension
- **neo4j**: neo4j:5.15 with APOC plugin (has configuration issues)
- **app**: Custom build from backend/Dockerfile (fails in sandboxed environment)

## Troubleshooting

### Common Issues
- **"relation does not exist"**: Run `alembic upgrade head` to create tables
- **"Invalid UUID"**: Use proper UUID format for user_id and session_id  
- **Import errors**: Ensure `PYTHONPATH` includes backend directory
- **Docker build fails**: Use local development setup due to SSL issues
- **Neo4j config errors**: PostgreSQL-only mode works for basic functionality

### Working Commands Reference
```bash
# Complete local setup sequence:
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
docker compose up postgres -d
cd backend && alembic upgrade head && cd ..
export PYTHONPATH="$PWD/backend"
export DATABASE_URL="postgresql+asyncpg://relevantic_user:relevantic_password@localhost:5432/relevantic_recall"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### API Endpoints
- **Health**: `GET /healthz`
- **Chat**: `POST /api/chat/` (requires UUID user_id, session_id, and message)
- **Documentation**: `GET /docs` (Swagger UI)
- **OpenAPI spec**: `GET /openapi.json`

Fixes #4.