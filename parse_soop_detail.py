from bs4 import BeautifulSoup
import json
import re

with open("soop_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# SOOP board container
# Let's find elements that look like list rows
rows = []

# Method 1: Find by class matching board items
# Usually, list items have class names containing 'board' or 'list' or are simply 'li' inside a list ul/ol
# Let's look for all 'li' items in the document and print their text if they contain a post link
for li in soup.find_all('li'):
    a_tag = li.find('a', href=re.compile(r'/post/\d+'))
    if a_tag:
        # Extract all text inside this li
        text_content = li.get_text(separator=' | ', strip=True)
        # Try to find date format (e.g. 2026-06-14 or 12시간 전 or 10:15)
        # Dates are usually in span with class like 'date' or just matches regex
        rows.append({
            'href': a_tag.get('href'),
            'raw_text': text_content
        })

# Method 2: If no li found, try any tr
if not rows:
    for tr in soup.find_all('tr'):
        a_tag = tr.find('a', href=re.compile(r'/post/\d+'))
        if a_tag:
            text_content = tr.get_text(separator=' | ', strip=True)
            rows.append({
                'href': a_tag.get('href'),
                'raw_text': text_content
            })

# Save to json file safely without encoding crash
with open("parsed_soop_posts.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)

print(f"Success: Parsed {len(rows)} posts and saved to parsed_soop_posts.json")
