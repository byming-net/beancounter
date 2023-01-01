
import os
from dotenv import load_dotenv  # pip install python-dotenv
import helpers.regex_helper as reg
from classes.AssetBean import AssetBean

load_dotenv()


def beanify(detail_mode):
    # define
    account_closed = os.getenv("EQ_HYBRID_CLOSED")
    bean_accounts = os.getenv("EQ_HYBRID_BEAN_ACCOUNTS")
    # John Doe Account #123123123  December 26, 2022 to January 25, 2023
    regex_period = reg.has_something_before + reg.month_name + \
        reg.any_chars + reg.to_in_string + reg.any_chars + reg.month_name + reg.any_chars
    # Dec 25 Direct deposit from SOMEWHERE $10.01 $10.01
    regex_transaction = reg.start_with + \
        reg.whoele_month_day + reg.any_chars + reg.price
    # init
    bean = AssetBean(
        account_closed,
        bean_accounts,
        regex_period,
        regex_transaction,
    )
    # beanify
    bean.beanify(detail_mode)
