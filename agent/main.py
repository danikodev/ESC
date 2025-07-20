import streamlit as st
import os
from streamlit.components.v1 import html

# Конфигурация страницы (полноэкранный режим)
st.set_page_config(
    page_title="TATLIN NEURO",
    page_icon="⚡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Неоновые CSS-стили для главной страницы
st.markdown("""
<style>
    /* Основные стили */
    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
    }
    
    /* Неоновый фон */
    .stApp {
        background-color: #000000;
        background-image: 
            radial-gradient(at 40% 20%, hsla(215,100%,30%,0.4) 0px, transparent 50%),
            radial-gradient(at 80% 0%, hsla(215,100%,30%,0.4) 0px, transparent 50%);
    }
    
    /* Неоновые контейнеры */
    .neon-box {
        background: rgba(0, 10, 30, 0.8);
        border: 2px solid #00a2ff;
        border-radius: 20px;
        box-shadow: 0 0 15px #0066ff, inset 0 0 10px #0066ff;
        padding: 2.5rem;
        margin-bottom: 2rem;
    }
    
    /* Крупный текст */
    h1 {
        font-size: 4rem !important;
        color: #00ccff !important;
        text-shadow: 0 0 10px #00a2ff;
        margin-bottom: 1.5rem !important;
    }
    
    h2 {
        font-size: 2.5rem !important;
        color: #00ccff !important;
        text-shadow: 0 0 5px #00a2ff;
    }
    
    /* Неоновые кнопки */
    .stButton>button {
        font-size: 1.5rem !important;
        background: linear-gradient(135deg, #0066ff 0%, #00ccff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1rem 2rem !important;
        box-shadow: 0 0 15px #0066ff !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        height: auto !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 25px #00a2ff !important;
    }
    
    /* Анимация пульсации */
    @keyframes pulse {
        0% { opacity: 0.8; }
        50% { opacity: 1; }
        100% { opacity: 0.8; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Дополнительные стили для главной страницы */
    .main-title {
        text-align: center;
        margin-bottom: 3rem !important;
    }
    
    .subtitle {
        font-size: 1.8rem !important;
        color: #00ccff !important;
        text-align: center;
        margin-bottom: 3rem !important;
        line-height: 1.5;
    }
    
    .features-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 2rem;
        margin-top: 3rem;
        margin-bottom: 3rem;
    }
    
    .feature-box {
        background: rgba(0, 20, 40, 0.6);
        border: 1px solid #00a2ff;
        border-radius: 15px;
        padding: 1.5rem;
        width: 28%;
        min-width: 250px;
        box-shadow: 0 0 10px rgba(0, 100, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0, 100, 255, 0.5);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        color: #00ccff;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .feature-title {
        font-size: 1.5rem !important;
        color: white !important;
        margin-bottom: 1rem !important;
        text-align: center !important;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
    }
    
    .feature-text {
        font-size: 1.1rem;
        color: #a0d0ff;
        text-align: center;
        line-height: 1.5;
    }
    
    /* Стиль для разделителей */
    .divider {
        display: flex;
        align-items: center;
        margin: 2rem 0;
    }
    
    .divider-line {
        flex-grow: 1;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00a2ff, transparent);
        position: relative;
    }
    
    .divider-line:before,
    .divider-line:after {
        content: "";
        position: absolute;
        width: 10px;
        height: 10px;
        background: #00a2ff;
        border-radius: 50%;
        top: 50%;
        transform: translateY(-50%);
    }
    
    .divider-line:before {
        left: 0;
        box-shadow: 0 0 10px #00a2ff;
    }
    
    .divider-line:after {
        right: 0;
        box-shadow: 0 0 10px #00a2ff;
    }
    
    /* Стиль для цитаты Татлина */
    .tatlin-quote {
        font-size: 2.2rem;
        color: #00ccff;
        text-align: center;
        padding: 2rem 0;
        font-style: italic;
        text-shadow: 0 0 8px rgba(0, 200, 255, 0.7);
        position: relative;
        margin: 2rem 0;
    }
    
    .tatlin-signature {
        font-size: 1.5rem;
        color: #00a2ff;
        text-align: center;
        margin-top: 1rem;
        font-style: normal;
        text-shadow: 0 0 5px rgba(0, 162, 255, 0.5);
    }
</style>

<link href='https://fonts.googleapis.com/css?family=Rajdhani' rel='stylesheet'>
""", unsafe_allow_html=True)

# Состояния сессии
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# JavaScript для редиректа
redirect_js = """
<script>
function redirectToChat() {
    window.location.href = "http://localhost:8503/chat";
}
</script>
"""

# Главная страница
def home_page():
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        # Основной заголовок
        st.markdown("""
        <div class="neon-box">
            <h1 class="pulse main-title">TATLIN NEURO</h1>
            <p class="subtitle">
                Ваш интеллектуальный AI-ассистент для работы с Tatlin Unified<br>
                Быстрые ответы, экспертные решения и автоматизация задач
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Кнопка перехода к чату
        if st.button("🚀 ПЕРЕЙТИ К ЧАТУ", key="go_to_chat"):
            st.switch_page("pages/chat.py")
            
        
        # Блок с преимуществами
        st.markdown("""
        <div class="features-container">
            <div class="feature-box">
                <div class="feature-icon">⚡️</div>
                <h3 class="feature-title">Мгновенные ответы</h3>
                <p class="feature-text">Получайте решения для Tatlin Unified в режиме реального времени</p>
            </div>
            <div class="feature-box">
                <div class="feature-icon">🤖</div>
                <h3 class="feature-title">Экспертные знания</h3>
                <p class="feature-text">Доступ к лучшим практикам и решениям от экспертов</p>
            </div>
            <div class="feature-box">
                <div class="feature-icon">🔧</div>
                <h3 class="feature-title">Автоматизация</h3>
                <p class="feature-text">Готовые команды и скрипты для автоматизации задач</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        

# Запуск главной страницы
if st.session_state.page == 'home':
    home_page()



# Футер
st.markdown("""
<style>
    .footer {
        margin-top: 3rem;
        padding: 2rem 0;
        text-align: center;
        color: white !important;
        background: linear-gradient(to bottom, transparent, rgba(0, 10, 30, 0.8));
    }
    .footer a {
        color: white !important;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    .footer a:hover {
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
    }
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 0.5rem;
    }
</style>

<div class="footer">
    <p>© 2025 NeuroLab AI. Все права защищены.</p>
    <div class="footer-links">
        <a href="#">Политика конфиденциальности</a>
        <span>•</span>
        <a href="#">Условия использования</a>
        <span>•</span>
        <a href="#">Контакты</a>
    </div>
</div>
""", unsafe_allow_html=True)