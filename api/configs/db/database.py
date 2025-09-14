import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm.session import sessionmaker
from typing import Final, Any

load_dotenv()

DATABASE_URL: Final[str | None] = os.getenv("DATABASE_URL")

if DATABASE_URL == None:
    raise ValueError("DATABASE_URL is none")

engine: Final[Engine] = create_engine(DATABASE_URL, echo=True)

SessionLocal: Final[sessionmaker[Session]] = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

Base: Final[Any] = declarative_base()

def get_db():
    db: Final[Session] = SessionLocal()
    try:
        yield db

    finally:
        db.close()

def create_tables():
    from api.models.entities.user_entity import UserEntity
    from api.models.entities.task_entity import TaskEntity
    
    Base.metadata.create_all(bind=engine)
