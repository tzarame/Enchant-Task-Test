from fastapi import FastAPI
from starlette.responses import FileResponse
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Создаем экземпляр FastAPI
app = FastAPI()

# Подключение к базе данных PostgreSQL
db_url = "postgresql://postgres:postgres@db:5433/postgres"  # Обратите внимание на изменение порта

try:
    engine = create_engine(db_url)
    engine.connect()
    db_status = "Connected to the PostgreSQL database"
except OperationalError as e:
    db_status = f"Failed to connect to the PostgreSQL database: {str(e)}"

# Определяем обработчик маршрута для корневого URL
@app.get("/")
def read_root():
    return FileResponse("index.html")
