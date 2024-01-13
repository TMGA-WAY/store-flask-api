from marshmallow import Schema, fields, validates_schema, ValidationError
import os
from flask_smorest.fields import Upload



###############  Store Schema  ###################
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


###############  Item Schema  ###################

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainStoreSchema(), dump_only=True))


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


###############  Tag Schema  ###################

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


######## Inheritance #########
class StoreSchema(PlainStoreSchema, PlainTagSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class MultipartFileSchema(Schema):
    file = Upload(required=True)
    @validates_schema
    def validate_file(self, data, **kwargs):
        file = data["file"]

        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        if file_size > 5 * 1024 * 1024:
            raise ValidationError("File size must be less than 5MB")

        ## Reset file pointer
        file.seek(0)

        allowed_extension = ('csv', 'xlsx')
        if not any(file.filename.endswith(ext) for ext in allowed_extension):
            raise ValidationError("File must be CSV or Excel")
        # except Exception as e:
        #     raise ValueError("File not present")

