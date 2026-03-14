import pandas as pd
import glob
import os

def merge_and_basic_clean():
    path = "C:/02WorkSpaces/Project3/saveFiles/"
    all_files = glob.glob(os.path.join(path, "*.csv"))
    
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, encoding='utf-8-sig')
        li.append(df)

    # 1. 일단 몽땅 합치기
    total_df = pd.concat(li, axis=0, ignore_index=True)
    
    # 2. 중복 제거 (파일 간에 겹치는 리뷰 삭제)
    before_len = len(total_df)
    total_df.drop_duplicates(subset=['review'], inplace=True)
    
    # 3. 최소 길이 제한 (15자 이하는 내용이 빈약함)
    total_df = total_df[total_df['review'].str.len() > 15]
    
    # 4. 저장
    total_df.to_csv(path + "FINAL_COMBINED_REVIEWS.csv", index=False, encoding='utf-8-sig')
    
    print(f"✅ 합치기 완료! ({before_len}건 -> {len(total_df)}건)")

if __name__ == "__main__":
    merge_and_basic_clean()