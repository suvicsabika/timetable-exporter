# -----------------------------
# timetable_exporter/models.py
# -----------------------------

from dataclasses import dataclass
from datetime import datetime, time
from ics import Event
from bs4 import BeautifulSoup
import re

@dataclass
class ClassEvent:
    """ Example from https://levelezo.inf.unideb.hu/orarend/#/timetable?program=AT-MSC-23-1

    Szenzor adatok feldolgozása (L)
    Kód:	ILMAM9914-23 / ILMAM9914L
    Szak:	Adattudomány MSc, 1. évfolyam (2023)
    Terem:	IK-206 (10:00-15:00)
    Oktató:	Ujvári Balázs
    Dátum:	március 28. (péntek)"""

    subject: str
    date: datetime
    start_time: time
    end_time: time
    location: str
    lecturer: str
    type: str  # Pl. 'E' (Előadás), 'L' (Labor), 'Gy' (Gyakorlat)

    @classmethod
    def from_scraped(cls, raw: dict) -> "ClassEvent":
        """Creating an object from the proccessed text."""
        return cls(
            subject=raw["subject"],
            date=datetime.strptime(raw["date"], "%Y-%m-%d"),
            start_time=datetime.strptime(raw["start_time"], "%H:%M").time(),
            end_time=datetime.strptime(raw["end_time"], "%H:%M").time(),
            location=raw["location"],
            lecturer=raw["lecturer"],
            type=raw["type"]
        )

    def to_dict(self) -> dict:
        """Converting to dict for pandas DataFrame or export."""
        return {
            "subject": self.subject,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "location": self.location,
            "lecturer": self.lecturer,
            "type": self.type
        }

    def to_ics_event(self) -> Event:
        """ics.Event object creation for export."""
        event = Event()
        event.name = self.subject
        event.begin = datetime.combine(self.date, self.start_time)
        event.end = datetime.combine(self.date, self.end_time)
        event.location = self.location
        event.description = f"Oktató: {self.lecturer}"
        return event
