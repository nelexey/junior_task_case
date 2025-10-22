import pytest
from database.models.Product import Product
from database.models.Sale import Sale
from datetime import date

def test_product_model_creation(temp_db):
    """Test creating a Product model instance"""
    session = temp_db.session
    
    # Create a product instance
    product = Product(
        id=1,
        title="Test Product",
        description="Test Description",
        category="Test Category"
    )
    
    # Add to database
    session.add(product)
    session.commit()
    
    # Retrieve from database
    retrieved_product = session.query(Product).filter(Product.id == 1).first()
    
    assert retrieved_product is not None
    assert retrieved_product.title == "Test Product"
    assert retrieved_product.description == "Test Description"
    assert retrieved_product.category == "Test Category"
    
    session.close()

def test_sale_model_creation(temp_db):
    """Test creating a Sale model instance"""
    session = temp_db.session
    
    # First create a product (foreign key constraint)
    product = Product(
        id=1,
        title="Test Product",
        description="Test Description",
        category="Test Category"
    )
    session.add(product)
    session.commit()
    
    # Create a sale instance
    sale = Sale(
        id=1,
        product_id=1,
        date=date(2025, 9, 1),
        qty=5,
        price=100.50
    )
    
    # Add to database
    session.add(sale)
    session.commit()
    
    # Retrieve from database
    retrieved_sale = session.query(Sale).filter(Sale.id == 1).first()
    
    assert retrieved_sale is not None
    assert retrieved_sale.product_id == 1
    assert retrieved_sale.date == date(2025, 9, 1)
    assert retrieved_sale.qty == 5
    assert retrieved_sale.price == 100.50
    
    session.close()

def test_product_category_index(temp_db):
    """Test that Product category field is indexed"""
    # Check that category column has index
    category_column = Product.__table__.columns.category
    assert category_column.index is True