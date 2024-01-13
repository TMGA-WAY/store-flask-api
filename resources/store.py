from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models import StoreModel
from db import db
from flask_jwt_extended import jwt_required

blp = Blueprint("stores", __name__, description="Operation on stores")


@blp.route("/store/<int:store_id>")
class store(MethodView):
    @blp.response(status_code=200, schema=StoreSchema)
    def get(self, store_id):
        store_ = StoreModel.query.get_or_404(store_id)
        return store_

    @blp.response(status_code=200)
    def delete(self, store_id):
        store_ = StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store_)
            db.session.commit()
            return {"message": f"Store with ID {store_id} got deleted"}
        except Exception as e:
            db.session.rollback()
            abort(http_status_code=400, message="Error while processing")


@blp.route("/store")
class StoreList(MethodView):
    @jwt_required()
    @blp.response(status_code=200, schema=StoreSchema(many=True))
    def get(self):
        try:
            stores = StoreModel.query.all()
            return stores
        except Exception as e:
            abort(http_status_code=500, message="Error while processing")

    @blp.arguments(StoreSchema)
    @blp.response(status_code=201)
    def post(self, store_data):
        try:
            store_ = StoreModel(**store_data)
            db.session.add(store_)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(http_status_code=500, message="Store not Created")
        return {"message": " Store Created succesfully"}
