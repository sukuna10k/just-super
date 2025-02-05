from aiohttp import web
import aiofiles
import os

routes = web.RouteTableDef()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web") 

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    """Renvoie le fichier index.html si disponible, sinon un message JSON."""
    index_path = os.path.join(WEB_DIR, "index.html")

    if os.path.exists(index_path):
        async with aiofiles.open(index_path, mode="r", encoding="utf-8") as f:
            content = await f.read()
        return web.Response(text=content, content_type="text/html")

    return web.json_response("Hinata est toujours en ligne")

async def web_server():
    """Initialise et lance le serveur web."""
    web_app = web.Application(client_max_size=30_000_000)
    web_app.add_routes(routes)
    return web_app


