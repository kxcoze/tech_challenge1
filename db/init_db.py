from db.models import Base
from db.session import engine


def init_db() -> None:
    # Simple db initialization without Alembic
    Base.metadata.create_all(bind=engine)
