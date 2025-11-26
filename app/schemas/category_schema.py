from pydantic import BaseModel

class CategoryRead(BaseModel):
    id: int
    name: str

class CategoryUpdate(BaseModel):
    name: str

class CategoryCreate(BaseModel):
    name: str
