import pandas as pd

# 아주 간단한 연습용 데이터 5개
raw_data = {
    'review': [
        '정말 재밌어요 최고입니다',
        '시간 아까워요 보지마세요',
        '배우들 연기가 대박이네요',
        '내용이 너무 지루해서 졸았어요',
        '인생 영화입니다 꼭 보세요'
    ]
}

# CSV 파일로 저장
df = pd.DataFrame(raw_data)
df.to_csv('movie_reviews.csv', index=False, encoding='utf-8-sig')
print("연습용 데이터 파일이 생성되었습니다!")

# 1. 원본 데이터 (리스트 형태)
data = [
    "영화 너무 재밌어요", "최악입니다 보지마세요", "그냥 그래요",
    "내 인생 최고의 영화", "돈 아깝다", "배우들 연기 대박", 
    "지루해서 자 버림", "와... 진짜 소름돋네요", "노잼", "꿀잼",
    "이걸 영화라고 만들었나", "가족들이랑 보기 좋아요", "감독 천재인 듯",
    "스토리가 산으로 가요", "영상미가 일품입니다", "개연성이 하나도 없음",
    "다시 보고 싶어요", "내용이 너무 뻔함", "감동적입니다", "기대 이하"
]
# 데이터프레임 생성
df = pd.DataFrame(data, columns=['review'])
df.to_csv('movie_reviews_v2.csv', index=False, encoding='utf-8-sig')
print("20개짜리 새로운 파일이 v2로 저장되었습니다!")