import streamlit as st

from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    student_data = st.session_state.get("student_data")
    if not student_data or not student_data.get("student_id"):
        st.warning("Please log in as a student before joining a subject.")
        if st.button("Close", key="close_auto_enroll_login"):
            st.query_params.clear()
            st.rerun()
        return

    join_code = str(subject_code).strip()
    if not join_code:
        st.error("The subject code is missing.")
        return

    student_id = student_data["student_id"]

    try:
        response = (
            supabase.table("subjects")
            .select("subject_id, name")
            .eq("subject_code", join_code)
            .limit(1)
            .execute()
        )
    except Exception as exc:
        st.error(f"Could not look up the subject: {exc}")
        return

    if not response.data:
        st.error("Subject code not found.")
        if st.button("Close", key="close_auto_enroll_not_found"):
            st.query_params.clear()
            st.rerun()
        return

    subject = response.data[0]
    subject_id = subject.get("subject_id")
    subject_name = subject.get("name") or "this subject"
    if subject_id is None:
        st.error("This subject has invalid data and cannot be joined.")
        return

    try:
        enrollment = (
            supabase.table("subject_students")
            .select("student_id")
            .eq("subject_id", subject_id)
            .eq("student_id", student_id)
            .limit(1)
            .execute()
        )
    except Exception as exc:
        st.error(f"Could not check your enrollment: {exc}")
        return

    if enrollment.data:
        st.info("You're already enrolled in this subject.")
        if st.button("Got it", key="close_auto_enroll_existing"):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(f"Would you like to enroll in **{subject_name}**?")

    cancel_col, enroll_col = st.columns(2)

    with cancel_col:
        if st.button("No thanks", key="cancel_auto_enroll", use_container_width=True):
            st.query_params.clear()
            st.rerun()

    with enroll_col:
        if st.button(
            "Enroll now",
            type="primary",
            key="confirm_auto_enroll",
            use_container_width=True,
        ):
            try:
                result = enroll_student_to_subject(student_id, subject_id)
            except Exception as exc:
                st.error(f"Enrollment failed: {exc}")
                return

            if not result:
                st.error("Enrollment failed. Please try again.")
                return

            st.toast(f"Joined {subject_name} successfully.")
            st.query_params.clear()
            st.rerun()


