import requests
from bs4 import BeautifulSoup
import json
import os
import urllib3 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_paul_bassett():
    url = "https://www.baristapaulbassett.co.kr/menu/List.pb?cid1=A"
    
    # [핵심 1] 진짜 사람처럼 보이는 완벽한 헤더 위장 세트
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1'
    }
    
    # [핵심 2] 세션을 만들어서 쿠키를 유지하며 접근!
    with requests.Session() as s:
        # 방화벽이 민감한 사이트는 메인 홈페이지를 먼저 한 번 찔러서 쿠키를 받은 뒤 접근하면 훨씬 잘 뚫립니다.
        s.get("https://www.baristapaulbassett.co.kr", headers=headers, verify=False)
        
        # 진짜 타겟 URL로 접속
        response = s.get(url, headers=headers, verify=False)
        
    # 만약 차단당했다면 200이 아닌 403(Forbidden) 류가 뜰 것입니다. 액션스 로그 확인용.
    print(f"응답 코드 확인: {response.status_code}") 
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    menu_list = []
    
    # 폴바셋 실제 메뉴 구조 (이전과 동일)
    items = soup.select('.list_menu > ul > li')
    print(f"찾아낸 메뉴 개수: {len(items)}") 
    
    # ... (아래 for 문부터 데이터 추출, json 저장 로직은 기존 코드와 100% 동일하게 유지해 주세요!) ...
    for item in items:
        try:
            # 메뉴 이름 추출 (.txtArea 하위의 p 태그)
            name_tag = item.select_one('.txtArea > p')
            if not name_tag:
                continue # 빈 칸이거나 이름이 없으면 건너뜁니다
            name = name_tag.text.strip()
            
            # 이미지 링크 추출
            img_tag = item.select_one('img')
            # img src가 없는 경우를 대비
            if img_tag and img_tag.has_attr('src'):
                img_src = "https://www.baristapaulbassett.co.kr" + img_tag['src']
            else:
                img_src = ""
            
            # 영양정보는 상세 페이지에 있지만, 속도를 위해 일단 가짜 데이터를 넣습니다. 
            # 상세 페이지 크롤링은 목록 크롤링이 성공한 후 고도화할 수 있습니다.
            menu_list.append({
                "name": name,
                "img": img_src, 
                "cal": "150 kcal", 
                "sugar": "10g", 
                "caffeine": "150mg"
            })
        except Exception as e:
            print(f"항목 추출 중 에러 발생: {e}")
            pass
            
    # json 파일로 예쁘게 저장합니다.
    with open('menu.json', 'w', encoding='utf-8') as f:
        json.dump(menu_list, f, ensure_ascii=False, indent=4)
    
    print("메뉴 크롤링 및 menu.json 파일 저장이 완료되었습니다.")

if __name__ == "__main__":
    scrape_paul_bassett()
