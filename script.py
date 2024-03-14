from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse
from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from jinja2 import Template
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

db_url = "postgresql://postgres:postgres@db:5432/postgres"

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Integer)

Base.metadata.create_all(bind=engine)

class ItemBase(BaseModel):
    name: str
    price: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/test")
def test_endpoint():
    return {"message": "it works"}

@app.post("/items/", response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemModel(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.price = item.price
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/db", response_class=HTMLResponse)
def read_db_status():
    try:
        connection = engine.connect()
        db_version = connection.execute(text("SELECT version();")).fetchone()[0]
        current_user = connection.execute(text("SELECT current_user;")).fetchone()[0]
        current_database = connection.execute(text("SELECT current_database();")).fetchone()[0]
        db_status = "Connected to the PostgreSQL database"
    except OperationalError as e:
        db_status = f"Failed to connect to the PostgreSQL database: {str(e)}"
        db_version = current_user = current_database = "Unknown"

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