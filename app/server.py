import asyncio, sys
from pathlib import Path
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse, JSONResponse
import pandas as pd

import util

# paths
path = Path(__file__).parent
alchemy_graphQL_url = 'https://api.thegraph.com/subgraphs/name/daostack/alchemy'


async def homepage(request: Request) -> Response:
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


# query and clean data for plots
async def cache_plot_data():
    response_reputation_holders = await util.query_all_rep_holders(alchemy_graphQL_url)
    reputation_holders = pd.DataFrame(response_reputation_holders)
    reputation_holders = util.clean_rep_holders_data(reputation_holders, 'dOrg')
    return reputation_holders.to_json(orient='records')

# cache data when server starts
data_cache = asyncio.run(cache_plot_data())


# return cached data on GET
async def rep_data(request: Request):
    return JSONResponse(data_cache)


# app and routes
routes = [
    Route('/', homepage),
    Mount('static', StaticFiles(directory=path / 'static')),
    Route('/data', rep_data, methods=['GET'])
]
app = Starlette(debug=True, routes=routes)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
