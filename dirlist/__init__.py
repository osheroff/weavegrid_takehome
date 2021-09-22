from flask import Flask, request
from dirent.base import Base
import os

def create_app(root, test_config = None):
    app = Flask(__name__)

    if test_config is not None:
        app.config.update(test_config)

    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['JSON_SORT_KEYS'] = False


    def get_path(path):
        parts = path.split("/")
        relative_path = os.path.join(*parts)

        dirent = Base.from_path(root, relative_path)
        if dirent is None:
            return { "error": "not found" }, 404

        recurse = 'recurse' in request.args
        try:
            json = dirent.json(include_contents=True, recurse = recurse)
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
