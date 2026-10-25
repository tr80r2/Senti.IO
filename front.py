import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/analyze")

st.set_page_config(page_title="Senti.io", layout="centered")

st.title("Senti.io")
st.write("Напишите что-нибудь, а сервис покажет скрытые эмоции текста :)")

user_text = st.text_area("Введите текст:", placeholder="Напишите комментарий или отзыв...")

if st.button("Анализировать", type="primary"):
    if not user_text.strip():
        st.warning("Поле ввода не должно быть пустым.")
        st.stop()
        
    with st.spinner("Обработка текста..."):
        try:
            response = requests.post(API_URL, json={"text": user_text}, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                label = data["sentiment"].upper()
                score = data["confidence"]
                
                if label == "POSITIVE":
                    st.success(f"Позитивный (Уверенность: {score:.2%})")
                elif label == "NEGATIVE":
                    st.error(f"Негативный... (Уверенность: {score:.2%})")
                else:
                    st.info(f"Нейтральный (Уверенность: {score:.2%})")
                    
                st.caption(f"Время обработки на бэкенде: {data['proc_time_sec']} сек.")
            else:
                st.error(f"Ошибка API: статус-код {response.status_code}")
                
        except requests.exceptions.Timeout:
            st.error("Превышено время ожидания ответа от сервера API.")
        except requests.exceptions.ConnectionError:
            st.error("Бэкенд FastAPI недоступен. Проверьте запуск сервера.")