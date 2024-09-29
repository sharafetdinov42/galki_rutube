from typing import List

# Путь к тренировочным данным
TRAIN_DATA_PATH: str = "src/data/train.parquet"

# Все столбцы, используемые в данных
ALL_COLUMNS: List[str] = ["Вопрос пользователя", "Классификатор 1 уровня", "Классификатор 2 уровня", "target"]

# Название модели классификатора
CLASSIFIER_MODEL_NAME: str = "intfloat/multilingual-e5-large-instruct"

# Название столбцов для целевых значений и векторов
TARGET_COLUMN: str = "target"
EMBEDDING_COLUMN: str = "embedding"

# Количество наиболее похожих классов для возврата
TOP_N: int = 1

# Настройки хоста и порта
HOST: str = "0.0.0.0"
PORT: int = 27370
