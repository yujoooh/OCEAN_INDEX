#[Geosystem Research : Department of Marine Forecast ]
#[Created by C.K. Park on 2018.10.23]
import json
import os
import urllib.request
import shutil
from collections import OrderedDict
from datetime import date, timedelta
from datetime import datetime

print("#KMA OBS data collection Start==========")

#[Date Set]===============================================================================================================
today = str(datetime.today().strftime('%Y%m%d%H'))
today2 = str(datetime.today().strftime('%Y%m%d'))
hr = str(datetime.today().strftime("%H"))
#today = '2021062108'
#today2 = '20210621'
#hr = '08'

#[폴더]
dir1 = './Result/'+today2

#[KMA API KEY and URL]] ==================================================================================================
API_KEY = "Kb%2BKlCpXZ7j3udye3E8YL8w4WRPsUtyadYzDUKAmJ6ZJoNKuLWBWqDJwHOAPuqKuRjPnotzwr2E14sBvyJ7lWw%3D%3D"


#Check KMA API access
#파고부이 http://apis.data.go.kr/1360000/OceanInfoService/getWhBuoy?ServiceKey=Kb%2BKlCpXZ7j3udye3E8YL8w4WRPsUtyadYzDUKAmJ6ZJoNKuLWBWqDJwHOAPuqKuRjPnotzwr2E14sBvyJ7lWw%3D%3D&numOfRows=62&pageNo=1&dataType=JSON&searchTime=20200428
#국내부이 http://apis.data.go.kr/1360000/OceanInfoService/getBuoyObs?ServiceKey=Kb%2BKlCpXZ7j3udye3E8YL8w4WRPsUtyadYzDUKAmJ6ZJoNKuLWBWqDJwHOAPuqKuRjPnotzwr2E14sBvyJ7lWw%3D%3D&numOfRows=17&pageNo=1&dataType=JSON&searchTime=20200428
#국내등표 http://apis.data.go.kr/1360000/OceanInfoService/getLhObs?ServiceKey=Kb%2BKlCpXZ7j3udye3E8YL8w4WRPsUtyadYzDUKAmJ6ZJoNKuLWBWqDJwHOAPuqKuRjPnotzwr2E14sBvyJ7lWw%3D%3D&numOfRows=8&pageNo=1&dataType=JSON&searchTime=20200428

WBUOY_URL = "http://apis.data.go.kr/1360000/OceanInfoService/getWhBuoy?ServiceKey="  #파고부이
BBUOY_URL = "http://apis.data.go.kr/1360000/OceanInfoService/getBuoyObs?ServiceKey=" #국내부이
#LAMP_URL = "http://apis.data.go.kr/1360000/OceanInfoService/getLhObs?ServiceKey=" #국내등표 -- 파고/수온 정보 미제공

#[Number of KMA OBS STATION] ===============================================================================================
WNUM = 75  # 파고부이 관측지점 수 
BNUM = 24  # 해양기상부이 관측지점 수
#LNUM = 17  # 국내등표 관측지점 수 -- 파고/수온 정보 미제공

data1 = [] # 파고부이 데이터 저장 리스트 생성
data2 = [] # 국내부이 데이터 저장 리스트 생성
#data3 = [] # 국내등표 데이터 저장 리스트 생성 -- 파고/수온 정보 미제공

Miss = '-999.0' #결측값 
#-----------------------------------[파고부이 자료수집]----------------------------------------------------
print(today2,"KMA Wave-Buoy obs data collection...","correction time", hr)
WURL = WBUOY_URL + API_KEY + "&numOfRows=" + str(WNUM) + "&pageNo=1&dataType=JSON"+"&searchTime=" + today
print(WURL)
WPAGE = urllib.request.urlopen(WURL)
WREAD = WPAGE.read()
WJSON = json.loads(WREAD)
#print(WJSON)

READ1 = WJSON.get('response')
READ2 = READ1.get('body')
READ3 = READ2.get('items')
READ4 = READ3.get('item')

ii = 0
while ii < WNUM - 1 :
	OBS = '파고부이'
	STN = READ4[ii].get('name')  #지점명
	WHT = READ4[ii].get('whSig') #유의파고
	SST = READ4[ii].get('tw')   #수온
	if WHT == 0.0 or WHT == "" : WHT = Miss
	if SST == 0.0 or SST == "" : SST = Miss
	ii = ii + 1
	data1.append([OBS,STN.strip(),SST,WHT])
	print(OBS, STN.strip(), WHT, SST)

#-----------------------------------[해양기상부이 자료수집]----------------------------------------------------
print(today2,"KMA Ocean-Buoy obs data collection...","correction time", hr)
BURL = BBUOY_URL + API_KEY + "&numOfRows=" + str(BNUM) + "&pageNo=1&dataType=JSON"+"&searchTime=" + today 
BPAGE = urllib.request.urlopen(BURL)
BREAD = BPAGE.read()
BJSON = json.loads(BREAD)
#print(WJSON)

READ1 = BJSON.get('response')
READ2 = READ1.get('body')
READ3 = READ2.get('items')
READ4 = READ3.get('item')

ii = 0
while ii < BNUM-1:
	OBS = '해양기상'
	STN = READ4[ii].get('name')  #지점명
	WHT = READ4[ii].get('whSig') #최대파고
	SST = READ4[ii].get('tw')   #수온
	if WHT == 0.0 or WHT == "" : WHT = Miss
	if SST == 0.0 or SST == "" : SST = Miss
	ii = ii + 1
	data2.append([OBS,STN.strip(),SST,WHT])
	print(OBS, STN.strip(), WHT, SST)

KMA_MISS = open('./Info/KMA_OBS_MISSING.csv','r',encoding='utf8')
KMA = [LST for LST in KMA_MISS.read().split()]
KMA_LEN = len(KMA)
#print(KMA_OBS[0], KMA_OBS[1], KMA_OBS[2],KMA_OBS[3])

#print(KMA)

data3 = []
ii = 4 
while ii < 76: 
	DEV = KMA[ii].split(',') ; TYPE = DEV[0] ; STN = DEV[1]
	jj = 0 ; num = 0
	while jj < len(data1)-1:
		if STN == data1[jj][1] : 
			break
		else :
			num = num + 1
		jj += 1
	if num == len(data1)-1 : 
		data3.append([TYPE,STN,'-999.0','-999.0'])
		print(TYPE,STN,'-999.0','-999.0')
	ii += 1
    
ii = 77
while ii < KMA_LEN-1: 
	DEV = KMA[ii].split(',') ; TYPE = DEV[0] ; STN = DEV[1]
	jj = 0 ; num = 0
	while jj < len(data2)-1:
		if STN == data2[jj][1] :
			break
		else :
			num = num + 1
		jj += 1

	if num == len(data2)-1  : 
		#print(STN, data2[jj][1],num)
		data3.append([TYPE,STN,'-999.0','-999.0'])
		print(TYPE,STN,'-999.0','-999.0')
	ii += 1
#print(KMA_LEN-1, len(data2)-1)
	
if hr < '12':
	with open(dir1+'/KMA_OBS_AM.csv','w',encoding='utf8') as file:
		file.write('OBS, STN, SST, MWHT\n')
		for i in data1:
			file.write('{0},{1},{2},{3}\n'.format(i[0],i[1],i[2],i[3]))
		for i in data2:
			file.write('{0},{1},{2},{3}\n'.format(i[0],i[1],i[2],i[3]))
		for i in data3:
			file.write('{0},{1},{2},{3}\n'.format(i[0],i[1],i[2],i[3]))
else:
	with open(dir1+'/KMA_OBS_PM.csv','w',encoding='utf8') as file:
		file.write('OBS, STN, SST, MWHT\n')
		for i in data1:
			file.write('{0},{1},{2},{3}\n'.format(i[0],i[1],i[2],i[3])) 
		for i in data2:
			file.write('{0},{1},{2},{3}\n'.format(i[0],i[1],i[2],i[3]))
		for i in data3:
			file.write('{0},{1},{2},{3}\n'.format(i[0],i[1],i[2],i[3]))
	if not os.path.exists(dir1+'/KMA_OBS_AM.csv'): shutil.copy(dir1+'/KMA_OBS_PM.csv', dir1+'/KMA_OBS_AM.csv') #12시 이후에 AM자료가 없으면 PM자료 복사해서 이름 바꾸기
			
print("#KMA OBS data collection Complete==========")
