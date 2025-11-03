import base64
import binascii
from collections.abc import Callable
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles


def get_file_stream(target_dir_path: str, username: str | None = None, password: str | None = None) -> FastAPI:
    app = FastAPI(title="Data Directory Server")

    @app.middleware("http")
    async def basic_auth_middleware(request: Request, call_next: Callable[..., Any]) -> Any:
        if username and password:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Basic "):
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Unauthorized"},
                    headers={"WWW-Authenticate": "Basic"},
                )
            try:
                encoded_credentials = auth_header.split(" ")[1]
                decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
                input_username, input_password = decoded_credentials.split(":", 1)
            except (ValueError, binascii.Error):
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": "Invalid authentication header"},
                )

            if input_username != username or input_password != password:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid credentials"},
                    headers={"WWW-Authenticate": "Basic"},
                )

        return await call_next(request)

    app.mount("/data", StaticFiles(directory=str(Path(target_dir_path))), name="data")

    return app
