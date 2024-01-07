from db import db


class TagModel(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.Foreignkey("stores.id"), nullable=False)

    store = db.relationship("StoreNodel", back_populates="tags")
    items = db.relationship("ItemModel", back_populate="tags", secondary="items_tags")
