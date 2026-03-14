import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

# 1. 경로 설정 (분석가님 경로에 맞게 확인!)
data_path = r"C:/02WorkSpaces/Project3/saveFiles/FINAL_COMBINED_REVIEWS.csv"

if os.path.exists(data_path):
    # 2. 데이터 불러오기
    df = pd.read_csv(data_path)
    
    # [중요] 리뷰 데이터가 비어있지 않은 것들만 추려냅니다
    df = df.dropna(subset=['review'])
    
    # 3. 라벨링 (학습을 위해 임시로 긍정/부정 기준을 정함)
     # 3. 라벨링 로직 업데이트 (긍정 단어를 대폭 추가!)
    pos_words = [
    '재미', '최고', '추천', '감동', '좋아', '재밌', '꿀잼', '훌륭', '대박', 
    '명작', '기대', '볼만', '굿', '최고', '위로', '따뜻', '힐링', '감동', '진국'
    ]

    df['label_num'] = df['review'].apply(lambda x: 1 if any(word in str(x) for word in pos_words) else 0)

    # [추가 팁] 데이터가 한쪽으로 쏠렸는지 확인하기 위한 코드
    print("--- 데이터 분포 확인 ---")
    print(df['label_num'].value_counts())

    # 4. TF-IDF 교육 (단어를 숫자로 바꾸는 법 배우기)
    # 이 과정이 "tfidf" 노란 줄을 없애는 핵심입니다!
    tfidf = TfidfVectorizer(max_features=2000) 
    X = tfidf.fit_transform(df['review'].astype(str)) # 전체 리뷰로 교육!
    y = df['label_num']

    # 5. 모델 교육 (데이터 간의 관계 학습)
    model = LogisticRegression()
    model.fit(X, y)

    # 6. 저장 (이제 노란 줄이 사라질 거예요!)
    joblib.dump(model, 'my_movie_model.pkl')
    joblib.dump(tfidf, 'my_tfidf.pkl')

    print(f"총 {len(df)}개의 리뷰 데이터를 성공적으로 학습시켰습니다!")
    print("'my_movie_model.pkl'과 'my_tfidf.pkl'이 생성되었습니다.")

else:
    print("파일 경로를 찾을 수 없습니다. 경로를 다시 확인해 주세요!")