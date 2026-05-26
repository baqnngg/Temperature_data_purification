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

# 지역별 데이터 저장용
region_data = {}

# ==========================
# 데이터 읽기
# ==========================

for region in regions:

    all_data = []

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

    # 저장
    region_data[region] = merged

# ==========================
# 하나의 그래프에 비교
# ==========================

plt.figure(figsize=(20, 8))

# 강북구 평균기온
plt.plot(
    region_data['강북구']['year_month'],
    region_data['강북구']['monthly_avg'],
    marker='o',
    label='강북구 월평균기온'
)

# 영등포 평균기온
plt.plot(
    region_data['영등포']['year_month'],
    region_data['영등포']['monthly_avg'],
    marker='o',
    label='영등포 월평균기온'
)

# 제목
plt.title('강북구 vs 영등포 월평균기온 비교')

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
plt.savefig('강북구_영등포_월평균기온_비교그래프.png')

# 출력
plt.show()

print('그래프 저장 완료')