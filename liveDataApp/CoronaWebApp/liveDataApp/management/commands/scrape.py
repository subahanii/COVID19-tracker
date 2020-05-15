from django.core.management.base import BaseCommand

import requests
from bs4 import BeautifulSoup
import re
from liveDataApp.models import dailyData
import schedule 
import datetime
import time



def filter_integer(x):
    array = re.findall(r'[0-9]+', x)
    return ''.join(array)

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
		print('exception from scrape.py')

class Command(BaseCommand):
	help = "collect jobs"
	def handle(self, *args, **options):
		insert_data_into_table(getData())

		self.stdout.write( 'job complete' )


def scrapeTime():
	insert_data_into_table(getData()) 
	print('job complete1')
	
schedule.every().day.at("05:10").do(scrapeTime)
#schedule.every(1).minutes.do(scrapeTime) 

while True: 
    # Checks whether a scheduled task  
    # is pending to run or not 
    schedule.run_pending() 
    time.sleep(1)



# data = getData()
# print(data)


# insert_data_into_table(data)
