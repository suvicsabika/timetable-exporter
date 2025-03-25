# -----------------------------
# timetable_exporter/main.py
# -----------------------------

from .scraping import scrape_schedule_from_file
from .fetch_html import fetch_dynamic_html
from .processor import events_to_dataframe, dict_to_events, export_to_csv, export_to_ics

# NEXT TODO IN VERSION 1.1:
# DONE >>> Use the ClassEvent: converting to ClassEvents -> objects -> list of objects
# DONE >>> Create the .ics file
# NEXT TODO IN VERSION 1.2:
# IN PROGRESS >>> Send the e-mail with the .ics file
# IN PROGRESS >>> E-mail template fixing
# -----------------------------

def main():
    # WORKING PART
    #####################################################################################xxxx
    # url = "https://levelezo.inf.unideb.hu/orarend/#/timetable?program=AT-MSC-23-1"
    # |-> In next year, it will be AT-MSC-23-2
    
    # fetch_dynamic_html(url)

    events = scrape_schedule_from_file("generated_page.html")

    print(events)

    df = events_to_dataframe(events)

    export_to_csv(df, "timetable.csv")
    
    event_objects = dict_to_events(events)
    
    export_to_ics(event_objects, "timetable.ics")

    # print("Export done: timetable.csv és timetable_DATE_YEAR_COURSE.ics")


if __name__ == "__main__":
    main()
