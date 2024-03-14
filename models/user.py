from pydantic import BaseModel


class User(BaseModel):
    name: str
    login: str
    password: str
