import httpx
import streamlit as st
from supabase import Client, create_client
from supabase.lib.client_options import SyncClientOptions


def _secret(name):
    try:
        return str(st.secrets.get(name, "")).strip()
    except Exception:
        return ""


SUPABASE_URL = _secret("SUPABASE_URL")
# Community Cloud should use the service-role key. SUPABASE_KEY is retained as
# a local-development fallback for existing installations.
SUPABASE_KEY = _secret("SUPABASE_SERVICE_ROLE_KEY") or _secret("SUPABASE_KEY")


def get_supabase_config_error():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set."
    if "your-project-ref" in SUPABASE_URL or "your-service-role-key" in SUPABASE_KEY:
        return "The Supabase example values have not been replaced."
    if not SUPABASE_URL.startswith("https://"):
        return "SUPABASE_URL must use HTTPS."
    return None


SUPABASE_CONFIG_ERROR = get_supabase_config_error()

supabase: Client = create_client(
    SUPABASE_URL or "https://invalid.local",
    SUPABASE_KEY or "invalid-key",
    SyncClientOptions(httpx_client=httpx.Client(trust_env=False)),
)