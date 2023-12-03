import requests
import pandas as pd

# 데이터를 가져올 API URL
url = 'http://apis.data.go.kr/6260000/FoodService/getFoodKr'
params = {
    'serviceKey': 'Zvj018VTnlTYlwmonzS4f0XotGZBB40/Fa+J2jGD3EqpJT+mTYxiqwwWkxHLma0uyYsjj7v2ZO/1FANaE3/1yQ==',
    'pageNo': 1,
    'numOfRows': 271,
    'resultType': 'json'
}

# API 요청을 보내고 응답을 받음
response = requests.get(url, params=params)
contents = response.json()

# API 응답 내용 출력 (주석 처리)
#print(contents)

# API 응답 내용에서 'item' 항목 추출
body = contents['getFoodKr']['item']

# 데이터프레임으로 변환
df = pd.json_normalize(body)

# 필요한 열만 선택
df_parsing = df.loc[:,['MAIN_TITLE', 'GUGUN_NM', 'LAT', 'LNG', 'ADDR1', 'CNTCT_TEL', 'USAGE_DAY_WEEK_AND_TIME', 'RPRSNTV_MENU']]

# 데이터 정제
df_parsing.index = range(1, len(df_parsing) + 1)
df_parsing['ADDR1'] = df_parsing['ADDR1'].str.replace('\t', '')

# 열 이름 변경
df_parsing = df_parsing.rename(columns={'MAIN_TITLE': 'NAME', 'GUGUN_NM' : 'GUGUN', 'ADDR1' : 'ADDR', 'CNTCT_TEL' : 'TEL', 'USAGE_DAY_WEEK_AND_TIME' : 'TIME', 'RPRSNTV_MENU' : 'MENU'})
df_parsing = df_parsing.rename_axis("INDEX_NUM", axis=0)

# 최종 결과물 출력 (주석 처리)
#print(df_parsing)

# 데이터프레임을 CSV 파일로 저장
df_parsing.to_csv('parsing.csv', encoding='UTF-8')