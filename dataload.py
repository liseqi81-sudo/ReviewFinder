import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer

## 1일차
# 1. 데이터 생성및 저장

# 20개의 더 정교한 연습용 데이터 리스트
data = [
    "영화 너무 재밌어요", "최악입니다 보지마세요", "그냥 그래요",
    "내 인생 최고의 영화", "돈 아깝다", "배우들 연기 대박", 
    "지루해서 자 버림", "와... 진짜 소름돋네요", "노잼", "꿀잼",
    "이걸 영화라고 만들었나", "가족들이랑 보기 좋아요", "감독 천재인 듯",
    "스토리가 산으로 가요", "영상미가 일품입니다", "개연성이 하나도 없음",
    "다시 보고 싶어요", "내용이 너무 뻔함", "감동적입니다", "기대 이하"
]

# 리스트를 데이터프레임으로 변환
df_to_save = pd.DataFrame(data, columns=['review'])

# CSV 파일로 저장 (인코딩 설정으로 한글 깨짐 방지)
df_to_save.to_csv('movie_reviews.csv', index=False, encoding='utf-8-sig')
print("movie_reviews.csv 파일 생성 완료")

# 2.데이터 불러오기 및 확인 (step 1)

file_path = 'movie_reviews.csv'
df = pd.read_csv(file_path, encoding='utf-8-sig')

print("\n 불러온 데이터 상단 확인")
print(df.head())

# 3. 결측치(NaN= Not a Number 값이 빈 상태)강제 추가 및 제거 테스트

# 20번 인덱스에 빈 칸 (None)을 강제로 하나 넣음
df.loc[20] = [None]
print(f"\n 결측치 추가 후 전체 갯수: {len(df)}개")

# 결측치가 있는 행(None)을 찾아서 제거
df = df.dropna(subset=['review'])
print(f"결측치 제거 후 최종갯수: {len(df)}개") 

# 4. 데이터 가공 및 필터링 연습

# 각 리뷰의 글자 수를 계산해서 새로운 컬럼 생성
df['length'] = df['review'].apply(len)

# '재밌' 이라는 단어가 포함된 리뷰만 필터링
fun_reviews = df[df['review'].str.contains('재밌')]

print("\n 최종 정제 데이터 (일부)")
print(df.head(10))

print("\n '재밌'이 들어간 리뷰 검색 결과")
print(fun_reviews)

# 5. 데이터 통계 요약

print("\n 데이터 통계 요약")
# 문자열 데이터이므로 갯수, 고유값 갯수, 최빈값 갯수를 보여준다.
print(df['review'].describe())

# 6. 최종 결과물 폴더별 저장

# 저장할 폴더명 설정
output_folder = 'saveFiles'

# 만약 폴더가 없으면 자동으로 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"\n [{output_folder}]폴더가 생성되었습니다.")

# 최종 파일명 설정 (날짜나 버전을 붙여서 관리)
output_file = f"{output_folder}/movie_reviews_day1_result.xlsx"

# 엑셀 파일로 저장 (인덱스 제외, 한글 깨짐 방지 설정)    
df. to_excel(output_file, index=False)

print(f"\n 1일차 정제 데이터 저장 완료!")
print(f"파일경로:{os.path.abspath(output_file)}")
print("-" * 40)



## 2일차 실습 시작
#from sklearn.feature_extraction.text import TfidfVectorizer (도구 가져온시점표시)

# 1. 도구 준비 (너무 흔한 단어는 빼달라고 설정해볼게요)
tfidf = TfidfVectorizer(max_features=100) 

# 2. 데이터 학습 (df['리뷰컬럼명'] 부분을 실제 이름으로 바꿔주세요!)
tfidf_matrix = tfidf.fit_transform(df['review'])

# 3. 단어별 점수 계산 및 정렬
word_names = tfidf.get_feature_names_out() # 단어 목록 추출
word_scores = tfidf_matrix.sum(axis=0).tolist()[0] # 단어별 중요도 점수 합산

# 4. 보기 좋게 표로 만들어서 TOP 10 출력
result_df = pd.DataFrame({'keyword': word_names, 'score': word_scores})
top_10 = result_df.sort_values(by='score', ascending=False).head(10)

print("\n" + "="*30)
print("     [ 2일차: 키워드 TOP 10 ]")
print("="*30)
print(top_10)

# 4번 아래에 이 코드를 추가하세요
top_10.to_excel("C:/02WorkSpaces/Project3/saveFiles/top10_keywords_day2.xlsx", index=False)
print("\n✔ TOP 10 키워드가 엑셀로 저장되었습니다!")