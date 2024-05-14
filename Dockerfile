# Используем базовый образ Python 3.11
FROM python:3.11

# Устанавливаем poetry
RUN pip install poetry

# Копируем файлы проекта
COPY . /

# Устанавливаем зависимости проекта с помощью poetry
RUN poetry install

# Открываем порт, на котором будет работать FastAPI
EXPOSE 8000


# Запускаем FastAPI
CMD ["poetry", "run", "uvicorn", "SHIFT:start_app", "--host", "0.0.0.0", "--port", "8000"]
