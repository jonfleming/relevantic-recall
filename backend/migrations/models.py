# Import the actual application models
import sys
import os

# Add the backend directory to the path so we can import app models
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.db.models import Base
# Import all models to ensure they're registered with the Base metadata
from app.db.models import ChatHistory, EntityDictionary

metadata = Base.metadata

