import asyncio
from pathlib import Path

from web import Server, Route
from web.handlers import report_handler, ping_handler, matching_handler
from database.main import Database
from database.models import register_models
from misc import settings


async def main():
    db = Database(settings.database_url)
    await register_models()

    report_route = Route('GET', '/report', report_handler.report_handler)
    chart_route = Route('GET', '/chart.png', report_handler.chart_handler)
    ping_route = Route('GET', '/', ping_handler.ping_handler)
    match_route = Route('GET', '/match', matching_handler.matching_handler)

    server = Server(host='localhost',
                    port=8000,
                    urls=[report_route, ping_route, chart_route, match_route])
    
    base_dir = Path(__file__).parent.resolve()
    
    server.app['db'] = db
    server.app.router.add_static('/resources', base_dir / 'resources')

    await server.start()

    while True:
        await asyncio.sleep(3600)

if __name__=='__main__':
    asyncio.run(main())