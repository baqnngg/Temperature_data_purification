import pandas as pd
import glob
import os

# 현재 폴더 안의 csv 파일 가져오기
files = glob.glob('*.csv')

# 제외할 파일/폴더 이름
exclude_keywords = [
    '1~4월_일평균',
    '월평균',
]

# 처리할 파일만 선택
target_files = []

for file in files:

    skip = False

    # 제외 키워드 포함 여부
    for keyword in exclude_keywords:
        if keyword in file:
            skip = True
            break

    if not skip:
        target_files.append(file)

print(f'처리할 파일 개수: {len(target_files)}')

# 파일 하나씩 처리
for file in target_files:

    try:

        print(f'\n처리중: {file}')

        # 파일명만 추출
        name = os.path.splitext(os.path.basename(file))[0]

        # CSV 읽기
        df = pd.read_csv(file, encoding='cp949')

        # 컬럼명
        day_col = ' format: day'
        hour_col = 'hour'

        # 온도 컬럼 자동 찾기
        temp_col = None

        for col in df.columns:
            if 'value location' in col:
                temp_col = col
                break

        print("온도 컬럼:", temp_col)

        current_month = "01"
        dates = []

        # 날짜 처리
        for value in df[day_col]:

            text = str(value).strip()

            # 월 변경 줄 처리
            if "Start :" in text:

                date_str = text.split(":")[1].strip()

                current_month = date_str[4:6]

                dates.append(None)

            # 숫자 날짜 처리
            elif text.isdigit():

                day = int(text)

                full_date = f"2025-{current_month}-{day:02d}"

                dates.append(full_date)

            else:
                dates.append(None)

        # 날짜 컬럼 추가
        df['date'] = dates

        # 날짜 없는 행 제거
        df = df[df['date'].notna()]

        # 숫자 변환
        df[hour_col] = pd.to_numeric(df[hour_col], errors='coerce')
        df[temp_col] = pd.to_numeric(df[temp_col], errors='coerce')

        # 시간 계산
        df['real_hour'] = df[hour_col] // 100

        # 0시는 24시 처리
        df.loc[df['real_hour'] == 0, 'real_hour'] = 24

        # 한국 일평균 계산 시간
        target_hours = [3, 6, 9, 12, 15, 18, 21, 24]

        # 필요한 시간만 선택
        filtered = df[df['real_hour'].isin(target_hours)]

        # 날짜별 평균 계산
        daily_avg = (
            filtered.groupby('date')[temp_col]
            .mean()
            .reset_index()
        )

        # 컬럼명 변경
        daily_avg.columns = ['date', 'daily_avg_temp']

        # 소수 둘째자리 반올림
        daily_avg['daily_avg_temp'] = daily_avg['daily_avg_temp'].round(2)

        # 저장 파일명
        output_file = f'{name}_일평균.csv'

        # 저장
        daily_avg.to_csv(output_file, index=False, encoding='utf-8-sig')

        print(f'{output_file} 저장 완료')

    except Exception as e:

        print(f'오류 발생 파일: {file}')
        print(e)