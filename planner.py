from datetime import date, timedelta
import pandas as pd

DIFFICULTY_WEIGHT = {"Easy": 1.0, "Medium": 2.0, "Hard": 3.0}
SESSION_HOURS = 1.0


def calculate_priority(task, today):
    """Higher scores mean a task should be scheduled earlier."""
    due = date.fromisoformat(str(task["due_date"]))
    days_left = (due - today).days
    urgency = 5.0 if days_left <= 0 else 5.0 / (days_left + 1)
    difficulty = DIFFICULTY_WEIGHT.get(str(task["difficulty"]), 2.0)
    remaining_hours = float(task["estimated_hours"])
    effort = min(remaining_hours, 5.0) / 5.0
    return round(difficulty + urgency + effort, 3)


def generate_schedule(tasks, start_date, plan_days, daily_hours):
    """
    Greedy, explainable scheduler.
    Returns one row per study session. Each session is at most one hour,
    and the total scheduled hours per day never exceeds daily_hours.
    """
    columns = ["date", "subject", "topic", "hours", "priority", "reason"]
    if tasks is None or len(tasks) == 0:
        return pd.DataFrame(columns=columns)

    pending = tasks[tasks["status"] != "Completed"].copy()
    if pending.empty:
        return pd.DataFrame(columns=columns)

    work = []
    for _, row in pending.iterrows():
        task = row.to_dict()
        task["remaining"] = float(task["estimated_hours"])
        task["priority"] = calculate_priority(task, start_date)
        work.append(task)

    result = []
    for day_offset in range(plan_days):
        current_day = start_date + timedelta(days=day_offset)
        available = float(daily_hours)
        while available > 1e-9:
            eligible = [t for t in work if t["remaining"] > 1e-9]
            if not eligible:
                break
            eligible.sort(
                key=lambda t: (
                    calculate_priority(t, current_day),
                    t["priority"],
                    -t["remaining"],
                ),
                reverse=True,
            )
            task = eligible[0]
            hours = min(SESSION_HOURS, available, task["remaining"])
            due = date.fromisoformat(str(task["due_date"]))
            if due < current_day:
                reason = "Overdue · prioritize now"
            elif (due - current_day).days <= 2:
                reason = "Deadline approaching"
            elif task["difficulty"] == "Hard":
                reason = "Difficult topic"
            else:
                reason = "Balanced study session"
            result.append({
                "date": current_day.isoformat(),
                "subject": str(task["subject"]),
                "topic": str(task["topic"]),
                "hours": round(hours, 2),
                "priority": calculate_priority(task, current_day),
                "reason": reason,
            })
            task["remaining"] = round(task["remaining"] - hours, 5)
            available = round(available - hours, 5)

    return pd.DataFrame(result, columns=columns)
