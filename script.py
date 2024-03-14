from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse  # Add this line
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from jinja2 import Template

app = FastAPI()

db_url = "postgresql://postgres:postgres@db:5432/postgres"

try:
    engine = create_engine(db_url)
    connection = engine.connect()
    db_version = connection.execute(text("SELECT version();")).fetchone()[0]
    current_user = connection.execute(text("SELECT current_user;")).fetchone()[0]
    current_database = connection.execute(text("SELECT current_database();")).fetchone()[0]
    db_status = "Connected to the PostgreSQL database"
except OperationalError as e:
    db_status = f"Failed to connect to the PostgreSQL database: {str(e)}"
    db_version = current_user = current_database = "Unknown"

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/db", response_class=HTMLResponse)
def read_db_status():
    template = Template("""
    <html>
        <body>
            <h1>{{ status }}</h1>
            <p>Version: {{ version }}</p>
            <p>User: {{ user }}</p>
            <p>Database: {{ database }}</p>
            <p>upd upd upd ТУЦ ТУЦ ТУЦ пыщь пыщь</p>
        </body>
    </html>
    """)
    if "Connected" in db_status:
        return template.render(status=db_status, version=db_version, user=current_user, database=current_database)
    else:
        raise HTTPException(status_code=500, detail=db_status)