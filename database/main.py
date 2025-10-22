from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base

class Database:

    BASE = declarative_base()

    def __init__(self, 
                 db_url: str = "sqlite:///./sql_app.db",
                 run_migrations: bool = True) -> None:
        self._engine: Engine = create_engine(db_url, 
                                             connect_args={"check_same_thread": False})

        self._SessionLocal = sessionmaker(autocommit=False, 
                                          autoflush=False, 
                                          bind=self._engine)
        
        if run_migrations:
            self.BASE.metadata.create_all(bind=self._engine)

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def session(self) -> Session:
        return self._SessionLocal()