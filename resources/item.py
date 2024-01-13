from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema, PlainItemSchema
from models import ItemModel
from db import db
from flask_jwt_extended import jwt_required

blp = Blueprint("items", __name__, description="Operation on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(status_code=200, schema=ItemSchema)
    def get(self, item_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            return item
        except Exception as e:
            abort(http_status_code=404, message=f"No item found with item_id {item_id}")

    @blp.response(status_code=200)
    def delete(self, item_id):
        item_ = ItemModel.query.get_or_404(item_id)
        try:
            db.session.delete(item_)
            db.session.commit()
            return {"message":f"Item with ID {item_id} got deleted"}
        except Exception as e:
            db.session.rollback()
            abort(http_status_code=400, message = "Error while processing")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(status_code=200, schema=ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = ItemModel.query.get(item_id)
            if item:
                item.price = item_data["price"]
                item.name = item_data["name"]
            else:
                item = ItemModel(**item_data)
            db.session.add(item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(http_status_code=500)
        return {"message": "Item updated successfully"}


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(status_code=200, schema=PlainItemSchema(many=True))
    def get(self):
        try:
            items = ItemModel.query.all()
            return items
        except Exception as e:
            abort(http_status_code=500, message= "Error while processing")

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(status_code=201)
    def post(self, item_data):
        try:
            item = ItemModel(**item_data)
            db.session.add(item)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(http_status_code=500, message="Item not created")
        return {"message": "Item created successfully"}
