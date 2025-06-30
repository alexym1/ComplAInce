"""FastAPI example with Pydantic model"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str

def standard(item):
    return item

def scale(item):
    return item

def compute(item):
    return item

@app.post("/items8/")
def create_item8(item: Item) -> dict[str, str]:
    obj = standard(item)
    obj = scale(obj)
    obj = compute(obj)
    return {"message": "Item received", "item": "obj"}

@app.post("/items/")
def create_item(item: Item) -> dict[str, str | int]:
    obj = standard(item)
    obj = scale(obj)
    return {"message": "Item received", "item": 10}
