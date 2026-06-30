from io import BytesIO
from html import escape

import pandas as pd
import streamlit as st


def _safe_pdf_text(value):
    return str(value).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _build_simple_pdf(title, lines):
    """Create a small text PDF without external dependencies."""
    content_lines = [title, ""] + [str(line) for line in lines]
    y = 800
    stream_parts = ["BT", "/F1 18 Tf", f"72 {y} Td", f"({_safe_pdf_text(content_lines[0])}) Tj"]
    y_step = 18

    for line in content_lines[1:]:
        escaped = _safe_pdf_text(line[:95])
        stream_parts.append(f"0 -{y_step} Td")
        stream_parts.append("/F1 11 Tf")
        stream_parts.append(f"({escaped}) Tj")

    stream_parts.append("ET")
    stream = "\n".join(stream_parts).encode("latin-1", errors="replace")

    objects = []
    objects.append(b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n")
    objects.append(b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n")
    objects.append(
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n"
    )
    objects.append(b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n")
    objects.append(
        b"5 0 obj << /Length " + str(len(stream)).encode("ascii") + b" >> stream\n" + stream + b"\nendstream endobj\n"
    )

    pdf = BytesIO()
    pdf.write(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(pdf.tell())
        pdf.write(obj)

    xref_start = pdf.tell()
    pdf.write(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.write(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.write(
        f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF".encode("ascii")
    )
    return pdf.getvalue()


def _build_excel_html(df):
    header = "".join(f"<th>{escape(str(col))}</th>" for col in df.columns)
    rows = []
    for _, row in df.iterrows():
        cells = "".join(f"<td>{escape(str(value))}</td>" for value in row)
        rows.append(f"<tr>{cells}</tr>")

    html = f"""
    <html>
    <head>
        <meta charset="utf-8" />
        <style>
            table {{ border-collapse: collapse; font-family: Arial, sans-serif; }}
            th {{ background: #7c4dff; color: white; }}
            th, td {{ border: 1px solid #cccccc; padding: 8px 12px; }}
        </style>
    </head>
    <body>
        <h2>SnapClass AI Attendance Report</h2>
        <table>
            <thead><tr>{header}</tr></thead>
            <tbody>{''.join(rows)}</tbody>
        </table>
    </body>
    </html>
    """
    return html.encode("utf-8")


def _ai_report_lines(summary_df):
    if summary_df.empty:
        return ["No attendance data available for report generation."]

    total_students = int(summary_df["Total_Count"].sum())
    present_students = int(summary_df["Present_Count"].sum())
    absent_students = total_students - present_students
    attendance_percent = (present_students / total_students * 100) if total_students else 0

    subject_stats = (
        summary_df.groupby("Subject")[["Present_Count", "Total_Count"]]
        .sum()
        .reset_index()
    )
    subject_stats["Attendance %"] = subject_stats.apply(
        lambda row: (row["Present_Count"] / row["Total_Count"] * 100) if row["Total_Count"] else 0,
        axis=1,
    )

    best = subject_stats.sort_values("Attendance %", ascending=False).iloc[0]
    weakest = subject_stats.sort_values("Attendance %", ascending=True).iloc[0]

    lines = [
        f"Overall attendance: {present_students}/{total_students} present ({attendance_percent:.1f}%).",
        f"Total absent marks: {absent_students}.",
        f"Best subject attendance: {best['Subject']} ({best['Attendance %']:.1f}%).",
        f"Needs attention: {weakest['Subject']} ({weakest['Attendance %']:.1f}%).",
    ]

    if attendance_percent >= 85:
        lines.append("AI insight: Attendance looks strong overall.")
    elif attendance_percent >= 70:
        lines.append("AI insight: Attendance is moderate; keep monitoring low-attendance subjects.")
    else:
        lines.append("AI insight: Attendance is low; follow-up is recommended.")

    return lines


def render_ai_reports(summary_df):
    st.subheader("AI Reports Generator")

    if summary_df.empty:
        st.info("No attendance records available to generate reports yet.")
        return

    report_df = summary_df.copy()
    report_df["Attendance %"] = report_df.apply(
        lambda row: round((row["Present_Count"] / row["Total_Count"] * 100), 1) if row["Total_Count"] else 0,
        axis=1,
    )

    lines = _ai_report_lines(report_df)
    with st.container(border=True):
        st.markdown("#### AI Summary")
        for line in lines:
            st.write(line)

    chart_df = (
        report_df.groupby("Subject")[["Present_Count", "Total_Count"]]
        .sum()
        .reset_index()
    )
    chart_df["Attendance %"] = chart_df.apply(
        lambda row: round((row["Present_Count"] / row["Total_Count"] * 100), 1) if row["Total_Count"] else 0,
        axis=1,
    )

    st.markdown("#### Attendance Graph")
    st.bar_chart(chart_df.set_index("Subject")[["Attendance %"]])

    export_df = report_df[
        ["Time", "Subject", "Subject Code", "Present_Count", "Total_Count", "Attendance %", "Attendance Stats"]
    ].rename(
        columns={
            "Present_Count": "Present",
            "Total_Count": "Total Students",
        }
    )

    pdf_lines = lines + [""] + [
        f"{row['Time']} | {row['Subject']} ({row['Subject Code']}) | {row['Present']}/{row['Total Students']} | {row['Attendance %']}%"
        for _, row in export_df.iterrows()
    ]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "Download PDF Report",
            data=_build_simple_pdf("SnapClass AI Attendance Report", pdf_lines),
            file_name="snapclass_ai_report.pdf",
            mime="application/pdf",
            width="stretch",
        )
    with col2:
        st.download_button(
            "Download Excel Report",
            data=_build_excel_html(export_df),
            file_name="snapclass_ai_report.xls",
            mime="application/vnd.ms-excel",
            width="stretch",
        )
    with col3:
        st.download_button(
            "Download CSV Data",
            data=export_df.to_csv(index=False).encode("utf-8"),
            file_name="snapclass_ai_report.csv",
            mime="text/csv",
            width="stretch",
        )
