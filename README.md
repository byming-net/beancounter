# beancounter
- Scripts for [beancount](https://beancount.github.io/docs/index.html)
- [Read](#Read) transaction from PDF statement and write them to corresponding `.bean` file

# Read
- [X] [BMO credit statement](https://github.com/byming-net/beancounter/blob/main/beanify-bmo-credit-stmt.py)
  - Read transactions and write them in the format of `YYYY-MM-DD * "<description>"<tab><beancount account name> +X,XXX.XX CAD` to `YYYY-MM.bean` file
    - Note: `<description>` is the text between transaction posted date and amount (e.g. DEC 11 `the string here` 1.00 CAD)
  - To use: 
    - Change `.envexample` to `.env` and configure data base on use case
    - Optional: In the `.py` file, set `detailedMode` to `True` for more details in your terminal
    - Run the script. You should find `YYYY-MM.bean` files in the output folder you specified
