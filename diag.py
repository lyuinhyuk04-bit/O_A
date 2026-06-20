import json
from collections import Counter

with open('schedule.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. member 필드 분포
print("=== member 필드 분포 ===")
counts = Counter(s.get('member', 'NONE') for s in data)
for k, v in sorted(counts.items()):
    print(f"  {k}: {v}개")

# 2. 오아 이번주 (6/9~6/15) 일정
print("\n=== 오아 6월 9~21일 일정 ===")
oa = [s for s in data if s.get('member') == 'oa']
for s in sorted(oa, key=lambda x: x['date']):
    if '2026-06-09' <= s['date'] <= '2026-06-21':
        print(f"  {s['date']} {s['day']} {s['time']} | {s['title'][:40]}")

# 3. 다른 멤버 샘플
print("\n=== 유키 최근 3개 ===")
yuki = sorted([s for s in data if s.get('member') == 'yuki'], key=lambda x: x['date'])
for s in yuki[-3:]:
    print(f"  {s['date']} {s['time']} | {s['title'][:40]}")

print("\n=== member 없는 항목 수 ===")
no_member = [s for s in data if not s.get('member')]
print(f"  {len(no_member)}개")
