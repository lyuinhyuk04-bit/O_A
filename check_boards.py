from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, re

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')

urls = [
    "https://www.sooplive.com/station/amaiyk0105/board/109321189",
    "https://www.sooplive.com/station/amaiyk0105/board/123920023",
]

for url in urls:
    print(f"\n--- {url} ---")
    d = webdriver.Chrome(options=opts)
    d.get(url)
    time.sleep(5)
    text = d.find_element("tag name", "body").text
    d.quit()
    # Print first 400 chars
    print(text[:600])
    print("...")
