import asyncio
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import logging
from aiohttp import web
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..middlewares import middleware, semaphore
from database.main import Database

logger = logging.getLogger(__name__)

def generate_report_sync(db_manager: Database, base_dir: Path):
    logger.debug("Starting report generation")
    matplotlib.use('Agg')

    db: Session = db_manager.session
    sales_data = get_top_sales_data(db)
    db.close()
    
    logger.debug(f"Retrieved {len(sales_data)} sales records for report")

    df = pd.DataFrame(sales_data, columns=['Название продукта', 'Общая выручка'])
    
    csv_path = base_dir / "resources" / "csv" / "report.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    logger.debug(f"CSV report saved to {csv_path}")

    png_path = base_dir / "resources" / "images" / "report.png"
    png_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))

    plt.barh(df['Название продукта'], df['Общая выручка'], color='skyblue')
    
    plt.xlabel('Общая выручка')
    plt.ylabel('Товар')
    plt.title('Топ-10 товаров по выручке за всё время')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(png_path)
    plt.close()
    
    logger.debug(f"PNG chart saved to {png_path}")

    template_path = base_dir / "templates" / "report.html"
    logger.debug("Report generation completed successfully")
    return {
        "status": "success",
        "image_url": "/resources/images/report.png",
        "csv_url": "/resources/csv/report.csv"
    }

# Import here to avoid circular imports
from database.methods.reports import get_top_sales_data

@middleware(semaphore(10, 10))
async def report_handler(request: web.Request) -> web.Response:
    logger.debug("Handling report request")
    base_dir = Path(__file__).resolve().parent.parent.parent
    
    db_manager: Database = request.app['db']

    report_data = await asyncio.to_thread(generate_report_sync, db_manager, base_dir)
    
    logger.debug("Report request handled successfully")
    return web.json_response(report_data)


def read_file_sync(path: Path) -> bytes:
    logger.debug(f"Reading file: {path}")
    with open(path, 'rb') as f:
        return f.read()

@middleware(semaphore(10, 10))
async def chart_handler(request: web.Request) -> web.Response:
    logger.debug("Handling chart request")
    base_dir = Path(__file__).resolve().parent.parent.parent
    db_manager: Database = request.app['db']
    
    await asyncio.to_thread(generate_report_sync, db_manager, base_dir)
    
    png_path = base_dir / "resources" / "images" / "report.png"
    
    if not png_path.exists():
        logger.error("Chart file not found after generation")
        return web.Response(status=500, text="File not found after generation.")

    png_content = await asyncio.to_thread(read_file_sync, png_path)
    
    logger.debug("Chart request handled successfully")
    return web.Response(body=png_content, content_type='image/png')