from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kingmas_inventory.db"
db = SQLAlchemy(app)

class Item (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column("Brand Name", db.String())
    name = db.Column("Item Name", db.String())
    department = db.Column("Department", db.String())
    local = db.Column("Made in Michigan?", db.String())
    size = db.Column("Item Size", db.String())
    attributes = db.Column("Item Attributes", db.Text)
    url = db.Column("Image", db.Text)
    
    def __repr__(self):
        return f"""<Item:
                Brand Name: {self.brand} 
                Name: {self.name}
                Department: {self.department}
                Made in Michigan?: {self.local}
                Item Size: {self.size}
                Attributes: {self.attributes}
                Image: {self.url}"""
                