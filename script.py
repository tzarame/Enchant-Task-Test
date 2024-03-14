from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

app = FastAPI()

db_url = "postgresql://postgres:postgres@db:5433/postgres"

try:
    engine = create_engine(db_url)
    connection = engine.connect()
    db_status = "Connected to the PostgreSQL database"
except OperationalError as e:
    db_status = f"Failed to connect to the PostgreSQL database: {str(e)}"

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/db")
def read_db_status():
    if "Connected" in db_status:
        return {"status": db_status}
    else:
        raise HTTPException(status_code=500, detail=db_status)