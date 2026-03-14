import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from collections import Counter
import re

# 1. 데이터 로드
path = r"C:/02WorkSpaces/Project3/saveFiles/FINAL_COMBINED_REVIEWS.csv"
df = pd.read_csv(path, encoding='utf-8-sig')

# 2~3. 텍스트 정제
def clean_text(text):
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', str(text))
    return text

df['review_clean'] = df['review'].apply(clean_text)

# 4~6. 형태소 분석 및 빈도 계산
okt = Okt()
all_text = " ".join(df['review_clean'].astype(str))
nouns = okt.nouns(all_text)
stopwords = ['영화', '진짜', '너무', '정말', '평점', '관람평', '리뷰', '최고', '생각', '사람', '보고', '보는', '다시', '그냥', '역시', '본', '좀', '더', '것']
clean_nouns = [n for n in nouns if n not in stopwords and len(n) > 1]
counts = Counter(clean_nouns)

# 7. 워드클라우드 객체 생성
wc = WordCloud(
    font_path='malgun',
    background_color='white',
    width=800, height=600,
    colormap='viridis'
).generate_from_frequencies(counts)

# 8. [중요] 시각화 및 저장 (순서가 핵심!)
plt.figure(figsize=(10, 8))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')

# 파일 저장 경로 (r을 붙여서 노란 줄 방지)
image_path = r"C:/02WorkSpaces/Project3/saveFiles/movie_wordcloud_final.png"
# 저장을 '먼저' 합니다!
plt.savefig(image_path, dpi=300, bbox_inches='tight')
print(f"이미지 저장 완료: {image_path}")

# 9. 엑셀 저장 (이미지 저장 후 진행)
word_df = pd.DataFrame(counts.most_common(), columns=['단어', '빈도수'])
excel_path = r"C:/02WorkSpaces/Project3/saveFiles/word_frequency_analysis.xlsx"

# 엑셀 저장 시 엔진을 명시해주면 더 확실합니다.
try:
    word_df.to_excel(excel_path, index=False, engine='openpyxl')
    print(f"엑셀 저장 완료: {excel_path}")
except ImportError:
    print("엑셀 저장 실패: 터미널에 'pip install openpyxl'을 입력해 주세요.")

# 10. 모든 저장이 끝난 후 마지막에 화면에 띄우기
print("모든 작업이 완료되었습니다. 창을 닫으면 프로그램이 종료됩니다.")
plt.show()