import io
from urllib.parse import quote

import qrcode
import streamlit as st

from src.app_config import APP_URL


@st.dialog("📤 Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    if not APP_URL:
        st.error("APP_URL is missing. Add the public Streamlit URL to app secrets.")
        return

    join_code = str(subject_code).strip()
    join_url = f"{APP_URL}/?join-code={quote(join_code)}"

    st.subheader(f"📚 {subject_name}")
    st.header("Scan to Join")

    qr = qrcode.make(join_url)
    out = io.BytesIO()
    qr.save(out, format="PNG")
    qr_image = out.getvalue()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔗 Join Link")
        st.code(join_url, language="text")
        st.markdown("### 🆔 Join Code")
        st.code(join_code, language="text")
        st.info("Share this link or join code with your students.")

    with col2:
        st.markdown("### 📱 QR Code")
        st.image(qr_image, caption="Scan to join this class", width=250)