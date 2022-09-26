from models import (Base, session,
                    Product, engine)
import datetime
import csv


def add_csv():
    with open("inventory.csv") as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            if len(row[2]) < 5:
                product_dict = {"Name": row[0], "Quantity": clean_quantity(row[2]), "Price": clean_price(row[1]), "Date": clean_date(row[3])}
                new_product = Product(product_name=product_dict["Name"], product_quantity=product_dict["Quantity"], product_price=product_dict["Price"], date_updated=product_dict["Date"])
                if session.query(Product).count() >= 27:
                    product_list = []
                    for product in session.query(Product.product_name):
                        product_list.append(product.product_name)
                    if f"{new_product.product_name}" not in product_list:
                        session.add(new_product)
                if session.query(Product).count() < 27:
                    session.add(new_product)
        session.commit()
                
                
def clean_quantity(quantity_str):
    cleaned_quantity = int(quantity_str)
    return cleaned_quantity


def clean_price(price_str):
    split_price = price_str.split("$")
    cleaned_price = int(float(split_price[1]) * 100)
    return cleaned_price


def clean_date(date_str):
    cleaned_date = datetime.datetime.strptime(date_str, "%m/%d/%Y")
    return cleaned_date


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    # app()