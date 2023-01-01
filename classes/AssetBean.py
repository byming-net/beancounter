import os
from dotenv import load_dotenv  # pip install python-dotenv
from PyPDF2 import PdfReader  # pip install PyPDF2
import helpers.helper_function as func
import helpers.process_helper as proc
import helpers.regex_helper as reg
import dictionary as dic

load_dotenv()


class AssetBean:
    def __init__(
        self,
        account_closed,
        bean_accounts,
        regex_period,
        regex_transaction,
    ):
        self.account_closed = (account_closed.lower() == 'true')
        self.bean_accounts = bean_accounts
        self.regex_period = regex_period
        self.regex_transaction = regex_transaction

    def beanify(self, detail_mode):
        proc.print_starting_asset_bean()

        accounts = self.bean_accounts.split(",")
        for (index, account) in enumerate(accounts):
            proc.print_account_in_process(account)
            stmt_folder_path = func.get_path_from_bean_def(account)

            # check documents are up to date
            latest_doc_date = func.get_latest_date_in_folder(stmt_folder_path)
            proc.check_doc_status(self.account_closed, latest_doc_date)

            # extract records from stmts
            files_read = 0
            for file in os.listdir(stmt_folder_path):
                files_read += 1

                stmt_period_collected = ""
                transactions_collected = []

                file_path = stmt_folder_path + os.fsdecode(file)
                pdf_file_obj = open(file_path, 'rb')
                pdf_reader = PdfReader(pdf_file_obj)

                # collect transactions
                for page_index in range(pdf_reader.numPages):
                    page_obj = pdf_reader.getPage(page_index)
                    lines = page_obj.extractText().split("\n")

                    for line_index in range(len(lines)):
                        current_line = lines[line_index]

                        if (reg.match(self.regex_period, current_line)):
                            stmt_period_collected = reg.grab(
                                self.regex_period, current_line)

                        if (reg.match(self.regex_transaction, current_line)):
                            transaction = reg.grab(
                                self.regex_transaction, current_line)

                            # if transaction is spread between two lines
                            last_line = lines[line_index-1]
                            if (not reg.match(reg.month_name, transaction) and reg.match(reg.month_name, last_line)):
                                transaction = last_line + \
                                    reg.grab(self.regex_transaction,
                                             current_line)

                            if (func.found_in_string("rbc", account)):
                                transaction = func.clean_rbc_transaction(
                                    transaction)

                            if (transaction):
                                transactions_collected.append(transaction)

                # write transactions to output file
                end_period = func.get_end_period(stmt_period_collected)

                proc.print_items_in_detail_mode(
                    detail_mode, {"end period": end_period})

                posted_dates_collected = []
                balance_collected = []

                for transaction in transactions_collected:
                    # description
                    description = func.get_description(transaction)

                    # date
                    if (not reg.match(reg.whoele_month_day, transaction)
                            and not reg.match(reg.whole_day_month, transaction)):
                        posted_date = posted_dates_collected[len(
                            posted_dates_collected)-1]
                    else:
                        posted_date = func.get_posted_date(
                            transaction, end_period)
                        posted_dates_collected.append(posted_date)

                    # price
                    price = func.get_price(transaction)

                    # flow
                    balance = func.get_balance(transaction)

                    if (balance and len(balance_collected) == 0):
                        flow = func.look_up_flow(
                            transaction, dic.asset_cash_flow)
                        last_record_has_balance = True
                        balance_collected.append(balance)
                    elif (balance):
                        balance_difference = float(
                            balance) - float(balance_collected[len(
                                balance_collected)-1])

                        if (last_record_has_balance):
                            flow = "+" if balance_difference > 0 else "-"
                        else:
                            flow = "b+" if balance_difference > 0 else "b-"

                        last_record_has_balance = True
                        balance_collected.append(balance)
                    else:
                        flow = func.look_up_flow(
                            transaction, dic.asset_cash_flow)
                        last_record_has_balance = False

                    # write
                    output_file = func.get_output_file_from_date(
                        posted_date)

                    if (func.found_in_string("closing balance", transaction)):
                        output_line = func.create_close_balance(
                            posted_date, account, price)
                    else:
                        to_account = func.decide_assets_use_account(
                            transaction)

                        output_line = posted_date + ' * "' + description + '"\t' + \
                            account + " " + flow + price + "\t" + to_account

                    output_file.write(output_line + "\n")

                    proc.print_items_in_detail_mode(detail_mode, {
                                                    "transaction": transaction,
                                                    "description": description,
                                                    "date": posted_date,
                                                    "price": price,
                                                    "flow": flow,
                                                    "balance": str(balance),
                                                    "output": output_line})

                proc.print_transactions_in_file(
                    file, len(transactions_collected))

            proc.print_files_read(files_read)

            # close pdf and output file
            pdf_file_obj.close()
            output_file.close()
