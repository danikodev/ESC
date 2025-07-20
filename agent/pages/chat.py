import streamlit as st
from streamlit.components.v1 import html
import requests
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

# Конфигурация страницы
st.set_page_config(
    page_title="TATLIN NEURO Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Стили для страницы чата
st.markdown("""
<style>
    /* Основные стили */
    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        color: #ffffff !important;
        margin: 0;
        padding: 0;
    }
    
    /* Фон */
    .stApp {
        background-color: #0a0a20;
        background-image: 
            radial-gradient(at 40% 20%, hsla(215,100%,30%,0.2) 0px, transparent 50%),
            radial-gradient(at 80% 0%, hsla(215,100%,30%,0.2) 0px, transparent 50%);
        padding: 0 !important;
    }
    
    /* Фиксированная неоновая рамка */
    .main-frame {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border: 2px solid #00a2ff;
        box-shadow: 0 0 30px rgba(0, 100, 255, 0.7), 
                    inset 0 0 20px rgba(0, 100, 255, 0.4);
        pointer-events: none;
        z-index: 999;
    }
    
    /* Шапка чата */
    .chat-header {
        position: fixed;
        top: 20px;
        left: 0;
        right: 0;
        height: 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 30px;
        background: rgba(0, 15, 30, 0.9);
        z-index: 1000;
        border-bottom: 1px solid #0066ff;
    }
    
    /* Название агента */
    .app-title {
        font-size: 2rem;
        color: #00ccff;
        text-shadow: 0 0 15px rgba(0, 200, 255, 0.7);
        margin: 0;
        background: linear-gradient(90deg, #00ccff, #0066ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: titleGlow 2s infinite alternate;
    }
    
    @keyframes titleGlow {
        from { text-shadow: 0 0 10px rgba(0, 200, 255, 0.5); }
        to { text-shadow: 0 0 20px rgba(0, 200, 255, 0.9); }
    }
    
    /* Область сообщений */
    .messages-container {
        position: fixed;
        top: 100px;
        left: 0;
        right: 0;
        bottom: 120px;
        padding: 20px;
        overflow-y: auto;
    }
    
    /* Сообщение пользователя */
    .user-message {
        background: linear-gradient(135deg, #0066ff 0%, #00a2ff 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 18px 18px 0 18px;
        margin-left: auto;
        margin-bottom: 15px;
        max-width: 70%;
        box-shadow: 0 5px 15px rgba(0, 100, 255, 0.4);
    }
    
    /* Сообщение бота */
    .bot-message {
        background: rgba(0, 30, 60, 0.7);
        color: #00ccff;
        padding: 15px 20px;
        border-radius: 18px 18px 18px 0;
        margin-right: auto;
        margin-bottom: 15px;
        max-width: 70%;
        border: 1px solid #0066ff;
        box-shadow: 0 5px 15px rgba(0, 50, 150, 0.3);
    }
    
    /* Панель ввода */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 120px;
        padding: 20px;
        background: rgba(0, 20, 40, 0.9);
        border-top: 1px solid #0066ff;
        display: flex;
        flex-direction: column;
    }
    
    /* Форма ввода */
    .input-form {
        display: flex;
        gap: 15px;
        width: 100%;
    }
    
    /* Поле ввода */
    .stTextInput>div>div>input {
        color: white !important;
        background: rgba(0, 25, 50, 0.8) !important;
        border: 1px solid #00a2ff !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
        font-size: 1.1rem !important;
        flex-grow: 1;
    }
    
    /* Кнопка отправки */
    .submit-button {
        background: linear-gradient(135deg, #0066ff 0%, #00a2ff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0 30px !important;
        font-size: 1.1rem !important;
        box-shadow: 0 0 15px rgba(0, 100, 255, 0.5) !important;
        transition: all 0.2s !important;
        height: auto !important;
    }
    
    .submit-button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 0 25px rgba(0, 150, 255, 0.8) !important;
    }
    
    /* Анимации */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .message {
        animation: fadeIn 0.3s ease-out;
    }
    
    /* Полоса прокрутки */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 20, 40, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00a2ff;
        border-radius: 4px;
    }
</style>

<link href='https://fonts.googleapis.com/css?family=Rajdhani' rel='stylesheet'>
""", unsafe_allow_html=True)

# Конфигурация API Langflow
API_KEY = os.getenv("API_KEY")
LANGFLOW_API_URL = os.getenv("LANGFLOW_API_URL", "http://langflow:7860")
FLOW_ID = os.getenv("FLOW_ID", "54925a2b-8469-4b28-8a85-34d75a8470cd")
API_URL = f"{LANGFLOW_API_URL}/api/v1/run/{FLOW_ID}"

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

def send_message(message):
    payload = {
        "input_value": message,
        "output_type": "chat"
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def process_response(response):
    try:
        if response and "outputs" in response:
            for output in response["outputs"]:
                if "outputs" in output:
                    for msg in output["outputs"]:
                        if "results" in msg:
                            return msg["results"]["message"]["text"]
        return "Не удалось обработать ответ API"
    except Exception as e:
        return f"Ошибка обработки ответа: {str(e)}"

# Инициализация истории чата
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Фиксированная неоновая рамка
st.markdown('<div class="main-frame"></div>', unsafe_allow_html=True)

# Шапка чата
st.markdown("""
<div class="chat-header">
    <h1 class="app-title">TATLIN NEURO</h1>
</div>
""", unsafe_allow_html=True)

# Область сообщений
st.markdown('<div class="messages-container">', unsafe_allow_html=True)

for message in st.session_state.messages:
    if message['role'] == 'user':
        st.markdown(f'<div class="user-message message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message message">{message["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Панель ввода
st.markdown('<div class="input-container">', unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    cols = st.columns([6, 1])
    with cols[0]:
        user_input = st.text_input(" ", placeholder="Введите ваш вопрос...", key="input", label_visibility="collapsed")
    with cols[1]:
        submitted = st.form_submit_button("Отправить", use_container_width=True)
    
    if submitted and user_input:
        # Добавляем сообщение пользователя
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Получаем ответ от Langflow
        with st.spinner("Агент думает..."):
            response = send_message(user_input)
            bot_response = process_response(response) or "Не удалось получить ответ"
            
        st.session_state.messages.append({"role": "bot", "content": bot_response})
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)