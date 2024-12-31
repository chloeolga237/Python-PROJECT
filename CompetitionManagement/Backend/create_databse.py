from models import Base
from sqlalchemy import create_engine

# Create SQLite database
engine = create_engine('sqlite:///tournament.db')
Base.metadata.create_all(engine)

print("Database created successfully!")
