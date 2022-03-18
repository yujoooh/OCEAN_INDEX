#[Geosystem Research : Department of Marine Forecast ]
#[Created by C.K. Park on 2018.10.23]
import json
import urllib.request
import numpy as np
from collections import OrderedDict
from datetime import date, timedelta
from datetime import datetime
from Function.kma_obs_missing_function import Missing_STN
from math import *

print("#KMA Yesterday OBS data collection Start==========")

#[Date Set]===============================================================================================================
today = '20211226'
yesterday = '20211225'
h = 0

dir1 = './Result/'+today

#[KMA API KEY] ==================================================================================================
API_KEY = "Kb%2BKlCpXZ7j3udye3E8YL8w4WRPsUtyadYzDUKAmJ6ZJoNKuLWBWqDJwHOAPuqKuRjPnotzwr2E14sBvyJ7lWw%3D%3D"

#파고부이 http://apis.data.go.kr/1360000/OceanInfoService/getWhBuoy?ServiceKey=Kb%2BKlCpXZ7j3udye3E8YL8w4WRPsUtyadYzDUKAmJ6ZJoNKuLWBWqDJwHOAPuqKuRjPnotzwr2E14sBvyJ7lWw%3D%3D&numOfRows=62&pageNo=1&dataType=JSON&searchTime=20200428
#국내부이 http://apis.data.go.kr/1360000/OceanInfoService/getBuoyObs?ServiceKey=Kb%2BKlCpXZ7j3udye3E8YL8w4WRPsUtyadYzDUKAmJ6ZJoNKuLWBWqDJwHOAPuqKuRjPnotzwr2E14sBvyJ7lWw%3D%3D&numOfRows=17&pageNo=1&dataType=JSON&searchTime=20200428
#국내등표 http://apis.data.go.kr/1360000/OceanInfoService/getLhObs?ServiceKey=Kb%2BKlCpXZ7j3udye3E8YL8w4WRPsUtyadYzDUKAmJ6ZJoNKuLWBWqDJwHOAPuqKuRjPnotzwr2E14sBvyJ7lWw%3D%3D&numOfRows=8&pageNo=1&dataType=JSON&searchTime=20200428

#[Number of KMA OBS STATION]
WNUM = 100  # 파고부이 관측지점 수  62
BNUM = 100 # 국내부이 관측지점 수 16
LNUM = 100  # 국내등표 관측지점 수 -- 파고/수온 정보 미제공 8

data1 = [] # 파고부이 데이터 저장 리스트 생성
data2 = [] # 국내부이 데이터 저장 리스트 생성
data3 = [] # 국내등표 데이터 저장 리스트 생성 -- 파고/수온 정보 미제공
while h < 24:
	hr = (f'{h:02d}')
	#print(hr,yesterday+hr)
	
	WBUOY_URL = "http://apis.data.go.kr/1360000/OceanInfoService/getWhBuoy?ServiceKey="  #파고부이
	BBUOY_URL = "http://apis.data.go.kr/1360000/OceanInfoService/getBuoyObs?ServiceKey=" #국내부이
	LAMP_URL = "http://apis.data.go.kr/1360000/OceanInfoService/getLhObs?ServiceKey=" #국내등표 -- 파고/수온 정보 미제공

	Miss = -999.0 #결측값 
	#-----------------------------------[파고부이 자료수집]----------------------------------------------------
	WURL = WBUOY_URL + API_KEY + "&numOfRows=" + str(WNUM) + "&pageNo=1&dataType=JSON"+"&searchTime=" + yesterday+hr
	#print(WURL)
	WPAGE = urllib.request.urlopen(WURL)
	WREAD = WPAGE.read()
	WJSON = json.loads(WREAD)
	#print(WJSON)
	
	READ1 = WJSON.get('response')
	READ2 = READ1.get('body')
	READ3 = READ2.get('items')
	if 'item' in READ3 :
		READ4 = READ3.get('item')
		READ5 = READ2.get('totalCount')
		
		ii = 0
		WBUOY_LIST=[]
		WBUOYID_LIST=[]
		while ii < READ5:
			OBS = '파고부이'
			STNID = READ4[ii].get('stnId') #지점번호
			STN = READ4[ii].get('name').strip()  #지점명
			LAT = str(READ4[ii].get('lat')) # 위도
			LON = str(READ4[ii].get('lon')) # 경도
			WHT = READ4[ii].get('whSig') #최대파고
			SST = READ4[ii].get('tw')   #수온
			WSPD = Miss
			WDIR = Miss
			USPD = Miss
			VSPD = Miss
			if WHT == 0.0 or WHT == ""  : WHT = Miss
			if SST == 0.0 or SST == "" : SST = Miss
			WBUOY_LIST = Missing_STN().WBUOY(ii,STN,WBUOY_LIST)
			WBUOYID_LIST = Missing_STN().WBUOYID(ii,STNID,WBUOYID_LIST)
			data1.append([str(STNID),STN,yesterday+hr,SST,WHT,WSPD,WDIR,USPD,VSPD,'파고부이'])
			if ii == READ5-1 and len(WBUOY_LIST) > 0 and len(WBUOYID_LIST) : 
				for jj in WBUOYID_LIST : STNID = jj
				for jj in WBUOY_LIST : STN = jj
				WHT = Miss
				SST = Miss
				#WSPD = Miss
				#WDIR = Miss
				data1.append([str(STNID),STN,yesterday+hr,SST,WHT,WSPD,WDIR,USPD,VSPD,'파고부이'])
			
			#print(WBUOY_LIST)
			#print(ii,STNID,STN.strip(),yesterday+hr,SST,WHT,WSPD)
			ii = ii + 1
	else :
		print('no data')
		
	#-----------------------------------[해양기상부이 자료수집]----------------------------------------------------
	BURL = BBUOY_URL + API_KEY + "&numOfRows=" + str(BNUM) + "&pageNo=1&dataType=JSON"+"&searchTime=" + yesterday+hr
	BPAGE = urllib.request.urlopen(BURL)
	BREAD = BPAGE.read()
	BJSON = json.loads(BREAD)
	#print(WJSON)
	
	READ1 = BJSON.get('response') ; CHECK2 = READ1.get('header') ; CHECK3 = CHECK2.get('resultCode')
	if CHECK3 == '03' :
		data2.append([str('21229'),'울릉도',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22101'),'덕적도',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22102'),'칠발도',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22103'),'거문도',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22104'),'거제도',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22105'),'동해',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22106'),'포항',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22107'),'마라도',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22108'),'외연도',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22183'),'신안',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22184'),'추자도',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22185'),'인천',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22186'),'부안',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22187'),'서귀포',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22188'),'통영',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22189'),'울산',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		data2.append([str('22190'),'울진',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'해양기상'])
		
	else :
		READ2 = READ1.get('body')
		READ3 = READ2.get('items')
		if 'item' in READ3 :
			READ4 = READ3.get('item')
			READ5 = READ2.get('totalCount')
		
			ii = 0
			BBUOY_LIST=[]
			BBUOYID_LIST=[]
			while ii < READ5 :
				OBS = '해양기상부이'
				STNID = READ4[ii].get('stnId') #지점번호
				STN = READ4[ii].get('name').strip()  #지점명
				#LAT = str(READ4[ii].get('lat')) # 위도 -- 정보미제공
				#LON = str(READ4[ii].get('lon')) # 경도 -- 정보미제공
				WHT = READ4[ii].get('whSig') #유의파고
				SST = READ4[ii].get('tw')   #수온
				WSPD = READ4[ii].get('ws1')   #풍속
				WDIR = READ4[ii].get('wd1')   #풍속
				if WHT == 0.0 or WHT == "" : WHT = Miss
				if SST == 0.0 or SST == "" : SST = Miss
				if WSPD == 0.0 or WSPD== "" : WSPD = Miss
				if WDIR == 0.0 or WDIR == "": WDIR = Miss
				if WDIR == Miss and WSPD == Miss :
					USPD = Miss ; VSPD = Miss
				else:
					USPD = round(-abs(WSPD)*sin(np.deg2rad(WDIR)),1)
					VSPD = round(-abs(WSPD)*cos(np.deg2rad(WDIR)),1)
					#print(WSPD, WDIR, USPD, VSPD)
				BBUOY_LIST = Missing_STN().BBUOY(ii,STN,BBUOY_LIST)
				BBUOYID_LIST = Missing_STN().BBUOYID(ii,STNID,BBUOYID_LIST)
				if yesterday+hr == '2019100902' : print(STNID, BBUOYID_LIST,STN,BBUOY_LIST,yesterday+hr,len(BBUOY_LIST),len(BBUOYID_LIST))
				data2.append([str(STNID),STN,yesterday+hr,SST,WHT,WSPD,WDIR,USPD,VSPD,'해양기상'])
				if ii == READ5-1 and len(BBUOYID_LIST) > 0 and len(BBUOY_LIST) > 0 : 
					for jj in BBUOYID_LIST : STNID = jj
					for jj in BBUOY_LIST: STN = jj
					WHT = Miss
					SST = Miss
					WSPD = Miss
					WDIR = Miss
					data2.append([str(STNID),STN.strip(),yesterday+hr,SST,WHT,WSPD,WDIR,USPD,VSPD,'해양기상'])
					print(data2.append)
				ii = ii + 1
				#print(ii,STNID,STN.strip(),yesterday+hr,SST,WHT,WSPD)
	#-----------------------------------[국내등표 자료수집]----------------------------------------------------
	LURL = LAMP_URL + API_KEY + "&numOfRows=" + str(LNUM) + "&pageNo=1&dataType=JSON"+"&searchTime=" + yesterday+hr
	LPAGE = urllib.request.urlopen(LURL)
	LREAD = LPAGE.read()
	LJSON = json.loads(LREAD)
	#print(LURL)
	
	READ1 = LJSON.get('response') ; CHECK2 = READ1.get('header') ; CHECK3 = CHECK2.get('resultCode')
	if CHECK3 == '03' :
		data3.append([str('955'),'서수도',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'국내등표'])
		data3.append([str('956'),'가대암',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'국내등표'])
		data3.append([str('957'),'십이동파',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'국내등표'])
		data3.append([str('958'),'갈매여',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'국내등표'])
		data3.append([str('959'),'해수서',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'국내등표'])
		data3.append([str('960'),'지귀도',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'국내등표'])
		data3.append([str('961'),'간여암',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'국내등표'])
		data3.append([str('963'),'이덕서',yesterday+hr,Miss,Miss,Miss,Miss,Miss,Miss,'국내등표'])
                
	else :
		READ2 = READ1.get('body')
		READ3 = READ2.get('items')
		if 'item' in READ3 :
			READ4 = READ3.get('item')
			READ5 = READ2.get('totalCount')
			ii = 0
			LAMP_LIST=[]
			LAMPID_LIST=[]
			while ii < READ5:
				OBS = '국내등표'
				STNID = READ4[ii].get('stn_id') #지점번호
				STN = READ4[ii].get('name').strip()  #지점명
				#LAT = str(READ4[ii].get('lat')) # 위도 -- 정보미제공
				#LON = str(READ4[ii].get('lon')) # 경도 -- 정보미제공
				WHT = Miss
				SST = Miss
				WSPD = READ4[ii].get('ws')   #풍속
				WDIR = READ4[ii].get('wd')   #풍속
				if WSPD == 0.0 or WSPD == "": WSPD = Miss
				if WDIR == 0.0 or WDIR == "": WDIR = Miss
				if WDIR == Miss and WSPD == Miss :
					USPD = Miss ; VSPD = Miss
				else:
					USPD = round(-abs(float(WSPD))*sin(np.deg2rad(float(WDIR))),1)
					VSPD = round(-abs(float(WSPD))*cos(np.deg2rad(float(WDIR))),1)
				LAMP_LIST = Missing_STN().LAMP(ii,STN,LAMP_LIST)
				LAMPID_LIST = Missing_STN().LAMPID(ii,STNID,LAMPID_LIST)
				data3.append([str(STNID),STN,yesterday+hr,SST,WHT,WSPD,WDIR,USPD,VSPD,'국내등표'])
				if ii == READ5-1 and len(LAMP_LIST) > 0 and len(LAMPID_LIST) > 0 : 
					for jj in LAMPID_LIST : STNID = jj
					for jj in LAMP_LIST : STN = jj
					#WHT = Miss
					#SST = Miss
					WSPD = Miss
					WDIR = Miss
					data3.append([str(STNID),STN,yesterday+hr,SST,WHT,WSPD,WDIR,USPD,VSPD,'국내등표'])
				ii = ii + 1
			#print(ii,STNID,STN.strip(),yesterday+hr,SST,WHT,WSPD)
				
	h = h + 1
data1.sort(); data1_len = len(data1) ; data2.sort(); data2_len = len(data2) ; data3.sort(); data3_len = len(data3)
		

com = [] # 1일자료 통합파일
com = data1+data2+data3
com_len = len(com)

#[obs data writing]---------------------------------------------------------------------------------------------
#[통합자료]

OUT_FNAME=dir1+'/OBS_Daily/OBS_KMA_'+yesterday+'.csv'
with open(OUT_FNAME,'w',encoding='utf8') as file:
	file.write('지점번호,지점명,년월일시,수온,파고,풍속,풍향,U풍속,V풍속,관측소\n')
	ii = 0
	while ii <= com_len-1:
		file.write(f'{com[ii][0]},{com[ii][1]},{com[ii][2]},{com[ii][3]},{com[ii][4]},{com[ii][5]},{com[ii][6]},{com[ii][7]},{com[ii][8]},{com[ii][9]}\n')
		ii = ii + 1

print("#KMA Yesterday OBS data collection Complete==========")


##[파고부이] 개별파일
#ii = 0
#while ii < data1_len-1:
#	STN=data1[ii][1]
#	print(STN,ii,data1[ii][0])
#	OUT_FNAME='./Result/OBS_Daily/1_'+yesterday+'_'+str(STN)+'.csv'
#	end = ii + 23
#	with open(OUT_FNAME,'w') as file:
#		file.write('지점,년월일시,수온,파고,풍속\n')
#		while ii <= end : 
#			file.write(f'{data1[ii][1]},{data1[ii][2]},{data1[ii][3]},{data1[ii][4]},{data1[ii][5]}\n')
#			ii = ii + 1
#	file.close()
#
##[해양기상부이]
#ii = 0
#while ii < data2_len-1:
#	STN=data2[ii][1]
#	#print(STN,ii,data2[ii][0])
#	OUT_FNAME='./Result/OBS_Daily/2_'+yesterday+'_'+str(STN)+'.csv'
#	end = ii + 23
#	with open(OUT_FNAME,'w') as file:
#		file.write('지점,년월일시,수온,파고,풍속\n')
#		while ii <= end : 
#			file.write(f'{data2[ii][1]},{data2[ii][2]},{data2[ii][3]},{data2[ii][4]},{data2[ii][5]}\n')
#			ii = ii + 1
#	file.close()
#
##[국내등표]
#ii = 0
#while ii < data3_len-1:
#	STN=data3[ii][1]
#	#print(STN,ii,data3[ii][0])
#	OUT_FNAME='./Result/OBS_Daily/3_'+yesterday+'_'+str(STN)+'.csv'
#	end = ii + 23
#	with open(OUT_FNAME,'w') as file:
#		file.write('지점,년월일시,수온,파고,풍속\n')
#		while ii <= end : 
#			file.write(f'{data3[ii][1]},{data3[ii][2]},{data3[ii][3]},{data3[ii][4]},{data3[ii][5]}\n')
#			ii = ii + 1
#	file.close()
