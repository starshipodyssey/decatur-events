from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime
import time

URL = "https://www.decaturga.com/calendar"

# Headless Chrome setup
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

driver.get(URL)

# Wait until the event list loads
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".event-title a"))
    )
    print("✅ Event items loaded.")
except:
    print("⚠️ Timed out waiting for events to load.")
    driver.quit()
    exit()

# Now parse the loaded HTML
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

    print(f"📅 Found event: {title} on {date_text}")

    event = Event()
    event.name = title
    event.begin = dt
    event.url = link
    events.append(event)

print(f"✅ Total events found: {len(events)}")

if events:
    calendar = Calendar(events=events)
    with open("decatur.ics", "w") as f:
        f.write(str(calendar))
else:
    print("⚠️ No events found — check CSS selectors or page structure.")
