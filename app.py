from datetime import date, timedelta
import pandas as pd
import plotly.express as px
import streamlit as st

from database import init_db, add_task, get_tasks, update_task_status, delete_task, replace_schedule, get_schedule
from planner import generate_schedule

st.set_page_config(page_title="Smart Study Planner AI", page_icon="📚", layout="wide")
init_db()

st.title("📚 Smart Study Planner AI")
st.caption("A personal study planner that prioritizes difficult topics, approaching deadlines, and unfinished work.")

with st.sidebar:
    st.header("⚙️ Planning settings")
    daily_hours = st.slider("Available study hours per day", 1, 12, 3)
    plan_days = st.slider("Plan length (days)", 1, 30, 7)
    start_date = st.date_input("Start date", value=date.today())
    st.divider()
    st.markdown("**How prioritization works**")
    st.write("The planner combines topic difficulty, deadline urgency, and remaining effort. It is a transparent scheduling heuristic, not a trained ML model.")

tab_tasks, tab_plan, tab_progress = st.tabs(["📝 Tasks", "🗓️ Study plan", "📈 Progress"])

with tab_tasks:
    st.subheader("Add a study task")
    with st.form("add_task_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        subject = c1.text_input("Subject", placeholder="e.g., Data Structures")
        topic = c2.text_input("Topic", placeholder="e.g., Binary trees")
        c3, c4, c5 = st.columns(3)
        due_date = c3.date_input("Exam / deadline", value=date.today() + timedelta(days=7))
        difficulty = c4.select_slider("Difficulty", options=["Easy", "Medium", "Hard"], value="Medium")
        estimated_hours = c5.number_input("Estimated hours", min_value=0.5, max_value=100.0, value=2.0, step=0.5)
        submitted = st.form_submit_button("Add task", type="primary")
        if submitted:
            if not subject.strip() or not topic.strip():
                st.error("Please enter both a subject and a topic.")
            else:
                add_task(subject.strip(), topic.strip(), due_date.isoformat(), difficulty, float(estimated_hours))
                st.success("Task added!")
                st.rerun()

    tasks = get_tasks()
    if tasks.empty:
        st.info("No tasks yet. Add your first topic above to get started.")
    else:
        st.subheader("Your tasks")
        for _, task in tasks.iterrows():
            with st.container(border=True):
                left, middle, right = st.columns([5, 2, 1])
                left.markdown(f"**{task['subject']} — {task['topic']}**")
                left.caption(f"Due {task['due_date']} · {task['difficulty']} · {task['estimated_hours']:g} h")
                if task["status"] == "Completed":
                    middle.success("Completed")
                else:
                    middle.warning("Pending")
                if right.button("🗑️", key=f"delete_{task['id']}", help="Delete task"):
                    delete_task(int(task["id"]))
                    st.rerun()
                if task["status"] != "Completed":
                    if st.button("Mark completed", key=f"complete_{task['id']}"):
                        update_task_status(int(task["id"]), "Completed")
                        st.rerun()
                else:
                    if st.button("Reopen", key=f"reopen_{task['id']}"):
                        update_task_status(int(task["id"]), "Pending")
                        st.rerun()

with tab_plan:
    st.subheader("Generate your study timetable")
    st.write("The planner assigns short sessions to the highest-priority pending tasks, while respecting your daily study-hour limit.")
    if st.button("✨ Generate / refresh study plan", type="primary"):
        tasks = get_tasks()
        schedule = generate_schedule(tasks, start_date, plan_days, daily_hours)
        replace_schedule(schedule)
        st.session_state["plan_generated"] = True

    schedule_df = get_schedule()
    if schedule_df.empty:
        st.info("Add tasks, then click **Generate / refresh study plan**.")
    else:
        schedule_df["date"] = pd.to_datetime(schedule_df["date"]).dt.date
        st.dataframe(
            schedule_df[["date", "subject", "topic", "hours", "priority", "reason"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "hours": st.column_config.NumberColumn("Hours", format="%.1f h"),
                "priority": st.column_config.NumberColumn("Priority", format="%.2f"),
            },
        )
        csv = schedule_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download timetable CSV", data=csv, file_name="study_timetable.csv", mime="text/csv")
        if schedule_df.empty:
            st.caption("No pending tasks fit into this planning window.")

with tab_progress:
    st.subheader("Your learning dashboard")
    tasks = get_tasks()
    if tasks.empty:
        st.info("Add some tasks to see your progress analytics.")
    else:
        total = len(tasks)
        completed = int((tasks["status"] == "Completed").sum())
        pending = total - completed
        a, b, c = st.columns(3)
        a.metric("Total topics", total)
        b.metric("Completed", completed)
        c.metric("Completion rate", f"{completed / total:.0%}")
        chart_data = tasks.groupby(["subject", "status"]).size().reset_index(name="topics")
        fig = px.bar(chart_data, x="subject", y="topics", color="status", barmode="group",
                     title="Topics by subject and status")
        st.plotly_chart(fig, use_container_width=True)
        st.progress(completed / total)
        st.caption(f"{pending} topic(s) remaining. Mark tasks complete as you study to keep this dashboard updated.")

st.divider()
st.caption("Built with Python · Streamlit · SQLite · Pandas · Plotly")
