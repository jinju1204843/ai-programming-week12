# [NEW v12] pandas로 성적을 단계별 정제하고 분석한다.
from pathlib import Path
import pandas as pd

# [NEW v12] 원본을 보존하고 명세에 적힌 순서대로 정제한다.
def 정제(df=None):
    if df is None:
        raise ValueError("정제할 DataFrame이 필요합니다.")
    result = df.copy()
    print("시작", len(result))
    # [NEW v12] 점수를 알 수 없는 행은 평균 계산에서 제외한다.
    result = result.dropna(subset=["점수"])
    print("빈 칸 제거", len(result))
    # [NEW v12] 공백을 정리하기 전에 완전히 같은 행만 제거한다.
    result = result.drop_duplicates().copy()
    print("중복 제거", len(result))
    # [NEW v12] 반과 과목의 앞뒤 공백을 정리한다.
    result["반"] = result["반"].str.strip()
    result["과목"] = result["과목"].str.strip()
    print("공백 정리", len(result))
    # [NEW v12] 정수이고 0~100점인 값만 남긴다.
    valid = result["점수"].between(0, 100) & result["점수"].mod(1).eq(0)
    result = result.loc[valid].copy()
    result["점수"] = result["점수"].astype(int)
    print("범위·정수 검증", len(result))
    return result


# [NEW v12] 반 이름을 키로 하고 평균을 값으로 하는 딕셔너리를 반환한다.
def 반별평균(df=None):
    if df is None:
        raise ValueError("분석할 DataFrame이 필요합니다.")
    return df.groupby("반")["점수"].mean().round(2).to_dict()


# [NEW v12] 불러오기, 필터링, 그룹화, 통계와 검증을 구분해 출력한다.
def main():
    folder = Path(__file__).resolve().parent
    original = pd.read_csv(folder / "scores_2026.csv", dtype={"학번": str})
    print("원본 행·열", original.shape)
    print("점수 결측", int(original["점수"].isna().sum()))
    print("완전 중복", int(original.duplicated().sum()))
    print("원본 반", original["반"].unique().tolist())
    print("원본 과목", original["과목"].unique().tolist())
    cleaned = 정제(original)
    mathematics = cleaned.loc[cleaned["과목"].eq("수학")]
    high_scores = cleaned.loc[cleaned["반"].eq("1반") & cleaned["점수"].ge(90)]
    print("수학 필터", len(mathematics))
    print("1반 90점 이상", len(high_scores))
    print("반별 평균", 반별평균(cleaned))
    print("과목 × 반 평균")
    print(cleaned.groupby(["과목", "반"])["점수"].mean().round(2))
    print("반별 통계")
    print(cleaned.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2))
    print("전체 합", int(cleaned["점수"].sum()))
    print("그룹 합의 합", int(cleaned.groupby("반")["점수"].sum().sum()))
    print("그룹 개수의 합", int(cleaned.groupby("반")["점수"].count().sum()))
    mini = 정제(pd.read_csv(folder / "mini.csv", dtype={"학번": str}))
    print("mini 반별 평균", 반별평균(mini))


if __name__ == "__main__":
    main()
