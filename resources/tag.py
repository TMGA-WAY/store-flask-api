from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
import logging

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

blp = Blueprint("tags", __name__, description="Operation on tags")


@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(status_code=200, schema=TagSchema(many=True))
    def get(self, store_id):
        try:
            store = StoreModel.query.get_or_404(store_id)
            return store.tags.all()
        except SQLAlchemyError as e:
            logger.info(f"exception message \t{e}")
            abort(http_status_code=500, message="Error while processing")

    @blp.arguments(schema=TagSchema)
    @blp.response(status_code=201, schema=TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(http_status_code=400, message="Tag already exists")
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.info(f"Exception message \t {e}")
            abort(http_status_code=500, message="Error while processing")
        return tag


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(status_code=200, schema=TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(status_code=202, description="Deletes a tag if no item is tagged",
                  example={"message": "Tag deleted"})
    @blp.alt_response(status_code=404, description="Tag not found")
    @blp.alt_response(status_code=400,
                      description="Returned if tag is assigned to one or more items. In this case, the tag is not "
                                  "deleted")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted"}
        abort(400, "Could not delete tag. make sure tag is not associated with any Items, then try again")


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(status_code=201, schema=TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        try:
            item.tags.append(tag)
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.info(f"Exception message \t{e}")
            abort(http_status_code=500, message="Error while committing")

        return tag

    @blp.response(status_code=200, schema=TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        try:
            item.tags.remove(tag)
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.info(f"Exception message \t{e}")
            abort(http_status_code=500, message="Error while committing")

        return {"message": "Item removed form tag."}
