import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime
from threading import Timer

import csv
import pymysql

date = datetime.today().strftime("%Y년 %m월")

# 데이터베이스 연결 설정
def connect_db():
    return mysql.connector.connect(
        host="0.tcp.jp.ngrok.io",
        port='17711',
        user="root",
        passwd="1111",
        db="newsDB"
    )

# 데이터베이스에서 데이터 검색
def get_data():
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM news"  # 'url' 컬럼을 제외한 나머지 컬럼만 선택
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(result, columns=['news_title', 'link'])

st.set_page_config(page_title="피부관련 최신 뉴스기사")

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
    st.markdown('<h1 class="title">피부 관련 최신 뉴스기사</h1>', unsafe_allow_html=True)

    # DB에서 df 가져오기
    df = get_data()
    df.index = range(1, len(df) + 1)
    df.rename(columns={'news_title': '기사제목', 'link': '기사링크'}, inplace=True)
    df_len = len(df)

    space = '&nbsp;' * 183
    st.write(f'{space}({date}자)')
    df['기사링크'] = df.apply(lambda row: f"<a href='{row['기사링크']}' target='_blank'>Click!</a>", axis=1)
    st.write(df.to_html(escape=False), unsafe_allow_html=True)  # 데이터프레임을 streamlit에 게시
    # escape=False: HTML을 변환할 때, 특수 문자(예: <, >, &)를 HTML 엔티티로 변환하지 않도록 함
    # unsafe_allow_html=True : HTML 코드가 웹 페이지에서 실제 HTML로 해석되고 렌더링되도록 함
            
if __name__ == "__main__":  # 특정 코드 블록이 직접 실행될 때만 실행되도록 하는 코드
    main()