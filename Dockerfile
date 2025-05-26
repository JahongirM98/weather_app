# Dockerfile
FROM python:3.12

# Установка рабочей директории
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Установка зависимостей
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Открываем порт
EXPOSE 8000

# Команда по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
