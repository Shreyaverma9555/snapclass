import streamlit as st
from httpx import RequestError
from postgrest.exceptions import APIError

from src.database.config import SUPABASE_CONFIG_ERROR


def get_query_param(name):
    value = st.query_params.get(name)
    if isinstance(value, list):
        return value[0] if value else None
    return value


def join_class(join_code):
    join_code = str(join_code).strip()
    if not join_code:
        return None

    st.session_state["pending_join_code"] = join_code
    if st.session_state.get("login_type") != "student":
        st.session_state["login_type"] = "student"
    st.session_state.setdefault("student_login_camera_open", True)
    return join_code


def show_setup_error():
    st.error(f"Supabase configuration error: {SUPABASE_CONFIG_ERROR}")
    st.write("Add these values in Streamlit Community Cloud → App settings → Secrets:")
    st.code(
        'SUPABASE_URL = "https://your-project-ref.supabase.co"\n'
        'SUPABASE_SERVICE_ROLE_KEY = "your-service-role-key"\n'
        'APP_URL = "https://your-app.streamlit.app"',
        language="toml",
    )


def render_current_screen():
    role = st.session_state.get("login_type")
    if role == "teacher":
        from src.screens.teacher_screen import teacher_screen

        teacher_screen()
    elif role == "student":
        from src.screens.student_screen import student_screen

        student_screen()
    else:
        from src.screens.home_screen import home_screen

        home_screen()


def main():
    st.set_page_config(
        page_title="SnapClass - Making Attendance faster using AI",
        page_icon="assets/snapclass-college-icon.png",
    )

    if SUPABASE_CONFIG_ERROR:
        show_setup_error()
        return

    st.session_state.setdefault("login_type", None)
    join_code = get_query_param("join-code")
    if join_code:
        join_code = join_class(join_code)

    try:
        render_current_screen()

        if (
            join_code
            and st.session_state.get("is_logged_in")
            and st.session_state.get("user_role") == "student"
        ):
            from src.components.dialog_auto_enroll import auto_enroll_dialog

            auto_enroll_dialog(join_code)
    except RequestError:
        st.error(
            "SnapClass could not connect to Supabase. Check SUPABASE_URL and "
            "the project status, then reboot the app."
        )
    except APIError as exc:
        if getattr(exc, "code", None) == "PGRST205":
            st.error(
                "The database schema is missing. Run supabase_schema.sql in "
                "the Supabase SQL Editor, then refresh this page."
            )
        else:
            st.error(f"Supabase request failed: {exc}")
    except Exception as exc:
        # Keep recoverable app errors inside Streamlit instead of terminating
        # the script with Community Cloud's generic 'Oh no' screen.
        st.error("SnapClass encountered a startup error.")
        st.exception(exc)


main()