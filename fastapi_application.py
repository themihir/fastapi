from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: int
    brand: Optional[str] = None

class UpadteItem(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    brand: Optional[str] = None

app = FastAPI()

inventory = {
    1: {
        "name": "Milk",
        "price": 8.99,
        "brand": None
    }
}

@app.get("/")
def home():
    return {"Date": "Testing"}

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of item you would like to view"), gt=0):
    return inventory.get(item_id, "Item Not Available")


@app.get("/get-by-name/")
def get_item(test: int, name: str = Query(None, title="Name", desciption="Name of item.")):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    raise HTTPException(status_code = 400, detail="Item name not found")

@app.post("/create-item/{item_id}")
def create_post(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code = 400, detail="Item already exist")
    inventory[item_id] = item
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpadteItem):
    if item_id not in inventory:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Item id not found")
    
    if item.name:
        inventory[item_id].name = item.name  
    if item.price:
        inventory[item_id].price = item.price
    if item.brand:
        inventory[item_id].brand = item.brand
    return inventory[item_id]

@app.delete("/delete-item/{item_id}")
# ... in query means, input is mandetory 
def delete_item(item_id: int = Query(..., description="The id of the Item to delete from the inventory")):
    if item_id not in inventory:
        return {"Error": "Item id already exist."}

    del inventory[item_id]
    return {"data": "success, record deleted"}



