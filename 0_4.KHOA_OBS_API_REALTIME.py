#[Geosystem Research : Department of Marine Forecast ]
#[Created by C.K. Park on 2018.10.23]
import json
import os
import urllib.request
import shutil
from collections import OrderedDict
from datetime import datetime, timedelta

print("#KOHA OBS data collection Start==========")

#[Date Set]===============================================================================================================
today = str(datetime.today().strftime('%Y%m%d'))
hr = str(datetime.today().strftime("%H"))

#[폴더]
dir1 = './Result/'+today

#[KMA API KEY and URL]] ==================================================================================================
API_KEY = "Qc54vQ0/kTdhe9lScuWU3l/e0heL5RjX05DWr6WdcJnSaeQRDJl/DgZKBwR6VEiq4hKfji6K15hMi8KImjjDw=="
UOBS = "&ObsCode="

TIDE_URL = "http://www.khoa.go.kr/oceangrid/grid/api/tideObsRecent/search.do?ServiceKey="  #조위관측소(DT_~~~~,IE_~~~~)
BUOY_URL = "http://www.khoa.go.kr/oceangrid/grid/api/buObsRecent/search.do?ServiceKey=" #해양관측부이(TW_~~~~)
#OCEAN_URL = "http://www.khoa.go.kr/oceangrid/grid/api/buObsRecent/search.do?ServiceKey=" #해양관측소(RT_~~~~)

OBS_READ = []
OBS_JSON = []
data1 = [] # 조위관측소 데이터 저장 리스트 생성
data2 = [] # 해양관측부이 데이터 저장 리스트 생성
Miss = '-999'
#-----------------------------------[조위관측소 자료수집]-----------------------------------------
TIDE_INF = open('./Info/TIDE_STATION_INFO.csv','r',encoding='utf8')
TIDE_STN = [str(INFO) for INFO in TIDE_INF.read().split()]
print(today,"KHOA Tide-station obs data collection...","correction time", hr)

ii = 1
while ii < 53: # 
#while ii < 50: # ObsCode에서 제공되는 왕돌초, 복사초, 교본초는 자료가 안들어옴
#    print(TIDE_STN[ii])
	TURL = TIDE_URL+API_KEY+UOBS+TIDE_STN[ii]+"&ResultType=json"
	OBS_PAGE = urllib.request.urlopen(TURL)     # OBS URL OPEN
	OBS_READ = OBS_PAGE.read()                  # url에 접속하여 json file read
	#OBS_JSON = json.loads(OBS_READ, object_pairs_hook=OrderedDict) # test
	OBS_JSON = json.loads(OBS_READ)             # json file을 load
	
	READ1 = OBS_JSON.get('result')              # result 하위 값 전체 get
	if 'error' in READ1 : 
		print(TIDE_STN[ii], "data not found")
	else : 
		READ2 = READ1.get('data')                   # result 하위의 data 하위값 전체 get
		READ3 = READ1.get('meta')                   # result 하위의 meta 하위값 전체 get
	
		STN = READ3.get('obs_post_name')            # meta 하위 값 중 관측지점 정보 get
		SST = READ2.get('water_temp')               # data 하위 값 중 수온정보 get
		if SST == None or SST == '0' or SST == '' or SST == 'null':
			SST = Miss
		MWHT = Miss                                 # 조위관측소는 파고자료 제공 하지 않음. 모두 missing 처리
		if STN == '왕돌초' or STN == '복사초' or STN == '교본초' or STN == '이어도' or STN == '신안가거초' or STN == '옹진소청초':
			MWHT = READ2.get('wave_hight')
			if MWHT == None or MWHT == '0' or MWHT == '' or MWHT == 'null':
				MWHT = Miss
		print(STN, SST, MWHT)
		data1.append([STN, SST, MWHT])              # data1[]에 자료 붙여넣기
	ii = ii +1

#-----------------------------------[해양관측부이 자료수집]-----------------------------------------
BUOY_INF = open('./Info/BUOY_STATION_INFO.csv','r',encoding='utf8')
BUOY_STN = [str(INFO) for INFO in BUOY_INF.read().split()]
print(today,"KHOA Ocean-buoy obs data collection...","correction time", hr)

ii = 1
#while ii < 35: # 
while ii < 33: # ObsCode에서 제공되는 송정해수욕장, 낙산해수욕장은 자료가 안들어옴
	BURL = BUOY_URL+API_KEY+UOBS+BUOY_STN[ii]+"&ResultType=json"
	OBS_PAGE = urllib.request.urlopen(BURL)     # OBS URL OPEN
	OBS_READ = OBS_PAGE.read()                  # url에 접속하여 json file read
	#OBS_JSON = json.loads(OBS_READ, object_pairs_hook=OrderedDict) # test
	OBS_JSON = json.loads(OBS_READ)             # json file을 load
#    print(OBS_JSON)
	
	READ1 = OBS_JSON.get('result')              # result 하위 값 전체 get
	if 'error' in READ1 : 
		print(BUOY_STN[ii], "data not found")
	else : 
		READ2 = READ1.get('data')                   # result 하위의 data 하위값 전체 get
		READ3 = READ1.get('meta')                   # result 하위의 meta 하위값 전체 get
		STN = READ3.get('obs_post_name')            # meta 하위 값 중 관측지점 정보 get
	
		SST = READ2.get('water_temp')               # data 하위 값 중 수온정보 get
		if SST == None or SST == '0' or SST == '' or SST == 'null':
			SST = Miss
		MWHT = READ2.get('wave_height')             # data 하위 값 중 파고정보 get
		if MWHT == None or MWHT == '0' or MWHT == '' or MWHT == 'null':
			MWHT = Miss
		print(STN, SST, MWHT)
		data2.append([STN, SST, MWHT])              # data2[]에 자료 붙여넣기
	ii = ii +1
if hr < '12':
	with open(dir1+'/KHOA_OBS_AM.csv','w',encoding='utf8') as file:
		file.write('OBS, STN, SST, MWHT\n')
		for i in data1:
			file.write('조위관측,{0},{1},{2}\n'.format(i[0], i[1], i[2])) 
		for i in data2:
			file.write('해양부이,{0},{1},{2}\n'.format(i[0], i[1], i[2]))      
	#    for i in data3:
	#        file.write('국내등표,{0},{1},{2}\n'.format(i[0], i[1], i[2]))         
else:
	with open(dir1+'/KHOA_OBS_PM.csv','w',encoding='utf8') as file:
		file.write('OBS, STN, SST, MWHT\n')
		for i in data1:
			file.write('조위관측,{0},{1},{2}\n'.format(i[0], i[1], i[2])) 
		for i in data2:
			file.write('해양부이,{0},{1},{2}\n'.format(i[0], i[1], i[2]))      
	#    for i in data3:
	#        file.write('국내등표,{0},{1},{2}\n'.format(i[0], i[1], i[2]))
	if not os.path.exists(dir1+'/KHOA_OBS_AM.csv'): shutil.copy(dir1+'/KHOA_OBS_PM.csv', dir1+'/KHOA_OBS_AM.csv') #12시 이후에 AM자료가 없으면 PM자료 복사해서 이름 바꾸기

print("#KOHA OBS data collection Complete==========")
