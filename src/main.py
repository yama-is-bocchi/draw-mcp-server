import asyncio
from logging import INFO, basicConfig
from typing import Literal, cast

from api_server import APIServer
from lib import parse_env
from mcp_server import get_draw_mcp_server


async def main() -> None:
    basicConfig(level=INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    # arguments parse
    options = parse_env()
    # get api server
    api_server = APIServer(options.target_directory, options.username, options.password)
    # get mcp server
    mcp_server = get_draw_mcp_server(options.target_directory, options.host, options.port)
    transport = cast(("Literal['stdio', 'http', 'sse', 'streamable-http'] | None"), options.mcp_transport)
    await asyncio.gather(
        api_server.start("0.0.0.0", options.port),  # noqa: S104
        asyncio.to_thread(mcp_server.run, transport=transport, host="0.0.0.0"),  # noqa: S104
    )


if __name__ == "__main__":
    asyncio.run(main())
