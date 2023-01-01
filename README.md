# beancounter

Scripts for [beancount](https://beancount.github.io/docs/index.html) automation

## What it does

- Read transactions from PDF statement
- Write them as beancount entry into corresponding `YYYY-MM.bean` file (sorted)

### Covers

- Liabilities
  - [x] BMO Canada Credit Card
  - [x] TD Canada Credit Card
  - [x] RBC Canada Credit Card
  - [x] CIBC Canada Credit Card
  - [x] BRIM Canada Credit Card
- Assets
  - [x] EQ Canada Hybrid Account
  - [x] RBC Canada Chequing and Savings Account
  - [x] Tangerine Canada Chequing and Savings Account

## To use

- Prerequisites

  - Have python installed on your local (you probably have it if you have beancount)
  - Install the package if haven't already:

    ```bash
    # You would need this for all scripts
    pip install python-dotenv

    # You would need this for Read scripts
    pip install PyPDF2
    ```

- Clone this repo
- Change `.envexample` to `.env` and `dictionary_example.py` to `dictionary.py`
- [Configure](#configurable) the data base on your use case
- `cd` into the repo and run the script with `python3 beanify.py`

### Configurable

- `.env`: you can define your set up here

  ```bash
  # folder where you store your statements
  DIR_STMTS="/home/user/beancount/beans/stmts/"
  # folder where you want your output be
  DIR_OUTPUT="/home/user/beancount/check/"
  # placeholder
  ASSETS_ACCOUNT_PLACEHOLDER="Assets:TBD"
  EXPENSES_ACCOUNT_PLACEHOLDER="Expenses:TBD"
  LIABILITIES_ACCOUNT_PLACEHOLDER="Liabilities:TBD"
  INCOME_ACCOUNT_PLACEHOLDER="INCOME:TBD"

  # beancount accounts
  ## bmo credit - support multiple accounts (joined by comma)
  BMO_CREDIT_BEAN_ACCOUNTS="Liabilities:CreditCard:BMOCashBack,Liabilities:CreditCard:BMOReward"
  BMO_CREDIT_CLOSED=False # if your account is closed in beancount
  ...
  ```

- `dictionary.py`: you can edit the trigger words that define which placeholder account to use, cash flow sign, etc
- `beanify.py`: you can toggle which account to read, `detail_mode` to show more info when running the script
