import httpx
import streamlit as st
import tomllib
from pathlib import Path
from supabase import Client, create_client
from supabase.lib.client_options import SyncClientOptions


def _load_supabase_settings():
    values = {
        "SUPABASE_URL": "",
        "SUPABASE_KEY": "",
    }

    try:
        if hasattr(st, "secrets"):
            values["SUPABASE_URL"] = str(st.secrets.get("SUPABASE_URL", "")).strip()
            values["SUPABASE_KEY"] = str(st.secrets.get("SUPABASE_KEY", "")).strip()
    except Exception:
        pass

    if not values["SUPABASE_URL"] or not values["SUPABASE_KEY"]:
        try:
            secrets_path = Path(__file__).resolve().parents[2] / ".streamlit" / "secrets.toml"
            if secrets_path.exists():
                with secrets_path.open("r", encoding="utf-8-sig") as handle:
                    parsed = tomllib.loads(handle.read())
                values["SUPABASE_URL"] = str(parsed.get("SUPABASE_URL", "")).strip()
                values["SUPABASE_KEY"] = str(parsed.get("SUPABASE_KEY", "")).strip()
        except Exception:
            pass

    return values


SUPABASE_SETTINGS = _load_supabase_settings()
SUPABASE_URL = SUPABASE_SETTINGS["SUPABASE_URL"]
SUPABASE_KEY = SUPABASE_SETTINGS["SUPABASE_KEY"]


def get_supabase_config_error():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return "SUPABASE_URL and SUPABASE_KEY must be set."
    if "your-project-ref" in SUPABASE_URL or "your-real-supabase-key" in SUPABASE_KEY:
        return "The Supabase example values have not been replaced."
    if not SUPABASE_URL.startswith(("https://", "http://")):
        return "SUPABASE_URL must start with https:// or http://."
    return None


SUPABASE_CONFIG_ERROR = get_supabase_config_error()

supabase: Client = create_client(
    SUPABASE_URL or "https://invalid.local",
    SUPABASE_KEY or "invalid-key",
    SyncClientOptions(httpx_client=httpx.Client(trust_env=False)),
)



