# beancounter

- Scripts I use for [beancount](https://beancount.github.io/docs/index.html) automation
- [Read](#Read) transactions from PDF statement and write them to corresponding `.bean` file

## Read

- Prompt reminder in terminal if the account is open and the latest statement is >28 days before today
- Read transactions and write them to `YYYY-MM.bean` file in the format of
  - `YYYY-MM-DD * "<description>"<tab><beancount liability account> -X,XXX.XX CAD<tab><bean expense account placeholder>` for credit
  - `YYYY-MM-DD * "<description>"<tab><beancount liability account> +X,XXX.XX CAD<tab><bean asset account placeholder>` for credit payment
- Option to turn on detailedMode for more detail (set `detailedMode` to `True` in the `.py` file)
  - print the transaction, date, description, price it reads

## Cover

- [x] [BMO credit statement](https://github.com/byming-net/beancounter/blob/main/beanify-bmo-credit-stmt.py)
  - Note: `<description>` is the text between transaction posted date and amount (e.g. DEC 11 `the string here` 1.00 CAD)

## To use

- Clone this repo, install python on your local machine (you probably have it if you have beancount)
- Change `.envexample` to `.env` and configure data base on your use case
- Run the script. You should find `YYYY-MM.bean` files in the output folder you specified
