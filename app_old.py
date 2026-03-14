import streamlit as st
import pandas as pd
import os
import joblib  # 직접 만든 모델을 불러오기 위해 필수!

# 1. 커스텀 모델 로드 (분석가님이 만든 pkl 파일 사용)
@st.cache_resource
def load_custom_model():
    # 저장된 모델과 벡터라이저를 불러옵니다.
    # 파일이 app.py와 같은 위치에 있는지 확인하세요.
    model = joblib.load('my_movie_model.pkl')
    tfidf = joblib.load('my_tfidf.pkl')
    return model, tfidf

# 모델 로드 시도
try:
    model, tfidf = load_custom_model()
except Exception as e:
    st.error(f"모델 파일을 찾을 수 없습니다. 에러내용: {e}")

# 2. 앱 페이지 설정
st.set_page_config(page_title="리뷰파인더 (Review Finder)", layout="wide")

# 3. 제목 부분
st.title("🔍 리뷰파인더 (Review Finder)")
st.subheader("3,012개의 관람객 리뷰를 분석해, 당신의 기분에 딱 맞는 영화를 찾아드립니다.")
st.markdown("---")

# 4. 사이드바: 기분 선택
st.sidebar.header("🎭 지금 기분이 어떠신가요?")
mood = st.sidebar.radio(
    "기분을 선택하면 AI가 리뷰를 매칭해 드립니다.",
    ["감동받고 싶어 (슬픔/위로)", "심장이 뛰고 싶어 (액션/스릴러)", "웃고 싶어 (코미디/드라마)"]
)

# 5. 메인 화면 구성 (2단 컬럼)
col1, col2 = st.columns([1, 1])

# --- 왼쪽: 분석 시각화 (워드클라우드) ---
with col1:
    st.header("📊 관객들의 생각 (키워드)")
    image_path = r"C:/02WorkSpaces/Project3/saveFiles/movie_wordcloud_final.png" 
    
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True, caption=f"'{mood}' 관련 키워드 분석")
    else:
        st.warning("워드클라우드 이미지 파일을 찾을 수 없습니다.")

# --- 오른쪽: 리뷰 추천 서비스 ---
with col2:
    st.header("💬 맞춤형 리뷰 추천")
    
    search_query = st.text_input("🔍 찾고 싶은 영화나 키워드를 입력하세요", placeholder="예: 원더랜드, 하이재킹, 감동")
    data_path = r"C:/02WorkSpaces/Project3/saveFiles/FINAL_COMBINED_REVIEWS.csv"
    
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        
        if search_query:
            # 검색어가 있으면 전체 데이터에서 검색
            filtered_df = df[
                df['label'].str.contains(search_query, na=False, case=False) | 
                df['review'].str.contains(search_query, na=False, case=False)
            ]
            st.info(f"🔍 '{search_query}' 검색 결과: {len(filtered_df)}건")
        else:
            # 검색어가 없을 때 기분별 필터링
            if "감동" in mood:
                target_keywords = "감동|눈물|슬픔|최고|여운|인생"
            elif "심장" in mood:
                target_keywords = "액션|긴장|스릴|대박|전율|몰입"
            else:
                target_keywords = "재미|웃음|힐링|가족|행복|드라마"
            
            filtered_df = df[df['review'].str.contains(target_keywords, na=False, case=False)]
            st.success(f"✅ '{mood}' 기분에 맞는 리뷰입니다.")

        # 리뷰 목록 출력
        st.dataframe(filtered_df[['label', 'review']].head(50), use_container_width=True, height=400)
    else:
        st.error("데이터 파일을 찾을 수 없습니다.")

# 6. 하단: AI 딥러닝 문맥 분석
if search_query:
    st.markdown("---")
    st.header("🧠 AI 딥러닝 문맥 분석 (학습 모델 v1.0)")
    
    # 1. 입력된 텍스트를 숫자로 변환
    vec_input = tfidf.transform([search_query])
    
    # 2. 결과 예측 (1: 긍정, 0: 부정)
    prediction = model.predict(vec_input)[0]
    
    # 3. 확신도 계산 (score)
    prob = model.predict_proba(vec_input)[0]
    score = max(prob)
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        if prediction == 1: # 긍정일 때
            st.success(f"### 😊 긍정적 맥락\n(확신도: {score:.1%})")
        else: # 부정일 때
            st.warning(f"### 🤔 주의/부정적 맥락\n(신뢰도: {score:.1%})")
            
    with col_b:
        st.write(f"🤖 **AI 분석 의견:**")
        if prediction == 1:
            st.write(f"입력하신 '{search_query}'(은)는 긍정적인 맥락으로 파악됩니다. 관련 리뷰들을 즐겁게 감상하세요!")
        else:
            st.write(f"입력하신 '{search_query}'(은)는 해당 장르에서 다소 중립적이거나 부정적인 맥락으로 쓰였을 가능성이 있습니다. 리뷰의 실제 내용을 다시 한번 확인해 보세요.")

# 7. 최하단: AI 추천 한 줄
st.markdown("---")
st.header("💡 오늘의 추천 한 마디")
if "감동" in mood:
    st.write("👉 배우들의 명연기가 빛나는 영화들입니다. 손수건을 준비하세요!")
elif "심장" in mood:
    st.write("👉 손에 땀을 쥐게 하는 긴장감! 지금 바로 몰입해 보세요.")
else:
    st.write("👉 지친 하루를 달래줄 유쾌한 영화들이 당신을 기다립니다.")