import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    with st.container(border=True):
        st.subheader(str(name))
        st.caption(f"Code: {code} · Section: {section}")

        if stats:
            columns = st.columns(len(stats))
            for column, (_, label, value) in zip(columns, stats):
                column.metric(str(label), value)

        if footer_callback:
            footer_callback()