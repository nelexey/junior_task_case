from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.engine import Engine
import logging

logger = logging.getLogger(__name__)

class Database:

    BASE = declarative_base()

    def __init__(self, 
                 db_url: str = "sqlite:///./sql_app.db",
                 run_migrations: bool = True) -> None:
        logger.debug(f"Initializing database with URL: {db_url}")
        self._engine: Engine = create_engine(db_url, 
                                             connect_args={"check_same_thread": False})

        self._SessionLocal = sessionmaker(autocommit=False, 
                                          autoflush=False, 
                                          bind=self._engine)
        
        if run_migrations:
            logger.debug("Running database migrations")
            self.BASE.metadata.create_all(bind=self._engine)
            logger.debug("Database migrations completed")

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def session(self) -> Session:
        logger.debug("Creating new database session")
        return self._SessionLocal()