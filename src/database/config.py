import streamlit as st
from supabase import Client, create_client


def _secret(name):
    try:
        return str(st.secrets.get(name, "")).strip()
    except Exception:
        return ""


SUPABASE_URL = _secret("SUPABASE_URL")
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
supabase: Client | None = None

# Never construct a client from placeholder values. The app displays a setup
# page first, and database modules are lazy-loaded only after validation.
if SUPABASE_CONFIG_ERROR is None:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as exc:
        SUPABASE_CONFIG_ERROR = f"Could not initialize Supabase: {exc}"