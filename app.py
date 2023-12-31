import uuid

from flask import Flask, request
from flask_smorest import abort
from db.db import items, stores
import traceback

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except Exception as e:
        print(traceback.print_exc())
        abort(http_status_code=404, message="Store not found.")


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        stores.pop(store_id)
        return {"message": "Store deleted"}
    except Exception as e:
        abort(http_status_code=404, messsage="store not found")


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        abort(http_status_code=404, message="Store not found.")
    item_id = uuid.uuid4().hex
    item = {**item_id, "id": item_id}
    items[item_id] = item
    return item, 201


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except Exception as e:
        print(traceback.print_exc())
        abort(http_status_code=404, message="Item not found.")


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(http_status_code=404, message="Bad request. Ensure 'price' and 'name' are included in JSON payload")
    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError as e:
        print(e)
        abort(http_status_code=404, message="Item not found")


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        items.pop(item_id)
        return {"message": "Item deleted"}
    except Exception as e:
        abort(http_status_code=404, messsage="Item not found")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4500, debug=True)
