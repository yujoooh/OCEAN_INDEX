#[Geosystem Research : Department of Marine Forecast ]
#[Created by C.K. Park on 2018.10.23]
import json
import urllib.request
import numpy as np
from collections import OrderedDict
from datetime import date, timedelta
from datetime import datetime
from math import *

print("#KHOA Yesterday OBS data collection Start==========")

#[Date Set]===============================================================================================================
today = str(datetime.today().strftime('%Y%m%d'))
yesterday = (date.today() - timedelta(1)).strftime('%Y%m%d')
hr = str(datetime.today().strftime("%H"))
h = 0

dir1 = './Result/'+today

#[KHOA API KEY and URL]===========================================================================================================
API_KEY = "Qc54vQ0/kTdhe9lScuWU3l/e0heL5RjX05DWr6WdcJnSaeQRDJl/DgZKBwR6VEiq4hKfji6K15hMi8KImjjDw=="
UOBS = "&ObsCode="

TIDE_TEMP_URL = "http://www.khoa.go.kr/oceangrid/grid/api/tideObsTemp/search.do?ServiceKey="
TIDE_WIND_URL = "http://www.khoa.go.kr/oceangrid/grid/api/tideObsWind/search.do?ServiceKey="
BUOY_TEMP_URL = "http://www.khoa.go.kr/oceangrid/grid/api/tidalBuTemp/search.do?ServiceKey="
BUOY_WIND_URL = "http://www.khoa.go.kr/oceangrid/grid/api/tidalBuWind/search.do?ServiceKey="
WAVE_HEIGHT_URL = "http://www.khoa.go.kr/oceangrid/grid/api/obsWaveHight/search.do?ServiceKey="
#조위관측소 실측 수온#http://www.khoa.go.kr/oceangrid/grid/api/tideObsTemp/search.do?ServiceKey=Qc54vQ0/kTdhe9lScuWU3l/e0heL5RjX05DWr6WdcJnSaeQRDJl/DgZKBwR6VEiq4hKfji6K15hMi8KImjjDw==&ObsCode=DT_0001&Date=20191001&ResultType=json
#조위관측소 실측 풍속 #http://www.khoa.go.kr/oceangrid/grid/api/tideObsWind/search.do?ServiceKey=Qc54vQ0/kTdhe9lScuWU3l/e0heL5RjX05DWr6WdcJnSaeQRDJl/DgZKBwR6VEiq4hKfji6K15hMi8KImjjDw==&ObsCode=DT_0001&Date=20160101&ResultType=json
#해양관측부이 실측 수온 #http://www.khoa.go.kr/oceangrid/grid/api/tidalBuTemp/search.do?ServiceKey=Qc54vQ0/kTdhe9lScuWU3l/e0heL5RjX05DWr6WdcJnSaeQRDJl/DgZKBwR6VEiq4hKfji6K15hMi8KImjjDw==&ObsCode=TW_0062&Date=20160101&ResultType=json
#해양관측부이 실측 풍속 #http://www.khoa.go.kr/oceangrid/grid/api/tidalBuWind/search.do?ServiceKey=Qc54vQ0/kTdhe9lScuWU3l/e0heL5RjX05DWr6WdcJnSaeQRDJl/DgZKBwR6VEiq4hKfji6K15hMi8KImjjDw==&ObsCode=TW_0062&Date=20160101&ResultType=json
#실측파고 #http://www.khoa.go.kr/oceangrid/grid/api/obsWaveHight/search.do?ServiceKey=Qc54vQ0/kTdhe9lScuWU3l/e0heL5RjX05DWr6WdcJnSaeQRDJl/DgZKBwR6VEiq4hKfji6K15hMi8KImjjDw==&ObsCode=TW_0062&Date=20141101&ResultType=json

OBS_READ = []
OBS_JSON = []
data1 = [] # 조위관측소 데이터 저장 리스트 생성
data2 = [] # 해양관측부이 데이터 저장 리스트 생성
Miss = '-999'

#-----------------------------------[조위관측소 자료수집]-----------------------------------------
TIDE_INF = open('./Info/TIDE_STATION_INFO2.csv','r')
TIDE_STN = [str(INFO) for INFO in TIDE_INF.read().split()]
TIDE_LEN = len(TIDE_STN)

ii = 1
while ii < TIDE_LEN: # 
	print(TIDE_STN[ii])
	TURL1 = TIDE_TEMP_URL+API_KEY+UOBS+TIDE_STN[ii]+"&Date="+yesterday+"&ResultType=json" #수온
	TURL2 = TIDE_WIND_URL+API_KEY+UOBS+TIDE_STN[ii]+"&Date="+yesterday+"&ResultType=json" #풍속
	#TURL3 = WAVE_HEIGHT_URL+API_KEY+UOBS+TIDE_STN[ii]+"&Date="+yesterday+"&ResultType=json" #파고

	OBS_PAGE1 = urllib.request.urlopen(TURL1)
	OBS_READ1 = OBS_PAGE1.read()
	OBS_JSON1 = json.loads(OBS_READ1)   
	READ1 = OBS_JSON1.get('result')

	OBS_PAGE2 = urllib.request.urlopen(TURL2)  
	OBS_READ2 = OBS_PAGE2.read()               
	OBS_JSON2 = json.loads(OBS_READ2)          
	READ4 = OBS_JSON2.get('result')

	if 'error' in READ1 and 'error' in READ4:
		print(TIDE_STN[ii], "data not found")
		
	elif 'data' in READ1 and 'data' in READ4 :
		READ2 = READ1.get('data') ; READ3 = READ1.get('meta')
		READ5 = READ4.get('data') ; READ6 = READ4.get('meta')
		STN = READ3.get('obs_post_name') ; STNID = READ3.get('obs_post_id')

		jj = 0; kk = 0
		while jj <len(READ2)-1:
			RTIME = READ2[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			SST=Miss ; SST = READ2[jj].get('water_temp')
			if SST == None : SST = Miss
			WHT = Miss
			if RTIME[14:16] == '00' : data2.append([STNID, STN, YMD, SST, WHT]) ; kk = kk + 1
			jj = jj + 1

		jj = 0 ; kk = 0
		while jj < len(READ5)-1:
			RTIME = READ5[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			WSPD=Miss ; WSPD = READ5[jj].get('wind_speed')
			WDIR=Miss ; WDIR = READ5[jj].get('wind_dir')
			if WSPD == None : WSPD = Miss
			if WDIR == None : WDIR = Miss
			if WDIR == Miss or WSPD == Miss :
				USPD = Miss ; VSPD = Miss
			else:
				USPD = round(-abs(float(WSPD))*sin(np.deg2rad(float(WDIR))),1)
				VSPD = round(-abs(float(WSPD))*cos(np.deg2rad(float(WDIR))),1)
			if RTIME[14:16] == '00' and YMD == data2[kk][2]:
				data2[kk].insert(5,WSPD)
				data2[kk].insert(6,WDIR)
				data2[kk].insert(7,USPD)
				data2[kk].insert(8,VSPD)
				#print(data2[kk][0],data2[kk][1],data2[kk][2],data2[kk][3],data2[kk][4],data2[kk][5],data2[kk][6],data2[kk][7],data2[kk][8],'조위관측')
				data1.append([data2[kk][0],data2[kk][1],data2[kk][2],data2[kk][3],data2[kk][4],data2[kk][5],data2[kk][6],data2[kk][7],data2[kk][8],'조위관측'])
				kk = kk + 1
			jj = jj + 1		
		data2.clear()
	elif 'data' in READ1 and 'error' in READ4:
		READ2 = READ1.get('data') ; READ3 = READ1.get('meta')
		STN = READ3.get('obs_post_name') ; STNID = READ3.get('obs_post_id')
		jj = 0
		while jj < len(READ2)-1:
			RTIME = READ2[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			SST=Miss ; SST = READ2[jj].get('water_temp')
			if SST == None : SST = Miss
			WSPD=Miss ;	WDIR=Miss ; WHT = Miss
			USPD=Miss ; VSPD=Miss
			if RTIME[14:16] == '00' :
				#print(STNID, STN, YMD, SST, WHT,WSPD,WDIR,USPD,VSPD,'조위관측')
				data1.append([STNID, STN, YMD, SST, WHT, WSPD, WDIR,USPD,VSPD,'조위관측'])              # data1[]에 자료 붙여넣기
			jj = jj + 1
	
	elif 'error' in READ1 and'data' in READ4 :
		READ5 = READ4.get('data') ; READ6 = READ4.get('meta')
		STN = READ6.get('obs_post_name') ; STNID = READ6.get('obs_post_id')
		jj = 0
		while jj < len(READ5)-1:
			RTIME = READ5[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			SST=Miss ; WHT = Miss
			WSPD=Miss ; WSPD = READ5[jj].get('wind_speed')
			WDIR=Miss ; WDIR = READ5[jj].get('wind_dir')
			if WSPD == None : WSPD = Miss
			if WDIR == None : WDIR = Miss
			if WDIR == Miss or WSPD == Miss :
				USPD = Miss ; VSPD = Miss
			else:
				USPD = round(-abs(float(WSPD))*sin(np.deg2rad(float(WDIR))),1)
				VSPD = round(-abs(float(WSPD))*cos(np.deg2rad(float(WDIR))),1)
			if RTIME[14:16] == '00' :
				#print(STNID, STN, YMD, SST, WHT,WSPD,WDIR,USPD,VSPD,'조위관측')
				data1.append([STNID, STN, YMD, SST, WHT, WSPD, WDIR,USPD,VSPD,'조위관측'])              # data1[]에 자료 붙여넣기
			jj = jj + 1
	ii = ii + 1
#-----------------------------------[해양관측부이 자료수집]-----------------------------------------
BUOY_INF = open('./Info/BUOY_STATION_INFO2.csv','r')
BUOY_STN = [str(INFO) for INFO in BUOY_INF.read().split()]
BUOY_LEN = len(BUOY_STN)

ii = 1
while ii < BUOY_LEN: # 
	print(BUOY_STN[ii])
	BURL1 = BUOY_TEMP_URL+API_KEY+UOBS+BUOY_STN[ii]+"&Date="+yesterday+"&ResultType=json"
	BURL2 = BUOY_WIND_URL+API_KEY+UOBS+BUOY_STN[ii]+"&Date="+yesterday+"&ResultType=json"
	BURL3 = WAVE_HEIGHT_URL+API_KEY+UOBS+BUOY_STN[ii]+"&Date="+yesterday+"&ResultType=json"

	OBS_PAGE1 = urllib.request.urlopen(BURL1)
	OBS_READ1 = OBS_PAGE1.read()
	OBS_JSON1 = json.loads(OBS_READ1)
	READ1 = OBS_JSON1.get('result')
	
	OBS_PAGE2 = urllib.request.urlopen(BURL2)
	OBS_READ2 = OBS_PAGE2.read()
	OBS_JSON2 = json.loads(OBS_READ2)	
	READ4 = OBS_JSON2.get('result')

	OBS_PAGE3 = urllib.request.urlopen(BURL3)
	OBS_READ3 = OBS_PAGE3.read()
	OBS_JSON3 = json.loads(OBS_READ3)	
	READ7 = OBS_JSON3.get('result')

	if 'error' in READ1 and 'error' in READ4 and 'error' in READ7:
		print(BUOY_STN[ii], "data not found")

	elif 'data' in READ1 and 'data' in READ4 and 'data' in READ7:
		READ2 = READ1.get('data') ; READ3 = READ1.get('meta')
		READ5 = READ4.get('data') ; READ6 = READ4.get('meta')
		READ8 = READ7.get('data') ; READ9 = READ7.get('meta')
		STN = READ3.get('obs_post_name') ; STNID = READ3.get('obs_post_id')

		jj = 0 ; kk = 0
		while jj < len(READ2)-1:
			RTIME = READ2[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			SST = Miss ; SST = READ2[jj].get('water_temp')
			if SST == None : SST = Miss
			if RTIME[14:16] == '00' : data2.append([STNID, STN, YMD, SST]) ; kk = kk + 1
			jj = jj + 1

		jj = 0 ; kk = 0
		while jj < len(READ5)-1:
			RTIME = READ5[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			WSPD=Miss ;WSPD = READ5[jj].get('wind_speed')	
			WDIR=Miss ;WDIR = READ5[jj].get('wind_dir')	
			if WSPD == None : WSPD = Miss
			if WDIR == None : WDIR = Miss
			if WDIR == Miss or WSPD == Miss :
				USPD = Miss ; VSPD = Miss
			else:
				USPD = round(-abs(float(WSPD))*sin(np.deg2rad(float(WDIR))),1)
				VSPD = round(-abs(float(WSPD))*cos(np.deg2rad(float(WDIR))),1)
			if RTIME[14:16] == '00' and YMD == data2[kk][2]:
				data2[kk].insert(4,WSPD) ; data2[kk].insert(5,WDIR) ; data2[kk].insert(6,USPD) ; data2[kk].insert(7,VSPD)
				kk = kk + 1
			jj = jj + 1

		jj = 0 ; kk = 0
		while jj < len(READ8)-1:
			RTIME = READ8[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			WHT=Miss ; WHT = READ8[jj].get('wave_height')
			if WHT == None : WHT = Miss
			if RTIME[14:16] == '00' and YMD == data2[kk][2]: 
				data2[kk].insert(4,WHT)
				#print(data2[kk][0],data2[kk][1],data2[kk][2],data2[kk][3],data2[kk][4],data2[kk][5],data2[kk][6],data2[kk][7],data2[kk][8],'해양부이')
				data1.append([data2[kk][0],data2[kk][1],data2[kk][2],data2[kk][3],data2[kk][4],data2[kk][5],data2[kk][6],data2[kk][7],data2[kk][8],'해양부이'])
				kk = kk + 1
			jj = jj + 1			
		data2.clear()
		#print(data1)

	elif 'data' in READ4 and 'data' in READ7 and 'error' in READ1:
		READ5 = READ4.get('data') ; READ6 = READ4.get('meta')
		READ8 = READ7.get('data') ; READ9 = READ7.get('meta')
		STN = READ9.get('obs_post_name') ; STNID = READ9.get('obs_post_id')

		jj = 0 ; kk = 0
		while jj < len(READ5)-1:
			RTIME = READ5[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			SST=Miss
			WSPD=Miss ;WSPD = READ5[jj].get('wind_speed')	
			WDIR=Miss ;WDIR = READ5[jj].get('wind_dir')
			if WSPD == None : WSPD = Miss
			if WDIR == None : WDIR = Miss
			if WDIR == Miss or WSPD == Miss :
				USPD = Miss ; VSPD = Miss
			else:
				USPD = round(-abs(float(WSPD))*sin(np.deg2rad(float(WDIR))),1)
				VSPD = round(-abs(float(WSPD))*cos(np.deg2rad(float(WDIR))),1)
			if RTIME[14:16] == '00' : data2.append([STNID, STN, YMD, SST, WSPD,WDIR,USPD,VSPD,'해양부이']) ; kk = kk + 1
			jj = jj + 1

		jj = 0 ; kk = 0
		while jj < len(READ8)-1:
			RTIME = READ8[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			WHT=Miss ; WHT = READ8[jj].get('wave_height')	
			if WHT == None : WHT = Miss
			if RTIME[14:16] == '00' and YMD == data2[kk][2]:
				data2[kk].insert(4,WHT)
				#print(data2[kk][0],data2[kk][1],data2[kk][2],data2[kk][3],data2[kk][4],data2[kk][5],data2[kk][6],data2[kk][7],data2[kk][8],'해양부이')
				data1.append([data2[kk][0],data2[kk][1],data2[kk][2],data2[kk][3],data2[kk][4],data2[kk][5],data2[kk][6],data2[kk][7],data2[kk][8],'해양부이'])
				kk = kk + 1
			jj = jj + 1		
		data2.clear()

	elif 'data' in READ1 and 'data' in READ7 and 'error' in READ4 :
		READ2 = READ1.get('data') ; READ3 = READ1.get('meta')
		READ8 = READ7.get('data') ; READ9 = READ7.get('meta')
		STN = READ3.get('obs_post_name') ; STNID = READ3.get('obs_post_id')
	
		jj = 0 ; kk = 0
		while jj < len(READ2)-1:
			RTIME = READ2[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			SST = Miss ; SST = READ2[jj].get('water_temp')
			if SST == None : SST = Miss
			WSPD = Miss ; WDIR = Miss ; USPD = Miss ; VSPD = Miss
			if RTIME[14:16] == '00' : data2.append([STNID, STN, YMD, SST, WSPD, WDIR,USPD, VSPD,'해양부이']) ; kk = kk + 1
			jj = jj + 1
		#print(len(data2))

		jj = 0 ; kk = 0
		while jj < len(READ8)-1:
			RTIME = READ8[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			WHT = Miss
			if 'wave_height' in READ8[jj] :
				WHT = READ8[jj].get('wave_height')
				if WHT == None : WHT = Miss
			if RTIME[14:16] == '00' and YMD == data2[kk][2]:
				data2[kk].insert(4,WHT)
				#print(data2[kk][0],data2[kk][1],data2[kk][2],data2[kk][3],data2[kk][4],data2[kk][5],data2[kk][6],data2[kk][7],data2[kk][8],'해양부이')
				data1.append([data2[kk][0],data2[kk][1],data2[kk][2],data2[kk][3],data2[kk][4],data2[kk][5],data2[kk][6],data2[kk][7],data2[kk][8],'해양부이'])
				kk = kk + 1
			jj = jj + 1		
		data2.clear()

	elif 'data' in READ1 and 'data' in READ4 and 'error' in READ7 :
		READ2 = READ1.get('data') ; READ3 = READ1.get('meta')
		READ5 = READ4.get('data') ; READ6 = READ4.get('meta')
		STN = READ3.get('obs_post_name') ; STNID = READ3.get('obs_post_id')
	
		jj = 0 ; kk = 0
		while jj < len(READ2)-1:
			RTIME = READ2[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			SST = Miss ; SST = READ2[jj].get('water_temp')
			if SST == None : SST = Miss
			WHT = Miss
			if RTIME[14:16] == '00' : data2.append([STNID, STN, YMD, SST, WHT]) ; kk = kk + 1
			jj = jj + 1

		jj = 0 ; kk = 0
		while jj < len(READ5)-1:
			RTIME = READ5[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			WSPD=Miss ;WSPD = READ5[jj].get('wind_speed')	
			WDIR=Miss ;WDIR = READ5[jj].get('wind_dir')	
			if WSPD == None : WSPD = Miss
			if WDIR == None : WDIR = Miss
			if WDIR == Miss or WSPD == Miss :
				USPD = Miss ; VSPD = Miss
			else:
				USPD = round(-abs(float(WSPD))*sin(np.deg2rad(float(WDIR))),1)
				VSPD = round(-abs(float(WSPD))*cos(np.deg2rad(float(WDIR))),1)			
			if RTIME[14:16] == '00' and YMD == data2[kk][2]:
				data2[kk].insert(5,WSPD)
				data2[kk].insert(6,WDIR)
				data2[kk].insert(7,USPD)
				data2[kk].insert(8,CSPD)
				#print(data2[kk][0],data2[kk][1],data2[kk][2],data2[kk][3],data2[kk][4],data2[kk][5],data2[kk][6],data2[kk][7],data2[kk][8],'해양부이')
				data1.append([data2[kk][0],data2[kk][1],data2[kk][2],data2[kk][3],data2[kk][4],data2[kk][5],data2[kk][6],data2[kk][7],data2[kk][8],'해양부이'])
				kk = kk + 1
			jj = jj + 1
		data2.clear()

	elif 'data' in READ7 and 'error' in READ1  and 'error' in READ4 :
		READ8 = READ7.get('data') ; READ9 = READ7.get('meta')
		STN = READ9.get('obs_post_name') ; STNID = READ9.get('obs_post_id')

		jj = 0
		while jj < len(READ8)-1:
			RTIME = READ8[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			SST = Miss ; 	WSPD = Miss ;	WDIR = Miss
			WHT = Miss ; WHT = READ8[jj].get('wave_height')
			if WHT == None : WHT = Miss
			if WDIR == Miss or WSPD == Miss :
				USPD = Miss ; VSPD = Miss
			else:
				USPD = round(-abs(float(WSPD))*sin(np.deg2rad(float(WDIR))),1)
				VSPD = round(-abs(float(WSPD))*cos(np.deg2rad(float(WDIR))),1)
			if RTIME[14:16] == '00' :
				#print(STNID, STN, YMD, SST, WHT,WSPD,WDIR,USPD, VSPD,'해양부이')
				data1.append([STNID, STN, YMD, SST, WHT, WSPD,WDIR,USPD, VSPD,'해양부이'])              # data1[]에 자료 붙여넣기
			jj = jj + 1

	elif 'data' in READ4 and 'error' in READ1  and 'error' in READ7  :
		READ5 = READ4.get('data') ; READ6 = READ4.get('meta')
		STN = READ6.get('obs_post_name') ; STNID = READ6.get('obs_post_id')

		jj = 0
		while jj < len(READ5)-1:
			RTIME = READ5[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			SST = Miss ; 	WHT = Miss
			WSPD = Miss ; WSPD = READ5[jj].get('wind_speed')
			WDIR = Miss ; WDIR = READ5[jj].get('wind_dir')
			if WSPD == None : WSPD = Miss
			if WDIR == None : WDIR = Miss
			if WDIR == Miss or WSPD == Miss :
				USPD = Miss ; VSPD = Miss
			else:
				USPD = round(-abs(float(WSPD))*sin(np.deg2rad(float(WDIR))),1)
				VSPD = round(-abs(float(WSPD))*cos(np.deg2rad(float(WDIR))),1)
			if RTIME[14:16] == '00' :
				#print(STNID, STN, YMD, SST, WHT,WSPD,WDIR,USPD, VSPD,'해양부이')
				data1.append([STNID, STN, YMD, SST, WHT,WSPD,WDIR,USPD, VSPD,'해양부이'])              # data1[]에 자료 붙여넣기
			jj = jj + 1

	elif 'data' in READ1 and 'error' in READ4  and 'error' in READ7  :
		READ2 = READ1.get('data') ; READ3 = READ1.get('meta')
		STN = READ3.get('obs_post_name') ; STNID = READ3.get('obs_post_id')
	
		jj = 0
		while jj < len(READ2)-1:
			RTIME = READ2[jj].get('record_time')
			YMD = RTIME[0:4]+RTIME[5:7]+RTIME[8:10]+RTIME[11:13]
			SST = Miss ; 	WHT = Miss ; 	WSPD = Miss ; WDIR = Miss
			SST = READ2[jj].get('water_temp')
			if SST == None : SST = Miss
			if WDIR == Miss or WSPD == Miss :
				USPD = Miss ; VSPD = Miss
			else:
				USPD = round(-abs(float(WSPD))*sin(np.deg2rad(float(WDIR))),1)
				VSPD = round(-abs(float(WSPD))*cos(np.deg2rad(float(WDIR))),1)
			if RTIME[14:16] == '00' :
				#print(STNID, STN, YMD, SST, WHT,WSPD,WDIR,USPD, VSPD,'해양부이')
				data1.append([STNID, STN, YMD, SST, WHT,WSPD,WDIR,USPD,VSPD,'해양부이'])              # data1[]에 자료 붙여넣기
			jj = jj + 1
	ii = ii + 1

data1_len = len(data1)
#[통합자료]
OUT_FNAME=dir1+'/OBS_Daily/OBS_KHOA_'+yesterday+'.csv'
with open(OUT_FNAME,'w',encoding='utf8') as file:
	file.write('지점번호,지점명,년월일시,수온,파고,풍속,풍향,U풍속,V풍속,관측소\n')
	ii = 0
	while ii <= data1_len-1:
		file.write(f'{data1[ii][0]},{data1[ii][1]},{data1[ii][2]},{data1[ii][3]},{data1[ii][4]},{data1[ii][5]},{data1[ii][6]},{data1[ii][7]},{data1[ii][8]},{data1[ii][9]}\n')
		ii = ii + 1

print("#KHOA Yesterday OBS data collection Complete==========")