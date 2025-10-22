from sqlalchemy.orm import Session
from typing import List, Dict, Any

from database.models.Sale import Sale
from datetime import date
from decimal import Decimal

def create_sales(db: Session, sales_list: List[Dict[str, Any]]):
    sales_to_add = []
    
    for item in sales_list:
        sale_data = dict(item) 
        
        sale_data['date'] = date.fromisoformat(sale_data['date'])
        sale_data['price'] = float(sale_data['price'])
        
        sale_data.pop('id', None)
        
        db_sale = Sale(**sale_data)
        sales_to_add.append(db_sale)
            
    if sales_to_add:
        db.add_all(sales_to_add)
        db.commit()
