Senti.IO - веб-приложение для определения тональности отзывов и комментариев на три класса: позитивный; нейтральный; негативный.

Бэкенд - FastAPI + Uvicorn.
Фронтенд - Steamlit.
Нейросеть и инференс - Transformers + PyTorch

Ссылка на веб-приложение: https://project-ziinm-1-26-tr80r2.msk1.amvera.tech/

Для определения тональности используется нейросеть - https://huggingface.co/blanchefort/rubert-base-cased-sentiment

Для установки:
1. Установить python 3.13.3;
2. Создать виртуальное окружение python -m venv venv;
3. Установить зависимости pip install -r requirements.txt

Запустите в одном терминале ide для старта бэкенда команду `uvicorn main:app --reload`.
Для Streamlit в терминале используйте `streamlit run front.py`
