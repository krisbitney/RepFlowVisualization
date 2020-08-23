from pathlib import Path
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse


# paths
path = Path(__file__).parent
alchemy_graphQL = 'https://api.thegraph.com/subgraphs/name/daostack/alchemy'


async def homepage(request: Request) -> Response:
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


# app and routes
routes = [
    Route('/', homepage),
    Mount('/static', StaticFiles(directory=path/'static')),
]
app = Starlette(debug=True, routes=routes)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
