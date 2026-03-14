import pandas as pd

# 파일 경로 (본인의 경로와 맞는지 꼭 확인!)
file_path = "C:/02WorkSpaces/Project3/saveFiles/movie_FINAL_TOTAL_dataset.csv"

def show_me_the_money():
    try:
        # 데이터 읽기
        df = pd.read_csv(file_path)
        
        # 중복 제거 (진짜 알맹이만 남기기)
        unique_df = df.drop_duplicates(subset=['review'])
        
        print("\n" + "="*40)
        print("영화 데이터 최종 수집 현황")
        print("="*40)
        
        # 영화별 개수 순서대로 출력
        counts = unique_df['label'].value_counts()
        for movie, count in counts.items():
            print(f"{movie.ljust(10)} : {count}개")
            
        print("-" * 40)
        print(f"중복 제거 후 최종 합계: {len(unique_df)}개")
        print("="*40)
        
        ### 추가: 중복이 제거된 깨끗한 데이터를 새 파일로 저장 ###
        final_path = "C:/02WorkSpaces/Project3/saveFiles/movie_final_cleaned.csv"
        unique_df.to_csv(final_path, index=False, encoding='utf-8-sig')
        print(f"✅ 정제된 파일 저장 완료: {final_path}")
        
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다! 경로를 다시 확인해주세요.")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    show_me_the_money()