import streamlit as st
import io
import qrcode


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    join_code = str(subject_code).strip()

    host = st.context.headers.get("host", "localhost:8501")

    if host.startswith("localhost") or host.startswith("127.0.0.1"):
        join_url = f"http://localhost:8501/?join-code={join_code}"
    else:
        join_url = f"http://{host}/?join-code={join_code}"

    st.header("Scan to Join")

    qr = qrcode.make(join_url)
    out = io.BytesIO()
    qr.save(out,format="PNG")
    qr_image = out.getvalue()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Copy Link")
        st.code(join_url, language="text")
        st.code(join_code, language="text")
        st.info("Copy this link to share on WhatsApp or Email")

    with col2:
        st.markdown("### Scan to Join")
        st.image(qr_image, caption="QR code for class joining", width=250)