import os
from dotenv import load_dotenv  # pip install python-dotenv
import helpers.regex_helper as reg
from classes.LiabilityBean import LiabilityBean

load_dotenv()


def beanify(detail_mode):
    # define
    account_closed = os.getenv("CIBC_CREDIT_CLOSED")
    bean_accounts = os.getenv("CIBC_CREDIT_BEAN_ACCOUNTS")
    # December 31 to January 1, 2023
    regex_period = reg.start_with + reg.month_name + reg.any_chars + \
        reg.to_in_string + reg.month_name + reg.any_chars + reg.year_digit
    # Dec 31 Jan 01 SOMETHING 10.01 (something spread between two lines)
    regex_transaction = reg.start_with + \
        reg.whoele_month_day + reg.any_chars + \
        reg.whoele_month_day + reg.any_chars
    # init
    bean = LiabilityBean(
        account_closed,
        bean_accounts,
        regex_period,
        regex_transaction,
    )
    # beanify
    bean.beanify(detail_mode)
