import os
from dotenv import load_dotenv  # pip install python-dotenv
import helpers.regex_helper as reg
from classes.LiabilityBean import LiabilityBean


load_dotenv()


def beanify(detail_mode):
    # define
    bean_accounts = os.getenv("RBC_CREDIT_BEAN_ACCOUNTS")
    account_closed = os.getenv("RBC_CREDIT_CLOSED")
    # STATEMENT FROM DEC 08 TO JAN 24, 2023
    regex_period = reg.start_with + "STATEMENT.?FROM.?" + reg.whoele_month_day + \
        reg.any_chars + reg.to_in_string + reg.any_chars + \
        reg.whoele_month_day + reg.any_chars
    # DEC 25 DEC 26 PAYMENT - THANK YOU / PAIEMENT - MERCI
    regex_transaction = reg.start_with + reg.whoele_month_day + reg.any_chars
    # init
    bean = LiabilityBean(
        account_closed,
        bean_accounts,
        regex_period,
        regex_transaction,
    )
    # beanify
    bean.beanify(detail_mode)
