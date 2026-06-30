import subprocess
import sys
from pathlib import Path

import streamlit as st
from httpx import RequestError
from postgrest.exceptions import APIError
from streamlit.runtime.scriptrunner import get_script_run_ctx

# Streamlit's Starlette server may receive Ctrl+C before Uvicorn startup has
# created its instance-level ``servers`` list. Provide an empty fallback for
# that early-shutdown path; normal Uvicorn startup replaces it on the instance.
try:
    from uvicorn import Server as UvicornServer

    if not hasattr(UvicornServer, "servers"):
        UvicornServer.servers = ()
except ImportError:
    pass


def ensure_streamlit_runtime():
    if __name__ == "__main__" and get_script_run_ctx(suppress_warning=True) is None:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(Path(__file__).resolve())],
            check=False,
        )
        raise SystemExit


ensure_streamlit_runtime()


def ensure_project_environment():
    project_python = Path(__file__).resolve().parent / "venv" / "Scripts" / "python.exe"
    running_python = Path(sys.executable).resolve()

    if project_python.exists() and running_python != project_python.resolve():
        st.set_page_config(page_title="SnapClass environment")
        st.error("SnapClass is running from the wrong Python environment.")
        st.write("You started Streamlit from Anaconda/base, but this project needs its local `venv` because it contains `dlib` and face-recognition dependencies.")
        st.code(r".\venv\Scripts\python.exe -m streamlit run app.py", language="powershell")

        st.stop()


ensure_project_environment()


from src.database.config import SUPABASE_CONFIG_ERROR


if SUPABASE_CONFIG_ERROR:
    st.set_page_config(page_title="SnapClass setup")
    st.error(f"Supabase configuration error: {SUPABASE_CONFIG_ERROR}")
    st.write(
        "Open `.streamlit/secrets.toml` and replace the example values with "
        "your Supabase project URL and API key."
    )
    st.code(
        'SUPABASE_URL = "https://your-project-ref.supabase.co"\n'
        'SUPABASE_KEY = "your-real-supabase-key"',
        language="toml",
    )
    st.stop()

from src.components.dialog_auto_enroll import auto_enroll_dialog
from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen


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

    # If a teacher shared a join link, auto-open the student's FaceID camera
    # so the student can sign in immediately and be auto-enrolled after login.
    st.session_state.setdefault("student_login_camera_open", True)
    return join_code


def main():
    st.set_page_config(
        page_title="SnapClass - Making Attendance faster using AI",
    )

    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None

    join_code = get_query_param("join-code")
    if join_code:
        join_code = join_class(join_code)

    try:
        match st.session_state["login_type"]:
            case "teacher":
                teacher_screen()
            case "student":
                student_screen()
            case None:
                home_screen()
    except RequestError:
        st.error(
            "SnapClass could not connect to Supabase. Check your internet "
            "connection and the SUPABASE_URL in `.streamlit/secrets.toml`."
        )
        return
    except APIError as exc:
        if exc.code == "PGRST205":
            st.error(
                "The Supabase database schema is missing. Run "
                "`supabase_schema.sql` in the Supabase SQL Editor, then "
                "refresh this page."
            )
            return
        raise

    if (
        join_code
        and st.session_state.get("is_logged_in")
        and st.session_state.get("user_role") == "student"
    ):
        auto_enroll_dialog(join_code)


main()


