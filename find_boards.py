from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time, json, re

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')

sid = "amaiyk0105"
url = f"https://www.sooplive.com/station/{sid}/board"

d = webdriver.Chrome(options=opts)
d.get(url)
time.sleep(5)

html = d.page_source
d.quit()

# Parse with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all links with /board/ pattern
boards = []
seen = set()
for a in soup.find_all('a', href=re.compile(r'/board/\d+')):
    href = a.get('href', '')
    m = re.search(r'/board/(\d+)', href)
    if m:
        bid = m.group(1)
        if bid not in seen:
            seen.add(bid)
            text = a.get_text(strip=True)
            boards.append({"board_id": bid, "name": text, "url": "https://www.sooplive.com" + href if href.startswith('/') else href})

print(f"Found {len(boards)} boards for {sid}:")
for b in boards:
    print(f"  [{b['board_id']}] '{b['name']}': {b['url']}")

with open("board_search_result.json", "w", encoding="utf-8") as f:
    json.dump({"유키": boards}, f, ensure_ascii=False, indent=2)
print("\nSaved to board_search_result.json")

