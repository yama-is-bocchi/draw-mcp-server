import base64
import binascii
import logging
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles


class APIServer:
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        target_dir_path: str,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        self.app = FastAPI(title="Data Directory Server")

        @self.app.middleware("http")
        async def basic_auth_middleware(request: Request, call_next: Any) -> Any:
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

        self.app.mount("/data", StaticFiles(directory=str(Path(target_dir_path))), name="data")

    async def start(self, host: str, port: int) -> None:
        self._logger.info("Starting API server at http://%s:%s", host, port)
        config = uvicorn.Config(self.app, host=host, port=port)
        server = uvicorn.Server(config)
        await server.serve()
