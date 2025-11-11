import uvicorn

from server.app import app
from server.config import Config


def main() -> None:
    """
    Summary
    -------
    programmatically run the server with uvicorn
    """
    config = Config()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=config.server_port,
        workers=config.worker_count,
        access_log=False,  # Disable uvicorn access logs - we use structured logging instead
    )


__all__ = ["app", "main"]
