from flask import (render_template, redirect,
                   url_for, request)
from models import db, Item, app


@app.route("/")
def index():
    items = Item.query.all()
    return render_template("index.html", items=items)


@app.route("/items/new", methods=["GET", "POST"])
def add_item():
    items = Item.query.all()
    if request.form:
        new_item = Item(brand=request.form["brand"],
                        name=request.form["name"],
                        department=request.form["department"],
                        local=request.form["local"],
                        size=request.form["size"],
                        attributes=request.form["attributes"],
                        url=request.form["url"])
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("add_item"))
    return render_template("additem.html", items=items) 


@app.route("/item/<id>")
def item(id):
    item = Item.query.get_or_404(id)
    return render_template("item.html", item=item)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", msg=error), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000, host="127.0.0.1")
    