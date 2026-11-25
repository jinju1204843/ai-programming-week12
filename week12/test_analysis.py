# [NEW v12] 명세의 숫자를 네 가지 자동 검사로 확인한다.
from pathlib import Path
import pandas as pd
import sys

# [NEW v12] 저장소 루트에서도 같은 모듈을 불러온다.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from analysis import 정제, 반별평균


# [NEW v12] 입력 파일은 모듈을 불러올 때 각각 한 번씩 읽는다.
폴더 = Path(__file__).resolve().parent
원본 = pd.read_csv(폴더 / "scores_2026.csv", dtype={"학번": str})
본 = 정제(원본)
미니 = 정제(pd.read_csv(폴더 / "mini.csv", dtype={"학번": str}))


# [NEW v12] 단계별로 빠진 행과 원본 보존을 확인한다.
def test_정제하면_100행이_남는다():
    assert len(본) == 100
    assert 원본.shape == (114, 5)
    assert 원본["점수"].isna().sum() == 6
    assert 본["점수"].between(0, 100).all()
    assert 본["점수"].mod(1).eq(0).all()


# [NEW v12] 공백이 붙은 그룹이 별도로 남지 않아야 한다.
def test_반은_두_종류만_남는다():
    assert sorted(본["반"].unique()) == ["1반", "2반"]
    assert sorted(본["과목"].unique()) == ["수학", "영어", "프로그래밍"]


# [NEW v12] 묶어도 점수 합계와 행 수가 보존되는지 확인한다.
def test_그룹합이_전체합과_같다():
    assert 본.groupby("반")["점수"].sum().sum() == 본["점수"].sum() == 7484
    assert 본.groupby("반")["점수"].count().sum() == len(본)


# [NEW v12] 작은 입력의 독립 산술 계산 결과와 대조한다.
def test_손계산과_일치한다():
    assert len(미니) == 7
    assert 반별평균(미니) == {"1반": 80.0, "2반": 70.0}
    assert 본.loc[본["반"].eq("1반") & 본["과목"].eq("수학"), "점수"].sum() == 480
