import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_paul_bassett():
    url = "https://www.baristapaulbassett.co.kr/menu/List.pb?cid1=A"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    menu_list = []
    items = soup.select('.menu_list > li')
    
    for item in items[:5]: # 테스트용 5개
        name = item.select_one('.txtWrap > .name').text.strip()
        img_src = "https://www.baristapaulbassett.co.kr" + item.select_one('img')['src']
        
        menu_list.append({
            "name": name,
            "img": img_src, 
            "cal": "150 kcal", # 실제 영양정보 크롤링 로직은 추후 보완
            "sugar": "10g", 
            "caffeine": "150mg"
        })
        
    # [수정된 부분] 수집한 데이터를 menu.json 파일로 저장합니다.
    # 현재 스크립트가 실행되는 위치에 파일을 만듭니다.
    with open('menu.json', 'w', encoding='utf-8') as f:
        json.dump(menu_list, f, ensure_ascii=False, indent=4)
    
    print("메뉴 크롤링 및 menu.json 파일 저장이 완료되었습니다.")

if __name__ == "__main__":
    scrape_paul_bassett()
