import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.main import Database
from database.models import register_models
from database.models.Product import Product
from database.models.Sale import Sale

@pytest.fixture(scope="function")
def temp_db():
    """Create a temporary database for testing"""
    # Create a temporary database file
    temp_db_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    temp_db_file.close()
    
    # Create database with temporary file
    db_url = f"sqlite:///{temp_db_file.name}"
    db = Database(db_url, run_migrations=True)
    
    yield db
    
    # Cleanup
    db.engine.dispose()
    os.unlink(temp_db_file.name)

@pytest.fixture(scope="function")
def sample_products():
    """Sample product data for testing"""
    return [
        {
            "id": 1,
            "title": "Test Product 1",
            "description": "Test Description 1",
            "category": "Test Category"
        },
        {
            "id": 2,
            "title": "Test Product 2",
            "description": "Test Description 2",
            "category": "Test Category"
        }
    ]

@pytest.fixture(scope="function")
def sample_sales():
    """Sample sales data for testing"""
    return [
        {
            "product_id": 1,
            "date": "2025-09-01",
            "qty": 5,
            "price": 100.0
        },
        {
            "product_id": 2,
            "date": "2025-09-02",
            "qty": 3,
            "price": 150.0
        }
    ]