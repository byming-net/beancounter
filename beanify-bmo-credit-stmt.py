import os
import re
import glob
from datetime import datetime
from PyPDF2 import PdfReader  # pip install PyPDF2
from dotenv import load_dotenv # pip install python-dotenv
import helperFunction as helperFunction

load_dotenv()

# config
detailedMode = False
dirStmts = os.getenv("DIR_STMTS")
dirOutput = os.getenv("DIR_OUTPUT")
accountClosed = os.getenv("BMO_CREDIT_CLOSED")
beanLiabilityAccount = os.getenv("BMO_CREDIT_BEAN_ACCOUNT")
beanExpenseAccount = os.getenv("BMO_EXPENSE_PLACEHOLDER")

# regex
regexTransaction = helperFunction.matchWholeMonthDayAtStart + helperFunction.matchSomeChars + helperFunction.matchPrice
regexPeriod = helperFunction.matchWholeMonthDayAtStart + ".{0,2}\d{4}.*" + helperFunction.matchWholeMonthDay + ".{0,2}\d{4}"
regexPostedDate = helperFunction.hasSomethingBefore + helperFunction.matchWholeMonthDay
regexDescription = helperFunction.hasSomethingBefore + helperFunction.matchWholeMonthDay + ".*" + helperFunction.matchPrice
regexPrice = helperFunction.matchPrice

# Start!
today = datetime.today()
print("🌞Today: " + str(today.strftime('%Y-%m-%d')))
print("📁Account in process: " + beanLiabilityAccount)

# Check documents are up to date
stmtFolder = helperFunction.getInputPathFromBeanDef(dirStmts, beanLiabilityAccount)
stmtFiles = glob.glob(stmtFolder+'*')
latestFile = sorted(stmtFiles, key=helperFunction.getStmtDateFromString, reverse=True)[0]
latestDocDate = helperFunction.getStmtDateFromString(latestFile)

if not accountClosed:
    dayDifference = (today - datetime.strptime(latestDocDate, "%Y-%m-%d")).days
    if dayDifference > 28:
        pause = input ("🙋 Your latest file has a date with >28 days of difference from today. Stop and go collect files? (y/n)")
        if (pause != "y"):
            exit(0)

# Clear output folder
print("🧽Clearing files in checks folder...")
outputFiles = glob.glob(dirOutput+"*")
for file in outputFiles:
    os.remove(file)

# Extract records from stmts
for file in os.listdir(os.fsencode(stmtFolder)):
    # prepare path
    fileName = os.fsdecode(file)
    filePath = stmtFolder + fileName

    # prepare pdf reader
    pdfFileObj = open(filePath, 'rb')
    pdfReader = PdfReader(pdfFileObj)
    
    # loop through pages
    for pageIndex in range(pdfReader.numPages):
        # create page object
        pageObj = pdfReader.getPage(pageIndex)

        # extracting text and split by line
        lines = pageObj.extractText().split("\n")

        # loop through lines
        for lineIndex in range(len(lines)):
            currentLine = lines[lineIndex]

            # look for transaction
            if(re.search(regexPeriod, currentLine, re.IGNORECASE)):
                periodStartYear = currentLine.split("-")[0].strip()[-4:]
                periodEnd = currentLine.split("-")[1].strip()
                endOfYear = True if "Dec" in periodEnd else False

            isTransaction = re.search(regexTransaction, currentLine, re.IGNORECASE)
            if(isTransaction):
                transaction = isTransaction.group()
                if detailedMode: print (transaction)
                postedDate = helperFunction.getPostedDateFromTransaction(transaction, regexPostedDate, endOfYear, periodStartYear)
                if detailedMode: print("date: " + postedDate)
                description = helperFunction.getDescriptionFromTransaction(transaction, regexDescription)
                if detailedMode: print("description: " + description)
                price = helperFunction.getPriceFromTransaction(transaction, regexPrice)
                if detailedMode: print("price: " + price)

                # write
                outputFileName = dirOutput + postedDate[0:7] + ".bean"

                if (os.path.exists(outputFileName)):
                    outputFile = open(outputFileName, "a") # append to it
                else:
                    outputFile = open(outputFileName, "x") # create one

                outputLine = postedDate + ' * "' + description + '"\t'+ beanLiabilityAccount + " " + price + "\t" + beanExpenseAccount  + "\n"
                outputFile.write(outputLine)
                if detailedMode: print(outputLine)
                if detailedMode: print()

    print("👌Read: " + fileName)

#close pdf and output file
pdfFileObj.close()
outputFile.close()

