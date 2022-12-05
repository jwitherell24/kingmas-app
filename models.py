from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kingmas_inventory.db"
db = SQLAlchemy(app)

class Item (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Item Name", db.String())
    department = db.Column("Department", db.String())
    made_in = db.Column("Made In", db.String())
    description = db.Column("Item Description", db.Text)
    image_link = db.Column("Image Link", db.Text)
    
    def __repr__(self):
        return f"""<Item:
                Name: {self.name}
                Department: {self.department}
                Made In: {self.made_in}
                Description: {self.description}
                Image: {self.image_link}"""