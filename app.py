from models import (Base, session, 
                    Product, engine)
import datetime
import csv


def menu():
    while True:
        print("""
              \nKINGMA'S MARKET INVENTORY
              \r1) View a product (press 'v' and 'enter')
              \r2) Add a new product (press 'a' and 'enter')
              \r3) Make a backup database (press 'b' and 'enter')
              \r4) Exit (press 'e' and 'enter)""")
        choice = input("Please select what you would like to do.  ").lower()
        if choice in ['v', 'a', 'b', 'e']:
            return choice
        else:
            input("""
                  \rPlease choose one of the options above.
                  \rEither v, a, b, or e.
                  \rPress enter to try again.""")
            
            
def clean_price(price_str):
    price_split = price_str.split("$")
    cleaned_price = int(float(price_str[1]) * 100)
    print(cleaned_price)             
            
def clean_quantity(quantity_str):
    quantity = int(quantity_str)
    print(quantity)
            
            
def clean_date(date_str):
    cleaned_date = datetime.datetime.strptime(date_str, "%m/%d/%Y")
    print(cleaned_date)
            
            
def add_csv():
    with open("inventory.csv") as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            if len(row[2]) < 5:
                product_dict = {"Name": row[0], "Price": clean_price(row[1]), 
                                "Quantity": clean_quantity(row[2]), "Date": clean_date(row[3])}
                new_product = Product(product_name=product_dict["Name"], product_price=product_dict["Price"], 
                                      product_quantity=product_dict["Quantity"], date_updated=product_dict["Date"])
                if session.query(Product).count() >= 27:
                    product_list = []
                    for product in session.query(Product.product_name):
                        product_list.append(product.product_name)
                    if f"{new_product.product_name}" not in product_list:
                        session.add(new_product)
                    else:
                        for product in session.query(Product):
                            info = str(product).split(";")
                            name = str(info[0]).split(":")
                            date = str(info[3]).split(":")
                            date_input = str(date[1]).split(" ")
                            date_changed = datetime.datetime.strptime(date_input[1], "%Y/%m/%d")
                            if name[1] == f"{new_product.product_name}" and date_changed < new_product.date_updated:
                                product.product_price = new_product.product_price
                                product.product_quantity = new_product.product_quantity
                                product.date_updated = new_product.date_updated
                            else:
                                continue
                else:
                    session.add(new_product)
    session.commit()
    products = session.query(Product)
    return products 
                
            
            
def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == "v":
            pass
        elif choice == "a":
            pass
        elif choice == "b":
            pass
        else:
            print("Goodbye!")
            app_running = False


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    #app()