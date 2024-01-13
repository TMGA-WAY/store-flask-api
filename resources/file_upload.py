from flask.views import MethodView
from flask_smorest import Blueprint
from werkzeug.utils import secure_filename
from schemas import MultipartFileSchema

blp = Blueprint("files", __name__, description="Operation on File upload")


@blp.route("/file")
class File(MethodView):
    @blp.arguments(schema=MultipartFileSchema, location="files")
    @blp.response(status_code=201)
    def post(self, files):
        file = files["file"]
        file.save("./upload/" + secure_filename(file.filename))
        return {"message": "File uploaded successfully"}
