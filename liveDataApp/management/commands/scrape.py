from django.core.management.base import BaseCommand

import requests
from bs4 import BeautifulSoup
import re
from liveDataApp.models import dailyData, TestCounter
import schedule 
import datetime
import time



def filter_integer(x):
    array = re.findall(r'[0-9]+', x)
    return ''.join(array)


def getTestData():
	URL = 'https://www.icmr.gov.in/'
	page = requests.get(URL)

	soup = BeautifulSoup(page.content, 'html.parser')
	testData = soup.findAll('span', attrs={'class':'counter'})
	testData = filter_integer(str(testData))
	return testData




def getData():
	URL = 'https://www.mohfw.gov.in/'
	page = requests.get(URL)

	soup = BeautifulSoup(page.content, 'html.parser')
	tableData = soup.findAll('div', attrs={'class':'data-table table-responsive'})
	tableData  = tableData[0].find('tbody')
	dataList=[]
	for i in tableData.findAll('tr'):
	    data=[]
	    for j,vlu in enumerate(i.findAll('td')):
	        if j==1:
	            data.append(vlu.text)
	        elif j>1:
	            data.append(filter_integer(vlu.text))
	    if len(data)>0:
	        dataList.append(data)

	total = ['Total number of confirmed cases in India']

	for vlu in dataList[-1]:    
	    total.append(filter_integer(vlu))
	    
	print(total)
	del dataList[-1]
	#dataList[-1]=total  
	for i in range(len(dataList)):
		
		dataList[i].insert(0, i+1)

	print(dataList)
	return dataList

def insert_data_into_table(data):
	try:

		for i in data:
			print(i)
			update = dailyData(stateName=i[1], confirmedCases=i[2], curedCases=i[3], deathCases=i[4])
			update.save()
	except:
		print('exception from scrape.py insert_data_into_table()')


def insert_testData_into_table(data):
	try:
		update = TestCounter(tests = data)
		update.save()
	except:
		print('exception from scrape.py insert_testData_into_table() ')







class Command(BaseCommand):
	help = "collect jobs"
	def handle(self, *args, **options):
		insert_data_into_table(getData())

		self.stdout.write( 'job complete' )


def scrapeTime():
	insert_data_into_table(getData()) 
	insert_testData_into_table(getTestData()) 
	print('job complete1')
	
#schedule.every().day.at("04:30").do(scrapeTime)
schedule.every(1).minutes.do(scrapeTime) 

while True: 
    # Checks whether a scheduled task  
    # is pending to run or not 
    schedule.run_pending() 
    time.sleep(1)



# data = getData()
# print(data)


# insert_data_into_table(data)