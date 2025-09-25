# Database Setup

## Initialize a new project
```bash
# Create ./alembic.ini and ./migrations folder with env.py
alembic init migrations

# Show current status
alembic current

# Uses ./migrations/models.py
alembic revision --autogenerate -m "Create a baseline migrations"

# Run the generated migration 
alembic upgrade head

# Show tables
# Example for PostgreSQL (adjust for your DB)
EXPORT PGPASSWORD=relevantic_password
psql -h localhost -U relevantic_user -d relevantic_recall -c "\dt"
```