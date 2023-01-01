import os
from dotenv import load_dotenv  # pip install python-dotenv
import helpers.regex_helper as reg
from classes.LiabilityBean import LiabilityBean

load_dotenv()


def beanify(detail_mode):
    # define
    account_closed = os.getenv("BRIM_CREDIT_CLOSED")
    bean_accounts = os.getenv("BRIM_CREDIT_BEAN_ACCOUNTS")
    # for Dec 26, 2022 - Jan 25, 2023
    regex_period = reg.start_with + "for" + reg.any_chars + reg.whoele_month_day + \
        reg.any_chars + reg.year_digit + reg.any_chars + reg.whoele_month_day + \
        reg.any_chars + reg.year_digit
    # May 29 May 30 SOMETHING $10.01
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
