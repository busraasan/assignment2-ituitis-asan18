import os

from bottle import Bottle


def home_page():
    return "Assignment 2"


def create_app():
    app = Bottle()
    app.route("/", "GET", home_page)
    return app


application = create_app()
application.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
