import secrets

from config import settings
from fastapi import Depends, FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

security = HTTPBasic()


def login_swagger(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.USERNAME)
    correct_password = secrets.compare_digest(credentials.password, settings.PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )


def setup_swagger(app: FastAPI):
    """
    Setup swagger

    >>> app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    >>> setup_swagger(app)
    """

    @app.get("/docs", include_in_schema=False)
    async def get_documentation(_: str = Depends(login_swagger)):
        return get_swagger_ui_html(openapi_url="/openapi.json", title=settings.TITLE)

    @app.get("/openapi.json", include_in_schema=False)
    async def openapi(_: str = Depends(login_swagger)):
        return get_openapi(title=settings.TITLE, version=settings.VERSION, routes=app.routes)
