import json, re

with open('notices_cache.json', 'r', encoding='utf-8') as f:
    cache = json.load(f)

for member, text in cache.items():
    if not text:
        continue
    # Find station IDs in the text
    station_ids = re.findall(r'sooplive\.com/station/([^/\s"\']+)', text)
    post_urls = re.findall(r'sooplive\.com/station/[^/]+/post/\d+', text)
    
    # Find board IDs mentioned in link text or navigation  
    board_ids = re.findall(r'/board/(\d+)', text)
    
    unique_stations = list(set(station_ids))
    unique_boards = list(set(board_ids))
    
    print(f"[{member}]")
    print(f"  Station IDs: {unique_stations}")
    print(f"  Board IDs: {unique_boards}")
    if post_urls:
        print(f"  Sample post: {post_urls[0]}")
    print()
