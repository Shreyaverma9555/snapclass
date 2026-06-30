import os

import streamlit as st


default_app_url = os.getenv("APP_URL") or "http://192.168.31.178:8501"
APP_URL = str(st.secrets.get("APP_URL", default_app_url)).rstrip("/")

