from api.router import router
from fastapi import FastAPI
from swagger import setup_swagger

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(router, prefix="/api")
setup_swagger(app)
