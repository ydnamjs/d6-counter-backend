from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def root():
    return {"Hello": "World"}

items = []

@app.post("/items")
def create_item(item: str):
    items.append(item)
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int) -> str:
    if item_id < len(items) and item_id >= 0:
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")