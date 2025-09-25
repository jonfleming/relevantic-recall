# Relevantic Recall

A full-stack application for AI-powered conversation recall and context management, featuring OAuth2 authentication with Google and GitHub.

## Architecture

- **Backend**: FastAPI (Python) with PostgreSQL and Neo4j databases
- **Frontend**: React + TypeScript with Vite
- **Authentication**: OAuth2 with JWT tokens

## Prerequisites

- **Node.js** 20+ (for frontend)
- **Python** 3.11+ (for backend)
- **PostgreSQL** and **Neo4j** databases
- **VS Code** with debugging extensions

## Quick Start with VS Code

### 1. Environment Setup

1. **Clone and setup environment**:
   ```bash
   git clone <repository-url>
   cd relevantic-recall
   cp .env.example .env
   ```

2. **Configure OAuth2 providers** (see [OAuth2_README.md](OAuth2_README.md) for detailed setup):
   - Google OAuth2: Get client ID/secret from Google Cloud Console
   - GitHub OAuth2: Get client ID/secret from GitHub Developer Settings
   - Update `.env` with your credentials

3. **Setup databases**:
   ```bash
   # Start databases with Docker Compose
   docker-compose up -d postgres neo4j
   ```

### 2. Backend Setup

1. **Create Python virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Run database migrations**:
   ```bash
   cd backend
   alembic upgrade head
   cd ..
   ```

### 3. Frontend Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### 4. Run Full Stack from VS Code

1. **Open the project in VS Code**

2. **Use the Full Stack launch configuration**:
   - Open the Run and Debug panel (Ctrl+Shift+D / Cmd+Shift+D)
   - Select "Full Stack: Frontend + Backend" from the dropdown
   - Click the green play button or press F5

   This will start both:
   - **Backend API**: http://localhost:8000
   - **Frontend App**: http://localhost:3000

3. **Access the application**:
   - Open http://localhost:3000 in your browser
   - Click "Login with Google" or "Login with GitHub"
   - Complete OAuth authentication
   - You'll be redirected back to the frontend with your JWT token stored

## Individual Service Debugging

You can also run services individually:

- **Backend only**: Select "Python: Uvicorn (FastAPI)" configuration
- **Frontend only**: Select "Frontend: Vite Dev Server" configuration

## API Endpoints

### Authentication
- `GET /api/auth/login/{provider}` - Initiate OAuth login (google/github)
- `GET /api/auth/callback/{provider}` - OAuth callback handler
- `GET /api/auth/me` - Get current user info (requires auth)

### Protected Endpoints (require JWT token)
- `POST /api/chat/` - Send chat messages
- `GET /api/context/{session_id}` - Get session context
- `POST /api/entity/resolve` - Resolve entity mentions

## Environment Variables

Key environment variables in `.env`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://relevantic_user:relevantic_password@localhost:5432/relevantic_recall
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=relevantic_password

# OAuth2
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Optional
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-jwt-secret-key
```

## Troubleshooting

### Common Issues

1. **"OAuth not configured" error**:
   - Ensure `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are set in `.env`
   - Verify OAuth redirect URIs are configured correctly

2. **Database connection errors**:
   - Check that PostgreSQL and Neo4j are running: `docker-compose ps`
   - Verify database URLs in `.env`

3. **Import errors in backend**:
   - Ensure you're running from the project root with proper PYTHONPATH
   - Use the VS Code launch configuration for correct working directory

4. **Frontend build errors**:
   - Run `npm install` in the frontend directory
   - Check Node.js version (20+ required)

### Debug Tips

- Use VS Code's debugger with breakpoints in both frontend and backend
- Check browser developer tools for frontend issues
- Check VS Code's terminal output for backend errors
- View database logs: `docker-compose logs postgres neo4j`

## Development

- **Backend**: Located in `backend/` directory
- **Frontend**: Located in `frontend/` directory
- **Database migrations**: `backend/migrations/`
- **API documentation**: Available at http://localhost:8000/docs when running

## Production Deployment

See `docker-compose-prod.yml` for production deployment configuration.
