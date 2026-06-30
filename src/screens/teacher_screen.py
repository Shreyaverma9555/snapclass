import streamlit as st
from httpx import RequestError

from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.ai_reports import render_ai_reports
from src.components.leave_management import teacher_leave_management
from src.components.ai_academic_tools import teacher_ai_academic_tools

from src.pipelines.face_pipeline import analyze_classroom_images
from src.components.dialog_attendence_result import attendance_result_dialog
import numpy as np

from datetime import datetime

import pandas as pd

from src.database.config import supabase


from src.components.dialog_voice_attendence import voice_attendance_dialog
def teacher_screen():

    style_base_layout()
    style_background_dashboard()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()





def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {teacher_data['name']} """)
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data 
            st.rerun()


    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
    tab1, tab2, tab3, tab4, tab5, tab6 = st.columns(6)


    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance',type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records',type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    with tab4:
        type4 = "primary" if st.session_state.current_teacher_tab == 'ai_reports' else "tertiary"
        if st.button('AI Reports', type=type4, width='stretch', icon=':material/analytics:'):
            st.session_state.current_teacher_tab = 'ai_reports'
            st.rerun()

    with tab5:
        type5 = "primary" if st.session_state.current_teacher_tab == 'leave_requests' else "tertiary"
        if st.button('Leave Requests', type=type5, width='stretch', icon=':material/event_available:'):
            st.session_state.current_teacher_tab = 'leave_requests'
            st.rerun()

    with tab6:
        type6 = "primary" if st.session_state.current_teacher_tab == 'ai_tools' else "tertiary"
        if st.button('AI Tools', type=type6, width='stretch', icon=':material/auto_awesome:'):
            st.session_state.current_teacher_tab = 'ai_tools'
            st.rerun()


    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()
    if st.session_state.current_teacher_tab == "ai_reports":
        teacher_tab_ai_reports()
    if st.session_state.current_teacher_tab == "leave_requests":
        teacher_tab_leave_requests()
    if st.session_state.current_teacher_tab == "ai_tools":
        teacher_tab_ai_tools()

    


    footer_dashboard()

def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')
    st.caption('Upload classroom photos to count faces, match enrolled students, group duplicates, and review annotated results.')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You have not created any subjects yet. Please create one to begin.')
        return

    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, width='stretch', caption=f'Photo {idx + 1}')

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.session_state.pop('face_attendance_analysis', None)
            st.rerun()

    with c2:
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Scanning classroom photos...'):
                enrolled_res = supabase.table('subject_students').select('*, students(*)').eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                    return

                analysis = analyze_classroom_images(st.session_state.attendance_images, enrolled_students)
                detected_ids = analysis['detected_students']
                detected_emotions = analysis['detected_emotions']

                results, attendance_to_log = [], []
                current_timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

                for node in enrolled_students:
                    student = node['students']
                    student_id = int(student['student_id'])
                    sources = detected_ids.get(student_id, [])
                    unique_sources = list(dict.fromkeys(sources))
                    is_present = bool(unique_sources)
                    emotion_values = detected_emotions.get(student_id, [])
                    emotion = max(set(emotion_values), key=emotion_values.count) if emotion_values else '-'

                    results.append({
                        'Name': student['name'],
                        'ID': student['student_id'],
                        'Source': ', '.join(unique_sources) if is_present else '-',
                        'Emotion': emotion if is_present else '-',
                        'Status': 'Present' if is_present else 'Absent',
                    })

                    attendance_to_log.append({
                        'student_id': student['student_id'],
                        'subject_id': selected_subject_id,
                        'timestamp': current_timestamp,
                        'is_present': bool(is_present),
                    })

                st.session_state.face_attendance_analysis = {
                    'summary': analysis['photo_summaries'],
                    'faces': analysis['face_rows'],
                    'annotated_images': analysis['annotated_images'],
                    'unique_people': analysis['unique_people'],
                    'results': results,
                    'logs': attendance_to_log,
                }

    with c3:
        if st.button('Use Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)

    analysis = st.session_state.get('face_attendance_analysis')
    if analysis:
        st.divider()
        st.subheader('Face Analysis Results')

        metric_cols = st.columns(3)
        total_faces = sum(row['Detected Faces'] for row in analysis['summary'])
        known_faces = sum(row['Known Students'] for row in analysis['summary'])
        metric_cols[0].metric('Detected faces', total_faces)
        metric_cols[1].metric('Known matches', known_faces)
        metric_cols[2].metric('Unique people', analysis['unique_people'])

        st.dataframe(pd.DataFrame(analysis['summary']), hide_index=True, width='stretch')

        if analysis['faces']:
            st.subheader('Per-Face Matches')
            st.dataframe(pd.DataFrame(analysis['faces']), hide_index=True, width='stretch')

        st.subheader('Annotated Photos')
        annotated_cols = st.columns(2)
        for idx, annotated in enumerate(analysis['annotated_images']):
            with annotated_cols[idx % 2]:
                st.image(annotated, width='stretch', caption=f'Annotated Photo {idx + 1}')

        attendance_result_dialog(pd.DataFrame(analysis['results']), analysis['logs'])



def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header('Manage Subjects', width='stretch')

    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)


    # LIST all SUBJECTS
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("Students", "Students", sub['total_students']),
                ("Classes", "Classes", sub['total_classes']),
            ]

            def share_btn(subject=sub):
                if st.button(f"Share Code: {subject['name']}", key=f"share_{subject['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(subject['name'], subject['subject_code'])
                st.space()

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn,
            )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")


def teacher_tab_attendance_records():
    st.header('Attendance Records')

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        render_ai_reports(pd.DataFrame())
        return
    
    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
            "Subject": r['subjects']['name'],
            "Subject Code":r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })


    df = pd.DataFrame(data)



    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count = ('is_present', 'sum'),
            Total_Count =('is_present', 'count')
        ).reset_index()

    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " /"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = ( summary.sort_values(by='ts_group' ,ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
                  )
    
    st.dataframe(display_df, width='stretch', hide_index=True)
    st.divider()
    render_ai_reports(summary)


def teacher_tab_ai_tools():
    teacher_ai_academic_tools(st.session_state.teacher_data['teacher_id'])


def teacher_tab_leave_requests():
    teacher_leave_management(st.session_state.teacher_data['teacher_id'])


def teacher_tab_ai_reports():
    st.header('AI Reports Generator')
    st.caption('Generate attendance graphs, AI summary, PDF report, Excel report, and CSV export.')

    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        render_ai_reports(pd.DataFrame())
        return

    data = []
    for r in records:
        ts = r.get('timestamp')
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False)),
        })

    df = pd.DataFrame(data)
    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count'),
        )
        .reset_index()
    )

    summary['Attendance Stats'] = (
        'Present ' + summary['Present_Count'].astype(str) + ' / '
        + summary['Total_Count'].astype(str) + ' Students'
    )

    render_ai_reports(summary)


def login_teacher(username, password):
    if not username or not password:
        return False, "Username and password are required."

    try:
        teacher = teacher_login(username, password)
    except RequestError:
        return False, (
            "Could not connect to Supabase. Check your internet connection "
            "and SUPABASE_URL in `.streamlit/secrets.toml`."
        )

    if not teacher:
        return False, "Invalid username or password."

    st.session_state.user_role = "teacher"
    st.session_state.teacher_data = teacher
    st.session_state.is_logged_in = True
    return True, "Welcome back!"


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using password', text_alignment='center')
    st.space()
    st.space()


    teacher_username = st.text_input("Enter username", placeholder='ananyaroy')

    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password")

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Login', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            success, message = login_teacher(teacher_username, teacher_pass)
            if success:
                st.toast(message)
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button('Register Instead', type="primary", icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type = 'register'

    footer_dashboard()



def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required."
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match."

    try:
        if check_teacher_exists(teacher_username):
            return False, "Username is already taken."
        create_teacher(teacher_username, teacher_pass, teacher_name)
    except RequestError:
        return False, (
            "Could not connect to Supabase. Check your internet connection "
            "and SUPABASE_URL in `.streamlit/secrets.toml`."
        )
    except Exception:
        return False, "Could not create the account. Please try again."

    return True, "Account created successfully. You can now log in."


def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()



    st.header('Register your teacher profile')

    st.space()
    st.space()

    
    teacher_username = st.text_input("Enter username", placeholder='ananyaroy')

    teacher_name = st.text_input("Enter name", placeholder='Ananya Roy')

    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password")

    teacher_pass_confirm = st.text_input("Confirm your password", type='password', placeholder="Enter password")

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Register now', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)


    with btnc2:
        if st.button('Login Instead', type="primary", icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type = 'login'

    footer_dashboard()









