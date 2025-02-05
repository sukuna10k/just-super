import os
import aiofiles
from aiohttp import web

routes = web.RouteTableDef()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")
@routes.get("/", allow_head=True)
async def root_route_handler(request):
    index_path = os.path.join(WEB_DIR, "index.html")
    if os.path.exists(index_path):
        async with aiofiles.open(index_path, mode="r", encoding="utf-8") as f:
            content = await f.read()
        return web.Response(text=content, content_type="text/html")

    return web.json_response({"error": "index.html non trouvé", "chemin": index_path})


async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

