# Imports
import argparse
import csv
from datetime import datetime, timedelta
import pandas as pd
import random
import numpy as np

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def prod_code_generator():
    new_number = True
    number = random.randint(10000, 99999)
    with open("products.csv", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if number == row["product code"]:
                new_number = False
    if new_number:
        return number
    else:
        prod_code_generator()


def buy_code_generator(date, product_code, repetition=0):
    stored_date = str(date).replace("-", "")
    stored_date = stored_date[5:] if len(stored_date) > 4 else stored_date
    stored_product_code = str(product_code)
    stored_repetition = str(repetition)
    new_number = True
    number = stored_date + stored_product_code + stored_repetition
    with open("transactions.csv", newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if number == row["buy code"]:
                new_number = False
    if new_number:
        return number
    else:
        return buy_code_generator(date, product_code, repetition + 1)


def createfile(filename, default_value):
    # Checks if the given filename exists, creates it with a default_value if not.
    try:
        with open(f"{filename}", 'r') as file:
            pass
    except FileNotFoundError:
        if filename.endswith(".txt"):
            with open(f"{filename}", 'w') as file:
                file.write(default_value)
        elif filename.endswith(".csv"):
            with open(f"{filename}", 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(default_value)


def get_date(str_format=False,date_modifier=0):
    today = str(datetime.today().date())
    createfile("date.txt", today)
    with open("date.txt", "r") as file:
        file = file.read()
        current_date = datetime.strptime(file, '%Y-%m-%d').date()
        if not date_modifier:
            return current_date if not str_format else str(current_date)

        if date_modifier:
            modified_date = current_date + timedelta(days=int(date_modifier))
            return modified_date if not str_format else str(modified_date)


def date_manager(namespace):
    # Checks if set_date is a valid date. If so, replaces date
    if namespace.set:
        try:
            datetime.strptime(namespace.set, '%Y-%m-%d')
            with open("date.txt", "w") as file:
                file.write(namespace.set)
            print(f"Date has been set to: {namespace.set}")
        except ValueError:
            print(
                f"Invalid date: {namespace.set}\nHas to be a possible date in format: YYYY-MM-DD")
    elif namespace.advance:
        # Modifies date stored in date.txt
            modified_date = get_date(str_format=True, date_modifier= int(namespace.advance))
            print(
                f"Date has been set to: {modified_date}.")
            with open("date.txt", "w") as file:
                file.write(modified_date)


def product_manager(namespace):
    # Handles adding and changing products in products.csv
    # Checks if passed in product_name and/or product_code are new or existing. Stores what row it's located if it already exists.
    with open("products.csv", newline='') as file:
        reader = csv.DictReader(file)
        new_product = True
        unique_product_code = True
        product_row_count = 0
        for row in reader:
            if str(namespace.product_code) == str(row["product code"]):
                unique_product_code = False
            if namespace.name == row["product name"] or namespace.name == row["product code"]:
                new_product = False
                product_row = product_row_count
            else:
                product_row_count += 1

    if namespace.product_code:
        # Checks if entered product_code is valid.
        # If not, replaces it with a generated code for added product, or the current one for change product
        if namespace.product_code <= 9999 or namespace.product_code > 99999:
            print(
                f"Entered product_code invalid: {namespace.product_code}, must be 5 digits, cannot start with 0")
            namespace.product_code = prod_code_generator(
            ) if namespace.subparser_name == "add" else None
            if namespace.product_code:
                print(
                    f"Product_code has been to: {namespace.product_code}")
    # Handles add product subparser
    if namespace.subparser_name == "add" and new_product:
        with open("products.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([namespace.name, namespace.product_code, namespace.buy_price,
                             namespace.sell_price, namespace.expiracy_time])
            print(f"Added product: {namespace.name}")
    elif namespace.subparser_name == "add" and not new_product:
        print(f"Cannot add product: {namespace.name} as it already exists")
    # Handles change product subparser
    df = pd.read_csv("products.csv")
    if namespace.subparser_name == "change" and not new_product:
        # check to see if namespace.name is a product_name or a product_code
        try:
            int(namespace.name)
            product_name = df.loc[product_row, 'product name']
        except ValueError:
            product_name = namespace.name
        selected_something = False
        if namespace.new_name:
            # Check if new name isn't already in use
            unique_name = True
            for row in reader:
                if namespace.new_name == row["product name"]:
                    unique_name = False
            if unique_name:
                df.loc[product_row, 'product name'] = namespace.new_name
                print(
                    f"Product: {product_name} has been changed to: {namespace.new_name}.")
            else:
                print(
                    f"Cannot change a product name to: {namespace.new_name}, name already exists.")
            selected_something = True
        if namespace.product_code and unique_product_code:
            df.loc[product_row, 'product code'] = namespace.product_code
            print(
                f"Product: {product_name} code has been set to: {namespace.product_code}.")
            selected_something = True
        if namespace.product_code and not unique_product_code:
            print(
                f"Product: {product_name} can't be set to: {namespace.product_code}. New code is already in use")
            selected_something = True
        if namespace.buy_price:
            df.loc[product_row, 'default buy price'] = namespace.buy_price
            print(
                f"Product: {product_name} default buy price has been set to: {namespace.buy_price}.")
            selected_something = True
        if namespace.sell_price:
            df.loc[product_row, 'default sell price'] = namespace.sell_price
            print(
                f"Product: {product_name} default sell price has been set to: {namespace.sell_price}.")
            selected_something = True
        if namespace.expiracy_time:
            df.loc[product_row,
                   'expiracy time in days'] = namespace.expiracy_time
            print(
                f"Product: {product_name} default expiracy time has been set to: {namespace.expiracy_time} days.")
            selected_something = True
        elif namespace.delete:
            df = df.drop(labels=product_row, axis=0)
            print(f"Product: {product_name} has been deleted.")
            selected_something = True
        if selected_something == False:
            print(
                f"You selected {product_name} to be changed, but Superpy found no (valid) inputs of attributes to change")
        df.to_csv("products.csv", index=False)
    elif namespace.subparser_name == "change" and new_product:
        print(
            f"Product: {namespace.name} does not exist and therefore cannot be changed")


def transactions_manager(namespace):
    if namespace.amount <= 0:
        return print("The amount of which you buy/sell cannot be zero or negative")
    # Checks if passed in product_name or product_code exist or not. If it does, stores what row it's located.
    with open("products.csv", newline='') as file:
        reader = csv.DictReader(file)
        product_row = 0
        existing_product = False
        for row in reader:
            if namespace.name == row["product name"] or namespace.name == row["product code"]:
                existing_product = True
                break
            else:
                product_row += 1
    if not existing_product:
        print(
            f"Product: {namespace.name} is not recognized, a product must be added before it can be bought/sold")

    if existing_product:
        product_df = pd.read_csv("products.csv")
        # check to see if namespace.name is a product_name or a product_code
        try:
            int(namespace.name)
            namespace.name = product_df.loc[product_row, 'product name']
        except ValueError:
            namespace.name = namespace.name
        if namespace.subparser_name == "buy":
            current_date = get_date(str_format=True)
            product_code = product_df.loc[product_row, 'product code']
            buy_price = product_df.loc[product_row,'default buy price'] if not namespace.buy_price else namespace.buy_price
            buy_code = buy_code_generator(current_date, product_code)
            expiracy_time = product_df.loc[product_row, 'default expiracy time'] if not namespace.expiracy_time else namespace.expiracy_time
            expiracy_date = get_date(str_format=True,date_modifier= expiracy_time)
            with open("transactions.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([buy_code, "buy", namespace.name, product_code, namespace.amount,
                                 buy_price, get_date(str_format=True), expiracy_date])
        if namespace.subparser_name == "sell":
            product_code = (product_df.loc[product_row, 'product code'])
            # expiracy_date = df.loc[product_row, 'expiracy date']
            sell_price = product_df.loc[product_row,'default sell price'] if not namespace.sell_price else namespace.sell_price
            print(product_code)
            stock = calc_stock(product_code, namespace.amount)
            print(stock)
            if not stock:
                print(f"Product: {namespace.name}, was not in stock and could not be sold")
            else:
                for stock_buy_code, amount, buy_date, exp_date in stock:
                    with open("transactions.csv", 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([stock_buy_code, "sell", namespace.name, product_code, f"-{amount}",
                                         sell_price, buy_date, exp_date, get_date(str_format=True)])    




def calc_stock(product_code, ordered_amount, date=get_date(), buy_code = 0, today_activity=False):
    # Returns a nested list of how much of a product is in stock
    if type(date) == "str":
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return print(f"Invalid date: {date}\nHas to be a possible date in format: YYYY-MM-DD")
    # Date changed to np64 so it can be compared to the dates in transactions.csv
    date64 = np.datetime64(date)
    transac_df = pd.read_csv("transactions.csv")
    transac_df['expiracy date'] = pd.to_datetime(transac_df['expiracy date'],format='%Y-%m-%d')
    transac_df['buy date'] = pd.to_datetime(transac_df['buy date'],format='%Y-%m-%d')
    # Filtering out all unnecessary transactions
    transac_df = transac_df.loc[transac_df['product code'] == product_code]
    transac_df = transac_df.loc[(transac_df['buy date'] <= date64)]
    if today_activity:
        transac_df = transac_df.loc[transac_df['expiracy date'] == date64]
    else:
        transac_df = transac_df.loc[transac_df['expiracy date'] > date64]
    if buy_code:
        transac_df = transac_df.loc[transac_df['buy code'] == buy_code]

    return_list = []
    while ordered_amount > 0 and len(transac_df) != 0:
        transac_df.sort_values(by='expiracy date', inplace = True)
        return_buy_code = transac_df['buy code'].values[0]
        return_buy_date = str(transac_df['buy date'].values[0])
        return_expiracy_date = str(transac_df['expiracy date'].values[0])
        in_stock_df = transac_df.loc[transac_df['buy code'] == return_buy_code]
        in_stock_df = in_stock_df["amount"]
        stock_amount = in_stock_df.sum()
        if stock_amount > 0:
            if stock_amount < ordered_amount:
                ordered_amount -= stock_amount
                return_list += [[return_buy_code, stock_amount, return_buy_date[0:10], return_expiracy_date[0:10]]]
            elif stock_amount >= ordered_amount:
                return_list += [[return_buy_code, ordered_amount, return_buy_date[0:10], return_expiracy_date[0:10]]]
                ordered_amount = 0
            transac_df = transac_df.loc[transac_df['buy code'] != return_buy_code]
        else:
            transac_df = transac_df.loc[transac_df['buy code'] != return_buy_code]
    return return_list


def today_activity(date=get_date(), product_code=False):
    return_list = []
    #Returns nested list of items bought, sold or expired (in that order) on given date
    if type(date) == "str":
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return print(f"Invalid date: {date}\nHas to be a possible date in format: YYYY-MM-DD")
    # Date changed to np64 so it can be compared to the dates in transactions.csv
    date64 = np.datetime64(date)
    #From transac_df a buy_df, sell_df and expired_df are made representing each element of the return_list
    transac_df = pd.read_csv("transactions.csv")
    if product_code:
        transac_df = transac_df.loc[transac_df['product code'] == product_code]
    transac_df['expiracy date'] = pd.to_datetime(transac_df['expiracy date'],format='%Y-%m-%d')
    transac_df['buy date'] = pd.to_datetime(transac_df['buy date'],format='%Y-%m-%d')
    transac_df['sell date'] = pd.to_datetime(transac_df['sell date'],format='%Y-%m-%d')
    #buy_df
    buy_df = transac_df.loc[transac_df['buy/sell'] == "buy"]
    buy_df = buy_df.loc[buy_df['buy date'] == date64]
    buy_return_list = []
    while len(buy_df) != 0:
        buy_buy_code = buy_df['buy code'].values[0]
        buy_product_code = buy_df['product code'].values[0]
        buy_amount = buy_df['amount'].values[0]
        buy_name = buy_df['product name'].values[0]
        buy_return_list += [[buy_name, buy_buy_code, buy_product_code, buy_amount]]
        buy_df = buy_df.loc[buy_df['buy code'] != buy_buy_code]

    #sell_df
    sell_df = transac_df.loc[transac_df['buy/sell'] == "sell"]
    sell_df = sell_df.loc[sell_df['sell date'] == date64]
    sell_return_list = []
    while len(sell_df) != 0:
        sell_buy_code = sell_df['buy code'].values[0]
        sell_name = sell_df['product name'].values[0]
        sell_product_code = sell_df['product code'].values[0]
        sell_amount = sell_df['amount'].values[0]
        sell_return_list += [[sell_name, sell_buy_code, sell_product_code, sell_amount]]
        sell_df = sell_df.loc[sell_df['buy code'] != sell_buy_code]
    #expired_df
    expired_df = transac_df.loc[transac_df['expiracy date'] == date64]
    expired_return_list = []
    while len(expired_df) != 0:
        expired_buy_code = expired_df['buy code'].values[0]
        expired_product_code = expired_df['product code'].values[0]
        expired_name = expired_df['product name'].values[0]
        expired_amount = expired_df['amount'].values[0]
        stock = calc_stock(expired_product_code, expired_amount, date=date, buy_code=expired_buy_code, today_activity=True)
        if len(stock) == 0:
            expired_df = expired_df.loc[expired_df['buy code'] != expired_buy_code]
        else:
            expired_return_list += [[expired_name, expired_buy_code, expired_product_code, stock[0][1]]]
            expired_df = expired_df.loc[expired_df['buy code'] != expired_buy_code]
    return_list += [buy_return_list, sell_return_list, expired_return_list]
    return return_list



def report_manager(namespace):
    # Getting the product code, if a product name was given it's product code is taken from products.csv
    if namespace.product:
        df = pd.read_csv("products.csv", index_col="product name")
        try:
            product_code = int(namespace.product)
        except ValueError:
            product_code = df.loc[namespace.product, 'product code']


    # Getting the date if today is entered. If another date is given checks to see it's valid.
    if namespace.date.lower() =="today":
        report_date = get_date(str_format=True)
    else:
        try:
            datetime.strptime(namespace.date, '%Y-%m-%d')
            report_date = namespace.date
        except ValueError:
            return print(f"Invalid date: {namespace.date}\nHas to be a possible date in format: YYYY-MM-DD")
        

    if report_date:
        report_activity = today_activity(report_date, product_code)
        if report_activity[0]:
            print(f"Products bought on {report_date}:")
            for report_name, report_buy_code, report_product_code, report_amount in report_activity[0]:
                print(f"Product: {report_name}({report_product_code}), amount: {report_amount}, buy code: {report_buy_code}")
        if report_activity[1]:
            print(f"Products sold on {report_date}:")
            for report_name, report_buy_code, report_product_code, report_amount in report_activity[1]:
                print(f"Product: {report_name}({report_product_code}), amount: {str(report_amount)[1:]}, buy code: {report_buy_code}")
        if report_activity[2]:
            print(f"Products expired on {report_date}:")
            for report_name, report_buy_code, report_product_code, report_amount in report_activity[2]:
                print(f"Product: {report_name}({report_product_code}), amount: {report_amount}, buy code: {report_buy_code}")



def main():
    createfile("products.csv", ["product name", "product code", "default buy price",
               "default sell price", "default expiracy time"])
    createfile("transactions.csv", ["buy code", "buy/sell", "product name", "product code", "amount",
                             "price", "buy date","sell date", "expiracy date"])
    parser = argparse.ArgumentParser(
        description="Welcome to SuperPy, the best tool to keep track of transactions and revenue!")

    subparsers = parser.add_subparsers(
        help='subparser help', dest='subparser_name')

    date_product_parser = subparsers.add_parser(
        'date',
        help='commands for setting and changing date',
    )
    date_product_parser.set_defaults(func=date_manager)
    date_product_parser.add_argument(
        "-s", "--set",
        help="Pass in a date (YYYY-MM-DD) to set a date."
    )
    date_product_parser.add_argument(
        "-a", "--advance",
        type = int,
        help="Pass in a number (or negative number) for the amount of days you want to advance stored date"
    )
    add_product_parser = subparsers.add_parser(
        'add',
        help='commands for adding a product',
    )
    add_product_parser.set_defaults(func=product_manager)
    add_product_parser.add_argument(
        "name",
        help="Add a product name",
        type=str
    )
    add_product_parser.add_argument(
        "-b", "--buy_price",
        type=float,
        help="Add a default buy price",
        default=0
    )
    add_product_parser.add_argument(
        "-s", "--sell_price",
        type=float,
        help="Add a default sell price",
        default=0
    )
    add_product_parser.add_argument(
        "-e", "--expiracy_time",
        type=int,
        help="Add a default expiracy time in days",
        default=0
    )
    add_product_parser.add_argument(
        "-c", "--product_code",
        type=int,
        help="Add a 5 digit code, must be unique and cannot start with 0 \n SuperPy will generate code if none given",
        default=prod_code_generator()
    )
    change_product_parser = subparsers.add_parser(
        'change',
        help='commands for changing a product',
    )
    change_product_parser.set_defaults(func=product_manager)
    change_product_parser.add_argument(
        "name",
        type=str,
        help="Enter product name or product code of the product you wish to change"
    )
    change_product_parser.add_argument(
        "-nn", "--new_name",
        type=str,
        help="Enter new product name"
    )
    change_product_parser.add_argument(
        "-b", "--buy_price",
        type=float,
        help="Change default buy price"
    )
    change_product_parser.add_argument(
        "-s", "--sell_price",
        type=float,
        help="Change default sell price",
    )
    change_product_parser.add_argument(
        "-e", "--expiracy_time",
        type=int,
        help="Change default expiracy time in days",
    )
    change_product_parser.add_argument(
        "-c", "--product_code",
        type=int,
        help="Change product code, must be a unique 5 digit code, cannot start with 0",
    )
    change_product_parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete product",
    )
    buy_product_parser = subparsers.add_parser(
        'buy',
        help='commands for setting and changing date',
    )
    buy_product_parser.set_defaults(func=transactions_manager)
    buy_product_parser.add_argument(
        "name",
        help="Enter product name or product code of the product you wish to buy"
    )
    buy_product_parser.add_argument(
        "amount",
        type=int,
        help="Enter the amount you wish to buy"
    )
    buy_product_parser.add_argument(
        "-b", "--buy_price",
        type=float,
        help="Enter buy price. If none given, SuperPy will use default buy price"
    )
    buy_product_parser.add_argument(
        "-e", "--expiracy_time",
        help="Enter epiracy time in days OR enter date it expires on (YYYY-MM-DD)",
    )
    # Sell parser
    sell_product_parser = subparsers.add_parser(
        'sell',
        help='commands for selling products',
    )
    sell_product_parser.set_defaults(func=transactions_manager)
    sell_product_parser.add_argument(
        "name",
        help="Enter product name or product code of the product you wish to sell"
    )
    sell_product_parser.add_argument(
        "amount",
        type=int,
        help="Enter the amount you wish to sell"
    )
    sell_product_parser.add_argument(
        "-s", "--sell_price",
        type=float,
        help="Enter buy price. If none given, SuperPy will use default sell price"
    )
    sell_product_parser.add_argument(
        "-bc", "--buy_code",
        help="Enter a product's buy_code if you want to sell that specific product",
    )
    # Report parser
    report_product_parser = subparsers.add_parser(
        'report',
        help='commands for requesting a report',
    )
    report_product_parser.set_defaults(func=report_manager)
    report_product_parser.add_argument(
        "date",
        help="Enter the date you wish to receive report from (YYYY-MM-DD), type today for current date",
    )
    report_product_parser.add_argument(
        "-p", "--product",
        help="Enter the product name or product code of the product you want to receive report from",
    )
    parsed_args = parser.parse_args()
    print(parsed_args)
    parsed_args.func(parsed_args)


if __name__ == "__main__":
    # print(calc_stock(12500, 5, date="2015-08-27", buy_code=828125003))
    main()
