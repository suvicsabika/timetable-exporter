# -----------------------------
# timetable_exporter/processor.py
# -----------------------------

import pandas as pd
from ics import Calendar
from .models import ClassEvent
from typing import List
import os

# def events_to_dataframe(events: List[ClassEvent]) -> pd.DataFrame:
#     return pd.DataFrame([e.to_dict() for e in events])
def events_to_dataframe(events: List[dict]) -> pd.DataFrame:
    return pd.DataFrame(events)


def export_to_ics(events: List[ClassEvent], filename: str):
    calendar = Calendar()
    for event in events:
        calendar.events.add(event.to_ics_event())
    with open(filename, "w") as f:
        f.writelines(calendar)



def export_to_csv(df: pd.DataFrame, filename: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # location of main.py
    full_path = os.path.join(base_dir, filename)
    df.to_csv(full_path, index=True, encoding="utf-8")
    print(f"Successful export: {full_path}")


def export_to_excel(df: pd.DataFrame, filename: str):
    df.to_excel(filename, index=False)
