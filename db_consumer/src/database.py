from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

engine = create_engine(
    "postgresql://postgres:postgres@localhost/wab_project"
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=True,
    bind=engine
)

Base = declarative_base()



# Dependency
def get_db():
    return Session(engine)