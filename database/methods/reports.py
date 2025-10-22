from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Float
from database.models.Product import Product 
from database.models.Sale import Sale
from typing import List, Tuple, cast as type_cast

def get_top_sales_data(db: Session) -> List[Tuple[str, float]]:
    query_result = db.query(
        Product.title.label('product_title'),
        cast(func.sum(Sale.qty * Sale.price), Float).label('total_revenue')
    ).join(Sale, Product.id == Sale.product_id).group_by(
        Product.title
    ).order_by(
        func.sum(Sale.qty * Sale.price).desc()
    ).limit(10).all()
    
    return type_cast(List[Tuple[str, float]], query_result)
