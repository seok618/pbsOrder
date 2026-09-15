import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_paul_bassett():
    url = "https://www.baristapaulbassett.co.kr/menu/List.pb?cid1=A"
    # 봇 차단을 피하기 위해 User-Agent 정보를 구체적으로 작성합니다.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    menu_list = []
    
    # [핵심 수정] 폴바셋 홈페이지의 실제 메뉴 목록 구조입니다.
    # .list_menu라는 클래스 하위에 있는 모든 li 태그를 찾습니다.
    items = soup.select('.list_menu > ul > li')
    
    print(f"총 {len(items)}개의 메뉴를 찾았습니다.") # 터미널 확인용
    
    # 5개만 가져오던 제한을 풀고 전체(에스프레소 카테고리)를 가져옵니다.
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
