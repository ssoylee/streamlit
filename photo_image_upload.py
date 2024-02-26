import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import cv2
from PIL import Image
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import requests
import os
import tempfile
from streamlit_webrtc import RTCConfiguration, VideoTransformerBase
import threading
import gdown
# RTC 설정 정의
RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

# 비디오 트랜스포머 클래스 정의
class VideoTransformer(VideoTransformerBase):
    def __init__(self) -> None:
        self.frame_lock = threading.Lock()
        self.in_frame = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        with self.frame_lock:
            self.in_frame = img
        return img

# 함수 정의
def load_metadata(file_path):
    return pd.read_csv(file_path)

def encode_user_input(metadata_df, age, sex_input, localization_input):
    sex_dict = {"남자": "male", "여자": "female"}
    localization_dict = {
        "복부": "abdomen", "등": "back", "가슴": "chest", "얼굴": "face",
        "발": "foot", "생식기": "genital", "다리": "lower extremity",
        "목": "neck", "두피": "scalp", "몸통": "trunk",
        "알수없음": "unknown", "팔": "upper extremity",
        "귀" : "ear", "손바닥" : "acral", "손" : "hand",
    }
    sex = sex_dict.get(sex_input, "unknown")
    localization = localization_dict.get(localization_input, "unknown")
    sex_encoded = 0 if sex == "male" else 1
    label_encoder = LabelEncoder().fit(metadata_df['localization'])
    localization_encoded = label_encoder.transform([localization])[0]
    return np.array([[age, sex_encoded, localization_encoded]])

def preprocess_image(uploaded_file):
    img = Image.open(uploaded_file)
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    return img_array

def predict_skin_disease(model, img_array, meta_input):
    predictions = model.predict([img_array, meta_input])
    return predictions[0]




# 메타데이터 로드
metadata_df = load_metadata('HAM10000_metadata.csv')


# Google Drive 공유 링크
google_drive_url = 'https://drive.google.com/uc?id=11t8zk8vkiu-g4KWbzYxiWaM6mvBzasiv'

# 모델 파일을 임시 파일로 다운로드
temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.h5')  # 확장자 추가
gdown.download(google_drive_url, temp_file.name, quiet=False)

# 모델 로드
model = load_model(temp_file.name)

# 임시 파일 삭제
os.remove(temp_file.name)

# 클래스 이름 매핑
class_names = {
    0: '피부 선암 (Actinic keratoses and intraepithelial carcinoma)',
    1: '기저세포암 (Basal cell carcinoma)',
    2: '벤인 케라토시스 라이크 레이즈니즈 (Benign keratosis-like lesions)',
    3: '피부 섬유종 (Dermatofibroma)',
    4: '흑색종 (Melanoma)',
    5: '멜라닌성 낭종 (Melanocytic nevi)',
    6: '혈관 병변 (Vascular lesions)'
}

class_descriptions = {
    0: '이 질환은 피부의 선피로 인한 변화를 나타내며 햇빛에 노출된 피부에서 발생합니다.',
    1: '기저세포암은 피부 기저세포에서 시작되는 흔한 피부암입니다.',
    2: '이 질환은 양성 피부 병변을 나타내며 주로 피부의 형태가 이상한 병변을 포함합니다.',
    3: '피부 섬유종은 피부의 섬유성 종양으로서 일반적으로 작고 단단한 결절로 나타납니다.',
    4: '흑색종은 피부암 중에서 가장 악성이고 위험한 종류로, 피부의 흑색 색소세포인 멜라닌 세포에서 발생합니다.',
    5: '멜라닌 세포에서 나타나는 양성 피부 종양으로 흔한 모양과 색상의 주근깨 또는 점으로 표시됩니다.',
    6: '혈관 이상을 나타내며 흔히 어지러운 혈관 패턴 또는 혈관의 이상이 있는 피부 병변을 포함합니다.'
}

def main():
    
    # st.session_state 초기화
    if 'frame' not in st.session_state:
        st.session_state['frame'] = None
        
        
    st.sidebar.title("메뉴")
    app_mode = st.sidebar.selectbox("모드 선택", ["사진찍기", "이미지 업로드"])
    
    if app_mode == "사진찍기":
        st.title("피부 질환 감지 - 사진찍기 모드")
        
        # 메타데이터 입력 받기
        age = st.number_input("나이를 입력하세요", min_value=1, max_value=100, value=30)
        sex = st.selectbox("성별을 선택하세요", ["남자", "여자"])
        localization = st.selectbox("질환 부위를 선택하세요", ["복부", "등", "가슴", "얼굴", "발", "생식기", "다리", "목", "두피", "몸통", "알수없음", "팔", "귀", "손바닥", "손"])
        
        # 메타데이터 인코딩
        meta_input = encode_user_input(metadata_df, age, sex, localization)
        
        webrtc_ctx = webrtc_streamer(key="example", video_processor_factory=VideoTransformer, rtc_configuration=RTC_CONFIGURATION)

        if webrtc_ctx.video_transformer:
            if st.button("사진찍기"):
                with webrtc_ctx.video_transformer.frame_lock:
                    frame = webrtc_ctx.video_transformer.in_frame
                    
                    if frame is not None:
                        # OpenCV로 이미지 처리
                        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        st.image(img, caption="캡처된 사진")
                        img = cv2.resize(img, (224, 224))  # 모델 입력 크기에 맞게 리사이즈
                        img = image.img_to_array(img)
                        img = np.expand_dims(img, axis=0) / 255.0

                        # 예측 수행
                        predictions = predict_skin_disease(model, img, meta_input)



                        # 예측 결과 표시
                        top_class_index = np.argmax(predictions)
                        top_class_name = class_names[top_class_index]
                        top_probability = predictions[top_class_index] * 100

                        st.write("피부 질환 예측 결과:")
                        st.write(f"1순위: {top_class_name} ({top_probability:.2f}%)")
                        if top_class_index in class_descriptions:
                            st.write("설명:", class_descriptions[top_class_index])

                        # 2순위 예측
                        second_class_index = np.argsort(-predictions)[1]  # 2순위 클래스의 인덱스
                        second_class_name = class_names[second_class_index]
                        second_probability = predictions[second_class_index] * 100

                        st.write(f"2순위: {second_class_name} ({second_probability:.2f}%)")
                        if second_class_index in class_descriptions:
                            st.write("설명:", class_descriptions[second_class_index])

                        # 3순위 예측
                        third_class_index = np.argsort(-predictions)[2]  # 3순위 클래스의 인덱스
                        third_class_name = class_names[third_class_index]
                        third_probability = predictions[third_class_index] * 100

                        st.write(f"3순위: {third_class_name} ({third_probability:.2f}%)")
                        if third_class_index in class_descriptions:
                            st.write("설명:", class_descriptions[third_class_index])
                        
                        # 피부 상태 제품 서비스로 이동하는 하이퍼링크 추가
                        st.markdown("### [여기를 클릭하여 피부 상태 제품 추천 서비스로 이동](https://app-eqmlagtpuerscreh89pscg.streamlit.app/)")

    if app_mode == "이미지 업로드":
        st.title("피부 질환 감지 - 이미지 업로드 모드")
    
        # "경고" 체크박스 추가
        show_warning = st.checkbox("주의: 이 딥러닝 모델은 정확하지 않을 수 있으며 결과에 대한 신뢰성이 없을 수 있습니다. 전문의의 상담이 필요할 수 있습니다.")
    
        # 사용자 입력 받기
        age = st.number_input("나이를 입력하세요", min_value=1, max_value=100, value=30)
        sex = st.selectbox("성별을 선택하세요", ["남자", "여자"])
        localization = st.selectbox("질환 부위를 선택하세요", ["복부", "등", "가슴", "얼굴", "발", "생식기", "다리", "목", "두피", "몸통", "알수없음", "팔", "귀", "손바닥", "손"])
    
        # 이미지 업로드 체크박스 조건부 활성화
        if show_warning:
            uploaded_files = st.file_uploader("피부 이미지를 업로드하세요 (최대 6장)", type=["jpg", "png"], accept_multiple_files=True)

            if uploaded_files:
                all_predictions = []
                img_arrays = []

                for uploaded_file in uploaded_files[:6]:
                    img_array = preprocess_image(uploaded_file)
                    img_arrays.append(img_array)
                    st.image(img_array, caption="업로드된 이미지", use_column_width=True)

                # 메타데이터 인코딩
                meta_input = encode_user_input(metadata_df, age, sex, localization)

                # 각 이미지에 대한 예측 수행 및 결과 취합
                for img_array in img_arrays:
                    predictions = predict_skin_disease(model, img_array, meta_input)
                    all_predictions.append(predictions)

                # 모든 예측 결과의 평균을 계산
                avg_predictions = np.mean(np.array(all_predictions), axis=0)

                # 예측 결과 표시
                top_class_index = np.argmax(avg_predictions)
                top_class_name = class_names[top_class_index]
                top_probability = avg_predictions[top_class_index] * 100

                st.write("피부 질환 예측 결과:")
                st.write(f"1순위: {top_class_name} ({top_probability:.2f}%)")
                if top_class_index in class_descriptions:
                    st.write("설명:", class_descriptions[top_class_index])

                # 2순위 예측
                second_class_index = np.argsort(-avg_predictions)[1]  # 2순위 클래스의 인덱스
                second_class_name = class_names[second_class_index]
                second_probability = avg_predictions[second_class_index] * 100

                st.write(f"2순위: {second_class_name} ({second_probability:.2f}%)")
                if second_class_index in class_descriptions:
                    st.write("설명:", class_descriptions[second_class_index])

                # 3순위 예측
                third_class_index = np.argsort(-avg_predictions)[2]  # 3순위 클래스의 인덱스
                third_class_name = class_names[third_class_index]
                third_probability = avg_predictions[third_class_index] * 100

                st.write(f"3순위: {third_class_name} ({third_probability:.2f}%)")
                if third_class_index in class_descriptions:
                    st.write("설명:", class_descriptions[third_class_index])
                    
                # 피부 상태 제품 서비스로 이동하는 하이퍼링크 추가
                st.markdown("### [여기를 클릭하여 피부 상태 제품 추천 서비스로 이동](https://app-eqmlagtpuerscreh89pscg.streamlit.app/)")

if __name__ == "__main__":
    main()
