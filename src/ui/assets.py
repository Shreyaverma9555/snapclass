"""Deployment-safe asset URLs for HTML and CSS rendered by Streamlit."""

import base64
import mimetypes
from functools import lru_cache
from pathlib import Path

_STATIC_ROOT = Path(__file__).resolve().parents[2] / "static"


@lru_cache(maxsize=None)
def static_data_uri(filename: str) -> str:
    """Return a checked-in static file as a cached data URI."""
    path = (_STATIC_ROOT / filename).resolve()
    if path.parent != _STATIC_ROOT.resolve() or not path.is_file():
        raise FileNotFoundError(f"Static asset not found: {filename}")
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"