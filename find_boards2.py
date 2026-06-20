from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, re, json

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')

# SOOP station IDs to investigate
targets = {
    "유키":  "amaiyk0105",
}

results = {}

for name, sid in targets.items():
    print(f"\n=== {name} ({sid}) ===")
    d = webdriver.Chrome(options=opts)
    try:
        # Go to station home to find the board navigation
        d.get(f"https://www.sooplive.com/station/{sid}")
        time.sleep(6)
        
        # Try to find board links rendered by JS
        els = d.find_elements(By.XPATH, '//a[contains(@href, "/board/")]')
        boards = []
        seen = set()
        for el in els:
            href = el.get_attribute('href') or ''
            m = re.search(r'/board/(\d+)', href)
            if m:
                bid = m.group(1)
                if bid not in seen:
                    seen.add(bid)
                    boards.append({"id": bid, "name": el.text.strip(), "url": href})
        
        if not boards:
            # Try clicking on the board menu item
            board_nav = d.find_elements(By.XPATH, '//a[contains(text(), "게시판") or contains(text(), "Board") or contains(text(), "공지")]')
            for nav in board_nav[:5]:
                print(f"  Nav item: '{nav.text}' -> {nav.get_attribute('href')}")
        
        print(f"  Found {len(boards)} board links:")
        for b in boards:
            print(f"    [{b['id']}] '{b['name']}': {b['url']}")
        
        results[name] = {"sid": sid, "boards": boards}
        
        if not boards:
            # Save page source snippet for debugging
            src = d.page_source
            # Find any board-related content
            board_mentions = re.findall(r'board["\s:/]+\d+', src[:50000])
            print(f"  Board mentions in source: {list(set(board_mentions))[:5]}")
    except Exception as e:
        print(f"  Error: {e}")
    finally:
        d.quit()

with open("member_boards.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("\nSaved to member_boards.json")
