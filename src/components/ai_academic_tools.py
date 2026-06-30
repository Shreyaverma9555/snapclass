from datetime import date, timedelta

import pandas as pd
import streamlit as st

from src.database.db import get_student_attendance, get_student_subjects, get_teacher_subjects


DEFAULT_TOPICS = "Introduction, key definitions, examples, practice questions, revision"


def _subject_names_from_student(student_id):
    try:
        rows = get_student_subjects(student_id)
    except Exception:
        return []
    return [row["subjects"]["name"] for row in rows if row.get("subjects")]


def _subject_names_from_teacher(teacher_id):
    try:
        rows = get_teacher_subjects(teacher_id)
    except Exception:
        return []
    return [row["name"] for row in rows]


def _attendance_insights(student_id):
    try:
        logs = get_student_attendance(student_id)
    except Exception as exc:
        return [f"Could not load attendance data: {exc}"]

    if not logs:
        return ["No attendance records yet. Start attending classes and I will generate insights here."]

    total = len(logs)
    present = sum(1 for log in logs if log.get("is_present"))
    percent = (present / total) * 100 if total else 0

    insights = [
        f"Overall attendance: {present}/{total} ({percent:.1f}%).",
    ]

    if percent >= 85:
        insights.append("Great work. You are safely above the common 75% attendance requirement.")
    elif percent >= 75:
        insights.append("You are okay, but avoid unnecessary leaves for the next few classes.")
    else:
        needed = max(1, int((0.75 * total - present) / 0.25) + 1)
        insights.append(f"Attendance is low. Attend around {needed} upcoming classes to recover toward 75%.")

    by_subject = {}
    for log in logs:
        subject = (log.get("subjects") or {}).get("name", "Unknown subject")
        by_subject.setdefault(subject, {"present": 0, "total": 0})
        by_subject[subject]["total"] += 1
        if log.get("is_present"):
            by_subject[subject]["present"] += 1

    for subject, stats in by_subject.items():
        subject_percent = (stats["present"] / stats["total"] * 100) if stats["total"] else 0
        insights.append(f"{subject}: {stats['present']}/{stats['total']} ({subject_percent:.1f}%).")

    return insights


def render_ai_timetable_generator(subjects):
    st.markdown("#### AI Timetable Generator")
    selected = st.multiselect("Subjects", subjects or ["Math", "Science", "English"], default=(subjects or ["Math", "Science"])[:2])
    hours = st.slider("Study hours per day", 1, 8, 3)
    start = st.date_input("Start date", value=date.today(), key="ai_timetable_start")

    if st.button("Generate Timetable", key="generate_timetable", type="primary"):
        if not selected:
            st.warning("Select at least one subject.")
            return
        rows = []
        for day in range(7):
            current = start + timedelta(days=day)
            subject = selected[day % len(selected)]
            rows.append({
                "Date": current.strftime("%d %b %Y"),
                "Day": current.strftime("%A"),
                "Subject": subject,
                "Plan": f"{hours} hour(s): concept revision + practice + quick recap",
            })
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")


def render_ai_attendance_insights(student_id):
    st.markdown("#### AI Attendance Insights")
    for insight in _attendance_insights(student_id):
        st.info(insight)


def render_exam_preparation_assistant(subjects):
    st.markdown("#### AI Exam Preparation Assistant")
    subject = st.selectbox("Exam subject", subjects or ["General Subject"], key="exam_subject")
    days = st.slider("Days left for exam", 1, 60, 7)
    difficulty = st.selectbox("Difficulty", ["Easy", "Moderate", "Hard"], key="exam_difficulty")

    if st.button("Create Exam Prep Plan", key="exam_plan", type="primary"):
        st.write(f"Exam prep plan for **{subject}** ({difficulty})")
        st.markdown(
            f"""
            - Day 1-{max(1, days//3)}: Finish core concepts and formulas.
            - Middle days: Solve previous questions and mark weak topics.
            - Last 2 days: Rapid revision, flashcards, and mock test.
            - Daily rule: 45 min study + 10 min break cycles.
            """
        )


def render_assignment_generator(subjects):
    st.markdown("#### AI Assignment Generator")
    subject = st.selectbox("Subject", subjects or ["General Subject"], key="assignment_subject")
    topic = st.text_input("Topic", placeholder="Example: Photosynthesis, DBMS normalization", key="assignment_topic")
    level = st.selectbox("Level", ["School", "College", "Advanced"], key="assignment_level")

    if st.button("Generate Assignment", key="generate_assignment", type="primary"):
        topic_text = topic or "selected topic"
        st.markdown(
            f"""
            ### Assignment: {topic_text}
            **Subject:** {subject}  
            **Level:** {level}

            1. Explain the concept of {topic_text} in your own words.
            2. Write five important points with examples.
            3. Draw a diagram/table/flowchart if applicable.
            4. Solve or create two practical problems related to {topic_text}.
            5. Conclude with real-life applications.
            """
        )


def render_question_paper_generator(subjects):
    st.markdown("#### AI Question Paper Generator")
    subject = st.selectbox("Subject", subjects or ["General Subject"], key="paper_subject")
    topics = st.text_area("Topics", value=DEFAULT_TOPICS, key="paper_topics")
    marks = st.selectbox("Total marks", [20, 40, 50, 80, 100], key="paper_marks")

    if st.button("Generate Question Paper", key="generate_paper", type="primary"):
        topic_list = [topic.strip() for topic in topics.split(",") if topic.strip()]
        st.markdown(f"### {subject} Question Paper — {marks} Marks")
        st.markdown("**Section A: Short Answer**")
        for index, topic in enumerate(topic_list[:5], start=1):
            st.write(f"{index}. Define/explain {topic}. ({marks//10 or 2} marks)")
        st.markdown("**Section B: Long Answer**")
        for index, topic in enumerate(topic_list[:3], start=1):
            st.write(f"{index}. Discuss {topic} with examples and applications. ({max(5, marks//5)} marks)")


def render_notes_summarizer():
    st.markdown("#### AI Notes Summarizer")
    notes = st.text_area("Paste notes here", height=180, key="notes_to_summarize")

    if st.button("Summarize Notes", key="summarize_notes", type="primary"):
        if not notes.strip():
            st.warning("Paste notes first.")
            return
        sentences = [sentence.strip() for sentence in notes.replace("\n", " ").split(".") if sentence.strip()]
        summary = sentences[:5]
        st.markdown("### Summary")
        for point in summary:
            st.write(f"- {point}.")
        st.markdown("### Key Words")
        words = [word.strip(',.():;').lower() for word in notes.split() if len(word.strip(',.():;')) > 6]
        keywords = list(dict.fromkeys(words))[:10]
        st.write(", ".join(keywords) if keywords else "No strong keywords found.")


def render_study_planner(subjects):
    st.markdown("#### AI Study Planner")
    selected = st.multiselect("Subjects to plan", subjects or ["Math", "Science", "English"], key="study_subjects")
    goal = st.text_input("Study goal", placeholder="Example: Complete unit 2 and revise formulas", key="study_goal")
    days = st.slider("Plan duration days", 1, 30, 7, key="study_days")

    if st.button("Generate Study Planner", key="generate_study_planner", type="primary"):
        selected = selected or (subjects or ["General Study"])
        rows = []
        for day in range(1, days + 1):
            subject = selected[(day - 1) % len(selected)]
            rows.append({
                "Day": day,
                "Subject": subject,
                "Task": goal or f"Revise {subject}, solve practice questions, and write doubts.",
            })
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")


def student_ai_academic_tools(student_id):
    st.subheader("AI Academic Tools")
    subjects = _subject_names_from_student(student_id)
    tabs = st.tabs([
        "Timetable",
        "Attendance Insights",
        "Exam Prep",
        "Notes Summarizer",
        "Study Planner",
    ])
    with tabs[0]:
        render_ai_timetable_generator(subjects)
    with tabs[1]:
        render_ai_attendance_insights(student_id)
    with tabs[2]:
        render_exam_preparation_assistant(subjects)
    with tabs[3]:
        render_notes_summarizer()
    with tabs[4]:
        render_study_planner(subjects)


def teacher_ai_academic_tools(teacher_id):
    st.header("AI Academic Tools")
    subjects = _subject_names_from_teacher(teacher_id)
    tabs = st.tabs([
        "Assignment Generator",
        "Question Paper Generator",
        "Timetable Generator",
        "Exam Prep Assistant",
        "Notes Summarizer",
    ])
    with tabs[0]:
        render_assignment_generator(subjects)
    with tabs[1]:
        render_question_paper_generator(subjects)
    with tabs[2]:
        render_ai_timetable_generator(subjects)
    with tabs[3]:
        render_exam_preparation_assistant(subjects)
    with tabs[4]:
        render_notes_summarizer()
