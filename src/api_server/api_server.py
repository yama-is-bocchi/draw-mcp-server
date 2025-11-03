import logging

import uvicorn
from fastapi import FastAPI

from .router.v1 import get_file_stream


class APIServer:
    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        target_dir_path: str,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        base_app = FastAPI(title="API Server")
        data_app = get_file_stream(
            target_dir_path=target_dir_path,
            username=username,
            password=password,
        )
        base_app.mount("/api/v1", data_app)
        self.app = base_app

    async def start(self, host: str, port: int) -> None:
        self._logger.info("Starting API server at http://%s:%s", host, port)
        config = uvicorn.Config(self.app, host=host, port=port)
        server = uvicorn.Server(config)
        await server.serve()
