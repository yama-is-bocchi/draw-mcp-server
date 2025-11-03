import os

from dotenv import load_dotenv
from pydantic import ValidationError

from .startup_options import StartupOptions


def parse_env() -> StartupOptions:
    load_dotenv()
    try:
        return StartupOptions(
            username=os.getenv("USERNAME"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST", "localhost"),
            port=int(os.getenv("PORT", "8080")),
            target_directory=os.getenv("DIRECTORY", "data"),
            mcp_transport=os.environ["TRANSPORT"],
        )
    except KeyError as e:
        msg = f"Missing required environment variable: {e.args[0]}"
        raise ValidationError(msg) from e
    except ValueError as e:
        msg = f"Invalid environment variable value: {e}"
        raise ValidationError(msg) from e
