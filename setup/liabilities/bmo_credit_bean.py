import os
from dotenv import load_dotenv  # pip install python-dotenv
import helpers.regex_helper as reg
from classes.LiabilityBean import LiabilityBean

load_dotenv()


def beanify(detail_mode):
    # define
    account_closed = os.getenv("BMO_CREDIT_CLOSED")
    bean_accounts = os.getenv("BMO_CREDIT_BEAN_ACCOUNTS")
    # Dec. 23, 2022 - Jan. 20, 2023
    regex_period = reg.start_with + reg.whoele_month_day + \
        reg.any_chars + reg.year_digit + reg.any_chars + reg.whoele_month_day + \
        reg.any_chars + reg.year_digit
    # Dec. 25 Dec. 26 PAYMENT RECEIVED - THANK YOU 12-312-3123 10.01
    regex_transaction = reg.start_with + \
        reg.whoele_month_day + reg.any_chars + \
        reg.whoele_month_day + reg.any_chars + reg.price
    # init
    bean = LiabilityBean(
        account_closed,
        bean_accounts,
        regex_period,
        regex_transaction,
    )
    # beanify
    bean.beanify(detail_mode)
