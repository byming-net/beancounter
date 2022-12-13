import os
import re
from dotenv import load_dotenv # pip install python-dotenv
from helperFunction import isFileNamePDF


load_dotenv()

dirDownLoad = os.getenv("DIR_DOWNLOAD")+os.getenv("DIR_DOWNLOAD_BMO_CREDIT")
renameTo=os.getenv("RENAME_BMO_CREDIT_TO")

noFiles=True

print("Renaming files in " + dirDownLoad)

for file in os.listdir(os.fsencode(dirDownLoad)):
    isPdf = isFileNamePDF(os.fsdecode(file))
    if(isPdf):
        # old: eStatement_2022-04-20.pdf
        # new: 2022-07-01.bmo-credit-cashback.pdf
        fileDate = fileName.split("_")[1]
        fileDate = fileDate.split(".")[0]
        beanName = fileDate +"."+ renameTo + ".pdf"
        os.rename(fileName,beanName)
        print("Renamed " + fileName + " to " + beanName)
        noFiles=False

if(noFiles):
    print("No PDF files to rename")