from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime
import time

URL = "https://www.decaturga.com/calendar"

# Configure headless browser
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get(URL)
time.sleep(5)  # Give the page time to load

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

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

print(f"Found {len(events)} events")

if events:
    calendar = Calendar(events=events)
    with open("decatur.ics", "w") as f:
        f.write(str(calendar))
else:
    print("⚠️ No events found. Check selectors or timing.")
