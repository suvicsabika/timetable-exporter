from bs4 import BeautifulSoup
import re
from datetime import datetime
from typing import List

#  Hungarian months to English monts, for datetime to understand
MONTHS_HU = {
    "január": "January",
    "február": "February",
    "március": "March",
    "április": "April",
    "május": "May",
    "június": "June",
    "július": "July",
    "augusztus": "August",
    "szeptember": "September",
    "október": "October",
    "november": "November",
    "december": "December"
}

def parse_hungarian_date(text: str) -> str:
    # Original text: "március 28. (péntek)"
    for hu, en in MONTHS_HU.items():
        if hu in text:
            text = text.replace(hu, en)
            break
    # "March 28. (péntek)" -> "March 28"
    text = text.split('(')[0].strip().replace('.', '')
    dt = datetime.strptime(text + " 2025", "%B %d %Y")  # static year
    return dt.strftime("%Y-%m-%d")

def scrape_schedule_from_file(file_path: str) -> List[dict]:
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    events = []

    for card in soup.find_all('div', class_='card'):
        try:
            header = card.find('div', class_='card-header')
            subject_full = header.get_text(strip=True)

            # Subject + type e.g.: "Szenzor adatok feldolgozása (L)"
            match = re.match(r"^(.*)\((.)\)$", subject_full)
            if match:
                subject = match.group(1).strip()
                subject_type = match.group(2).strip()
            else:
                subject = subject_full
                subject_type = "?"

            table_div = card.find('div', class_='card-body')
            if not table_div:
                print("Missing card-body, skipped.")
                continue

            table = table_div.find('table')
            if not table:
                print("Missing table, skipped.")
                continue

            rows = table.find_all('tr')


            location = lecturer = date = "?"

            for row in rows:
                th = row.find('th')
                td = row.find('td')
                if not th or not td:
                    continue
                label = th.get_text(strip=True)
                value = td.get_text(strip=True)
                if label == 'Terem:':
                    location = value
                elif label == 'Oktató:':
                    lecturer = value
                elif label == 'Dátum:':
                    date = parse_hungarian_date(value)

            card = table_div
            parent_td = card.find_parent('td')
            start_tag = parent_td.find('span', class_='start-badge')
            end_tag = parent_td.find('span', class_='end-badge')

            if not start_tag or not end_tag:
                print("Missing starting or ending time, skipped.")
                continue

            start_time = start_tag.get_text(strip=True)
            end_time = end_tag.get_text(strip=True)



            events.append({
                "subject": subject,
                "type": subject_type,
                "date": date,  # "2025-03-28"
                "start_time": start_time,  # "10:00"
                "end_time": end_time,      # "15:00"
                "location": location,
                "lecturer": lecturer
            })

        except Exception as e:
            print("Error occured:", e)

    return events

# Test
if __name__ == '__main__':
    from timetable_exporter.models import ClassEvent

    raw_events = scrape_schedule_from_file('generated_page.html')
    events = [ClassEvent.from_scraped(raw) for raw in raw_events]

    for e in events:
        print(e)
