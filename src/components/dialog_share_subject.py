import io
import qrcode
import streamlit as st


@st.dialog("📤 Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    # Create join URL
    join_code = str(subject_code).strip()
    join_url = f"{st.secrets['APP_URL']}/?join-code={join_code}"

    st.subheader(f"📚 {subject_name}")
    st.header("Scan to Join")

    # Generate QR Code
    qr = qrcode.make(join_url)
    out = io.BytesIO()
    qr.save(out, format="PNG")
    qr_image = out.getvalue()

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔗 Join Link")
        st.code(join_url, language="text")

        st.markdown("### 🆔 Join Code")
        st.code(join_code, language="text")

        st.info("Copy the link or join code and share it with your students via WhatsApp, Email, or any messaging platform.")

    with col2:
        st.markdown("### 📱 QR Code")
        st.image(qr_image, caption="Scan to join this class", width=250)