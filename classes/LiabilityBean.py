import os
from dotenv import load_dotenv  # pip install python-dotenv
from PyPDF2 import PdfReader  # pip install PyPDF2
import helpers.helper_function as func
import helpers.process_helper as proc
import helpers.regex_helper as reg
import dictionary as dic


class LiabilityBean:
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
        proc.print_starting_liability_bean()

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
                transaction_read = 0

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
                            end_period = func.get_end_period(
                                reg.grab(
                                    self.regex_period, current_line))

                            proc.print_items_in_detail_mode(detail_mode, {
                                "end period": end_period})

                        if (reg.match(self.regex_transaction, current_line)):
                            transaction_read += 1

                            transaction = reg.grab(
                                self.regex_transaction, current_line)

                            # description
                            description = func.get_description(transaction)

                            # date
                            posted_date = func.get_posted_date(
                                transaction, end_period)

                            # price (rbc price could be next/next next line)
                            price = func.get_price(
                                transaction, lines=lines, index=line_index)

                            # flow
                            flow = func.look_up_flow(
                                transaction, dic.liability_cash_flow_in)
                            if (flow == "?"):
                                flow = "-"

                            # write
                            output_file = func.get_output_file_from_date(
                                posted_date)

                            to_account = func.decide_liability_use_account(
                                flow)

                            output_line = posted_date + ' * "' + description + '"\t' + \
                                account + " " + flow + price + "\t" + to_account

                            output_file.write(output_line + "\n")

                            proc.print_items_in_detail_mode(detail_mode, {
                                "transaction": transaction,
                                "description": description,
                                "date": posted_date,
                                "price": price,
                                "flow": flow,
                                "output": output_line})

                            output_file.close()

                # close pdf and output file
                pdf_file_obj.close()
                proc.print_transactions_in_file(
                    file, transaction_read)

            proc.print_files_read(files_read)
