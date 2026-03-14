import streamlit as st
import pandas as pd
import os
import joblib
import plotly.graph_objects as go

# 1. 모델 로드
@st.cache_resource
def load_custom_model():
    model = joblib.load('my_movie_model.pkl')
    tfidf = joblib.load('my_tfidf.pkl')
    return model, tfidf

try:
    model, tfidf = load_custom_model()
except Exception as e:
    st.error(f"모델 파일을 찾을 수 없습니다: {e}")

# 2. 페이지 설정
st.set_page_config(page_title="리뷰파인더 (Review Finder)", layout="wide")

# 3. 사이드바 구성 (입력 및 정보)
with st.sidebar:
    st.header("🎭 서비스 설정")
    mood = st.sidebar.radio(
        "지금 기분이 어떠신가요?",
        ["감동받고 싶어 (슬픔/위로)", "심장이 뛰고 싶어 (액션/스릴러)", "웃고 싶어 (코미디/드라마)"]
    )

    st.markdown("---")
    st.subheader("📊 전체 데이터 요약")
    # 긍부정 비율 도넛 차트
    fig_pie = go.Figure(data=[go.Pie(labels=['긍정', '부정'], values=[2100, 912], hole=.4)])
    fig_pie.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.info("""
    **📊 Model Info**
    - Algorithm: Logistic Regression
    - Accuracy: 85.4%
    - Data: 3,012 Reviews
    """)
    
    st.caption("🚀 사용법: 키워드를 검색하거나 기분을 선택해 보세요!")

# 4. 메인 화면 헤더
st.title("🔍 AI 리뷰파인더 (Review Finder)")
st.markdown("### 3,012개의 관람객 데이터를 학습한 커스텀 감성 분석 엔진")

# 대시보드 메트릭 배치
m1, m2, m3, m4 = st.columns(4)
m1.metric("학습 데이터", "3,012 건")
m2.metric("모델 유형", "NLP / TF-IDF")
m3.metric("파일 용량", "93.4 KB")
m4.metric("분석 상태", "실시간 (Active)", delta="Online")
st.markdown("---")

# 5. 탭 구성 (메인 화면을 두 개의 탭으로 분리)
tab1, tab2 = st.tabs(["🎯 실시간 분석 서비스", "📈 모델 분석 리포트"])

with tab1:
    col1, col2 = st.columns([1, 1.2])

with tab2:
    st.header("📈 모델 성능 상세 리포트")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("✅ 긍정 판단 주요 키워드")
        st.write("최고, 감동, 인생영화, 연기력, 대박, 추천")
        st.success("위 단어들이 포함될 경우 긍정 확률이 비약적으로 상승합니다.")
        
    with col_b:
        st.subheader("🚫 부정 판단 주요 키워드")
        st.write("노잼, 실망, 최악, 지루함, 아깝다, 알바")
        st.error("위 단어들이 포함될 경우 모델은 문맥을 부정으로 확신합니다.")

    st.markdown("---")
    st.subheader("📊 모델 검증 지표")
    st.table({
        "평가 항목": ["정확도(Accuracy)", "정밀도(Precision)", "재현율(Recall)", "데이터셋 크기"],
        "수치": ["85.4%", "86.1%", "84.2%", "3,012건"]
    })    

    # --- 왼쪽: 분석 시각화 (이미지) ---
    with col1:
        st.header("📊 관객 키워드 분석")
        image_path = r"C:/02WorkSpaces/Project3/saveFiles/movie_wordcloud_final.png" 
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.warning("이미지 경로를 확인해주세요.")

    # --- 오른쪽: 리뷰 추천 서비스 ---
    with col2:
        st.header("💬 맞춤형 리뷰 검색")
        search_query = st.text_input("🔍 키워드 입력", placeholder="예: 원더랜드, 감동, 액션")
        data_path = r"C:/02WorkSpaces/Project3/saveFiles/FINAL_COMBINED_REVIEWS.csv"
        
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            if search_query:
                filtered_df = df[df['label'].str.contains(search_query, na=False, case=False) | 
                                 df['review'].str.contains(search_query, na=False, case=False)]
            else:
                target_keywords = "감동|눈물|슬픔|최고" if "감동" in mood else "액션|긴장|스릴" if "심장" in mood else "재미|웃음|힐링"
                filtered_df = df[df['review'].str.contains(target_keywords, na=False, case=False)]
            
            if not filtered_df.empty:
                st.dataframe(filtered_df[['label', 'review']].head(50), use_container_width=True, height=350)
            else:
                st.warning(f"⚠️ '{search_query}' 키워드가 포함된 실제 리뷰는 데이터에 없습니다.")
                st.info("💡 하지만 아래 AI 보고서를 통해 이 문장의 감성(긍정/부정)을 확인하실 수 있습니다!")

    # --- 하단: AI 문맥 분석 (검색 시에만 노출) ---
    if search_query:
        st.markdown("---")
        st.header("🧠 AI 실시간 문맥 분석")
        
        vec_input = tfidf.transform([search_query])
        prediction = model.predict(vec_input)[0]
        prob = model.predict_proba(vec_input)[0]
        score = max(prob)
        
        c_left, c_right = st.columns([1, 1])
        with c_left:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score * 100,
                title = {'text': "AI 확신도 (%)"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#1f77b4" if prediction == 1 else "#ff4b4b"},
                    'steps': [{'range': [0, 100], 'color': "#f2f2f2"}]
                }
            ))
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)

        with c_right:
            res_label = "긍정(Positive)" if prediction == 1 else "부정/중립(Negative/Neutral)"
            st.subheader(f"분석 결과: {res_label}")
            st.info(f"🤖 **AI 의견:** '{search_query}'(은)는 약 **{score:.1%}**의 확률로 **{res_label}** 문맥입니다.")

with tab2:
    st.header("📈 모델 성능 상세 데이터")
    st.write("모델의 학습 파라미터와 성능 지표를 확인할 수 있는 섹션입니다.")
    # 여기에 추가적인 그래프나 모델 설명 텍스트를 자유롭게 넣으시면 됩니다.
    st.table({
        "Metric": ["Precision", "Recall", "F1-Score", "Data Size"],
        "Value": ["0.86", "0.84", "0.85", "3,012"]
    })