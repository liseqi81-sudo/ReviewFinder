import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def dune_final_attack():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://search.naver.com/search.naver?query=영화+듄2+관람평")
    driver.maximize_window()
    
    # [중요] 지금부터 30초 동안 수동으로 스크롤을 내리거나 더보기를 누르세요!
    print("🔥 [긴급] 지금부터 30초 동안 크롬 창에서 스크롤을 끝까지 내리거나 '더보기'를 광클하세요!!")
    time.sleep(30) 

    all_reviews = []
    # 보이는 모든 텍스트 요소를 다 가져옵니다.
    items = driver.find_elements(By.CSS_SELECTOR, "span._text, div.comment_content, p.text")
    
    for item in items:
        txt = item.text.strip()
        if len(txt) > 10:
            all_reviews.append(txt)
            
    unique_reviews = list(set(all_reviews))
    print(f"🎯 듄2 최종 성공: {len(unique_reviews)}개!")
    driver.quit()
    return unique_reviews

if __name__ == "__main__":
    res = dune_final_attack()
    if res:
        save_path = "C:/02WorkSpaces/Project3/saveFiles/movie_FINAL_TOTAL_dataset.csv"
        df = pd.DataFrame({'label': ["듄2"] * len(res), 'review': res})
        # 기존 파일 뒤에 붙이기
        df.to_csv(save_path, mode='a', index=False, header=False, encoding='utf-8-sig')
        print("✅ 파일 저장 완료!")