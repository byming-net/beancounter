import os
import glob
from dotenv import load_dotenv  # pip install python-dotenv
import helpers.helper_function as func
# liabilities
import setup.liabilities.bmo_credit_bean as bmo_credit_bean
import setup.liabilities.rbc_credit_bean as rbc_credit_bean
import setup.liabilities.brim_credit_bean as brim_credit_bean
import setup.liabilities.cibc_credit_bean as cibc_credit_bean
import setup.liabilities.td_credit_bean as td_credit_bean
# assets
import setup.assets.eq_hybrid_bean as eq_hybrid_bean
import setup.assets.rbc_cheq_sav_bean as rbc_cheq_sav_bean
import setup.assets.tangerine_cheq_sav_bean as tangerine_cheq_sav_bean

load_dotenv()

# config
DIR_OUTPUT = accountClosed = os.getenv("DIR_OUTPUT")
detail_mode = False
beanify_liability = True
beanify_assets = True

# liabilities
beanify_bmo_credit = beanify_liability
bmo_detail_mode = detail_mode

beanify_rbc_credit = beanify_liability
rbc_credit_detail_mode = detail_mode

beanify_brim_credit = beanify_liability
brim_credit_detail_mode = detail_mode

beanify_cibc_credit = beanify_liability
cibc_detail_mode = detail_mode

beanify_td_credit = beanify_liability
td_credit_detail_mode = detail_mode

# assets
beanify_eq_hybrid = beanify_assets
eq_hybrid_detail_model = detail_mode

beanify_rbc_cheq_sav = beanify_assets
rbc_cheq_sav_detail_mode = detail_mode

beanify_tangerine_cheq_sav = beanify_assets
tangerine_cheq_sav_detail_mode = detail_mode

# create output folder if not exists
if not os.path.exists(DIR_OUTPUT):
    print("🏗️Creating your output folder...")
    os.makedirs(DIR_OUTPUT)

# clear check folders
print("🧽 Clearing files in output folder....", end=" ")
all_output_files = glob.glob(DIR_OUTPUT + "*")
files_cleared = 0
for file in all_output_files:
    files_cleared += 1
    os.remove(file)
print("cleared " + str(files_cleared) + " files")

# execution
if (beanify_bmo_credit):
    bmo_credit_bean.beanify(bmo_detail_mode)

if (beanify_rbc_credit):
    rbc_credit_bean.beanify(rbc_credit_detail_mode)

if (beanify_brim_credit):
    brim_credit_bean.beanify(brim_credit_detail_mode)

if (beanify_cibc_credit):
    cibc_credit_bean.beanify(cibc_detail_mode)

if (beanify_td_credit):
    td_credit_bean.beanify(td_credit_detail_mode)

if (beanify_eq_hybrid):
    eq_hybrid_bean.beanify(eq_hybrid_detail_model)

if (beanify_rbc_cheq_sav):
    rbc_cheq_sav_bean.beanify(rbc_cheq_sav_detail_mode)

if (beanify_tangerine_cheq_sav):
    tangerine_cheq_sav_bean.beanify(tangerine_cheq_sav_detail_mode)

# sort files content
all_output_files = glob.glob(DIR_OUTPUT + "*")
files_sorted = 0
for file in all_output_files:
    lines = []
    with open(file, "r") as unsorted_file:
        for line in unsorted_file:
            stripped = line.strip("\n")
            lines.append(stripped)

    lines.sort()
    with open(file, "w") as sorted_file:
        for line in lines:
            sorted_file.write(line + "\n")

    files_sorted += 1
print("sorted " + str(files_sorted) + " files")
