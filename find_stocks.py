import requests
import xlsxwriter
from bs4 import BeautifulSoup
from string import ascii_uppercase

train_data = []
result_data = []
symbols = []
def get_chart(symbol):
    chart_url = 'http://charting.nasdaq.com/ext/charts.dll?2-1-14-0-0-512-03NA000000'+ symbol + '-&SF:1|5-BG=FFFFFF-BT=0-WD=635-HT=395--XTBL-'
    try:
        chart_page = requests.get(chart_url)
        get_chart = BeautifulSoup(chart_page.content, 'html.parser')
        chart_page.close()
        c = 0
        first = 0
        train = []
        for data in get_chart.findAll("table", {"class":"DrillDown"})[0].findAll("tr"):
            try:
                num = float(data.findAll("td")[1].get_text())
                # if (c == 1): first = num
                # elif (c == 100): change = (first - num) / num
                # elif (c > 100 and c <= 200): 
                if (c < 200):
                    train.append(num)
                c += 1
            except:
                continue
        if (len(train) == 200):
            train_data.append(train)
            symbols.append(symbol)
            print(symbol)
    except:
        None

def find_stocks():
    for char in ascii_uppercase:
        print(char)
        stock_url = 'http://www.advfn.com/nasdaq/nasdaq.asp?companies=' + char
        try:
            find_page = requests.get(stock_url)
            get_stocks = BeautifulSoup(find_page.content, 'html.parser')
            find_page.close()
            for symbol in get_stocks.findAll("table", {"class":"market tab1"})[0].findAll('tr'):
                try:
                    get_chart(symbol.findAll('td')[1].a.get_text())
                except:
                    continue
        except:
            continue

find_stocks()

workbook = xlsxwriter.Workbook('stock_data.xlsx')
worksheet = workbook.add_worksheet()
for row in range(len(train_data)):
    worksheet.write(row, 0, symbols[row])
    # worksheet.write(row, 1, result_data[row])
    for col in range(len(train_data[row])):
        worksheet.write(row, col + 1, train_data[row][col])

workbook.close()



