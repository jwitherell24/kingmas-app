from models import (Base, session,
                    Product, engine)
import datetime
import csv


def menu():
    print("""
          \nKIGNMA'S MARKET INVENTORY MAIN MENU\n
          \r1) View a sing product's inventory (enter 'v')
          \r2) Add a new product to the database (enter'a')
          \r3) Make a backup of the entire inventory (enter 'b')""")
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
                else:
                    for product in session.query(Product):
                        product_str = str(product).split("; ")
                        product_name = str(product_str[0]).split(": ")
                        date_str = str(product_str[3]).split(":")
                        date_input = str(date_str[1]).split(" ")
                        date_updated = datetime.datetime.strptime(date_input[1], "%Y-%m-%d")
                        if product_name[1] == f"{new_product.product_name}" and date_updated < new_product.date_updated:
                            product.product_price = new_product.product_price
                            product.product_quantity = new_product.product_quantity
                            product.date_updated = new_product.date_updated
                        else:
                            continue
                if session.query(Product).count() < 27:
                    session.add(new_product)
        session.commit()
        
        
def backup():
    with open("backup.csv", "w") as csvbackup:
        backup_writer = csv.DictWriter(csvbackup, fieldnames=["product_name", "product_price", "product_quantity", "date_updated"])
        backup_writer.writeheader()
        
        product_names = []
        product_prices = []
        product_quantities = []
        dates_updated = []
        for name in session.query(Product.product_name):
            product_names.append(name.product_name)
        for price in session.query(Product.product_price):
            product_prices.append(price.product_price)
        for quantity in session.query(Product.product_quantity):
            product_quantities.append(quantity.product_quantity)
        for date in session.query(Product.date_updated):
            dates_updated.append(date.date_updated)
            
        id = 0
        while id < len(product_names):
            backup_writer.writerow({"product_name": product_names[id], "product_price": product_prices[id], 
                                    "product_quantity": product_quantities[id], "date_updated": dates_updated[id]})   
            id += 1        
        
                            
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
    quantity_split = product_split[1].split(": ")
    price_str = str(product_split[2])
    price_split = price_str.split(":")
    date_str = str(product_split[3]).split(" ")
    date_formatted = datetime.datetime.strptime(date_str[2], "%Y-%m-%d")
    print(f"""
          \n{product_split[0]}
          \rQuantity: {clean_quantity(quantity_split[1])}
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
            print("\n")
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
        elif choice == "a":
            new_name = input("""
                             \nYou have chosen to add a new item. Please provide:
                             \rProduct name:  """)
            while ValueError:
                try:
                    new_quantity = int(input("Quantity:  "))
                except ValueError:
                    input("""
                          \rPlease enter your product quantity in integer form (i.e. 25).
                          \rPress enter to continue.  """)
                else:
                    break
            while IndexError:
                try:
                    new_price = clean_price(input("Price (ex. $5.99):  "))
                except IndexError:
                    input("""
                          \rPlease enter your price using the $5.99 example format.
                          \rPress enter to continue.  """)
                else:
                    break
            new_date = datetime.datetime.now()
            new_date_str = datetime.datetime.strftime(new_date, "%m/%d/%Y")
            cleaned_new_date = clean_date(new_date_str)
            new_product = Product(product_name=new_name, product_quantity=new_quantity, product_price=new_price, date_updated=cleaned_new_date)
            product_list = []
            for product in session.query(Product.product_name):
                product_list.append(product.product_name)
            if f"{new_product.product_name}" not in product_list:
                session.add(new_product)
                print("New product added!")
            else:
                for product in session.query(Product):
                    product_str = str(product).split("; ")
                    product_name = str(product_str[0]).split(": ")
                    if product_name[1] == f"{new_product.product_name}":
                        product.product_price = new_product.product_price
                        product.product_quantity = new_product.product_quantity
                        product.date_updated = new_product.date_updated
                        print("Product updated!")
                    else:
                        continue
            session.commit()
        elif choice == "b":
            backup()
            input("\nBackup file has been created! Press enter to continue. ")
            
            
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()