from pydantic import BaseModel


class StartupOptions(BaseModel):
    username: str | None
    password: str | None
    host: str
    port: int
    target_directory: str
    mcp_transport: str
