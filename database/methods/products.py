from sqlalchemy.orm import Session
from typing import List, Dict, Any

from database.models.Product import Product 

def create_products(db: Session, product_list: List[Dict[str, Any]]):
    products_to_add = []
    
    for item in product_list:
        product_data = dict(item)
        title_to_check = product_data.get('title')

        if title_to_check:
            existing_product = db.query(Product).filter(Product.title == title_to_check).first()
            
            if existing_product:
                continue 
        
        product_data.pop('id', None)
        
        db_product = Product(**product_data)
        products_to_add.append(db_product)
            
    if products_to_add:
        db.add_all(products_to_add)
        db.commit()

def get_all_products(db: Session) -> List[Dict[str, Any]]:
    rows = db.query(Product).all()
    products = []
    for r in rows:
        products.append({
            "id": int(r.id),
            "title": r.title or "",
            "description": r.description or "",
            "category": r.category or ""
        })
    return products