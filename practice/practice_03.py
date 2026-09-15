"""
    실습용 사이트에서
        종목 메뉴 페이지의 섹터를 "IT 서비스"로 검색한 결과 데이터를 추출
    
    - 요청 주소: ??
    TODO: 오늘(09/15) 18시까지 이메일로 제출
"""
import requests, json
from urllib.parse import urljoin

from config import BASE, HEADERS, TIMEOUT
import parsers

resp = requests.get(f"{urljoin(BASE, '/stocks?sector=S08')}", headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()

html = resp.text

stocks = parsers.parse_stocks(html)

print(f"{'코드':<8}{'종목명':<14}{'섹터':<10}{'현재가':>12}{'등락률':>9}")

for s in stocks:
    print(f"{s['code']:<8}{s['name']:<14}{s['sector']:<10}{s['price']:>12}{s['rate']:>9}")

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

save_json(stocks,"stocks_for_practice.json")