import pandas as pd
import glob
import os

# 처리할 폴더
folders = ['강북구', '영등포']

for folder in folders:

    files = glob.glob(f'{folder}/*일평균.csv')

    all_data = []

    for file in files:

        print(f'\n현재 파일 처리 중: {file}')

        # CSV 읽기
        df = pd.read_csv(file)

        # 날짜 원본 저장
        original_dates = df['date'].copy()

        # 날짜 변환
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # 잘못된 날짜 찾기
        invalid_dates = original_dates[df['date'].isna()]

        # 오류 출력
        if len(invalid_dates) > 0:

            print(f'오류 발생 파일: {file}')
            print('잘못된 날짜:')

            for d in invalid_dates.unique():
                print(d)

        # 잘못된 날짜 제거
        df = df[df['date'].notna()]

        # 월 추출
        df['month'] = df['date'].dt.month

        # 동 이름 추출
        dong_name = os.path.basename(file).split('_')[0]

        df['dong'] = dong_name

        all_data.append(df)

    # 모든 데이터 합치기
    merged = pd.concat(all_data, ignore_index=True)

    # 월별 평균/최고/최저 계산
    monthly_stats = (
        merged.groupby('month')['daily_avg_temp']
        .agg(
            monthly_avg='mean',
            monthly_max='max',
            monthly_min='min'
        )
        .reset_index()
    )

    # 반올림
    monthly_stats['monthly_avg'] = monthly_stats['monthly_avg'].round(2)
    monthly_stats['monthly_max'] = monthly_stats['monthly_max'].round(2)
    monthly_stats['monthly_min'] = monthly_stats['monthly_min'].round(2)

    # 저장 파일명
    output_file = f'{folder}_월기온통계.csv'

    # CSV 저장
    monthly_stats.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f'\n[{folder} 월 기온 통계]')
    print(monthly_stats)

    print(f'{output_file} 저장 완료')