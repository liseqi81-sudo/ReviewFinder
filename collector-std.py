import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import random

def get_real_reviews(movie_name):
    """
    네이버 영화 관람평 페이지에서 리뷰를 수집하는 함수
    :param movie_name: 검색할 영화 제목
    :return: 중복이 제거된 리뷰 리스트
    """
    # 1. 크롬 드라이버 설정 (자동화 감지 회피 및 창 최대화)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) # 자동화 제어 메시지 제거
    options.add_argument("--start-maximized") # 브라우저 창을 최대 크기로 실행 (버튼 가림 방지)
    
    # webdriver_manager를 통해 크롬 드라이버를 자동으로 설치하고 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # 2. 검색 페이지 접속
    # 영화 제목 뒤에 '관람평'을 붙여 네이버 검색 결과의 관람평 탭으로 바로 유도
    url = f"https://search.naver.com/search.naver?query=영화+{movie_name}+관람평"
    driver.get(url)
    time.sleep(3) # 페이지 로딩을 위해 3초 대기 (네트워크 속도 고려)

    print(f"[{movie_name}] 리뷰 무한 스크롤 및 더보기 클릭 중...")
    
    # 3. '더보기' 버튼 반복 클릭 (데이터 펼치기)
    for i in range(30): # 최대 30번 클릭 시도
        try:
            # [포인트] 화면 끝까지 스크롤하여 '더보기' 버튼이 화면에 나타나게 함
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.2)
            
            # [XPATH 활용] 텍스트가 '더보기'인 요소를 정밀하게 타격
            # //a[@role='button']: 버튼 역할을 하는 <a> 태그 중에서
            # //span[contains(text(), '더보기')]: '더보기'라는 글자를 포함한 <span> 찾기
            more_btn = driver.find_element(By.XPATH, "//a[@role='button']//span[contains(text(), '더보기')]")
            
            # [JS 클릭] 일반적인 click()은 다른 요소에 가려지면 에러가 나므로, JavaScript로 직접 클릭 명령
            driver.execute_script("arguments[0].click();", more_btn)
            
            print(f"   - 더보기 클릭 성공 ({i+1}/30)")
            
            # [랜덤 대기] 네이버의 매크로 차단 방지를 위해 1.0~1.5초 사이로 랜덤하게 쉼
            time.sleep(random.uniform(1.0, 1.5))
        except:
            # 더 이상 클릭할 버튼이 없으면(끝까지 다 펼쳤으면) 루프 탈출
            break

    # 4. 펼쳐진 화면에서 리뷰 데이터 추출
    all_reviews = []
    
    # [사용자 피드백 반영] F12로 찾은 'span.desc._text' 클래스를 정확히 타격
    # 셀레니움의 find_elements는 해당 조건에 맞는 모든 요소를 리스트 형태로 반환함
    items = driver.find_elements(By.CSS_SELECTOR, "span.desc._text")
    
    for item in items:
        try:
            # [innerText 중요!] item.text는 화면에 안 보이면 빈 값을 가져오는 경우가 많음
            # .get_attribute("innerText")를 사용하면 HTML 안에 숨겨진 텍스트까지 싹 긁어옴
            rev = item.get_attribute("innerText").strip()
            
            # 리뷰 텍스트 안에 '더보기'라는 글자가 섞여 수집되는 경우가 있어 제거
            rev = rev.replace("더보기", "").strip()
            
            # 의미 없는 아주 짧은 리뷰(예: "와", "굳")는 10자 기준으로 필터링
            if len(rev) > 10:
                all_reviews.append(rev)
        except:
            continue
            
    driver.quit() # 브라우저 종료 (메모리 확보)
    
    # 5. 데이터 정제 및 반환
    unique_reviews = list(set(all_reviews)) # 중복 수집된 리뷰 제거 (Set 자료형 활용)
    print(f"   - 최종 추출 완료: {len(unique_reviews)}개 확보")
    
    return unique_reviews

if __name__ == "__main__":
    # 수집 대상 영화 리스트 (원하는 만큼 추가 가능)
    movie_list = ["인사이드아웃2", "듄2", "위키드", "하얼빈", "파묘"]
    
    # 결과 저장 경로 설정
    save_path = "C:/02WorkSpaces/Project3/saveFiles"
    file_full_path = f"{save_path}/movie_nav_dataset.csv"
    
    # 폴더가 없으면 자동으로 생성
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    print(f"총 {len(movie_list)}개 영화 수집 파이프라인 가동!")

    # 영화 리스트를 하나씩 돌면서 수집 작업 수행
    for movie_name in movie_list:
        print(f"\n--- [{movie_name}] 수집 시작 ---")
        new_reviews = get_real_reviews(movie_name)
        
        if new_reviews:
            # 수집된 데이터를 판다스 데이터프레임으로 변환
            df = pd.DataFrame({
                'label': [movie_name] * len(new_reviews), # 어떤 영화인지 태깅
                'review': new_reviews # 수집한 리뷰 본문
            })
            
            # [파일 저장 전략]
            # mode='a': 기존 파일이 있으면 끝에 이어쓰기 (Append)
            # header=not file_exists: 파일이 처음 만들어질 때만 컬럼명(label, review) 쓰기
            file_exists = os.path.isfile(file_full_path)
            df.to_csv(file_full_path, mode='a', index=False, header=not file_exists, encoding='utf-8-sig')
            
            print(f"[{movie_name}] 저장 완료!")
        else:
            print(f"[{movie_name}] 수집 실패 (데이터 확인 필요)")
            
        # 다음 영화로 넘어가기 전 서버 부하 방지를 위해 2초 대기
        time.sleep(2)

    # 6. 최종 수집 결과 요약 보고서 출력
    if os.path.exists(file_full_path):
        final_df = pd.read_csv(file_full_path)
        print("\n" + "="*40)
        print(f"📊 최종 수집 결과 보고서")
        print(f"전체 리뷰 수: {len(final_df)}개")
        print("-"*40)
        # 각 영화별로 몇 개씩 수집되었는지 요약
        print(final_df['label'].value_counts())
        print("="*40)