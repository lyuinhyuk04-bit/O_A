import json
with open('schedule.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

from collections import Counter
members = Counter(s.get('member','?') for s in data)
print('Total entries:', len(data))
for k, v in members.items():
    print(f'  {k}: {v}개')

print()
print('[유키 최근 일정]')
yuki = sorted([s for s in data if s.get('member')=='yuki'], key=lambda x: x['date'])
for s in yuki[-6:]:
    print(f"  {s['date']} {s['day']} {s['time']} - {s['title'][:35]}")
