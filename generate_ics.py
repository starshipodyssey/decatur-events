import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime
import re

URL = "https://www.decaturga.com/calendar"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_events():
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")
    events = []

    for item in soup.select(".event-title a"):
        title = item.get_text(strip=True)
        link = "https://www.decaturga.com" + item["href"]
        date_block = item.find_parent("li").find("span", class_="date-display-single")
        date_text = date_block.get("content", "") if date_block else ""
        try:
            dt = datetime.strptime(date_text, "%Y-%m-%dT%H:%M:%S")
        except:
            continue

        event = Event()
        event.name = title
        event.begin = dt
        event.url = link
        events.append(event)
    
    return events

def build_calendar(events):
    c = Calendar()
    for e in events:
        c.events.add(e)
    return c

if __name__ == "__main__":
    events = fetch_events()
    calendar = build_calendar(events)
    with open("decatur.ics", "w") as f:
        f.write(str(calendar))

