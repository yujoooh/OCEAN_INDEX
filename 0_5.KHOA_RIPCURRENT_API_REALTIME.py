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
if not os.path.exists(dir1): os.makedirs(dir1)

#[API KEY and URL]] ==================================================================================================
API_KEY = "Qc54vQ0/kTdhe9lScuWU3l/e0heL5RjX05DWr6WdcJnSaeQRDJl/DgZKBwR6VEiq4hKfji6K15hMi8KImjjDw=="
RIP_URL = "http://www.khoa.go.kr/oceangrid/grid/api/ripCurrentRecent/search.do?ServiceKey="  #이안류 최신지수

#[API KEY and URL]] ==================================================================================================
RIP_READ = []
RIP_JSON = []
data1 = [] # API 데이터 저장 리스트 생성

RURL = RIP_URL+API_KEY+"&ResultType=json"
print(RURL)
RIP_PAGE = urllib.request.urlopen(RURL)     # OBS URL OPEN
RIP_READ = RIP_PAGE.read()                  # url에 접속하여 json file read
RIP_JSON = json.loads(RIP_READ)             # json file을 load
	
READ1 = RIP_JSON.get('result')              # result 하위 값 전체 get
READ2 = READ1.get('data')
RIP_LEN = len(READ2)
print(READ2[0], RIP_LEN)

ii = 0
while ii <= RIP_LEN-1 :
	DY = READ2[ii].get('obs_time')							#날짜
	if READ2[ii].get('beach_name') == '중문 해수욕장':
		BEACH = READ2[ii].get('beach_name').replace("중문 해수욕장", "중문색달해수욕장")	
	else :
		BEACH = READ2[ii].get('beach_name').replace(" ", "")	#해수욕장
	LEVEL = READ2[ii].get('score_msg')						#단계               
	SCORE = READ2[ii].get('score')							#지수           
	print(DY, BEACH, LEVEL, SCORE)
	data1.append([DY, BEACH, LEVEL, SCORE])
	ii = ii + 1

with open(dir1+'/KHOA_RIPCURRENT_LEVEL_'+today+hr+'.csv','w',encoding='utf8') as file:
	file.write('Date_time,beach,level,score\n')
	for i in data1:
		file.write('{0},{1},{2},{3}\n'.format(i[0],i[1],i[2],i[3])) 
		#file.write('DATE_TIME,{0},{1},{2},{3}\n'.format(i[0], i[1], i[2])) 

print("#KOHA OBS data collection Complete==========")
