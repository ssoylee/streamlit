import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime
from threading import Timer

import csv
import pymysql

date = datetime.today().strftime("%Y/%m/%d")

st.set_page_config(page_title="피부상태별 제품추천 서비스") #, layout="wide")

# 데이터베이스 연결 설정
def connect_db():
    return mysql.connector.connect(
        host="0.tcp.jp.ngrok.io",
        port='17711',
        user="root",
        passwd="1111",
        db="coupangDB"
    )

# 데이터베이스에서 데이터 검색
def get_data(table_name):
    conn = connect_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name}"  # 'url' 컬럼을 제외한 나머지 컬럼만 선택
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(result, columns=['id', 'product', 'price', 'rate', 'url'])

# 메인 함수
def main():
    # 페이지 제목 스타일 설정
    st.markdown("""
        <style>
        .title {
            font-size: 50px;
            font-weight: bold;
            color: #333333; /* 어두운 회색 글씨 */
            text-align: center;
            margin: 20px;
            padding: 20px;
            background-color: #FFFFFF; /* 흰색 배경 */
            border-radius: 10px;
            border: 1px solid #DDDDDD; /* 연한 회색 테두리 */
            box-shadow: 3px 3px 3px #BBBBBB; /* 더 섬세한 그림자 효과 */
            font-family: 'Arial', sans-serif; /* 간결한 폰트 스타일 */
            margin-bottom: 50px;
        }
        </style>
        """, unsafe_allow_html=True)

    # 페이지 제목 추가
    st.markdown('<h1 class="title">피부상태별 제품추천</h1>', unsafe_allow_html=True)
    # st.title("피부 상태 기반 추천 서비스")
    skin_problem_options = ['가려움', '아토피', '건선', '지루성 피부염', '습진']
    skin_problem = st.selectbox('피부 문제를 선택하세요:', skin_problem_options, index=0)

    if st.button('정보 확인'):
        if skin_problem == '가려움':
            st.image('itching.jpeg')
            st.markdown('# 가려움')
            st.write('''소양감(가려움증)이란 피부를 긁거나 문지르고 싶은 충동을 일으키는 불쾌한 감각으로 가장 흔한 피부증상이다.\
                이는 피부질환 뿐만 아니라 전신 질환이 있는 경우에도 나타날 수 있다. 가려움증은 매우 주관적인 감각으로서 \
                    신체의 부위나 개인에 따라 매우 다양하게 나타나며, 같은 사람에서도 동일한 자극이라도 때에 따라 정도가 다른 가려움증을 일으킬 수 있다.''')
            st.markdown('[출처 : 네이버 지식백과]')
            st.write('')
            st.write('')
            st.markdown('### 추천 제품')

        elif skin_problem == '아토피':
            st.image('atopy.jpg')
            st.markdown('# 아토피')
            st.write('''아토피피부염은 주로 유아기 혹은 소아기에 시작되는 만성 재발성의 염증성 피부질환으로 소양증(가려움증)과 피부건조증, 특징적인 습진을 동반한다. \
                유아기에는 얼굴과 팔다리의 폄 쪽 부분에 습진으로 시작되지만, 소아기가 되면서 특징적으로 팔이 굽혀지는 부분(팔오금)과 \
                    릎 뒤의 굽혀지는 부위(오금)에 습진을 나타낸다. 많은 경우에 성장하면서 자연히 호전되는 경향을 보이지만 알레르기 비염, 천식 같은 호흡기\
                        아토피를 동반하는 경우도 많다.''')
            st.markdown('[출처 : 네이버 지식백과]')
            st.write('')
            st.write('')
            st.markdown('### 추천 제품')

        elif skin_problem == '건선':
            st.image('psoriasis.jpg')
            st.markdown('# 건선')
            st.write('''건선은 붉은 반점과 비늘처럼 일어나는 피부각질(인설)을 동반한 발진(구진)이 주로 압력이나 마찰을 받는 부위 즉 팔다리의 관절 부위, 엉덩이,\
                두피 등에 흔히 나타나는 질환이다. 손발톱 무좀과 유사한 변형이 손발톱에 나타나기도 하며 관절염이 발생하기도 한다. 수년간 큰 변화를 보이지\
                    않을 수도 있지만 경우에 따라 감기를 앓고 나서 혹은 약을 잘못 복용한 후 전신적으로 작은 반점이 갑자기 번지는 경우도 있다. 따라서 건선 \
                        환자들은 평소 건강 관리에 유의해야 하며 염증을 악화시킬 수 있는 음주를 삼가고 때를 미는 등 피부에 과도한
                        자극과 마찰을 주는 행위를 금해야 한다. 건선의 원인은 아직도 확실히 알려지지 않고 있으나 최근에는 유전자와 면역학적
                        이상이 주된 연구분야로 떠오르고 있다.''')
            st.markdown('[출처 : 네이버 지식백과]')
            st.write('')
            st.write('')
            st.markdown('### 추천 제품')

        elif skin_problem == '지루성 피부염':
            st.image('seborrheic.jpg')
            st.markdown('# 지루성 피부염')
            st.write('''지루성 피부염은 생후 3개월 이내 그리고 40~70세 사이에 발생빈도가 높다. 유아에서는 성별간의 차이가 없으나\
                성인에서는 남성에게 더 흔하며 지성 피부와 관련이 있다. 홍반 위에 발생한 건성 혹은 기름기가 있는 노란 비늘(인설)이 특징이며 \
                    가려움증을 동반할 수 있다. 호전과 악화를 되풀이하며 전신으로 나타날 수도 있으나 한 부위에 국한된 발진으로 나타날 수도 있다. \
                    두피에는 쌀겨 모양의 표피탈락이 생길 수 있는데 이런 현상을 비듬이라 한다. 얼굴의 지루성 피부염은 뺨, 코, 이마에 \
                구진성(1cm 미만 크기의 솟아 오른) 발진으로 나타날 수 있다. 쉽게 벗겨지는 비늘과 홍반이 눈썹에서 발견되고 비늘 \
                    밑의 피부는 붉은 색을 띈다. 눈꺼풀도 황적색을 띄며 미세한 비늘로 덮여있는 경우가 있다. 귀에서 생긴 지루성 피부염은 \
                    감염으로 인한 겉귀길염(외이도염)으로 오진될 수 있다. 바깥귀길에는 심한 가려움증을 동반한 비늘이 발생하고\
                        귀 뒤 부위와 귓불 아래의 피부에도 발생할 수 있다. 겨드랑이 부위에서는 발진이 양측성으로 꼭지에서 시작되어\
                        주변의 피부로 퍼지므로 방취제에 의한 알레르기 접촉 피부염과 유사한 모양을 나타낸다. 샅고랑 부위, 둔부\
                        사이의 주름에도 비늘이 미세하고 경계가 덜 명확하며 양측성과 대칭성 경향이 있다. 피부가 겹친 부위에는 균열이 발생하기도 한다. \
                            유아에서 두피에 쌓이고 엉겨붙은 황색 또는 갈색 병변을 애기머릿기름이라고 한다.''')
            st.markdown('[출처 : 네이버 지식백과]')
            st.write('')
            st.write('')
            st.markdown('### 추천 제품')

        elif skin_problem == '습진':
            st.image('eczema.jpg')
            st.markdown('# 습진')
            st.write('''습진은 공통적인 임상적, 조직학적 특징을 보이는 피부 질환군을 통칭하는 용어이다. \
                피부 증상을 살펴보면 초기에는 주로 가려움과 함께 물집 구진, 홍반, 부기 등이 관찰되며 만성기에는 부기, \
                    물집은 줄어드는 대신 피부 주름이 두드러지거나 피부가 두꺼워지는 태선화, 비늘, 색소침착 등을 보인다. \
                        일반적으로 피부염과 습진은 동의어로 사용되고 있으나, 피부염은 모든 염증을 지칭하는 용어로 엄밀한 \
                            정의로는 피부염이 습진보다 더 넓은 의미를 가진다.''')
            st.markdown('[출처 : 네이버 지식백과]')
            st.write('')
            st.write('')
            st.markdown('### 추천 제품')
        
        table_mapping = {
            '가려움': 'itching',
            '아토피': 'atopy',
            '건선': 'psoriasis',
            '지루성 피부염': 'seborrheic',
            '습진': 'eczema'
        }
        
        table_name = table_mapping[skin_problem]
        df = get_data(table_name)

        df.index = range(1, len(df) + 1)
        df['rate'] = df['rate'].round(1)
        df.rename(columns={'id': '번호', 'product': '상품명', 'price': '가격', 'rate': '평점', 'url': '구매링크'}, inplace=True)
        df = df.drop('번호', axis=1)
        df_len = len(df)

        html_code = f"""
            <div class="custom-header">
                <h4>{skin_problem} 관련 제품 판매량순 TOP {df_len}</h4>
            </div>
            <style>
                .custom-header {{
                    background-color: #F2F2F2; /* 배경색 설정 */
                    padding: 20px; /* 내부 여백 설정 */
                    border-radius: 20px; /* 테두리 둥글게 설정 */
                    box-shadow: 5px 5px 5px #888888; /* 그림자 효과 설정 */
                    text-align: center; /* 텍스트 가운데 정렬 */
                    display: inline-block;
                    margin-left: 130px; /* 상하좌우 자동 마진 설정 */
                }}

                .custom-header h4 {{
                    font-size: 24px; /* 헤더의 글꼴 크기 설정 */
                    font-weight: bold; /* 글꼴 굵게 설정 */
                }}
            </style>
            """
        
        # 구매링크 생성
        st.markdown(html_code, unsafe_allow_html=True)
        
        # st.markdown(f'#### {skin_problem} 관련 제품 판매량순 TOP {len(df)}')
        st.write('')
        space = '&nbsp;' * 145
        st.write(f'{space} 출처 : coupang  &nbsp;  ({date}기준)')
        df['구매링크'] = df.apply(lambda row: f"<a href='{row['구매링크']}' target='_blank'>Click!</a>", axis=1)
        st.write(df.to_html(escape=False), unsafe_allow_html=True)
            
if __name__ == "__main__":
    main()
