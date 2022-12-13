from datetime import datetime
import re

# 1234-12-12
stmtDatePattern = "%Y-%m-%d"

# 1234-12-12
regexStmtDate = "\d{4}-\d{2}-\d{2}"
# regex
matchWholeMonthDay = "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\b.{0,2}\d{1,2}" # Jan 14 | Jan. 14 | Jan14
matchWholeMonthDayAtStart = "^" + matchWholeMonthDay 
matchSomeChars = ".{10,}"
matchPrice = "(\d{1,3},)?\d{1,3}.?\.\d{2}" # 1,111.11
hasSomethingBefore = "(?<!^)"

def getInputPathFromBeanDef(dirStmts, beanDef):
    return dirStmts + beanDef.replace(":","/") + "/"

def getStmtDateFromString(string):
    date = re.search(regexStmtDate,string).group()
    return(date)

def cleanString(string):
    return re.sub('\.|,', "", string).strip()

def getPostedDateFromTransaction(transaction, regex, endOfYear, startYear):
    # Jul. 18
    match = re.search(regex, transaction, re.IGNORECASE).group().strip()
    year = startYear+1 if "Jan" in match and endOfYear else startYear
    dateString = cleanString(match) + " " + cleanString(year)
    date = datetime.strptime(dateString, "%b %d %Y")
    return date.strftime("%Y-%m-%d")

def getDescriptionFromTransaction(transaction, regex):
    match = re.search(regex, transaction, re.IGNORECASE).group()
    # remove month and day
    match = re.sub(matchWholeMonthDay, "", match)
    # remove price
    match = re.sub(matchPrice, "", match)
    return match.strip()

def getPriceFromTransaction(transaction, regex):
    match =  re.search(regex, transaction, re.IGNORECASE).group().strip()
    return match + " CAD"
    

    

