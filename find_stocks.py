import requests
import xlsxwriter
from bs4 import BeautifulSoup
from string import ascii_uppercase

train_data = []
volume_data = []
date_data =[]

symbols = []
def get_chart(symbol):
	chart_url = 'http://charting.nasdaq.com/ext/charts.dll?2-1-14-0-0-512-03NA000000'+ symbol + '-&SF:1|5-BG=FFFFFF-BT=0-WD=635-HT=395--XTBL-'
	try:
		chart_page = requests.get(chart_url)
		get_chart = BeautifulSoup(chart_page.content, 'html.parser')
		chart_page.close()
		c = 0
		first = 0
		dates =[]
		train = []
		volumes = []
		for data in get_chart.findAll("table", {"class":"DrillDown"})[0].findAll("tr"):
			try:
				date = str(data.findAll("td")[0].get_text())
				num = float(data.findAll("td")[1].get_text())
				volume = float(data.findAll("td")[2].get_text().replace(',', ''))
				if (c < 200):
					dates.append(date)
					train.append(num)
					volumes.append(volume)
				c += 1
			except:
				continue
		if (len(train) == 200):
			train_data.append(train)
			volume_data.append(volumes)
			date_data.append(dates)
			symbols.append(symbol)
	except:
		None

def find_stocks():
	for char in ascii_uppercase:
		stock_url = 'http://www.advfn.com/nasdaq/nasdaq.asp?companies=' + char
		try:
			find_page = requests.get(stock_url)
			get_stocks = BeautifulSoup(find_page.content, 'html.parser')
			find_page.close()
			for symbol in get_stocks.findAll("table", {"class":"market tab1"})[0].findAll('tr'):
				try:
					get_chart(symbol.findAll('td')[1].a.get_text())
					print(symbol.findAll('td')[1].a.get_text())
				except:
					continue
		except:
			continue

find_stocks()

workbook = xlsxwriter.Workbook('stock_data_1.xlsx')
worksheet = workbook.add_worksheet()
for row in range(0, 3 * len(train_data), 3):
	worksheet.write(row, 0, symbols[int(row / 3)] + '_date')
	worksheet.write(row + 1, 0, symbols[int(row / 3)] + '_price')
	worksheet.write(row + 2, 0, symbols[int(row / 3)] + '_volume')
	for col in range(len(train_data[int(row / 3)])):
		worksheet.write(row, col + 1, date_data[int(row / 3)][col])
		worksheet.write(row + 1, col + 1, train_data[int(row / 3)][col])
		worksheet.write(row + 2, col + 1, volume_data[int(row / 3)][col])

workbook.close()



