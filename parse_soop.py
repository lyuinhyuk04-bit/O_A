from bs4 import BeautifulSoup
import json

with open("soop_page.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Print out some text elements or links to see the pattern
posts = []
# SOOP board list elements usually have class names like 'post_list' or 'list_board'
# Let's search for links containing '/post/' or having class names
links = soup.find_all('a')
for link in links:
    href = link.get('href', '')
    if '/post/' in href:
        parent_text = link.get_text(separator=' ', strip=True)
        posts.append({
            'href': href,
            'text': parent_text
        })

print("Found links with /post/:")
for p in posts[:20]:
    print(p)

# Also let's write all text of elements with suspicious class names
with open("soop_texts.txt", "w", encoding="utf-8") as out:
    for div in soup.find_all(['div', 'li', 'tr', 'span']):
        cls = div.get('class', [])
        if cls:
            text = div.get_text(strip=True)
            if text and len(text) < 200:
                out.write(f"Class {cls}: {text}\n")
