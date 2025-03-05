import openai
import base64
import os
from dotenv import load_dotenv
import tempfile

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

openai.api_key = openai_api_key

def stt(audio_data):
    """음성 데이터를 텍스트로 변환하는 함수 (STT)"""
    if not audio_data:
        return "오디오 데이터가 없습니다."

    # 오디오 데이터를 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_data)  # 바이트 데이터를 파일로 변환
        temp_audio_path = temp_audio.name  # 생성된 파일 경로 저장

    # OpenAI Whisper API 최신 방식 적용
    with open(temp_audio_path, "rb") as audio_file:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    
    return response.text.strip()  # 반환 값 변경
def ask_gpt(question):
    """GPT-4o 모델을 사용하여 질문에 대한 답변을 생성하는 함수"""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """당신은 유쾌한 AI 바리스타입니다.  
질문에 대해 창의적이고 재치 있는 답변을 제공하고, 유머를 담아 짧은 답변을 하세요."""},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content.strip()



def tts(text):
    # OpenAI 최신 TTS API 사용
    response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",  # "alloy", "echo", "fable", "onyx", "nova", "shimmer" 중 선택 가능
        input=text
    )

    # 임시 파일 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        temp_audio_file.write(response.read())  # 최신 API에서는 response.read() 사용
        temp_audio_file_path = temp_audio_file.name

    # 음원 인코딩 후 HTML audio 태그 생성
    with open(temp_audio_file_path, 'rb') as f:
        data = f.read()
        base64_encoded = base64.b64encode(data).decode()
        audio_tag = f"""
        <audio autoplay="true" controls>
            <source src="data:audio/mp3;base64,{base64_encoded}" type="audio/mp3">
        </audio>
        """

    # 임시 파일 삭제
    os.remove(temp_audio_file_path)

    return audio_tag


# def tts(text):
#     # OpenAI 최신 TTS API 사용
#     response = openai.Audio.speech(
#         model="tts-1",
#         voice="echo",  # "alloy", "echo", "fable", "onyx", "nova", "shimmer" 중 선택 가능
#         input=text
#     )

#     # 임시 파일 저장
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
#         temp_audio_file.write(response.read())  # 최신 API에서는 response.read() 사용
#         temp_audio_file_path = temp_audio_file.name

#     # 음원 인코딩 후 HTML audio 태그 생성
#     with open(temp_audio_file_path, 'rb') as f:
#         data = f.read()
#         base64_encoded = base64.b64encode(data).decode()
#         audio_tag = f"""
#         <audio autoplay="true" controls>
#             <source src="data:audio/mp3;base64,{base64_encoded}" type="audio/mp3">
#         </audio>
#         """

#     # 임시 파일 삭제
#     os.remove(temp_audio_file_path)

#     return audio_tag