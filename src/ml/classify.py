import asyncio
import json
from collections import Counter

import numpy as np
import pandas as pd
import requests
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.ml.config import CLASSIFIER_MODEL_NAME, EMBEDDING_COLUMN, HOST, PORT, TARGET_COLUMN, TOP_N, TRAIN_DATA_PATH

# Инициализация модели и данных
model = SentenceTransformer(CLASSIFIER_MODEL_NAME)
train = pd.read_parquet(TRAIN_DATA_PATH)


class Request(BaseModel):
    """Модель для запроса с вопросом."""

    question: str


class Response(BaseModel):
    """Модель для ответа с предсказанными классами."""

    text: str
    class_1: str
    class_2: str


app = FastAPI()


@app.get("/")
def index() -> dict:
    """Проверка работы API."""
    return {"text": "Интеллектуальный помощник оператора службы поддержки."}


@app.post("/predict", response_model=Response)
async def predict_class(request: Request) -> Response:
    """Предсказать класс на основе заданного вопроса.

    Args:
        request (Request): Запрос с вопросом.

    Returns:
        Response: Ответ с предсказанными классами.
    """
    query = request.question

    text_url = "http://5.182.86.183:27361/api/v1/get_answer"  # Укажите URL вашего API
    payload = {
    "history": [
        {
        "role": "user",
        "content": "Отвечай кратко и по делу, но учитывая всю специфику вопроса" + query
        }
    ]
    }
    headers = {"Content-Type": "application/json"}

    text_response = requests.post(text_url, json=payload, headers=headers)

    # Извлекаем текст из ответа
    response_text = text_response.json()

    predicted_class = find_similar_class(query, train, model, TOP_N)

    return Response(
        text=response_text, 
        class_1=predicted_class.split("_")[0], 
        class_2=predicted_class.split("_")[1]
    )


def find_similar_class(query: str, train: pd.DataFrame, model: SentenceTransformer, top_n: int) -> str:
    """Найти наиболее похожий класс для заданного вопроса.

    Args:
        query (str): Вопрос для поиска.
        train (pd.DataFrame): Датасет с классами.
        model (SentenceTransformer): Модель для векторизации.
        top_n (int): Количество наиболее похожих классов.

    Returns:
        str: Наиболее распространенный класс.
    """
    query_embedding = model.encode([query])

    try:
        similarities = cosine_similarity(query_embedding, np.array(train[EMBEDDING_COLUMN].tolist()))
    except ValueError as e:
        return f"Ошибка в вычислении сходства: {e}"

    similar_indices = np.argsort(similarities[0])[::-1][:top_n]
    similar_classes = train.iloc[similar_indices][TARGET_COLUMN]
    most_common_class = Counter(similar_classes).most_common(1)[0][0]

    return most_common_class


if __name__ == "__main__":
    config = uvicorn.Config(app, host=HOST, port=PORT)
    server = uvicorn.Server(config)
    loop = asyncio.get_running_loop()
    loop.create_task(server.serve())
