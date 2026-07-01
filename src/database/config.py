import base64
import json

import streamlit as st
from supabase import Client, create_client


def _secret(name):
    try:
        return str(st.secrets.get(name, "")).strip()
    except Exception:
        return ""


def _jwt_role(key):
    """Read the public role claim only to catch an anon key pasted by mistake."""
    try:
        payload = key.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload))["role"]
    except (IndexError, KeyError, ValueError, json.JSONDecodeError):
        return None


SUPABASE_URL = _secret("SUPABASE_URL")
SUPABASE_KEY = _secret("SUPABASE_SERVICE_ROLE_KEY")


def get_supabase_config_error():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in Streamlit Secrets."
    if "your-project-ref" in SUPABASE_URL or "your-service-role-key" in SUPABASE_KEY:
        return "The Supabase example values have not been replaced."
    if not SUPABASE_URL.startswith("https://"):
        return "SUPABASE_URL must use HTTPS."
    if _jwt_role(SUPABASE_KEY) == "anon":
        return "SUPABASE_SERVICE_ROLE_KEY contains an anon key. Paste the service_role key instead."
    return None


SUPABASE_CONFIG_ERROR = get_supabase_config_error()
supabase: Client | None = None

if SUPABASE_CONFIG_ERROR is None:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as exc:
        SUPABASE_CONFIG_ERROR = f"Could not initialize Supabase: {exc}"