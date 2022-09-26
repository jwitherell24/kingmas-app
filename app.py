from models import (Base, session,
                    Product, engine)
import datetime
import csv


def menu():
    print("""
          \nKIGNMA'S MARKET INVENTORY\n
          \r1) View a product (enter 'v')
          \r2) Add item to database (enter'a')
          \r3) Make a backup file (enter 'b')""")
    choice = input("What would you like to do?  ").lower()
    if choice in ["v", "a", "b"]:
        return choice
    else:
        input("""
              \rPlease choose from one of the options above.
              \rEither v, a, or b.
              \rPress enter to try again.""")


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


def print_product(product):
    product_str = str(product)
    product_split = product_str.split(";")
    price_str = str(product_split[2])
    price_split = price_str.split(":")
    date_str = str(product_split[3]).split(" ")
    date_formatted = datetime.datetime.strptime(date_str[2], "%Y-%m-%d")
    print(f"""
          \n{product_split[0]}
          \rQuantity: {product_split[1]}
          \rPrice: ${int(price_split[1])/100}
          \rUpdated: {print_date(date_formatted)}
          """)


def print_date(date_value):
    date = datetime.datetime.strftime(date_value, "%B %d, %Y")
    return date

    
def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == "v":
            id = 1
            for product in session.query(Product.product_name):
                print(f"{id}  {product.product_name}")
                id += 1
            while ValueError:
                try:
                    id_choice = int(input("\nSelect the id number of the product you would like to view.  "))
                    if id_choice not in range(1, session.query(Product).count()+1):
                        raise ValueError("""\rPlease select a valid id choice.
                            \rPress enter to continue.  """)
                except ValueError:
                    input(f"""\rId value must be a number from 1 to {session.query(Product).count()}
                          Press enter to continue.  """)
                else:
                    for product in session.query(Product.product_id):
                        if id_choice == product.product_id:
                            search_id = 1
                            for product in session.query(Product):
                                if id_choice == search_id:
                                    print_product(product)
                                    input("\nPress enter to continue.  ")
                                    break
                                else:
                                    search_id += 1
                        else:
                            continue
                    break
                

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()