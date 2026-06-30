from datetime import datetime, timedelta

import streamlit as st

from src.database.config import supabase
from src.database.db import get_student_attendance, get_student_subjects


CHATBOT_HINTS = [
    "What is my attendance?",
    "Show faculty details",
    "What is tomorrow timetable?",
    "Any assignment due date?",
]


def _format_percent(present, total):
    if total == 0:
        return "0%"
    return f"{(present / total) * 100:.1f}%"


def _attendance_answer(student_id):
    logs = get_student_attendance(student_id)

    if not logs:
        return "I could not find attendance records yet. Once your teacher saves attendance, I can summarize it here."

    total = len(logs)
    present = sum(1 for log in logs if log.get("is_present"))
    absent = total - present

    by_subject = {}
    for log in logs:
        subject = log.get("subjects") or {}
        subject_name = subject.get("name", "Unknown subject")
        subject_code = subject.get("subject_code", "-")
        key = f"{subject_name} ({subject_code})"

        if key not in by_subject:
            by_subject[key] = {"total": 0, "present": 0}

        by_subject[key]["total"] += 1
        if log.get("is_present"):
            by_subject[key]["present"] += 1

    lines = [
        "Here is your attendance summary:",
        f"Overall: {present}/{total} present ({_format_percent(present, total)})",
        f"Absent: {absent}",
        "",
        "Subject-wise:",
    ]

    for subject, stats in by_subject.items():
        lines.append(
            f"- {subject}: {stats['present']}/{stats['total']} present "
            f"({_format_percent(stats['present'], stats['total'])})"
        )

    return "\n".join(lines)


def _faculty_answer(student_id):
    try:
        response = (
            supabase.table("subject_students")
            .select("subjects(name, subject_code, section, teachers(name, username))")
            .eq("student_id", student_id)
            .execute()
        )
        rows = response.data or []
    except Exception:
        rows = get_student_subjects(student_id)

    if not rows:
        return "I could not find enrolled subjects yet, so faculty details are not available."

    lines = ["Here are your faculty details:"]

    for row in rows:
        subject = row.get("subjects") or {}
        teacher = subject.get("teachers") or {}

        subject_name = subject.get("name", "Unknown subject")
        subject_code = subject.get("subject_code", "-")
        section = subject.get("section", "-")
        teacher_name = teacher.get("name", "Teacher details not available")
        teacher_username = teacher.get("username")

        faculty_line = f"- {subject_name} ({subject_code}), Section {section}: {teacher_name}"
        if teacher_username:
            faculty_line += f" (@{teacher_username})"
        lines.append(faculty_line)

    return "\n".join(lines)


def _tomorrow_timetable_answer():
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%A, %d %B %Y")
    return (
        f"Tomorrow is {tomorrow}. Timetable data is not added in the database yet. "
        "If you add a timetable table later, I can show tomorrow's classes here."
    )


def _assignment_answer():
    return (
        "Assignment due-date data is not added in the database yet. "
        "If you add an assignments table later, I can show pending work and due dates here."
    )


def _chatbot_answer(question, student_id):
    q = question.lower().strip()

    if any(word in q for word in ["attendance", "attendence", "present", "absent"]):
        return _attendance_answer(student_id)

    if any(word in q for word in ["faculty", "teacher", "sir", "madam", "professor"]):
        return _faculty_answer(student_id)

    if any(word in q for word in ["timetable", "time table", "schedule", "tomorrow", "tommarow"]):
        return _tomorrow_timetable_answer()

    if any(word in q for word in ["assignment", "homework", "due", "deadline", "submission"]):
        return _assignment_answer()

    return (
        "You can ask me things like:\n"
        "- What is my attendance?\n"
        "- What is tomorrow timetable?\n"
        "- Any assignment due date?\n"
        "- Show faculty details"
    )


def student_ai_chatbot(student_id):
    st.subheader("AI Student Assistant")
    st.caption("Ask about attendance, timetable, assignments, or faculty details.")

    if "student_chat_messages" not in st.session_state:
        st.session_state.student_chat_messages = [
            {
                "role": "assistant",
                "content": "Hi! I am your SnapClass assistant. Ask me about attendance, timetable, assignments, or faculty details.",
            }
        ]

    hint_cols = st.columns(2)
    for index, hint in enumerate(CHATBOT_HINTS):
        with hint_cols[index % 2]:
            if st.button(hint, key=f"chat_hint_{index}", width="stretch"):
                st.session_state.student_chat_messages.append({"role": "user", "content": hint})
                st.session_state.student_chat_messages.append(
                    {"role": "assistant", "content": _chatbot_answer(hint, student_id)}
                )
                st.rerun()

    with st.container(border=True):
        for message in st.session_state.student_chat_messages[-8:]:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    question = st.chat_input("Ask SnapClass AI...")
    if question:
        st.session_state.student_chat_messages.append({"role": "user", "content": question})
        st.session_state.student_chat_messages.append(
            {"role": "assistant", "content": _chatbot_answer(question, student_id)}
        )
        st.rerun()
