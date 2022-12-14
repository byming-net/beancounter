import os
from dotenv import load_dotenv  # pip install python-dotenv
import helpers.regex_helper as reg
from classes.AssetBean import AssetBean

load_dotenv()


def beanify(detail_mode):
    # define
    account_closed = os.getenv("RBC_CHEQ_SAV_CLOSED")
    bean_accounts = os.getenv("RBC_CHEQ_SAV_BEAN_ACCOUNTS")
    # From  December 26, 2022 to January 25, 2023
    regex_period = reg.has_something_before + reg.month_name + \
        reg.any_chars + reg.to_in_string + reg.any_chars + reg.month_name + reg.any_chars
    # 28 Dec SOMETHING - 1234 10.01 10.01
    regex_transaction = reg.optional_pattern(
        reg.start_with + reg.whole_day_month) + reg.any_chars + reg.price
    # init
    bean = AssetBean(
        account_closed,
        bean_accounts,
        regex_period,
        regex_transaction,
    )
    # beanify
    bean.beanify(detail_mode)
