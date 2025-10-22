import pytest
from database.methods.products import create_products, get_all_products
from database.methods.sales import create_sales
from database.methods.reports import get_top_sales_data

def test_create_products(temp_db, sample_products):
    """Test creating products in the database"""
    session = temp_db.session
    
    # Create products
    create_products(session, sample_products)
    
    # Verify products were created
    products = get_all_products(session)
    assert len(products) == 2
    assert products[0]["title"] == "Test Product 1"
    assert products[1]["title"] == "Test Product 2"
    
    session.close()

def test_create_products_duplicate_handling(temp_db, sample_products):
    """Test that duplicate products are not created"""
    session = temp_db.session
    
    # Create products twice
    create_products(session, sample_products)
    create_products(session, sample_products)
    
    # Should still only have 2 products
    products = get_all_products(session)
    assert len(products) == 2
    
    session.close()

def test_get_all_products_empty_db(temp_db):
    """Test getting all products from empty database"""
    session = temp_db.session
    
    products = get_all_products(session)
    assert len(products) == 0
    
    session.close()

def test_create_sales(temp_db, sample_products, sample_sales):
    """Test creating sales in the database"""
    session = temp_db.session
    
    # First create products (sales need product_id to exist)
    create_products(session, sample_products)
    
    # Create sales
    create_sales(session, sample_sales)
    
    # Verify sales were created by checking count
    from database.models.Sale import Sale
    sales_count = session.query(Sale).count()
    assert sales_count == 2
    
    session.close()

def test_get_top_sales_data(temp_db, sample_products, sample_sales):
    """Test getting top sales data"""
    session = temp_db.session
    
    # First create products and sales
    create_products(session, sample_products)
    create_sales(session, sample_sales)
    
    # Get top sales data
    top_sales = get_top_sales_data(session)
    
    # Should have 2 entries
    assert len(top_sales) == 2
    
    # Check that the data is correctly calculated
    # Product 2: 3 * 150.0 = 450.0
    # Product 1: 5 * 100.0 = 500.0
    # Should be ordered by revenue (descending)
    assert top_sales[0][0] == "Test Product 1"  # Product with highest revenue
    assert top_sales[0][1] == 500.0  # Revenue for product 1
    
    session.close()