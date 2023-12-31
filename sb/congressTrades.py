#congressTrades.py
#By: Sam Schmitz
#finds the stocks traded by members of The US Congress

from datetime import datetime
from datetime import date
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary
from time import sleep
import requests
from bs4 import BeautifulSoup

HEADER = {'Connection': 'keep-alive',
            'Expires': '-1',
            'Upgrade_Insecure-Requests' : '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
            }

def getTrades(date, member=None):
    """Go to capitaltrades.com/trades and find all trades recorded after a certain date
    inclusive for date (date tracked at timezone 0)
    date = (YYYY-MM-DD) or Unix date
    returns [tick, (buy or sell), dateBought] within a list (1 list for each stock found)
    """
    stockData = []
    stop = False
    pageNum = 0
    mem = None
    if member is not None:
        mem = getMemberCode(member)
    while stop != True:
        pageNum += 1
        stop, data = _getPageInfo2(date, pageNum, member=mem)
        stockData += data
    return stockData


def _getPageInfo2(dateStop, pageNum, member=None):
    """Gets the trades from a page on capitaltrades.com using selenium
    dateStop = the date to stop expressed as a unix date
    pageNum = an int that tells the page to search
    returns a list of [tick, saleType(buy or sell), datebought, dateDis] for each stock found
    """
    driver = webdriver.Chrome()
    if member != None:
        driver.get(f"https://www.capitoltrades.com/trades?page={str(pageNum)}&pageSize=50&politician={member}")
    else:
        driver.get(f"https://www.capitoltrades.com/trades?page={str(pageNum)}&pageSize=50")
    sleep(2)
    #p_element = driver.find_element(By.CLASS_NAME, "q-pagination")
    #print(p_element.text)
    pageInfo = []
    stop = False
    for i in range(1, 51):
        #checkdate
        dateDis = driver.find_element(By.XPATH, f"//div[@class='trade-table-scroll-wrapper']/table/tbody/tr[{i}]/td[3]").text.replace("\n", " ")
        dateDis = abrev_to_unix(dateDis)
        if dateDis < dateStop:
            stop = True
            break
        tick = driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[2]").text.replace(":US", "").split("\n")    #the tick is formated as [full tick name, TICK]
        saleType = driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[7]").text
        dateBought = driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[4]").text.replace("\n", " ")
        dateBought = abrev_to_unix(dateBought)
        member = driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[1]").text.split("\n")
        pageInfo.append([tick[1], saleType, dateBought, dateDis, member[0]])
        #print("row data:", tick[1], saleType, dateBought, dateDis, member)
    return stop, pageInfo

def _checkDate2(dateDis, dateStop):
    try:
        dateRecord = abrev_to_unix(dateDis)
    except:
        if dateDis.find('yesterday') == 0:
            dateR = date.today() - timedelta(days=1)
        else:
            dateR = date.today()
        dateRecord = datetime(dateR.year, dateR.month, dateR.day)
    return dateRecord < dateStop

def abrev_to_unix(abrev):
    """turns the abreviated version of a date(ex:2022 13 Oct) into a datetime form
    """
    try:
        try:
            return datetime.strptime(abrev[:11], '%Y %d %b')
        except:
            return datetime.strptime(abrev[:10], '%Y %d %b')
    except:
        if abrev.find('yesterday') == 0:
            dateR = date.today() - timedelta(days=1)
        else:
            dateR = date.today()
        return datetime(dateR.year, dateR.month, dateR.day)

def getMemberCode(member):
    """return a congress members code for capitaltrades
    example member: Doe, John
    """
    driver = webdriver.Chrome()
    driver.get("https://www.congress.gov/help/field-values/member-bioguide-ids")
    tbody = driver.find_element(By.XPATH, "//table[@class='std full']/tbody")
    tb = tbody.text.split("\n")
    for tr in tb:
        if member in tr:
            return tr[-7:]


if __name__ == "__main__":
    #d = date.today()-timedelta(days=3)
    #print(getTrades(datetime(d.year, d.month, d.day)))
    #print(getMemberCode("Abdnor, James"))
    print(getTrades(datetime(2023, 1, 1), member="Blumenauer, Earl"))
