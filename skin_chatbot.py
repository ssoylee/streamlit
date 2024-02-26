import streamlit as st
from openai import OpenAI
import base64 

# OpenAI API 키 설정
api_key = st.secrets["openai_secret"]
client = OpenAI(api_key=api_key)

# 페이지 설정
st.set_page_config(page_title="챗봇 서비스 페이지")

# CSS 스타일 정의
st.markdown("""
<style>
.header-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-left: 24px;
}

.header-title-container {
    flex-grow: 1;
    text-align: center;
}

.back-button {
    background-color: transparent;
    border: none;
    font-size: 24px;
    padding: 0;
    margin: 0 10px 0 0;
}

.text-title {
    font-size: 25px;
    line-height: 1;
    margin: 0;
    display: inline-block;
}

.chat-container {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.chat-messages-container {
    display: flex;
    flex-direction: column;
    align-items: flex-end; /* 메시지를 오른쪽에 정렬 */
    width: 70%; /* 필요에 따라 너비 조절 */
}

.chat-icon {
    height: 50px; /* 아이콘 크기 조절 */
    width: 50px;
    margin-right: -10px;
}

.chat-message {
    padding: 10px;
    border-radius: 20px;
    margin-bottom: 10px;
    word-wrap: break-word;
    width: auto; /* 너비를 자동으로 조절 */
    min-width: 50px; /* 최소 너비 설정 */
    max-width: 70%; /* 최대 너비 설정 */
    display: inline-block; /* 내용에 맞춰 크기 조절 */
}

.user-message {
    background-color: #0b93f6;
    color: white;
    margin: 10px;
    font-size: 15px;
    float: right; /* 사용자 메시지를 오른쪽에 정렬 */
}

.assistant-message {
    background-color: #e5e5ea;
    color: black;
    margin: 10px;
    font-size: 15px;
    float: left; /* 챗봇 메시지를 왼쪽에 정렬 */
}

body {
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# 헤더 컨테이너 추가
st.markdown('<div class="header-container">', unsafe_allow_html=True)

# 뒤로가기 버튼과 제목 추가
st.markdown("""
    <a href="http://host240102.dothome.co.kr/WebPage/index.html#">
        <button class="back-button">
            &lt; <!-- 화살표 아이콘 -->
        </button>
    </a>
    <div class="header-title-container">
        <span class="text-title">유비케어 챗봇 서비스</span>
    </div>
""", unsafe_allow_html=True)

# 헤더 컨테이너 닫기
st.markdown('</div>', unsafe_allow_html=True)

# 챗봇 대화 기록 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{'role': 'assistant', 'content': '저는 피부 질환 전문가입니다. 피부에 대해 궁금하신 점을 질문해주세요.'}]

# 대화 입력
prompt = st.chat_input("메시지 입력")
if prompt:
    st.session_state['messages'].append({'role': 'user', 'content': prompt})

    specialized_prompt = f"피부질환 전문가로서 다음 질문에 답해주세요: {prompt}"
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": specialized_prompt}], max_tokens=2000)

    if response.choices:
        extracted_text = response.choices[0].message.content
        st.session_state['messages'].append({'role': 'assistant', "content": extracted_text})

def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

image_path = "ubicare.png"
image_base64 = get_image_as_base64(image_path)

# 대화 표시
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.markdown('<div class="chat-messages-container">', unsafe_allow_html=True)
for message in st.session_state['messages']:
    if message['role'] == "assistant":
        st.markdown(
            f"""
            <div style="display: flex; align-items: center;">
                <img src="data:image/png;base64,{image_base64}" class="chat-icon" />
                <div class='chat-message assistant-message'>{message['content']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    elif message['role'] == "user":
        st.markdown(
            f"<div class='chat-message user-message'>{message['content']}</div>",
            unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
