# Database Setup

## Initialize a new project
```bash
# Create ./alembic.ini and ./migrations folder with env.py
alembic init migrations

# Uses ./migrations/models.py
alembic revision --autogenerate -m "Create a baseline migrations"

# Run the generated migration 
alembic upgrade head
```