FROM python:3.12

# Копируем requirements.txt в образ
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Устанавливаем рабочую директорию для приложения
WORKDIR /app

# Запуск script.py
CMD ["python", "script.py"]
