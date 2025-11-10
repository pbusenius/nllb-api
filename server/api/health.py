from litestar import Router, get

from server.schemas import Health


@get("/health", cache=True, sync_to_thread=False, tags=["Monitoring"])
def health() -> Health:
    """
    Summary
    -------
    the `/health` route will return a shields.io endpoint badge response
    """
    return Health()


monitoring_router = Router(
    path="/",
    route_handlers=[health],
)
