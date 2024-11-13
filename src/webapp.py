from src.controllers.version import version_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI
import uvicorn

app = FastAPI()

app.include_router(
    router=version_router,
    prefix='/api/version'
)

app.mount(
    path='/ui',
    app=StaticFiles(
        directory='src/ui'
    ),
    name="ui",
)

@app.get('/')
def serve_angular_root():
    return FileResponse('src/ui/index.html')

@app.exception_handler(404)
def serve_angular_root(_, __):
    return FileResponse('src/ui/index.html')

def start_webapp(reload: bool):
    uvicorn.run(
        app='src.webapp:app',
        host='0.0.0.0',
        port=8000,
        reload=reload,
    )
