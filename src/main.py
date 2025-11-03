import asyncio
from logging import INFO, basicConfig

from api_server import APIServer
from lib import parse_args


def main() -> None:
    basicConfig(level=INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    # arguments parse
    options = parse_args()
    # start server
    asyncio.run(APIServer("data", options.username, options.password).start("localhost", 8080))
    # TODO: start mcp server


if __name__ == "__main__":
    main()
