import argparse

from pydantic import BaseModel


class StartupOptions(BaseModel):
    username: str | None
    password: str | None
    auth_script_path: str | None
    mcp_transport: str | None


def parse_args() -> StartupOptions:
    parser = argparse.ArgumentParser(description="Parse startup options for authentication and transport.")
    parser.add_argument("-u", "--username", type=str, help="Username for authentication")
    parser.add_argument("-p", "--password", type=str, help="Password for authentication")
    parser.add_argument("-s", "--script", type=str, help="Path to authentication script")
    parser.add_argument("-t", "--transport", type=str, help="MCP transport type")

    args = parser.parse_args()

    return StartupOptions(
        username=args.username,
        password=args.password,
        auth_script_path=args.script,
        mcp_transport=args.transport,
    )
