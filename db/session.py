from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import config

engine = create_engine(config.POSTGRES_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
