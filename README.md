# beancounter

Scripts for [beancount](https://beancount.github.io/docs/index.html) automation

## This repo has scripts for

- [Renaming](#rename) downloaded PDF statements into `YYYY-MM-DD.<a name you want>.pdf`
- [Read](#read) transactions from PDF statement and write them into corresponding `YYYY-MM.bean` file

### it currently handles statement from

- [x] BMO Canada Credit Card
  - [Rename](./rename-bmo-credit-stmt.py)
  - [Read](./beanify-bmo-credit-stmt.py)

## To use

- Prerequisites

  - Have python installed on your local (you probably have it if you have beancount)
  - Install the package you need:

    ```bash
    # You would need this for all scripts
    pip install python-dotenv

    # You would need this for Read scripts
    pip install PyPDF2
    ```

- Clone this repo
- Change `.envexample` to `.env` and [configure](#configurable) data base on your use case
- `cd` into the repo and run the script with `python3 <script of your choice>`

## Configurable

```bash
# For RENAME scripts
DIR_DOWNLOAD="/home/user/Downloads/" # Folder where download files go
## Sub folders inside DIR_DOWNLOAD
DIR_DOWNLOAD_BMO_CREDIT="bmoCredit/"
## The <name> in "YYYY-MM-DD.<name>.pdf" when renaming
RENAME_BMO_CREDIT_TO="bmo-credit-cashback"
# For READ scripts
DIR_STMTS="/home/user/beancount/beans/stmts/" # Folder where you store your statements
DIR_OUTPUT="/home/user/beancount/check/bmoCredit/" # Folder where you want to store your output files
## beancount accounts
### bmo credit
BMO_CREDIT_BEAN_ACCOUNT="Liabilities:CreditCard:BMOCashBack"
BMO_EXPENSE_PLACEHOLDER="Expenses:TBD"
BMO_ASSET_PLACEHOLDER="Assets:TBD"
BMO_CREDIT_CLOSED=False # if your account is closed in beancount
```

## What the script does

### Rename

- Look for PDF files in the download path (e.g. `DIR_DOWNLOAD+DIR_DOWNLOAD_BMO_CREDIT`)
- Rename them into `YYYY-MM-DD.<name>.pdf` (e.g. `YYYY-MM-DD.<DIR_DOWNLOAD_BMO_CREDIT>.pdf`)

### Read

- Prompt reminder in terminal if
  - the account is open (e.g. `BMO_CREDIT_CLOSED=Flase`) AND
  - the latest statement in your statement folder (`DIR_STMTS`) is >28 days before today
- Read transactions and write them into corresponding `YYYY-MM.bean` file in the format of
  - `YYYY-MM-DD * "<description>"<tab><beancount liability account> -X,XXX.XX CAD<tab><bean expense account placeholder>` for credit
  - `YYYY-MM-DD * "<description>"<tab><beancount liability account> +X,XXX.XX CAD<tab><bean asset account placeholder>` for credit payment
- Option to show more details in terminal (set `detailedMode` to `True` in the beanify `.py` file). It will print out
  - `transaction`: the transaction line from PDF
  - `date`: the posted date of a transaction converted into `YYYY-MM-DD` format
  - `description`: text between `date` and `price` (e.g. DEC 11 `the string here` 1.00 CAD)
  - `price`: amount
