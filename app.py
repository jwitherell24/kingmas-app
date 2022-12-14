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


@app.route("/items/<id>")
def items(id):
    items = Item.query.all()
    item = Item.query.get_or_404(id)
    return render_template("items.html", items=items, item=item)


@app.route("/items/<id>/edit", methods=["GET", "POST"]) 
def edit_item(id):
    items = Item.query.all()
    item = Item.query.get_or_404(id)
    if request.form:
        item.brand = request.form["brand"]
        item.name = request.form["name"]
        item.department = request.form["department"]
        item.local = request.form["local"]
        item.size = request.form["size"]
        item.attributes = request.form["attributes"]
        item.url = request.form["url"] 
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edititem.html", items=items, item=item)


@app.route("/items/<id>/delete")
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", msg=error), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000, host="127.0.0.1")
    