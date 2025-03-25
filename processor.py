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


def dict_to_events(events: List[dict]) -> List[ClassEvent]:
    return [ClassEvent.from_scraped(event) for event in events]


def export_to_ics(events: List[ClassEvent], filename: str):
    """ Three main bugs:
    
    1. Wrong path, it saves into Documents instead of the project folder.
    2. UTF-8 is missing, á and é characters are marked with a ? mark.
    3. The time description is correct but the actual time setting is +1 hour, time zone difference issue."""
    calendar = Calendar()
    for event in events:
        calendar.events.add(event.to_ics_event())
        
    base_dir = os.path.dirname(os.path.abspath(__file__))  # location of main.py
    full_path = os.path.join(base_dir, filename)

    with open(full_path, "w", encoding="utf-8") as f:
        f.writelines(calendar)


def export_to_csv(df: pd.DataFrame, filename: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # location of main.py
    full_path = os.path.join(base_dir, filename)
    df.to_csv(full_path, index=False, encoding="utf-8")
    print(f"Successful export: {full_path}")
