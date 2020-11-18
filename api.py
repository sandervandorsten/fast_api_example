from typing import List, Optional
from enum import Enum
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel


app = FastAPI()


class Article(BaseModel):
    content: str
    comments: List["str"] = []


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        item.price_with_tax = item.price + item.tax
    return item


@app.put("/items/{item_id}")
async def create_item(
    item: Item,
    item_id: int = Path(..., description="Id for the item."),
    q: Optional[str] = Query(None, description="Quantity"),
):
    return {"item_id": item_id, **item.dict()}


@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "DL"}
    if model_name == ModelName.lenet:
        return {"model_name": model_name, "message": "RESNET"}
    else:
        return {"model_name": model_name, "message": "last resort"}


@app.get("/file/{file_path:path}")
async def get_file(file_path: str = Path(..., description="File path to get")):
    return {"file_path": file_path}


@app.post("/article/")
def stuff(
    articles: List[Article],
    lang: str = Query(..., min_length=2, max_length=2),
    big_model: bool = Query(False, description="Use the big model"),
):
    for comment in articles[0].comments:
        comment + "5000"
    return articles
