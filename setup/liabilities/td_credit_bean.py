import os
from dotenv import load_dotenv  # pip install python-dotenv
import helpers.regex_helper as reg
from classes.LiabilityBean import LiabilityBean

load_dotenv()


def beanify(detail_mode):
    # define
    account_closed = os.getenv("TD_CREDIT_CLOSED")
    bean_accounts = os.getenv("TD_CREDIT_BEAN_ACCOUNTS")
    # STATEMENT PERIOD: December 31,2022toJanuary01,2023
    regex_period = reg.has_something_before + reg.month_name + reg.any_chars + \
        reg.year_digit + reg.any_chars + reg.month_name + reg.any_chars + reg.year_digit
    # DEC25 DEC26 $10.01 BLABLABLA
    regex_transaction = reg.start_with + \
        reg.month_name + reg.any_chars + \
        reg.month_name + reg.any_chars + reg.price
    # init
    bean = LiabilityBean(
        account_closed,
        bean_accounts,
        regex_period,
        regex_transaction,
    )
    # beanify
    bean.beanify(detail_mode)
