import cloudscraper
from bs4 import BeautifulSoup
import json
import urllib3

# SSL 경고 숨기기
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_paul_bassett():
    url = "https://www.baristapaulbassett.co.kr/menu/List.pb?cid1=A"
    
    # [핵심] 일반 requests 대신 cloudscraper를 생성하여 방화벽을 우회합니다!
    scraper = cloudscraper.create_scraper()
    
    # verify=False 옵션은 그대로 유지
    response = scraper.get(url, verify=False)
    
    # 🚨 디버깅: 방화벽이 뚫렸는지 확인하기 위해 깃액션 로그에 HTML 앞 300자를 찍어봅니다.
    print("✅ 서버 응답 텍스트 일부 확인:")
    print(response.text[:300]) 
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    items = soup.select('.list_menu > ul > li')
    print(f"찾아낸 메뉴 개수: {len(items)}") 
    
    menu_list = []
    
    for item in items:
        try:
            name_tag = item.select_one('.txtArea > p')
            if not name_tag:
                continue
            name = name_tag.text.strip()
            
            img_tag = item.select_one('img')
            if img_tag and img_tag.has_attr('src'):
                img_src = "https://www.baristapaulbassett.co.kr" + img_tag['src']
            else:
                img_src = ""
            
            menu_list.append({
                "name": name,
                "img": img_src, 
                "cal": "150 kcal", 
                "sugar": "10g", 
                "caffeine": "150mg"
            })
        except Exception as e:
            pass
            
    with open('menu.json', 'w', encoding='utf-8') as f:
        json.dump(menu_list, f, ensure_ascii=False, indent=4)
    
    print("메뉴 크롤링 및 menu.json 파일 저장이 완료되었습니다.")

if __name__ == "__main__":
    scrape_paul_bassett()
