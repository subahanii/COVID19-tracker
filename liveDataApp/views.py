from django.shortcuts import render

import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict as dfd
from .models import *
from datetime import date
from datetime import timedelta
from django.db.models import Sum
from django.db.models import Count
from django.db.models.functions import ExtractDay,ExtractMonth,ExtractYear

today = date.today()
yesterday = today - timedelta(days = 1) 

colorList = {
				1:"#FF0000",
				2:"#FF4040",
				3:"#FF4040",
				4:"#FF4040",
				5:"#FF7474",
				6:"#FF7474",
				7:"#FF7474",
				8:"#FF7474",
				9:"#FF7474",
				10:"#FF7474",
				11:"#FF7474",
				12:"#FF7474",
				13:"#FF8787",
				14:"#FF8787",
				15:"#FF8787",
				16:"#FF8787",
				17:"#FF8787",
				18:"#FF8787",
				19:"#FF8787",
				20:"#FFB3B3",
				21:"#FFB3B3",
				22:"#FFB3B3",
				23:"#FFB3B3",
				24:"#FFB3B3",
				25:"#FFB3B3",
				26:"#FFECEC",
				27:"#FFECEC",
				28:"#FFECEC",
				29:"#FFECEC",
				30:"#FFE0E0",
				31:"#FFE0E0",
				32:"#FFE0E0",
				33:"#FFE0E0",
				34:"#FFE0E0",
				35:"#FFE0E0",
				
				



				}


stateCode = {
	'Andaman and Nicobar Islands': "AN" ,
	'Andhra Pradesh': "AP",
	'Arunachal Pradesh': "AR",
	'Assam': "AS" ,
	'Bihar':"BR" ,
	'Chandigarh':"CT" ,
	'Chhattisgarh': "CH",
	'Delhi':"DL" ,
	'Dadara & Nagar Havelli': "DN",
	'Goa':"GA" ,
	'Gujarat': "GJ",
	'Haryana': "HR",
	'Himachal Pradesh': "HP",
	'Jammu and Kashmir': "JK" ,
	'Jharkhand': "JH",
	'Karnataka': "KA",
	'Kerala': "KL",
	'Ladakh': "LK",
	'Lakshadweep': "LD",
	'Madhya Pradesh': "MP",
	'Maharashtra':"MH" ,
	'Manipur':"MN" ,
	'Meghalaya': "ML",
	'Mizoram': "MZ",
	'Nagaland': "NL",
	'Odisha': "OD",
	'Puducherry': "PY",
	'Punjab': "PB",
	'Rajasthan': "RJ",
	'Sikkim': "SK",
	'Tamil Nadu':"TN" ,
	'Telengana': "TS",
	'Tripura':"TR" ,
	'Uttarakhand': "UK",
	'Uttar Pradesh':"UP" ,
	'West Bengal':"WB" 
	
}

# Create your views here.
def filter_integer(x):
    array = re.findall(r'[0-9]+', x)
    return ''.join(array)

def getData():

	#get data directlly to scrape site
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	# URL = 'https://www.mohfw.gov.in/'
	# page = requests.get(URL)

	# soup = BeautifulSoup(page.content, 'html.parser')
	# tableData = soup.findAll('div', attrs={'class':'data-table table-responsive'})
	# tableData  = tableData[0].find('tbody')
	# dataList=[]
	# for i in tableData.findAll('tr'):
	#     data=[]
	#     for j,vlu in enumerate(i.findAll('td')):
	#         if j==1:
	#             data.append(vlu.text)
	#         elif j>1:
	#             data.append(filter_integer(vlu.text))
	#     if len(data)>2:
	#         dataList.append(data)

	# total = ['Total number of confirmed cases in India']

	# for vlu in dataList[-1]:    
	#     total.append(filter_integer(vlu))
	    
	# print(total)
	# del dataList[-1]
	# #dataList[-1]=total  
	# for i in range(len(dataList)):		
	# 	dataList[i].insert(0, i+1)

	# print(dataList)
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


	#get data from database
	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	dataList = []
	tconfirmCases,tcuredCases,tdeathCases=0,0,0
	updateDate=0

	for i,vlu in enumerate(dailyData.objects.filter(when__date=date.today()) ):
		dataList.append([i+1, vlu.stateName, vlu.confirmedCases, vlu.curedCases, vlu.deathCases])
		updateDate = vlu.when

		tconfirmCases+=int(vlu.confirmedCases)
		tcuredCases+= int(vlu.curedCases)
		tdeathCases+= int(vlu.deathCases)

	
	total = ['Total number of confirmed cases in India',tconfirmCases,tcuredCases,tdeathCases]
	#print('databse')
	#print(total, dataList)





	#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



	confirmCases = dfd(list)

	for i in dataList:
		try:
			confirmCases[ stateCode[i[1]] ].append(int(i[2])) 
			confirmCases[ stateCode[i[1]] ].append(i[1]) 
			confirmCases[ stateCode[i[1]] ].append(stateCode[i[1]]) 
		except:
			print("Except from getData()")

	sortedConfirmedCases = sorted(confirmCases.items(), key=lambda x: x[1] , reverse=True)
	#print(sortedConfirmedCases)
	sortedConfirmedCasesList = []
	colorData = dict()
	colorFill=dict()



	c=0
	c2=255
	radius=32
	colorCode=1
	for i in sortedConfirmedCases:
		sortedConfirmedCasesList.append({
			
                'centered': i[1][2],
                'fillKey': i[1][2],
                'radius': radius+((i[1][0])//2400)*2,
                'state': i[1][1]+","+str(i[1][0])
            
			})
		#colorFill[ i[1][2] ] = "rgb("+str(c2)+","+ str(0)+","+str(c) +")"
		colorFill[ i[1][2] ] = colorList[colorCode]
		colorCode+=1
		#print(colorCode)

		colorData[ i[1][2] ]={ 'fillKey': i[1][2]  }


		c+=(i[1][0])//200
		radius-=1

	colorFill['defaultFill'] = '#dddddd'

	return dataList, total,sortedConfirmedCasesList,colorData,colorFill, updateDate



def tripleGraph(data):
		dataPoint1,dataPoint2,dataPoint3= [],[],[]
		#print(data)

		for i in data:
			
			dataPoint1.append({ 'y': int(i[2]), 'label': i[1] ,'indexLabel': i[2] ,'indexLabelFontSize': 10})
			dataPoint2.append({ 'y': int(i[3]), 'label': i[1] ,'indexLabel': i[3] ,'indexLabelFontSize': 10})
			dataPoint3.append({ 'y': int(i[4]), 'label': i[1] ,'indexLabel': i[4] ,'indexLabelFontSize': 10})

		#print(dataPoint1)
		#print(dataPoint2)
		#print(dataPoint3)


		return dataPoint1,dataPoint2,dataPoint3

def getPieData(data):
	confirmedPie,curedPie,deathPie = [], [], []
	for i in data:
		if i[0]==1:
			confirmedPie.append({ 'y': i[2], 'name': i[1], 'exploded': 'true' })
			curedPie.append({ 'y': i[3], 'name': i[1], 'exploded': 'true' })
			deathPie.append({ 'y': i[4], 'name': i[1], 'exploded': 'true' })
		else:
			confirmedPie.append({ 'y': i[2], 'name': i[1]})
			curedPie.append({ 'y': i[2], 'name': i[1]})
			deathPie.append({ 'y': i[2], 'name': i[1]})

	return confirmedPie,curedPie,deathPie
			

def findNewCases():
	todayDataDB = dailyData.objects.filter(when__date=date.today()) 
	yesterdayDataDB = dailyData.objects.filter(when__date=(  date.today() - timedelta(days = 1)  ))

	todayConfirmedData =0
	todayCuredData = 0
	todayDeathData = 0

	yesterdayConfirmedData =0
	yesterdayCuredData = 0
	yesterdayDeathData = 0

	for vlu in todayDataDB:
		todayConfirmedData+= int(vlu.confirmedCases)
		todayCuredData+= int(vlu.curedCases)
		todayDeathData+= int(vlu.deathCases)



	for vlu in yesterdayDataDB:
		yesterdayConfirmedData+= int(vlu.confirmedCases)
		yesterdayCuredData+= int(vlu.curedCases)
		yesterdayDeathData+= int(vlu.deathCases)


	return (todayConfirmedData - yesterdayConfirmedData),(todayCuredData - yesterdayCuredData),(todayDeathData - yesterdayDeathData)


def getIncrementedData():
	dataFromDM = dailyData.objects.values( day=ExtractDay('when'), 
										month=ExtractMonth('when'),
										year = ExtractYear('when') ).annotate(Sum('confirmedCases'),
																				Sum('curedCases'),
																				Sum('deathCases'))
	dataFromDM= dataFromDM.order_by('month')
	#print(dataFromDM)
	#print(len(dataFromDM))

	incrementedConfirmedCases,incrementedCuredCases, incrementedDeathCases = dfd(int), dfd(int), dfd(int)
	temp1, temp2, temp3 = 25435,5000,800

	for i in dataFromDM:
		d='{}/{}/{}'.format(i['day'],i['month'],i['year'])
		incrementedConfirmedCases[d]=(i['confirmedCases__sum'] - temp1)
		incrementedCuredCases[d]=(i['curedCases__sum'] - temp2)
		incrementedDeathCases[d]=(i['deathCases__sum'] - temp3)
		temp1 = i['confirmedCases__sum']
		temp2 = i['curedCases__sum']
		temp3 = i['deathCases__sum']


		#print(i['confirmedCases__sum'],d)
	#print(incrementedConfirmedCases)
	#print(incrementedCuredCases)
	#print(incrementedDeathCases)

	dateOfCnfInc ,dataOfCnfInc = list(incrementedConfirmedCases.keys()), list(incrementedConfirmedCases.values())
	dateOfCurInc ,dataOfCurInc = list(incrementedCuredCases.keys()), list(incrementedCuredCases.values())
	dateOfDthInc ,dataOfDthInc = list(incrementedDeathCases.keys()), list(incrementedDeathCases.values())

	

	return dateOfCnfInc ,dataOfCnfInc,dateOfCurInc ,dataOfCurInc,dateOfDthInc ,dataOfDthInc

def getIncrementedTestData():
	todayTests = 1000000
	incTestCount = 100000
	yesterdayTests = 900000
	testIncreamentData = []
	try:
		todayTests = TestCounter.objects.get( when__date=date.today()  )
		yesterdayTests = TestCounter.objects.get(when__date=(  today - timedelta(days = 1)  ))
		todayTests =  todayTests.tests
		#print('---> ',yesterdayTests.tests)
		yesterdayTests = yesterdayTests.tests
		#print("dhdh") 
		incTestCount = todayTests - yesterdayTests

	except:
		print("Except from getIncrementedTestData() ")


	temp =1199081
	for i in TestCounter.objects.all():
		#print(i.tests,str(i.when)[:10] ) 
		testIncreamentData.append({ 'y': i.tests-temp, 'label': str(i.when)[:10]  })
		temp = i.tests

	#print(testIncreamentData)
	

	return testIncreamentData, todayTests, incTestCount 



def home(request):
	data,total,sortedConfirmedCasesList,colorData,colorFill ,updateDate = getData()
	sortedData = sorted(data,key= lambda x: int(x[2]))
	#print("sorted data",sortedData)
	dataPoint1,dataPoint2,dataPoint3 = tripleGraph(sortedData[12:])
	confirmedPie,curedPie,deathPie = getPieData(sortedData[12:])
	#print(total)

	newConfirmedCases,newCuredCases, newDeathCases = findNewCases()

	dateOfCnfInc ,dataOfCnfInc,dateOfCurInc ,dataOfCurInc,dateOfDthInc ,dataOfDthInc = getIncrementedData()
	testIncreamentData, todayTests, incTestCount  = getIncrementedTestData()
	#getIncrementedTestData

	visiting = Counter(count1=1)
	visiting.save()
	visited = Counter.objects.all().count()


	# totalTests = TestCounter.objects.get( when__date=date.today()  )
	# totalTests =  totalTests.tests
	
	context= {
	'data':data,
	'total':total,
	'sortedConfirmedCasesList':sortedConfirmedCasesList,
	'colorData':colorData,

	"totalConf":total[1],
	"totalCure":total[2],
	"totalDeath":total[3],
	'colorFill':colorFill,

	'dataPoint1':dataPoint1,
	'dataPoint2':dataPoint2,
	'dataPoint3':dataPoint3,

	'totalAffected':len(data),
	'updateDate':updateDate,
	'visited':visited,

	'confirmedPie':confirmedPie,
	'curedPie':curedPie,
	'deathPie':deathPie,



	'newConfirmedCases':newConfirmedCases,
	'newCuredCases':newCuredCases,
	'newDeathCases':newDeathCases,


	 'confirmDataOfLineGraph':[{ 'label': i[0], 'y': i[1] } for i in zip(dateOfCnfInc,dataOfCnfInc)] ,  
	 'curedDataOfLineGraph':[{ 'label': i[0], 'y': i[1] } for i in zip(dateOfCurInc,dataOfCurInc)] ,
	 'deathDataOfLineGraph':[{ 'label': i[0], 'y': i[1] } for i in zip(dateOfDthInc,dataOfDthInc)] ,


	 'todayTests':todayTests,
	 'testIncreamentData':testIncreamentData,
	 'incTestCount':incTestCount
	 
	}

	#print(dailyData.objects.filter(when__date=yesterday) )
	#print([{ 'label': i[0], 'y': i[1] } for i in zip(dateOfCnfInc,dataOfCnfInc)])
	#print('today',today)


	return render(request,'home.html',context)