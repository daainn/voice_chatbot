import streamlit as st
from openai_api import stt, ask_gpt, tts
from audio_recorder_streamlit import audio_recorder
from streamlit_chat import message
import time
import tempfile
import base64
import openai
import os

# Streamlit UI 설정
st.set_page_config(layout="wide")  # 화면을 넓게 사용
st.markdown(
    """
    <style>
        .center-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #333333;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 제목 출력
st.markdown('<h1 class="center-title">🎙 GPT와 티타임 🥤</h1>', unsafe_allow_html=True)

 # 구분선 추가
st.markdown("---")

# 채팅 기록 초기화 버튼
if st.sidebar.button("🗑️ 채팅 기록 초기화"):
    st.session_state.chat_history = []
    st.success("✅ 채팅 기록이 초기화되었습니다!")


# 페이지 레이아웃 설정
col1, col2 = st.columns([1, 2])  # 왼쪽(1) / 오른쪽(2) 비율 설정

with col1:
    # 인공지능 이미지 추가
    st.image("https://files.oaiusercontent.com/file-B4t5etLy4wTMjcDHXYBFsT?se=2025-03-05T06%3A16%3A06Z&sp=r&sv=2024-08-04&sr=b&rscc=max-age%3D604800%2C%20immutable%2C%20private&rscd=attachment%3B%20filename%3D51583c76-cd30-4c5c-9d4e-cdf38b1d9a26.webp&sig=aUymPbrYfGvGvsD2J65uOYYRPfmqgP6XOsmbvG2h%2BLg%3D", width=500)
    
    # 오디오 녹음 버튼 표시 (Click to record)
    st.info("🎤 버튼을 클릭하고 말해주세요!")
    audio_data = audio_recorder("🎤 Click to record")

    if audio_data:
        st.success("✅ 녹음 완료! 질문을 분석 중입니다...")

        # STT 변환 실행 (파일 경로 전달)
        recognized_text = stt(audio_data)

        # GPT 답변 생성 중 메시지 표시
        with st.spinner("🤖 답변을 생성하는 중..."):
            response_text = ask_gpt(recognized_text)

        # GPT 답변 표시
        st.success("✅ 답변 생성 완료!")

        # 채팅 기록 업데이트
        st.session_state.chat_history.append({"role": "user", "content": recognized_text})
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})

    #    # GPT 답변 생성 후 음성 변환
    #     audio_path = tts(response_text)  # 음성 파일 생성
    #     st.audio(audio_path, format="audio/mp3")  # Streamlit에서 재생
        # GPT 응답 생성 후 음성 변환
        audio_tag = tts(response_text)
        st.markdown(audio_tag, unsafe_allow_html=True)


with col2:
    # 세션 상태에 채팅 기록 저장
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
   
    
    # 질문 및 응답 출력
    if st.session_state.chat_history:
        for i, chat in enumerate(st.session_state.chat_history):
            message(chat["content"], is_user=(chat["role"] == "user"), key=str(i))




# # Streamlit UI
# st.set_page_config(layout="wide")  # 화면을 넓게 사용
# st.title("🎙 GPT와 티타임 🥤")

# # 채팅 기록 초기화 버튼
# if st.sidebar.button("🗑️ 채팅 기록 초기화"):
#     st.session_state.chat_history = []
#     st.success("✅ 채팅 기록이 초기화되었습니다!")

# # 페이지 레이아웃 설정
# col1, col2 = st.columns([1, 2])  # 왼쪽(1) / 오른쪽(2) 비율 설정

# with col1:
#     # 인공지능 이미지 추가
#     st.image("https://www.k-health.com/news/photo/202306/65884_71441_1839.jpg", width=300)
    
#     # 오디오 녹음 버튼 표시 (Click to record)
#     st.info("🎤 버튼을 클릭하고 말한 후 다시 클릭하면 자동으로 질문이 생성됩니다.")
#     audio_data = audio_recorder("🎤 Click to record")

#     if audio_data:
#         st.success("✅ 녹음 완료! 질문을 분석 중입니다...")

#         # STT 변환 실행 (파일 경로 전달)
#         recognized_text = stt(audio_data)

#         # GPT 답변 생성 중 메시지 표시
#         with st.spinner("🤖 답변을 생성하는 중..."):
#             response_text = ask_gpt(recognized_text)

#         # GPT-4o로 질문 후 결과 표시
#         st.success("✅ 답변 생성 완료!")

#         # 채팅 기록 업데이트
#         st.session_state.chat_history.append({"role": "user", "content": recognized_text})
#         st.session_state.chat_history.append({"role": "assistant", "content": response_text})

#         # # TTS로 GPT 응답 음성 출력
#         # audio_tag = tts(response_text)

# with col2:
#     # 세션 상태에 채팅 기록 저장
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []
    
#     # 구분선 추가
#     st.markdown("---")
    
#     # 질문 및 응답 출력
#     if st.session_state.chat_history:
#         for i, chat in enumerate(st.session_state.chat_history):
#             message(chat["content"], is_user=(chat["role"] == "user"), key=str(i))
