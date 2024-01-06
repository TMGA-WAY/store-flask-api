from marshmallow import Schema, fields


class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class StoreSchema(PlainStoreSchema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class ItemUpdateSchema(ItemSchema):
    store = fields.Nested(ItemSchema(), dump_only=True)
