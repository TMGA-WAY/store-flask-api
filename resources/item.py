import uuid
import traceback
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db.db import items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operation on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(status_code=200, schema=ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except Exception as e:
            print(traceback.print_exc())
            abort(http_status_code=404, message="item not found.")

    def delete(self, item_id):
        try:
            items.pop(item_id)
            return {"message": "item deleted"}
        except Exception as e:
            abort(http_status_code=404, messsage="item not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(status_code=200, schema=ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError as e:
            print(e)
            abort(http_status_code=404, message="item not found")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(status_code=200, schema=ItemSchema(many=True))
    def get(self):
        return list(items.values())

    @blp.arguments(ItemSchema)
    @blp.response(status_code=201, schema=ItemSchema)
    def post(self):
        item_data = request.get_json()
        item_id = uuid.uuid4().hex
        new_item = {**item_data, "id": item_id}
        items[item_id] = new_item
        return new_item, 201
