"""Flask example with Pydantic model"""

from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError

app = Flask(__name__)

class Item(BaseModel):
    name: str
    description: str

def standard(item):
    return item

def scale(item):
    return item

def compute(item):
    return item

@app.route("/items8/", methods=["POST"])
def create_item8():
    try:
        item_data = request.get_json()
        item = Item(**item_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    obj = standard(item)
    obj = scale(obj)
    obj = compute(obj)
    return jsonify({"message": "Item received", "item": "obj"})

@app.route("/items/", methods=["POST"])
def create_item():
    try:
        item_data = request.get_json()
        item = Item(**item_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    obj = standard(item)
    obj = scale(obj)
    return jsonify({"message": "Item received", "item": 10})

if __name__ == "__main__":
    app.run(debug=True)
