import csv
from datetime import datetime, timedelta
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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
            with open("products.csv", newline='') as file:
                reader = csv.DictReader(file)
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
                f"Product: {product_name} expiracy time in days has been set to: {namespace.expiracy_time} days.")
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

        # Buying product
        if namespace.subparser_name == "buy":
            current_date = get_date(str_format=True)
            product_code = product_df.loc[product_row, 'product code']
            buy_price = product_df.loc[product_row,'default buy price'] if not namespace.buy_price else namespace.buy_price
            buy_code = buy_code_generator(current_date, product_code)
            expiracy_time = product_df.loc[product_row, 'expiracy time in days'] if not namespace.expiracy_time else namespace.expiracy_time
            expiracy_date = get_date(str_format=True,date_modifier= expiracy_time)
            with open("transactions.csv", 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([buy_code, "buy", namespace.name, product_code, namespace.amount,
                                 buy_price, get_date(str_format=True), expiracy_date])
                print(f"{namespace.amount} of product {namespace.name} bought, buy_code {buy_code}")

        # Selling product        
        if namespace.subparser_name == "sell":
            product_code = (product_df.loc[product_row, 'product code'])
            sell_price = product_df.loc[product_row,'default sell price'] if not namespace.sell_price else namespace.sell_price
            stock = calc_stock(product_code, namespace.amount)
            if not stock:
                print(f"Product: {namespace.name}, was not in stock and could not be sold")
            else:
                total_amount = 0
                for stock_buy_code, amount, buy_date, exp_date in stock:
                    total_amount += amount
                    with open("transactions.csv", 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([stock_buy_code, "sell", namespace.name, product_code, f"-{amount}",
                                         sell_price, buy_date, exp_date, get_date(str_format=True)])
                        print(f"{amount} of product {namespace.name} sold, buy_code {stock_buy_code}")
                if total_amount < namespace.amount:
                    print(f"The full amount of {namespace.amount} could not be sold as there was not enough in stock.")


def calc_stock(product_code, ordered_amount, date=get_date(), buy_code = 0, return_expired=False):
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
    if return_expired:
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
    # Reads and stores all first row information, removes first row, repeats till df is empty
    while len(buy_df) != 0:
        buy_buy_code = buy_df['buy code'].values[0]
        buy_product_code = buy_df['product code'].values[0]
        buy_amount = buy_df['amount'].values[0]
        buy_price = buy_df['price'].values[0]
        buy_name = buy_df['product name'].values[0]
        buy_return_list += [[buy_name, buy_buy_code, buy_product_code, buy_amount, buy_price]]
        buy_df = buy_df.loc[buy_df['buy code'] != buy_buy_code]

    #sell_df
    sell_df = transac_df.loc[transac_df['buy/sell'] == "sell"]
    sell_df = sell_df.loc[sell_df['sell date'] == date64]
    sell_return_list = []
    # Reads and stores all first row information, removes first row, repeats till df is empty
    while len(sell_df) != 0:
        sell_buy_code = sell_df['buy code'].values[0]
        sell_name = sell_df['product name'].values[0]
        sell_product_code = sell_df['product code'].values[0]
        sell_amount = sell_df['amount'].values[0]
        sell_amount = sell_amount * -1 # Sell amounts are negative in the df for calculations, negative removed for display
        sell_price = sell_df['price'].values[0]
        sell_return_list += [[sell_name, sell_buy_code, sell_product_code, sell_amount, sell_price]]
        sell_df = sell_df.loc[sell_df['buy code'] != sell_buy_code]

    #expired_df
    expired_df = transac_df.loc[transac_df['expiracy date'] == date64]
    expired_return_list = []
    # Reads and stores all first row information, removes first row, repeats till df is empty
    while len(expired_df) != 0:
        expired_buy_code = expired_df['buy code'].values[0]
        expired_product_code = expired_df['product code'].values[0]
        expired_name = expired_df['product name'].values[0]
        expired_amount = expired_df['amount'].values[0]
        expired_price = expired_df['price'].values[0]
        #Checks to see how much of the expired_amount was still in stock
        stock = calc_stock(expired_product_code, expired_amount, date=date, buy_code=expired_buy_code, return_expired=True)
        if len(stock) == 0:
            expired_df = expired_df.loc[expired_df['buy code'] != expired_buy_code]
        else:
            expired_return_list += [[expired_name, expired_buy_code, expired_product_code, stock[0][1], expired_price]]
            expired_df = expired_df.loc[expired_df['buy code'] != expired_buy_code]

    # Puts all stored information into one list and returns
    return_list += [buy_return_list, sell_return_list, expired_return_list]
    return return_list


def plot_pie_chart(stock_labels, stock_sizes, total_stock):
    # Combine small slices into 'Other' category if needed
    threshold = total_stock/20
    combined_label = 'Other'
    combined_size = 0
    combined_index = None
    labels_to_display = []
    sizes_to_display = []

    for i, size in enumerate(stock_sizes):
        if size < threshold:
            combined_size += size
            if combined_index is None:
                combined_index = i
            else:
                combined_index = min(combined_index, i)
        else:
            labels_to_display.append(stock_labels[i])
            sizes_to_display.append(size)

    # If there are slices to be combined, add the combined slice
    if combined_index is not None:
        labels_to_display.append(combined_label)
        sizes_to_display.append(combined_size)


# Create pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes_to_display, labels=labels_to_display, autopct=lambda p: f'{total_stock*p/100:.0f}', startangle=90)
    ax.axis('equal')
    ax.text(0.5, 1.1, f'Total Stock: {total_stock}', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

    plt.show()

# Function to plot the transactions bar chart
def plot_transac_one_date(report_date, report_activity):
    # Extract product codes and amounts for each type of activity
    product_codes = []
    bought_amounts = []
    sold_amounts = []
    expired_amounts = []

    # Add data for bought products
    for item in report_activity[0]:
        product_codes.append(item[2])
        bought_amounts.append(int(item[3]))
        sold_amounts.append(0)
        expired_amounts.append(0)

    # Add data for sold products
    for item in report_activity[1]:
        if item[2] in product_codes:
            index = product_codes.index(item[2])
            sold_amounts[index] = int(item[3])
        else:
            product_codes.append(item[2])
            bought_amounts.append(0)
            sold_amounts.append(int(item[3]))
            expired_amounts.append(0)

    # Add data for expired products
    for item in report_activity[2]:
        if item[2] in product_codes:
            index = product_codes.index(item[2])
            expired_amounts[index] = int(item[3])
        else:
            product_codes.append(item[2])
            bought_amounts.append(0)
            sold_amounts.append(0)
            expired_amounts.append(int(item[3]))

    # Create the bar chart
    x = np.arange(len(product_codes))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width, bought_amounts, width, label='Bought')
    bars2 = ax.bar(x, sold_amounts, width, label='Sold')
    bars3 = ax.bar(x + width, expired_amounts, width, label='Expired')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Product Codes')
    ax.set_ylabel('Amounts')
    ax.set_title(f'Transaction Report on {report_date}')
    ax.set_xticks(x)
    ax.set_xticklabels(product_codes)
    ax.legend()

    fig.tight_layout()

    plt.show()


def plot_transac_several_date(report_data):
    # Extract dates and initialize data containers
    dates = list(report_data.keys())
    bought_amounts = []
    sold_amounts = []
    expired_amounts = []

    # Initialize dictionaries to accumulate amounts by date
    for date in dates:
        bought_amount = sum(int(item[3]) for item in report_data[date][0])
        sold_amount = sum(int(item[3]) for item in report_data[date][1])
        expired_amount = sum(int(item[3]) for item in report_data[date][2])
        bought_amounts.append(bought_amount)
        sold_amounts.append(sold_amount)
        expired_amounts.append(expired_amount)

    # Create the bar chart
    x = np.arange(len(dates))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots(figsize=(12, 6))
    bars1 = ax.bar(x - width, bought_amounts, width, label='Bought')
    bars2 = ax.bar(x, sold_amounts, width, label='Sold')
    bars3 = ax.bar(x + width, expired_amounts, width, label='Expired')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Dates')
    ax.set_ylabel('Amounts')
    ax.set_title('Transaction Report Over Multiple Dates')
    ax.set_xticks(x)
    ax.set_xticklabels(dates)
    ax.legend()

    fig.tight_layout()

    plt.show()



# Handles stock, revenue and transaction reports of one date or a period (meaning two dates and all dates in between)
# Also handles reports of the current date (in date.txt) and currently known products (in products.csv)
def report_manager(namespace):

    # Getting information

    # Getting the product code, if a product name was given it's product code is taken from products.csv
    if namespace.product:
        df = pd.read_csv("products.csv", index_col="product name")
        try:
            report_product_code = int(namespace.product)
        except ValueError:
            try:
                report_product_code = df.loc[namespace.product, 'product code']
            except KeyError:
                return print(f"Product: {namespace.product} was not found.")
    else:
        report_product_code = 0    # No passed in product means 0 or False, 

    # Getting report_date from passed in namespace
    # If no date is passed in, date is pulled from date.txt
    if not namespace.date1:
        report_date = get_date(str_format=True)

        # Putting the date and product_code (if given) into today_activity
        report_activity = today_activity(report_date, report_product_code)

    # Report current date
    if namespace.option == "current_date":
        return print(f"Current date is {get_date(str_format=True)}")
    
    # Report products
    if namespace.option == "products":
        file_path = 'products.csv'

        with open(file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            headers = next(csv_reader)

            # Find the indices of the 'product name' and 'product code' columns
            product_name_idx = headers.index('product name')
            product_code_idx = headers.index('product code')

            # Print the headers for clarity
            print(f"{headers[product_name_idx]}, {headers[product_code_idx]}")

            for row in csv_reader:
                product_name = row[product_name_idx]
                product_code = row[product_code_idx]
                print(f"{product_name}, {product_code}")



    # If one date was passed in, report_date is set to passed in date if valid
    elif namespace.date1 and not namespace.date2:
        try:
            datetime.strptime(namespace.date1, '%Y-%m-%d')
            report_date = namespace.date1
        except ValueError:
            return print(f"Invalid date: {namespace.date1}\nHas to be a possible date in format: YYYY-MM-DD")

        # Putting the date and product_code (if given) into today_activity
        report_activity = today_activity(report_date, report_product_code)

    # Reports with one or many products, one date. 
    if not namespace.date2:
        # Transaction report, one date Creates bar chart
        if namespace.option == "transactions":

            # Bought products
            if report_activity[0]:
                print(f"Products bought on {report_date}:")
                for report_name, report_buy_code, report_product_code, report_amount, report_price in report_activity[0]:
                    print(f"""
    Product: {report_name}({report_product_code}), buy code: {report_buy_code}
    amount: {report_amount}, for a total of: {int(report_amount)*int(report_price)} euros""")

            # Sold products
            if report_activity[1]:
                print(f"\nProducts sold on {report_date}:")
                for report_name, report_buy_code, report_product_code, report_amount, report_price in report_activity[1]:
                    print(f"""
    Product: {report_name}({report_product_code}), buy code: {report_buy_code}
    amount: {report_amount}, for a total of: {int(report_amount)*int(report_price)} euros""")

            # Expired products
            if report_activity[2]:
                print(f"\nProducts expired on {report_date}:")
                for report_name, report_buy_code, report_product_code, report_amount, report_price in report_activity[2]:
                    print(f"""
    Product: {report_name}({report_product_code}), buy code: {report_buy_code}
    amount: {report_amount}, for a total of: {int(report_amount)*int(report_price)} euros""")

            # Messages for when no activity is found
            if all(not product_activity for product_activity in report_activity) and not report_product_code:
                print(f"No information found on {report_date} about any product.")
            if all(not product_activity for product_activity in report_activity) and report_product_code:
                print(f"No information found on {report_date} about {report_product_code}.")

        # Plot the transactions report bar chart
            plot_transac_one_date(report_date, report_activity)



        # Revenue report, one or many products (revenue always takes all products), one date. Creates bar chart.
        if namespace.option == "revenue":
            bought_total = 0
            sold_total = 0
            expired_total = 0

            print(f"Revenue {report_date}:")
            # Bought
            for activity in report_activity[0]:
                bought_total += (float(activity[3]) * float(activity[4]))
            if bought_total > 0:
                print(f"Items bought for a total of {bought_total:.2f} euros.")

            # Sold
            for activity in report_activity[1]:
                sold_total += (float(activity[3]) * float(activity[4]))
            if sold_total > 0:
                print(f"Items sold for a total of {sold_total:.2f} euros.")

            # Expired
            for activity in report_activity[2]:
                expired_total += (float(activity[3]) * float(activity[4]))
            if expired_total > 0:
                print(f"Items expired for a total of {expired_total:.2f} euros.")

            # Total
            sum_total = sold_total - (expired_total + bought_total)
            if sum_total > 0:
                print(f"Total profit is {sum_total:.2f} euros.")
            elif sum_total == 0:
                print("Not a loss but no profit either, completely break even")
            else:
                print(f"Total amount is a loss of {(-sum_total):.2f} euros.")

            # Create bar chart
            categories = ['Bought', 'Sold', 'Expired']
            values = [bought_total, sold_total, expired_total]

            plt.bar(categories, values, color=['blue', 'green', 'red'])

            # Add text above the bars
            for i, value in enumerate(values):
                plt.text(i, value + 5, f"€{value:.2f}", ha='center', va='bottom')

            plt.xlabel(f'Total profit: {sum_total:.2f}')
            plt.ylabel('Amount (euros)')
            plt.title(f'Revenue Report {report_date}')
            plt.show()


        # Stock reports with one date
        if namespace.option == "stock":

            # Stock report with one product, one date. Creates a pie chart
            if report_product_code:

                # Using calc stock to get stock data, storing it in lists to create pie chart from
                stock = calc_stock(report_product_code,99999999,report_date)
                if stock:
                    stock_labels = []
                    stock_sizes = []                
                    total_stock = 0
                    print(f"{report_product_code} stock:")
                    for item in stock:
                        total_stock += item[1]
                        stock_labels.append(item[0])
                        stock_sizes.append(item[1])
                        print(f"Buy code: {item[0]}: {item[1]}")
                    print(f"Total in stock is: {total_stock}")

                    # Creating pie chart
                    plot_pie_chart(stock_labels, stock_sizes, total_stock)

                else:
                    return(print(f"No stock was found of item:{report_product_code}"))


            # Stock report with all products, one date. Creates bar chart, a bar for each product
            if not report_product_code:
                # Getting a list of all products to calc the stock from
                df = pd.read_csv("transactions.csv")
                unique_products = df['product code'].unique()
                unique_products_list = list(unique_products)
                stock_message = False
                product_stocks = {}  # Dictionary to store product stocks
                # Loop that calculates stock of every product in transactions.csv and stores it in product_stocks dictionary
                for product in unique_products_list:
                    stock = calc_stock(product,99999999,report_date)
                    if stock:
                        stock_message = True
                        product_stock_info = []  # List to store stock info of each product
                        total_stock = 0
                        print(f"The amount in stock of item: {product}")
                        for item in stock:
                            total_stock += item[1]
                            product_stock_info.append((item[0], str(item[1])))
                            print(f"Buy code: {item[0]}: {item[1]}")
                        print(f"Total in stock is: {total_stock}")
                        product_stocks[str(product)] = total_stock, product_stock_info


                if stock_message:
                    # Plotting the bar chart
                    products = list(product_stocks.keys())
                    stock_amounts = [product_stocks[product][0] for product in products]

                    plt.bar(products, stock_amounts)
                    plt.xlabel('Product Code')
                    plt.ylabel('Amount in Stock')
                    plt.title('Stock Information')
                    plt.show()

                else:
                    print("No stock was found of any item")


    # Reports with two dates

    # If two dates were passed in, report_date is set to the period between and including both dates if both are valid.
    elif namespace.date1 and namespace.date2:
        report_dates = [namespace.date1, namespace.date2]
        for date in report_dates:
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return print(f"Invalid date: {date}\nHas to be a possible date in format: YYYY-MM-DD")
            
        # If both passed in dates are the same, resulting charts won't function as intended
        if namespace.date1 == namespace.date2:
            return print("The two passed in dates were the same, please try again using one date or two unequal dates.")

        # Swapping dates if date1 isn't the earliest of the two
        elif namespace.date1 > namespace.date2:
            namespace.date1, namespace.date2 = namespace.date2, namespace.date1
    

        # Creating list of dates
        dates_list = []
        namespace.date1 = datetime.strptime(namespace.date1, '%Y-%m-%d')
        namespace.date2 = datetime.strptime(namespace.date2, '%Y-%m-%d')
        current_date = namespace.date1
        while current_date <= namespace.date2:
            dates_list.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
        report_date = dates_list
        
        # Stock reports with one product, two dates, creates bar chart. A bar for each date
        if namespace.option == "stock" and report_product_code:
            # Getting and storing activity from all passed-in dates
            dates = []
            total_stocks = []
            for date in dates_list:

                # Getting stock data for the current date
                stock = calc_stock(report_product_code, 99999999, date)
                if stock:
                    total_stock = sum(item[1] for item in stock)
                    dates.append(date)
                    total_stocks.append(total_stock)
                    print(f"Total in stock for {date} is: {total_stock}")
                else:
                    print(f"No stock was found for {date}")

            # Plotting stock bar chart
            plt.figure(figsize=(10, 6))
            plt.bar(dates, total_stocks, color='blue')
            plt.xlabel('Dates')
            plt.ylabel('Total Stock Amount')
            plt.title('Total Stock Amount by Date')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()   

        # Stock reports with several products, two dates. Creates line chart, a line for each product.
        elif namespace.option == "stock" and not report_product_code:
            # Getting a list of all products to calc the stock from
            df = pd.read_csv("transactions.csv")
            unique_products = df['product code'].unique()
            unique_products_list = list(unique_products)

            # Getting stock data from every product in transactions.csv for every date
            # Stock values of 0 are not filtered out so there wont be dates missing in the chart.
            product_stock_data = {product: {'dates': [], 'stock': []} for product in unique_products_list}
            for date in dates_list:
                print(f"Stock on {date}:")
                stock_message = False
                for product in unique_products_list:
                    stock = calc_stock(product,99999999,date)
                    stock_message = True
                    total_stock = 0
                    total_stock = sum(item[1] for item in stock)
                    product_stock_data[product]['dates'].append(date)
                    product_stock_data[product]['stock'].append(total_stock)
                    print(f"The amount in stock of item: {product}")
                    print(f"Total in stock is: {total_stock}")

            # Plotting line chart
            plt.figure(figsize=(10, 6))
            for product, data in product_stock_data.items():
                plt.plot(data['dates'], data['stock'], label=product, drawstyle='steps-post')
            plt.xlabel('Date')
            plt.ylabel('Stock Amount')
            plt.title('Stock Amount Over Time')
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        # Transaction report, multiple dates, created triple bar chart. 1 set of triple bars for bought, sold, expired for each date.
        if namespace.option == "transactions":
            report_data = {}  # Dictionary to hold data for each date
            transac_product_code = report_product_code

            for report_date in dates_list:  # Assume dates_list is a list of dates
                report_activity = today_activity(report_date, transac_product_code)
                report_data[report_date] = [[], [], []]  # Initialize the list for each date

                # Collecting report data for each date
                for activity_type, activity_list in enumerate(report_activity):
                    for report_item in activity_list:
                        report_data[report_date][activity_type].append(report_item)


                if report_activity[0]:
                    print(f"Products bought on {report_date}:")
                    for report_name, report_buy_code, report_product_code, report_amount, report_price in report_activity[0]:
                        print(f"""
        Product: {report_name}({report_product_code}), buy code: {report_buy_code}
        amount: {report_amount}, for a total of: {int(report_amount)*int(report_price)} euros""")

                if report_activity[1]:
                    print(f"\nProducts sold on {report_date}:")
                    for report_name, report_buy_code, report_product_code, report_amount, report_price in report_activity[1]:
                        print(f"""
        Product: {report_name}({report_product_code}), buy code: {report_buy_code}
        amount: {report_amount}, for a total of: {int(report_amount)*int(report_price)} euros""")

                if report_activity[2]:
                    print(f"\nProducts expired on {report_date}:")
                    for report_name, report_buy_code, report_product_code, report_amount, report_price in report_activity[2]:
                        print(f"""
        Product: {report_name}({report_product_code}), buy code: {report_buy_code}
        amount: {report_amount}, for a total of: {int(report_amount)*int(report_price)} euros""")

                # Messages for when no activity is found
                if all(not product_activity for product_activity in report_activity):
                    print(f"No information found on {report_date}")


            # Plot the transactions report bar chart
            plot_transac_several_date(report_data)



    # Revenue report, one or many products (revenue always takes all products), two dates. Creates bar chart, a bar for bought, sold and expired
        if namespace.option == "revenue":
            bought_total = 0
            sold_total = 0
            expired_total = 0
            for report_date in dates_list:
                report_activity = today_activity(report_date, report_product_code)
                print(f"Adding revenue {report_date}:")


                # Bought
                for activity in report_activity[0]:
                    bought_total += (float(activity[3]) * float(activity[4]))
                if bought_total > 0:
                    print(f"Items bought for a total of {bought_total:.2f} euros.")

                # Sold
                for activity in report_activity[1]:
                    sold_total += (float(activity[3]) * float(activity[4]))
                if sold_total > 0:
                    print(f"Items sold for a total of {sold_total:.2f} euros.")

                # Expired
                for activity in report_activity[2]:
                    expired_total += (float(activity[3]) * float(activity[4]))
                if expired_total > 0:
                    print(f"Items expired for a total of {expired_total:.2f} euros.")

                # Total
                sum_total = sold_total - (expired_total + bought_total)
                if sum_total > 0:
                    print(f"Total profit is {sum_total:.2f} euros.")
                elif sum_total == 0:
                    print("Not a loss but no profit either, completely break even")
                else:
                    print(f"Total amount is a loss of {(-sum_total):.2f} euros.")

            # Create bar chart
            categories = ['Bought', 'Sold', 'Expired']
            values = [bought_total, sold_total, expired_total]

            plt.bar(categories, values, color=['blue', 'green', 'red'])

            # Add text above the bars
            for i, value in enumerate(values):
                plt.text(i, value + 5, f"€{value:.2f}", ha='center', va='bottom')

            plt.xlabel(f'Total profit: {sum_total:.2f}')
            plt.ylabel('Amount (euros)')
            plt.title(f'Revenue Report {dates_list[0]} to {dates_list[-1]}')
            plt.show()

             
                













