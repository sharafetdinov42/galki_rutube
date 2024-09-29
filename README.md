# Интеллектуальный помощник оператора службы поддержки

<div align="center">
  <img src="extensions/views/rutube_logo.jpg" alt="Интеллектуальный помощник оператора службы поддержки (Решение от команды ГАИки)">
</div>

## Описание

Интеллектуальный помощник предназначен для автоматизации процессов поддержки клиентов, использующий модели машинного обучения для анализа и классификации вопросов пользователей. 

## Установка

Следуйте этим шагам для установки и запуска проекта:

1. Установите **Poetry**. [Инструкции по установке Poetry](https://python-poetry.org/docs/#installation).

2. Склонируйте данный репозиторий:

    ```bash
    git clone <URL_репозитория>
    cd <имя_каталога>
    ```

3. Установите среду с помощью Poetry:

    ```bash
    poetry shell
    poetry install
    ```

4. Настройте параметры в конфигурационных файлах, если это необходимо. Убедитесь, что вы указали правильные пути и настройки для вашего окружения.

5. Запустите приложение:

    ```bash
    poetry run uvicorn src.ml.classify:app --host 0.0.0.0 --port 27370
    ```

## Docker

Если вы предпочитаете использовать Docker, вы можете собрать образ и запустить контейнер с приложением. Вот пример `Dockerfile`:

```dockerfile
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
```


# Проверка API

Для тестирования API используйте следующий пример кода на Python:

```python
import requests

# URL вашего API
url = "http://83.143.66.65:27370/predict" # API

# Запрос к API
payload = {"question": "Что такое метка 18+?"} # Впишите сюда свой запрос
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Ответ:", response.json())
    else:
        print("Ошибка:", response.status_code, response.text)
except requests.exceptions.RequestException as e:
    print("Произошла ошибка при подключении к API:", e)
