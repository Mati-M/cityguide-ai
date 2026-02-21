from fastapi import FastAPI


app = FastAPI()


items = []


@app.get("/")
def root() -> dict:
    return {"Hello": "World"}


@app.post("/items")
def add_item(item: str):
    items.append(item)
    return items


@app.get("/items")
def get_items(limit: int = 2):
    return items[:limit]
