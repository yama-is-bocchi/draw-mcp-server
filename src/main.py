import asyncio
from logging import INFO, basicConfig
from typing import Literal, cast

from api_server import APIServer
from lib import parse_args
from mcp_server import get_draw_mcp_server


async def main() -> None:
    # infos
    target_dir = "data"
    host = "localhost"
    port = 8080
    basicConfig(level=INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    # arguments parse
    options = parse_args()
    # get api server
    api_server = APIServer(target_dir, options.username, options.password)
    # get mcp server
    mcp_server = get_draw_mcp_server(host, port)
    transport = cast(("Literal['stdio', 'http', 'sse', 'streamable-http'] | None"), options.mcp_transport)
    await asyncio.gather(
        api_server.start(host, port),
        asyncio.to_thread(mcp_server.run, transport),
    )


if __name__ == "__main__":
    asyncio.run(main())
