from datetime import datetime, timedelta
import os
import glob
from dotenv import load_dotenv  # pip install python-dotenv
import dictionary as dic
import helpers.regex_helper as reg

load_dotenv()

DIR_STMTS = os.getenv("DIR_STMTS")
DIR_OUTPUT = accountClosed = os.getenv("DIR_OUTPUT")
ASSETS_ACCOUNT_PLACEHOLDER = os.getenv("ASSETS_ACCOUNT_PLACEHOLDER")
EXPENSES_ACCOUNT_PLACEHOLDER = os.getenv("EXPENSES_ACCOUNT_PLACEHOLDER")
LIABILITIES_ACCOUNT_PLACEHOLDER = os.getenv("LIABILITIES_ACCOUNT_PLACEHOLDER")
INCOME_ACCOUNT_PLACEHOLDER = os.getenv("INCOME_ACCOUNT_PLACEHOLDER")


def match_any_item(word, arrays):
    word = word + "\\b"
    return any(item.lower() in word.lower() for item in arrays)


def found_in_string(word, string):
    return word.lower() in string.lower()


def clean_date_string(date):
    return reg.replace('\\.*|,*', "", date).strip()


def clean_description_string(description):
    description = reg.replace(reg.whole_day_month, "", description)
    description = reg.replace("-*", "", description)
    return description.strip()


def clean_price_string(string):
    return reg.replace('\,*|\\$*|\s*', "", string).strip()


def convert_string_to_date_format(string):
    date_format = reg.replace(reg.year_digit, "%Y", string)
    date_format = reg.replace(reg.day_digit, "%d", date_format)
    date_format = reg.replace(reg.month_name, "%b", date_format)
    return date_format


def get_date_from_file_name(string):
    return reg.grab(reg.year_digit + "-" + reg.month_digit, string)


def get_path_from_bean_def(bean_def):
    return DIR_STMTS + bean_def.replace(":", "/") + "/"


def get_output_file_from_date(date):
    output_file = DIR_OUTPUT + date[0:7] + ".bean"

    if (os.path.exists(output_file)):
        output_file = open(output_file, "a")  # append to it
    else:
        output_file = open(output_file, "x")  # create one

    return output_file


def get_latest_date_in_folder(folder):
    files = glob.glob(folder+'*')
    latestFile = sorted(files, key=get_date_from_file_name, reverse=True)[0]
    return get_date_from_file_name(latestFile)


def get_end_period(period_string):
    end_period = period_string.lower()
    split_by = "-"

    if (reg.match(reg.to_in_string, end_period)):
        split_by = " to "

    end_period = end_period.rsplit(split_by, 1)
    end_period = end_period[len(end_period)-1]

    return clean_date_string(end_period)


def get_description(transaction):
    description = reg.replace(reg.whoele_month_day, "", transaction)
    description = reg.replace(reg.price, "", transaction)
    return clean_description_string(description)


def get_posted_date(transaction, end_period):
    # get date based on format
    two_month_day = reg.has_something_before + reg.whoele_month_day
    two_day_month = reg.has_something_before + reg.whole_day_month
    month_day = reg.month_name + reg.two_chars_max + reg.day_digit
    day_month = reg.day_digit + reg.month_name + reg.two_chars_max

    posted_date = reg.grab(reg.find_first_match(
        transaction, two_month_day, two_day_month, month_day, day_month), transaction)

    # get year based on date and end period
    if (found_in_string("jan", end_period) and found_in_string("dec", posted_date)):
        year = str(int(end_period.strip()[-4:])-1)
    else:
        year = end_period.strip()[-4:]

    date = clean_date_string(posted_date) + " " + clean_date_string(year)

    # get date object based on format
    date_format = convert_string_to_date_format(date)
    return datetime.strptime(date, date_format).strftime("%Y-%m-%d")


def get_price(transaction, **kwargs):
    lines = kwargs.get('lines', None)
    index = kwargs.get('index', None)
    price_found = False

    if (lines and index):
        while not price_found and index < len(lines):
            price_found = reg.match(reg.price, lines[index])
            index += 1
        price_found = reg.grab(reg.price, lines[index-1])
    else:
        price_found = reg.grab(reg.price, transaction)

    return clean_price_string(price_found) + " CAD"


def get_balance(transaction):
    if (not reg.match(reg.twice_pattern(reg.price + reg.any_chars), transaction)):
        return False
    return clean_price_string(reg.grab(reg.price+reg.end_with, transaction))


def look_up_flow(transaction, flow_dictionary):
    flow = "?"

    for key_sign, val_triggers in flow_dictionary.items():
        match = match_any_item(transaction, val_triggers)
        if (match):
            flow = key_sign

    return flow


def decide_liability_use_account(flow):
    if flow == "+":
        to_account = ASSETS_ACCOUNT_PLACEHOLDER
    else:
        to_account = EXPENSES_ACCOUNT_PLACEHOLDER

    return to_account


def decide_assets_use_account(transaction):
    for key_account, val_triggers in dic.asset_use_account.items():
        if (match_any_item(
                transaction, val_triggers)):
            if (key_account == "income"):
                to_account = INCOME_ACCOUNT_PLACEHOLDER
            elif (key_account == "assets"):
                to_account = ASSETS_ACCOUNT_PLACEHOLDER
            elif (key_account == "liabilities"):
                to_account == LIABILITIES_ACCOUNT_PLACEHOLDER
            elif (key_account == "expenses"):
                to_account = EXPENSES_ACCOUNT_PLACEHOLDER
            break
        else:
            to_account = ASSETS_ACCOUNT_PLACEHOLDER

    return to_account


def create_close_balance(date, account, price):
    next_day_obj = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
    next_day = next_day_obj.strftime("%Y-%m-%d")
    return next_day + " balance " + account + " " + price


def clean_rbc_transaction(transaction):
    extract_string = "The Royal Trust Company GST Registration Number"
    delete_matches = [
        "Total deposits into your account",
        "Total withdrawals from your account",
        "Your closing balance on",
        "Your opening balance on",
        "Opening Balance",
    ]

    if (match_any_item(transaction, delete_matches)):
        result = False
    elif (found_in_string(extract_string, transaction)):
        if (found_in_string(reg.month_name, transaction)):
            regex = reg.day_digit + reg.one_char + \
                reg.month_name + reg.any_chars + reg.price
        else:
            regex = reg.any_non_digits + reg.price
        result = reg.grab(regex, transaction)
    else:
        result = transaction

    return result
