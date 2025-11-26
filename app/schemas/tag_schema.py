from pydantic import BaseModel


class TagRead(BaseModel):
    id: int
    name: str


class TagCreate(BaseModel):
    name: str
