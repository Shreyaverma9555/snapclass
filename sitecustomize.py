"""Project-wide Python startup compatibility hooks."""

# Streamlit's Starlette wrapper can cancel Uvicorn while startup is still in
# progress. Uvicorn creates ``Server.servers`` near the end of startup, but its
# shutdown path reads it unconditionally. A class-level empty tuple is a safe
# fallback for that early-cancellation window; successful startup replaces it
# with the normal instance list.
try:
    from uvicorn import Server

    if not hasattr(Server, "servers"):
        Server.servers = ()
except ImportError:
    pass