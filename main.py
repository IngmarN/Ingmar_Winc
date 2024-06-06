# Imports
import argparse
from functions import *

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.


def main():
    createfile("products.csv", ["product name", "product code", "default buy price",
               "default sell price", "default expiracy time"])
    createfile("transactions.csv", ["buy code", "buy/sell", "product name", "product code", "amount",
                             "price", "buy date","expiracy date", "sell date"])
    parser = argparse.ArgumentParser(
        description="Welcome to SuperPy, the best tool to keep track of products, transactions and revenue!")

    subparsers = parser.add_subparsers(
        help='subparser help', dest='subparser_name')

    date_product_parser = subparsers.add_parser(
        'date',
        help='commands for setting and changing date',
    )
    date_product_parser.set_defaults(func=date_manager)
    date_product_parser.add_argument(
        "-s", "--set",
        help="Pass in a date (YYYY-MM-DD) to set as date."
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
        help="Enter new product name, cannot be the same as an existing product"
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
        type=int,
        help="Enter expiracy time in days",
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
        "option",
        choices=["transactions","revenue", "stock", "products", "current_date"],
        help="Select which report you wish to receive",
    )
    report_product_parser.add_argument(
        "date1",
        nargs="?",
        default=None,
        help="Enter the (first) date you wish to receive report from (YYYY-MM-DD) If no date is passed in, report will use current_date",
    )
    report_product_parser.add_argument(
        "date2",
        nargs="?",
        default=None,
        help="If you want a report on several days, enter a second date (YYYY-MM-DD). The report will include both dates and every date in between",
    )
    report_product_parser.add_argument(
        "-p", "--product",
        help="(optional) Enter the product name or product code of the product you want to receive report from. Only affects options transactions and stock",
    )
    parsed_args = parser.parse_args()
    parsed_args.func(parsed_args)


if __name__ == "__main__":
    main()
