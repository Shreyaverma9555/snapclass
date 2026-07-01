import os

import streamlit as st


def _setting(name):
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return str(value or os.getenv(name, "")).strip()


# APP_URL must be the public HTTPS URL on Community Cloud so generated QR and
# subject-join links work for other devices.
APP_URL = _setting("APP_URL").rstrip("/")