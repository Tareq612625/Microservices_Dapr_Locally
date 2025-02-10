from fastapi import FastAPI
import json
import os
import random

app = FastAPI()

FILE_PATH = "items.json"

def load_items():
    """Load items from the JSON file."""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    return []

def save_items_to_file(items):
    """Save items to the JSON file."""
    with open(FILE_PATH, "w") as file:
        json.dump(items, file, indent=4)

def generate_random_item():
    """Generate a random item."""
    item_id = random.randint(100, 999)
    names = ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard", "Mouse"]
    name = random.choice(names)
    price = random.randint(100, 2000)
    return {"id": item_id, "name": name, "price": price}

@app.get("/")
def root():
    return {"message": "Hello from service_1 with JSON storage!"}

@app.post("/save-items")
def save_items():
    """Generate and save a new random item to a JSON file."""
    items = load_items()
    new_item = generate_random_item()
    items.append(new_item)
    save_items_to_file(items)
    return {"message": "Item saved successfully", "item": new_item}

@app.get("/get-items")
def get_items():
    """Retrieve items from the JSON file."""
    items = load_items()
    return items if items else {"message": "No items found"}
