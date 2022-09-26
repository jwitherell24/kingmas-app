from models import (Base, session,
                    Product, engine)
import datetime
import csv


def add_csv():
    with open("inventory.csv") as csvfile:
        data = csv.reader(csvfile)
        if len(row[2]) > 5:
            for row in data:
                product_dict = ["Name": row[0], "Quantity": clean_quantity(row[2]), "Price": clean_price(row[1]), "Date": clean_date(row[3])]
                
                
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
    app()