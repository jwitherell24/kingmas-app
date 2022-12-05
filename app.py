from flask import (render_template, redirect,
                   url_for, request)
from models import db, Item, app


@app.route("/")
def index():
    items = Item.query.all()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000, host="127.0.0.1")