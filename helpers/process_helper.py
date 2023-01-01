from datetime import datetime


def check_doc_status(account_closed, latest_doc_date):
    if (account_closed):
        print("💁 This account is closed")
    else:
        day_difference = (datetime.today() -
                          datetime.strptime(latest_doc_date, "%Y-%m")).days
        if day_difference > 28:
            pause = input(
                "🙋 Your latest file has a date with >28 days of difference from today. Stop and go collect files? (y/n)")
            if (pause == "y"):
                exit(0)
            else:
                ("💁 The latest file is " + str(day_difference) + " days from today")
        else:
            ("💁 The latest file is " + day_difference + " days from today")


def print_starting_asset_bean():
    print()
    print("===== Asset Bean ====")


def print_starting_liability_bean():
    print()
    print("===== Liability Bean ====")


def print_account_in_process(account):
    print()
    print("📁 Account in process: " + account)


def print_transactions_in_file(file, transactions):
    print()
    print("📖 Read " + str(transactions) + " transaction(s) in " + file)


def print_files_read(files):
    print()
    print("📚 Read files: " + str(files))


def print_items_in_detail_mode(detail_mode, itemsObj):
    if (detail_mode):
        print()
        for key, val in itemsObj.items():
            print("--" + key + ": " + val)
