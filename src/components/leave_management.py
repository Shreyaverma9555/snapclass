from datetime import date

import streamlit as st
from postgrest.exceptions import APIError

from src.database.db import (
    create_leave_request,
    get_student_leave_requests,
    get_student_subjects,
    get_teacher_leave_requests,
    update_leave_request_status,
)


STATUS_BADGES = {
    "pending": "🟡 Pending",
    "approved": "🟢 Approved",
    "rejected": "🔴 Rejected",
}


def _missing_table_message():
    st.warning(
        "Leave management database table is not created yet. Run the updated "
        "`supabase_schema.sql` once in Supabase SQL Editor."
    )


def student_leave_management(student_id):
    st.subheader("Leave Management")
    st.caption("Apply for leave and track approval status from your teacher.")

    try:
        enrolled_subjects = get_student_subjects(student_id)
    except APIError:
        st.error("Could not load subjects right now.")
        return

    if not enrolled_subjects:
        st.info("Enroll in a subject first to apply for leave.")
        return

    subject_options = {
        f"{node['subjects']['name']} ({node['subjects']['subject_code']})": node["subjects"]["subject_id"]
        for node in enrolled_subjects
        if node.get("subjects")
    }

    with st.container(border=True):
        st.markdown("#### Apply for Leave")
        selected_subject = st.selectbox("Select subject", list(subject_options.keys()))
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From date", value=date.today(), key="leave_start_date")
        with col2:
            end_date = st.date_input("To date", value=date.today(), key="leave_end_date")

        reason = st.text_area("Reason", placeholder="Example: Fever, family function, medical appointment...")

        if st.button("Submit Leave Request", type="primary", width="stretch"):
            if end_date < start_date:
                st.error("End date cannot be before start date.")
            elif not reason.strip():
                st.warning("Please enter a reason for leave.")
            else:
                try:
                    create_leave_request(
                        student_id=student_id,
                        subject_id=subject_options[selected_subject],
                        start_date=start_date.isoformat(),
                        end_date=end_date.isoformat(),
                        reason=reason.strip(),
                    )
                    st.success("Leave request submitted successfully.")
                    st.rerun()
                except APIError:
                    _missing_table_message()
                except Exception as exc:
                    st.error(f"Could not submit leave request: {exc}")

    st.markdown("#### My Leave Requests")
    try:
        requests = get_student_leave_requests(student_id)
    except APIError:
        _missing_table_message()
        return
    except Exception as exc:
        st.error(f"Could not load leave requests: {exc}")
        return

    if not requests:
        st.info("No leave requests submitted yet.")
        return

    for request in requests:
        subject = request.get("subjects") or {}
        with st.container(border=True):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(
                    f"**{subject.get('name', 'Subject')} ({subject.get('subject_code', '-')})**"
                )
                st.write(f"{request.get('start_date')} to {request.get('end_date')}")
                st.caption(request.get("reason", ""))
                if request.get("teacher_note"):
                    st.info(f"Teacher note: {request['teacher_note']}")
            with c2:
                status = request.get("status", "pending")
                st.markdown(f"**{STATUS_BADGES.get(status, status.title())}**")


def teacher_leave_management(teacher_id):
    st.header("Leave Management")
    st.caption("Review student leave requests and approve or reject them.")

    try:
        requests = get_teacher_leave_requests(teacher_id)
    except APIError:
        _missing_table_message()
        return
    except Exception as exc:
        st.error(f"Could not load leave requests: {exc}")
        return

    if not requests:
        st.info("No leave requests found yet.")
        return

    pending_count = sum(1 for request in requests if request.get("status") == "pending")
    st.metric("Pending Requests", pending_count)

    for request in requests:
        student = request.get("students") or {}
        subject = request.get("subjects") or {}
        status = request.get("status", "pending")

        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"### {student.get('name', 'Student')}")
                st.write(f"Subject: {subject.get('name', 'Subject')} ({subject.get('subject_code', '-')})")
                st.write(f"Leave: {request.get('start_date')} to {request.get('end_date')}")
                st.caption(f"Reason: {request.get('reason', '-')}")
                if request.get("teacher_note"):
                    st.info(f"Teacher note: {request['teacher_note']}")
            with c2:
                st.markdown(f"**{STATUS_BADGES.get(status, status.title())}**")

            if status == "pending":
                note = st.text_input(
                    "Teacher note optional",
                    key=f"leave_note_{request['leave_id']}",
                    placeholder="Optional note for student",
                )
                approve_col, reject_col = st.columns(2)
                with approve_col:
                    if st.button("Approve", key=f"approve_leave_{request['leave_id']}", type="primary", width="stretch"):
                        update_leave_request_status(request["leave_id"], "approved", note)
                        st.success("Leave approved.")
                        st.rerun()
                with reject_col:
                    if st.button("Reject", key=f"reject_leave_{request['leave_id']}", width="stretch"):
                        update_leave_request_status(request["leave_id"], "rejected", note)
                        st.warning("Leave rejected.")
                        st.rerun()
