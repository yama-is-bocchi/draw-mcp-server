import argparse

from pydantic import BaseModel


class StartupOptions(BaseModel):
    username: str | None
    password: str | None
    host: str
    port: int
    target_directory: str
    mcp_transport: str


def parse_args() -> StartupOptions:
    parser = argparse.ArgumentParser(description="Parse startup options for authentication and transport.")
    parser.add_argument("-u", "--username", type=str, help="Username for authentication")
    parser.add_argument("-p", "--password", type=str, help="Password for authentication")
    parser.add_argument("--host", type=str, default="localhost", help="Host address where the server will run (default: localhost)")
    parser.add_argument("--port", type=int, default=8080, help="Port number for the server to listen on (default: 8080)")
    parser.add_argument("-d", "--directory", type=str, default="data", help="Source directory for generating PUML diagrams and serving image files")
    parser.add_argument("-t", "--transport", type=str, help="MCP transport type only(sse or http or streamable-http)", required=True)

    args = parser.parse_args()

    return StartupOptions(
        username=args.username,
        password=args.password,
        mcp_transport=args.transport,
        host=args.host,
        port=args.port,
        target_directory=args.directory,
    )
