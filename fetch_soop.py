from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

try:
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.sooplive.com/station/gjstn7637/board/120654963")
    
    # Wait for the board list to load
    # Usually the board posts have some specific class name or tag
    time.sleep(5)
    
    # Let's save the page source to analyze it
    html = driver.page_source
    with open("soop_page.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    print("Success: Page source saved to soop_page.html")
    driver.quit()
except Exception as e:
    print("Error:", e)
