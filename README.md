# 📚 Smart Study Planner AI

A Python web app that creates a study timetable based on topic difficulty, deadlines, and estimated study effort. Track completed topics, view progress analytics, and export the plan to CSV.

> **Important:** The first version uses an explainable priority-based scheduling heuristic. It is not a trained machine-learning model and does not predict exam results. A later version can add study-history-based recommendations.

## Features

- Add subjects, topics, deadlines, difficulty, and estimated effort
- Generate a daily study schedule within a chosen hours-per-day limit
- Prioritize difficult and urgent tasks
- Mark tasks complete, reopen them, or delete them
- View completion metrics and subject-wise charts
- Export the generated timetable as CSV
- Store tasks and schedules in SQLite
- Unit tests for scheduling logic

## Tech stack

- Python
- Streamlit
- Pandas
- SQLite
- Plotly
- Pytest

## Architecture

```text
User
 |
 v
Streamlit UI (app.py)
 |                 \
 v                  v
SQLite layer       Scheduling engine
(database.py)      (planner.py)
 |                  |
 v                  v
Tasks and plan  Prioritized sessions
 |
 v
Progress charts + CSV export
```

## Run locally

### 1. Install Python

Use Python 3.10 or newer.

### 2. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/smart-study-planner-ai.git
cd smart-study-planner-ai
```

### 3. Create and activate a virtual environment

**Windows**
```bash
python -m venv .venv
.venv\\Scripts\\activate
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the app

```bash
streamlit run app.py
```

Your browser should open the local Streamlit app. If it does not, use the local URL printed in the terminal.

## Run tests

```bash
pytest -q
```

## How the planner works

Each pending task gets a priority score based on:
- Difficulty: hard topics receive more weight
- Deadline urgency: tasks due soon receive more weight
- Estimated effort: longer tasks receive a modest boost

The planner assigns sessions of up to one hour until each day's available hours are used or all tasks are scheduled. Tasks not fitted into the selected planning window remain unscheduled and can be included by generating a longer plan.

## Project structure

```text
smart-study-planner-ai/
├── app.py
├── planner.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
└── tests/
    └── test_planner.py
```

## Future improvements

- User accounts and separate profiles
- Calendar view and reminders
- Break scheduling and Pomodoro timer
- Import tasks from CSV
- Personalized recommendations based on historical completion time
- Optional ML model to estimate task duration after collecting sufficient data
- Deploy the app so recruiters can try it online

## Privacy

The app stores task information locally in `study_planner.db`. Do not commit personal study data or the generated database to GitHub.

## License

This project is provided under the MIT License. Add a `LICENSE` file before publishing if you want to formally apply that license.
