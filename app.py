from models import (Base, session, 
                    Product, engine)
import datetime
import csv 
import time


def clean_price(price_str):
    try:
        price_float = float((price_str).split("$")[1])
    except ValueError:
        input("""
              \n****** PRICE ERROR ******
              \rThe price should be a number without a currency symbol.
              \rEx. 10.99
              \rPress enter to try again.
              ***************************""")
    else:
        return int(price_float * 100)


def clean_date():
    pass


def add_csv():
    with open("inventory.csv") as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = row[2]
                date_updated = clean_date(row[3])
                   

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    # add_csv()
    # app()