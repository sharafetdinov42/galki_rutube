import asyncio
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import uvicorn

from src.ml.config import TRAIN_DATA_PATH, CLASSIFIER_MODEL_NAME, EMBEDDING_COLUMN, TARGET_COLUMN, QUESTION_COLUMN, TOP_N

# Инициализация модели и данных
model = SentenceTransformer(CLASSIFIER_MODEL_NAME)
train = pd.read_parquet(TRAIN_DATA_PATH)

class Request(BaseModel):
    question: str

class Response(BaseModel):
    class_1: str
    class_2: str

app = FastAPI()

@app.get("/")
def index():
    return {"text": "Интеллектуальный помощник оператора службы поддержки."}

@app.post("/predict", response_model=Response)
async def predict_class(request: Request):
    query = request.question
    predicted_class = find_similar_class(query, train, model, TOP_N)
    
    response = Response(
        class_1=predicted_class.split('_')[0],
        class_2=predicted_class.split('_')[1]
    )

    return response

def find_similar_class(query: str, train: pd.DataFrame, model: SentenceTransformer, top_n: int):
    query_embedding = model.encode([query])
    
    try:
        similarities = cosine_similarity(query_embedding, np.array(train[EMBEDDING_COLUMN].tolist()))
    except ValueError as e:
        return [], f"Ошибка в вычислении сходства: {e}"

    similar_indices = np.argsort(similarities[0])[::-1][:top_n]
    similar_classes = train.iloc[similar_indices][TARGET_COLUMN]
    most_common_class = Counter(similar_classes).most_common(1)[0][0]
    
    return most_common_class

if __name__ == "__main__":
    host = "0.0.0.0"
    config = uvicorn.Config(app, host=host, port=38731)
    server = uvicorn.Server(config)
    loop = asyncio.get_running_loop()
    loop.create_task(server.serve())
