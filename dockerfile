FROM python:3.10

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Удаляем старую виртуальную среду, если она есть
RUN poetry env remove python || true

# Устанавливаем зависимости
RUN poetry install --no-root

# Копируем весь код приложения из src
COPY src/ ./src

# Команда для запуска приложения
CMD ["poetry", "run", "uvicorn", "src.ml.classify:app", "--host", "0.0.0.0", "--port", "27370"]
