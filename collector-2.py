import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def final_booster_collect():
    # 1. 대상 영화 리스트
    movie_list = ["어바웃타임", "극한직업", "기생충", "너의이름은", "범죄도시4"]
    save_path = "C:/02WorkSpaces/Project3/saveFiles/movie_TOTAL_v2_dataset.csv"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for movie in movie_list:
        print(f"\n🔥 [{movie}] 수집 시작! 지금부터 40초간 '더보기'를 광클하세요!!")
        url = f"https://search.naver.com/search.naver?query=영화+{movie}+관람평"
        driver.get(url)
        
        # 40초 동안 사용자님이 스크롤 내리고 더보기 누를 시간을 줍니다.
        # 이 시간 동안 화면에 리뷰를 최대한 많이 펼쳐야 합니다!
        time.sleep(40) 

        print(f"📸 [{movie}] 펼쳐진 데이터 낚시질 중...")
        all_reviews = []
        
        # 우리가 찾아낸 모든 성공적인 선택자들을 다 넣었습니다.
        items = driver.find_elements(By.CSS_SELECTOR, "span._text, span.desc, div.comment_content, p.text")
        
        for item in items:
            txt = item.text.strip()
            # 15자 이상의 의미 있는 문장만 수집
            if len(txt) > 15 and "더보기" not in txt and "관람평" not in txt:
                all_reviews.append(txt)
        
        unique_reviews = list(set(all_reviews))
        print(f"🎯 [{movie}] 이번 판 성공: {len(unique_reviews)}개!")

        # 즉시 파일에 추가 저장
        if unique_reviews:
            df = pd.DataFrame({'label': [movie] * len(unique_reviews), 'review': unique_reviews})
            df.to_csv(save_path, mode='a', index=False, header=not os.path.exists(save_path), encoding='utf-8-sig')

    driver.quit()
    print("\n✨ 모든 영화 수집 완료! 이제 파일을 확인해보세요.")
    
if __name__ == "__main__":
    final_booster_collect()    
