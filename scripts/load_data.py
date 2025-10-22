import asyncio
from pathlib import Path
from typing import List
import json
import logging
from sqlalchemy.orm import Session

from database import Database
from database.models import register_models
from database.methods.products import create_products
from database.methods.sales import create_sales
from misc import settings

logger = logging.getLogger(__name__)

async def main():
    logger.debug("Starting data loading process")
    await register_models()
    db: Database = Database(settings.database_url)
    logger.debug(f"Database initialized with URL: {settings.database_url}")

    data_dir = "mock_data"

    def find_files_sync(pattern: str) -> List[str]:
        return [str(p) for p in Path(data_dir).rglob(pattern)]

    products_paths, sales_paths = await asyncio.gather(
        asyncio.to_thread(find_files_sync, "products_page_*.json"),
        asyncio.to_thread(find_files_sync, "sales_*.json")
    )
    
    logger.debug(f"Found {len(products_paths)} product files and {len(sales_paths)} sales files")

    BATCH_SIZE = 20
    
    for path in products_paths:
        session: Session = db.session
        try:
            logger.debug(f"Processing product file: {path}")
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                product_list = data.get("products", [])

            for i in range(0, len(product_list), BATCH_SIZE):
                batch = product_list[i:i + BATCH_SIZE] 
                logger.debug(f"Creating products batch {i//BATCH_SIZE + 1} with {len(batch)} items")
                create_products(session, batch) 
                
        except Exception as e:
            logger.error(f"Error processing product file {path}: {str(e)}")
            session.rollback()
        finally:
            session.close()


    for path in sales_paths:
        session: Session = db.session
        try:
            logger.debug(f"Processing sales file: {path}")
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                sales_list = data 

            for i in range(0, len(sales_list), BATCH_SIZE):
                batch = sales_list[i:i + BATCH_SIZE] 
                logger.debug(f"Creating sales batch {i//BATCH_SIZE + 1} with {len(batch)} items")
                create_sales(session, batch) 
                
        except Exception as e:
            logger.error(f"Error processing sales file {path}: {str(e)}")
            session.rollback()
        finally:
            session.close()

    logger.debug("Data loading process completed")

if __name__=='__main__':
    asyncio.run(main())