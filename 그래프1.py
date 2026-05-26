import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트
plt.rcParams['font.family'] = 'Malgun Gothic'

# 연도 폴더 정보
year_info = {
    '20년': 2020,
    '21년': 2021,
    '22년': 2022,
    '23년': 2023,
    '24년': 2024,
    '25년': 2025,
    '26년 1 - 4월 까지': 2026
}

# 지역
regions = ['강북구', '영등포']

for region in regions:

    all_data = []

    # 연도별 CSV 읽기
    for folder, year in year_info.items():

        file = f'{folder}/{region}_월기온통계.csv'

        print(f'읽는 중: {file}')

        # CSV 읽기
        df = pd.read_csv(file, encoding='utf-8-sig')

        # 연도 추가
        df['year'] = year

        # 연-월 생성
        df['year_month'] = (
            df['year'].astype(str)
            + '-'
            + df['month'].astype(str).str.zfill(2)
        )

        all_data.append(df)

    # 데이터 합치기
    merged = pd.concat(all_data, ignore_index=True)

    # ==========================
    # 그래프
    # ==========================

    plt.figure(figsize=(20, 8))

    # 평균기온
    plt.plot(
        merged['year_month'],
        merged['monthly_avg'],
        marker='o',
        label='월평균기온'
    )

    # 최고기온
    plt.plot(
        merged['year_month'],
        merged['monthly_max'],
        marker='o',
        label='월최고기온'
    )

    # 최저기온
    plt.plot(
        merged['year_month'],
        merged['monthly_min'],
        marker='o',
        label='월최저기온'
    )

    # 제목
    plt.title(f'{region} 연도별 월 기온 변화')

    # 축 이름
    plt.xlabel('연-월')
    plt.ylabel('기온(℃)')

    # x축 회전
    plt.xticks(rotation=45)

    # 격자
    plt.grid(True)

    # 범례
    plt.legend()

    # 여백 자동 조절
    plt.tight_layout()

    # 저장
    plt.savefig(f'{region}_전체년도_기온그래프.png')

    # 출력
    plt.show()

    print(f'{region} 그래프 저장 완료')