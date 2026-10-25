import logging
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# Настройка логирования вместо принтов
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("Senti.io_core")

app = FastAPI(title="Senti.io API")

logger.info("Инициализация пайплайна нейросети")

try:
    # Загрузка модели на CPU с использованием PyTorch
    classifier = pipeline(
        "sentiment-analysis", 
        model="blanchefort/rubert-base-cased-sentiment",
        framework="pt",
        device=-1
    )
    logger.info("Модель загружена.")
except Exception as e:
    logger.critical(f"Не удалось загрузить модель: {e}")
    classifier = None


class TextPayload(BaseModel):
    text: str


@app.post("/analyze")
def analyze_text(payload: TextPayload):
    if classifier is None:
        raise HTTPException(status_code=503, detail="Модель не запущена.")
        
    start_time = time.time()
    
    try:
        # Инференс с обязательным ограничением по длине для архитектуры BERT
        model_output = classifier(
            payload.text,
            truncation=True,
            max_length=512
        )
        
        # Обработка ответа
        res = model_output[0]
        sentiment = res["label"]
        confidence = round(float(res["score"]), 4)
        
    except Exception as e:
        logger.error(f"Ошибка инференса: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка.")
        
    execution_time = round(time.time() - start_time, 4)
    logger.info(f"Запрос обработан за {execution_time}сек. Результат: {sentiment} ({confidence})")
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "proc_time_sec": execution_time
    }