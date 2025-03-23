# -----------------------------
# timetable_exporter/main.py
# -----------------------------

from .scraping import scrape_schedule_from_file
from .fetch_html import fetch_dynamic_html
from .processor import events_to_dataframe, export_to_ics, export_to_csv

# NEXT TODO IN VERSION 1.1:
# Use the ClassEvent: converting to ClassEvents -> objects -> list of objects
# Create the .ics file
# Send the e-mail with the .ics file
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
    #####################################################################################xxxx
    
    # export_to_ics(events, "timetable.ics")

    # print("Export done: timetable.csv és timetable_DATE_YEAR_COURSE.ics")


if __name__ == "__main__":
    main()
