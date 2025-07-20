import streamlit as st
import requests
import os
# import json

# from dotenv import load_dotenv
# from datetime import datetime

# dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
# load_dotenv(dotenv_path)

# Конфигурация API
# API_KEY = "sk-as43lzhdKPBZ7icPoDr6rKTSJi86iRdVVHKL_V8iMT0"
API_KEY = os.getenv("API_KEY")
API_URL = "http://localhost:7860/api/v1/run/54925a2b-8469-4b28-8a85-34d75a8470cd"

# Настройка заголовков  
headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

# Функция для отправки сообщения
def send_message(message):
    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": message
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка API: {str(e)}")
        return None

# Обработка и форматирование ответа
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

# Настройка интерфейса Streamlit
st.title("🤖 TATLIN NEURO")
st.caption("Чат-интерфейс для вашего LangFlow API")

# Инициализация истории чата
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображение истории сообщений
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Обработка ввода пользователя
if prompt := st.chat_input("Напишите ваше сообщение..."):
    # Добавление сообщения пользователя в историю
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Отправка запроса к API
    with st.spinner("Агент думает..."):
        response = send_message(prompt)
        full_response = process_response(response)
    
    # Добавление ответа агента в историю
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        with st.chat_message("assistant"):
            st.markdown(full_response)