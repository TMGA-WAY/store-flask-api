import uuid
import traceback
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db.db import stores
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operation on stores")


@blp.route("/store/<string:store_id>")
class store(MethodView):
    @blp.response(status_code=200, schema=StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except Exception as e:
            print(traceback.print_exc())
            abort(http_status_code=404, message="store not found.")

    def delete(self, store_id):
        try:
            stores.pop(store_id)
            return {"message": "store deleted"}
        except Exception as e:
            abort(http_status_code=404, messsage="store not found")

    @blp.response(status_code=200, schema=StoreSchema)
    def put(selfself, store_id):
        store_data = request.get_json()
        if "price" not in store_data or "name" not in store_data:
            abort(http_status_code=404, message="Bad request. Ensure 'price' and 'name' are included in JSON payload")
        try:
            store = stores[store_id]
            store |= store_data
            return store
        except KeyError as e:
            print(e)
            abort(http_status_code=404, message="store not found")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(status_code=200, schema=StoreSchema(many=True))
    def get(self):
        return list(stores.values())

    @blp.arguments(StoreSchema)
    @blp.response(status_code=201, schema=StoreSchema)
    def post(self, store_data):
        for store in stores:
            if store_data["name"] == store["name"]:
                abort(http_status_code=404, message="store Already exists.")
        store_id = uuid.uuid4().hex
        store = {**store_id, "id": store_id}
        stores[store_id] = store
        return store, 201
