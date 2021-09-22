from flask import Flask
from dirent.base import Base
import os

def create_app(root, test_config = None):
    app = Flask(__name__)

    if test_config is not None:
        app.config.update(test_config)

    def get_path(path):
        parts = path.split("/")
        relative_path = os.path.join(*parts)

        dirent = Base.from_path(root, relative_path)
        if dirent is None:
            return { "error": "not found" }, 404

        try:
            json = dirent.json(include_contents=True)
        except PermissionError:
            return { "error": "permission denied"}, 403
        return json

    @app.route("/<path:path>")
    def get_subpath(path):
        return get_path("/" + path)

    @app.route("/")
    def get_root():
        return get_path("/")

    return app
