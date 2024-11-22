# -*- coding: utf-8 -*-
'''
ZettaBGP - Advanced Anomaly Detection in Internet Routing
Copyright (c) 2024 Benedikt Schwering and Sebastian Forstner

This work is licensed under the terms of the MIT license.
For a copy, see LICENSE in the project root.

Author:
    Benedikt Schwering <bes9584@thi.de>
    Sebastian Forstner <sef9869@thi.de>
'''
from src.controllers.mrt_library import mrt_library_router
from src.controllers.version import version_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI
import uvicorn, os

app = FastAPI()

app.include_router(
    router=mrt_library_router,
    prefix='/api/mrt-library'
)
app.include_router(
    router=version_router,
    prefix='/api/version'
)

app.mount(
    path='/ui',
    app=StaticFiles(
        directory=os.getenv('ZETTABGP_WEBAPP_UI_PATH', 'src/ui'),
    ),
    name="ui",
)

@app.get('/')
def serve_angular_root():
    '''
    Route to serve the index.html of the Angular UI.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    return FileResponse(os.getenv('ZETTABGP_WEBAPP_UI_PATH', 'src/ui') + '/index.html')

@app.exception_handler(404)
def serve_angular_root(_, __):
    '''
    Route to serve the index.html of the Angular UI when a 404 error occurs.
    This is needed due to the reactive routing of Angular.

    Author:
        Benedikt Schwering <bes9584@thi.de>
    '''
    return FileResponse(os.getenv('ZETTABGP_WEBAPP_UI_PATH', 'src/ui') + '/index.html')

def start_webapp(reload: bool):
    '''
    Start the web application.

    Author:
        Benedikt Schwering <bes9584@thi.de>

    Args:
        reload (bool): Reload the WebApp on changes.
    '''
    uvicorn.run(
        app=os.getenv('ZETTABGP_WEBAPP_APP', 'src.webapp:app'),
        host='0.0.0.0',
        port=8000,
        reload=reload,
    )
