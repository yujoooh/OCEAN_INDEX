#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2020.08.11]

import os
import json
import urllib.request
import numpy as np
from collections import OrderedDict
from datetime import date, timedelta
from datetime import datetime


print("#KMA Forecast_CITY data collection Start========")

#[Date Set]==================================================================================================
yesterday = (date.today() + timedelta(-1)).strftime('%Y%m%d')
today = str(datetime.today().strftime('%Y%m%d'))
afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')
afterday3 = (date.today() + timedelta(3)).strftime('%Y%m%d')
afterday4 = (date.today() + timedelta(4)).strftime('%Y%m%d')
afterday5 = (date.today() + timedelta(5)).strftime('%Y%m%d')
afterday6 = (date.today() + timedelta(6)).strftime('%Y%m%d')
hr = str(datetime.today().strftime("%H"))
#print(today, afterday1, afterday2, hr)

#[폴더생성]
dir1 = './Result/'+today
if not os.path.exists(dir1): os.makedirs(dir1)

#[KMA API KEY and URL]] ==================================================================================================
API_KEY = "%2FtpOfcOL1h6oaaa5fQmJGu%2FUO%2FMPmyJLomOzHymKjaFGJ8mL1dxspAvT5TtMFVqoT5HoFgVL19xe%2BrQTB4cluQ%3D%3D" #일일 트래픽 100000 # 단기예보 key(2021.08.12)
MID_API_KEY = "%2FtpOfcOL1h6oaaa5fQmJGu%2FUO%2FMPmyJLomOzHymKjaFGJ8mL1dxspAvT5TtMFVqoT5HoFgVL19xe%2BrQTB4cluQ%3D%3D" #일일 트래픽 100000

#Check KMA API access
#동네예보 http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey=%2FtpOfcOL1h6oaaa5fQmJGu%2FUO%2FMPmyJLomOzHymKjaFGJ8mL1dxspAvT5TtMFVqoT5HoFgVL19xe%2BrQTB4cluQ%3D%3D&numOfRows=225&pageNo=1&dataType=JSON&base_date=20210818&base_time=0200&nx=46&ny=71
#중기예보 http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst?serviceKey=%2FtpOfcOL1h6oaaa5fQmJGu%2FUO%2FMPmyJLomOzHymKjaFGJ8mL1dxspAvT5TtMFVqoT5HoFgVL19xe%2BrQTB4cluQ%3D%3D&numOfRows=100&pageNo=1&regId=11B00000&tmFc=202008210600&dataType=JSON
CITY_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey="  #단기예보 URL(2021.08.12, 동네예보 폐기예정, 단기예보에 기존사항 포함)
MID_URL  = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst?serviceKey="    #중기예보(육상) URL

#[해수욕지수 정보 수집] ==================================================================================================
data1 = [] # 동네예보 기온 정보 저장
data2 = [] # 동네예보 날씨 정보 저장
data3 = [] # 동네예보 풍속 정보 저장
data4 = [] # 동네예보 파고 정보 저장
data5 = [] # 동네예보 강수량 정보 수집
data6 = [] # 동네예보 강수확률 정보 수집
data7 = [] # 동네예보 습도 정보 수집
com = [] # 동네예보 수집자료 결합


#동네예보자료 정상 갱신여부 check 
CHECK1 = CITY_URL + API_KEY + "&numOfRows=225&pageNo=1&dataType=JSON"+ "&base_date="+ today + "&base_time=0200&nx=46&ny=71"
print(CHECK1)
CPAGE = urllib.request.urlopen(CHECK1)
CREAD = CPAGE.read() ; CJSON = json.loads(CREAD)
READ1 = CJSON.get('response') ; CHECK2 = READ1.get('header') ; CHECK3 = CHECK2.get('resultCode')
if CHECK3 == '10' :
	print('No data')
elif CHECK3 == '00' :
	READ2 = READ1.get('body');READ3 = READ2.get('items');READ4 = READ3.get('item')
	jj = 0 ; AA = 0; BB = 0 ; CC = 0; DD = 0 ; EE = 0
	while jj <= len(READ4)-1:
		CATEGORY = READ4[jj].get('category')
		if 'TMP' in CATEGORY : AA += 1
		if 'SKY' in CATEGORY : BB += 1
		if 'WSD' in CATEGORY : CC += 1
		if 'WAV' in CATEGORY : DD += 1
		if 'PCP' in CATEGORY : EE += 1
		jj += 1
	#print(AA, BB, CC, DD, EE) # 정상일 경우 각각 20 20 20 20 10개
	
	if int(hr) >= 14 and AA == 20 and BB == 20 and CC == 20 and DD == 20 and EE == 10 :
		#base_time fixed [0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300] / #base_time 제공시간 [0210, 0510, 0810, 1110, 1410, 1710, 2010, 2310]
		base_time = ['0500', '0800', '1400']
	else :
		base_time = ['0500', '0800']
		hr = 9
	
	#[INFO FILE NAME READ]
	INDEX_LIST = ['JEJU','BUSAN','YEOSU','INCHEON','GANGNEUNG','TAEAN']
	#INDEX_LIST = ['JEJU','BUSAN','YEOSU']
	for LIST in INDEX_LIST:
		#[READ each Info Data] ========================================================================================
		POINT_INF = open('./Info/'+LIST+'_Point_Info.csv','r',encoding='utf8')
		INF = [str(INFO) for INFO in POINT_INF.read().split()]
		INF_LEN = len(INF)
		print(today,LIST,"City forecast data collection", INF_LEN)
		ii = 1
		while ii <= INF_LEN-1 :
			DEV = INF[ii].split(',')
			FC_AREA = DEV[0]; STN = DEV[1] ; AREA = DEV[2]; NAME = DEV[3] ; CITY_X = int(DEV[18]) ; CITY_Y = int(DEV[19])
			
			#-----------------------------------[동네예보 자료수집]----------------------------------------------------
			CURL2 = CITY_URL + API_KEY +"&numOfRows=809&pageNo=1&dataType=JSON"+"&base_date=" + yesterday + "&base_time=2300&nx=" + str(CITY_X) + "&ny=" + str(CITY_Y) #어제 20시 예보자료, 금일 00시 03시 자료 수집을 위함
			#print(CURL2)

			CPAGE2 = urllib.request.urlopen(CURL2)
			CREAD2 = CPAGE2.read() ; 	CJSON2 = json.loads(CREAD2)
			READ5 = CJSON2.get('response')#.decode('euc-kr').encode('utf-8')
			READ6 = READ5.get('body')
			READ7 = READ6.get('items')
			READ8 = READ7.get('item')
			CITY_LEN2 = len(READ8)

			#[COM00 : 00시~05시, COM06:06시~08시, COM09:09시~12시, COM13:13시~18시, COM19:19시~23시]
			DAY1_RAIN_COM00 = 0 ; DAY1_RAIN_COM06 = 0 ; DAY1_RAIN_COM09 = 0 ; DAY1_RAIN_COM13 = 0 ;	DAY1_RAIN_COM19 = 0 
			DAY2_RAIN_COM00 = 0 ; DAY2_RAIN_COM06 = 0 ; DAY2_RAIN_COM09 = 0 ; DAY2_RAIN_COM13 = 0 ;	DAY2_RAIN_COM19 = 0 
			DAY3_RAIN_COM00 = 0 ; DAY3_RAIN_COM06 = 0 ; DAY3_RAIN_COM09 = 0 ; DAY3_RAIN_COM13 = 0 ;	DAY3_RAIN_COM19 = 0 

			jj = 0
			while jj <= CITY_LEN2-1 : # 전일 23시 예측자료 기반 당일 00시~05시 자료 수집
				CATEGORY2 = READ8[jj].get('category')

				if CATEGORY2 == 'TMP': # 기온정보 수집 : 1시간 간격
					DATE2 = READ8[jj].get('fcstDate')
					TIME2 = READ8[jj].get('fcstTime')
					AIRT2 = READ8[jj].get('fcstValue')
					if str(DATE2) == today and (str(TIME2) == '0000' or str(TIME2) == '0100' or str(TIME2) == '0200' or str(TIME2) == '0300' or str(TIME2) == '0400' or str(TIME2) == '0500'):
						data1.append([FC_AREA, STN, NAME, DATE2, TIME2[0:2], float(AIRT2)])
		
				if CATEGORY2 == 'SKY': # 날씨정보 수집 : 1시간 간격 [맑음:1, 구름조금:2, 구름많음:3, 흐림:4]
					DATE2 = READ8[jj].get('fcstDate')
					TIME2 = READ8[jj].get('fcstTime')
					SKY2 = READ8[jj].get('fcstValue')
					if str(DATE2) == today and (str(TIME2) == '0000' or str(TIME2) == '0100' or str(TIME2) == '0200' or str(TIME2) == '0300' or str(TIME2) == '0400' or str(TIME2) == '0500'):
						data2.append([FC_AREA, STN, NAME, DATE2, TIME2[0:2], SKY2])
					# 전일 23시 예측 자료로 금일 00 03시 자료 수집

				if CATEGORY2 == 'WSD': # 풍속정보 수집 : 1시간 간격
					DATE2 = READ8[jj].get('fcstDate')
					TIME2 = READ8[jj].get('fcstTime')
					WSD2 = READ8[jj].get('fcstValue')
					if str(DATE2) == today and (str(TIME2) == '0000' or str(TIME2) == '0100' or str(TIME2) == '0200' or str(TIME2) == '0300' or str(TIME2) == '0400' or str(TIME2) == '0500'):
						data3.append([FC_AREA, STN, NAME, DATE2, TIME2[0:2], float(WSD2)])

				if CATEGORY2 == 'PCP': # 강수정보 수집 : 1시간 간격
					DATE2 = READ8[jj].get('fcstDate')
					TIME2 = READ8[jj].get('fcstTime')
					RAIN_AMT2 = READ8[jj].get('fcstValue')
					if RAIN_AMT2 == "강수없음" :
						RAIN_AMT2 = '0.0'

					elif RAIN_AMT2 == "50mm이상" :
						RAIN_AMT2 = '50.0'

					elif RAIN_AMT2 == "1.0mm 미만" :
						RAIN_AMT2 = '0.0'						
					else :
						RAIN_AMT2 = RAIN_AMT2.replace('mm','')
						RAIN_AMT2 = RAIN_AMT2.replace('~',',')
						RAIN_AMT2 = RAIN_AMT2.split(',')
						RAIN_AMT2 = RAIN_AMT2[0]

					#강수량 누적# 00~05
					if str(DATE2) == today and (str(TIME2) == '0000' or str(TIME2) == '0100' or str(TIME2) == '0200' or str(TIME2) == '0300' or str(TIME2) == '0400' or str(TIME2) == '0500'):
						DAY1_RAIN_COM00 = DAY1_RAIN_COM00 + float(RAIN_AMT2)
					if str(DATE2) == today and (str(TIME2) == '0000' or str(TIME2) == '0100' or str(TIME2) == '0200' or str(TIME2) == '0300' or str(TIME2) == '0400' or str(TIME2) == '0500'):
						data5.append([FC_AREA, STN, NAME, DATE2, TIME2[0:2], RAIN_AMT2, DAY1_RAIN_COM00])

				if CATEGORY2 == 'POP': # 강수확률정보 수집 : 1시간 간격
					DATE2 = READ8[jj].get('fcstDate')
					TIME2 = READ8[jj].get('fcstTime')
					POP2 = READ8[jj].get('fcstValue')
# 전일 23시 예측 자료로 금일 00 05시 자료 수집 
					if str(DATE2) == today and (str(TIME2) == '0000' or str(TIME2) == '0100' or str(TIME2) == '0200' or str(TIME2) == '0300' or str(TIME2) == '0400' or str(TIME2) == '0500'):
						data6.append([FC_AREA, STN, NAME, DATE2, TIME2[0:2], POP2])

				if CATEGORY2 == 'REH': # 습도정보 수집 : 1시간 간격
					DATE2 = READ8[jj].get('fcstDate')
					TIME2 = READ8[jj].get('fcstTime')
					REH2 = READ8[jj].get('fcstValue')
					# 전일 23시 예측 자료로 금일 00 05시 자료 수집 
					if str(DATE2) == today and (str(TIME2) == '0000' or str(TIME2) == '0100' or str(TIME2) == '0200' or str(TIME2) == '0300' or str(TIME2) == '0400' or str(TIME2) == '0500'):
						data7.append([FC_AREA, STN, NAME, DATE2, TIME2[0:2], REH2])
				jj += 1

			for bt in base_time : # 금일 05시 ~ 모레 23시 자료 수집
				CURL = CITY_URL + API_KEY +"&numOfRows=809&pageNo=1&dataType=JSON"+"&base_date=" + today + "&base_time=" + bt + "&nx=" + str(CITY_X) + "&ny=" + str(CITY_Y)
				#print(CURL)
		
				CPAGE = urllib.request.urlopen(CURL)
				CREAD = CPAGE.read() ; 	CJSON = json.loads(CREAD)
				READ1 = CJSON.get('response')#.decode('euc-kr').encode('utf-8')
				READ2 = READ1.get('body')
				READ3 = READ2.get('items')
				READ4 = READ3.get('item')
				CITY_LEN = len(READ4)

				jjj = 0
				while jjj <= CITY_LEN-1:
					CATEGORY = READ4[jjj].get('category')

					if CATEGORY == 'TMP': # 기온정보 수집 : 1시간 간격
						DATE = READ4[jjj].get('fcstDate')
						TIME = READ4[jjj].get('fcstTime')
						AIRT = READ4[jjj].get('fcstValue')

						if int(hr) < 14 : # 당일 06시 자료가 있는 0500과 최신자료인 0800 base_time사용
							if bt == '0500' and str(DATE) == today and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data1.append([FC_AREA, STN, NAME, DATE, TIME[0:2], float(AIRT)])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200' or str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800' or str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data1.append([FC_AREA, STN, NAME, DATE, TIME[0:2], float(AIRT)])
							elif bt == '0800' and (str(DATE) == afterday1 or str(DATE) == afterday2):
								data1.append([FC_AREA, STN, NAME, DATE, TIME[0:2], float(AIRT)])
						else : # 당일 06시 자료가 있는 0500, 14시 이전자료가 있는 0800, 이후 최신자료인 base_time사용
							if bt == '0500' and str(DATE) == today and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data1.append([FC_AREA, STN, NAME, DATE, TIME[0:2], float(AIRT)])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200' or str(TIME) == '1300' or str(TIME) == '1400'):
								data1.append([FC_AREA, STN, NAME, DATE, TIME[0:2], float(AIRT)])
							elif bt == '1400' and str(DATE) == today and (str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800' or str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data1.append([FC_AREA, STN, NAME, DATE, TIME[0:2], float(AIRT)])					
							elif bt == '1400' and (str(DATE) == afterday1 or str(DATE) == afterday2):
								data1.append([FC_AREA, STN, NAME, DATE, TIME[0:2], float(AIRT)])					
		
					if CATEGORY == 'SKY': # 날씨정보 수집 : 3시간 간격 [맑음:1, 구름많음:3, 흐림:4]
						DATE = READ4[jjj].get('fcstDate')
						TIME = READ4[jjj].get('fcstTime')
						SKY = READ4[jjj].get('fcstValue')

						if int(hr) < 14 : # 당일 06시 자료가 있는 0500과 최신자료인 0800 base_time사용
							if bt == '0500' and str(DATE) == today and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data2.append([FC_AREA, STN, NAME, DATE, TIME[0:2], SKY])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200' or str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800' or str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data2.append([FC_AREA, STN, NAME, DATE, TIME[0:2], SKY])
							elif bt == '0800' and (str(DATE) == afterday1 or str(DATE) == afterday2):
								data2.append([FC_AREA, STN, NAME, DATE, TIME[0:2], SKY])
						else : # 당일 06시 자료가 있는 0500, 14시 이전자료가 있는 0800, 이후 최신자료인 base_time사용
							if bt == '0500' and str(DATE) == today and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data2.append([FC_AREA, STN, NAME, DATE, TIME[0:2], SKY])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200' or str(TIME) == '1300' or str(TIME) == '1400'):
								data2.append([FC_AREA, STN, NAME, DATE, TIME[0:2], SKY])
							elif bt == '1400' and str(DATE) == today and (str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800' or str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data2.append([FC_AREA, STN, NAME, DATE, TIME[0:2], SKY])					
							elif bt == '1400' and (str(DATE) == afterday1 or str(DATE) == afterday2):
								data2.append([FC_AREA, STN, NAME, DATE, TIME[0:2], SKY])	

					if CATEGORY == 'WSD': # 풍속정보 수집 : 1시간 간격
						DATE = READ4[jjj].get('fcstDate')
						TIME = READ4[jjj].get('fcstTime')
						WSD = READ4[jjj].get('fcstValue')

						if int(hr) < 14 : # 당일 06시 자료가 있는 0500과 최신자료인 0800 base_time사용
							if bt == '0500' and str(DATE) == today and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data3.append([FC_AREA, STN, NAME, DATE, TIME[0:2], float(WSD)])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200' or str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800' or str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data3.append([FC_AREA, STN, NAME, DATE, TIME[0:2], float(WSD)])
							elif bt == '0800' and (str(DATE) == afterday1 or str(DATE) == afterday2):
								data3.append([FC_AREA, STN, NAME, DATE, TIME[0:2], float(WSD)])
						else : # 당일 06시 자료가 있는 0500, 14시 이전자료가 있는 0800,  이후 최신자료인 base_time사용
							if bt == '0500' and str(DATE) == today and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data3.append([FC_AREA, STN, NAME, DATE, TIME[0:2], float(WSD)])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200' or str(TIME) == '1300' or str(TIME) == '1400'):
								data3.append([FC_AREA, STN, NAME, DATE, TIME[0:2], float(WSD)])
							elif bt == '1400' and str(DATE) == today and (str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800' or str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data3.append([FC_AREA, STN, NAME, DATE, TIME[0:2], float(WSD)])					
							elif bt == '1400' and (str(DATE) == afterday1 or str(DATE) == afterday2):
								data3.append([FC_AREA, STN, NAME, DATE, TIME[0:2], float(WSD)])	
					
					if CATEGORY == 'PCP': # 강수정보 수집 : 6시간 간격
					    #오전/오후의 강수량 누력자료사용 시 오전은 12시(09~12 최종 누적값), 오후는 18시(13~18최종 누적값) 자료 활용해야함
						DATE = READ4[jjj].get('fcstDate')
						TIME = READ4[jjj].get('fcstTime')
						RAIN_AMT = READ4[jjj].get('fcstValue')
						if RAIN_AMT == "강수없음" :
							RAIN_AMT = '0.0'

						elif RAIN_AMT == "50mm이상" :
							RAIN_AMT = '50.0'

						elif RAIN_AMT == "1.0mm 미만" :
							RAIN_AMT = '0.0'							
							
						else :
							RAIN_AMT = RAIN_AMT.replace('mm','')
							RAIN_AMT = RAIN_AMT.replace('~',',')
							RAIN_AMT = RAIN_AMT.split(',')
							RAIN_AMT = RAIN_AMT[0]

						if int(hr) < 14 : # 당일 06시 자료가 있는 0500과 최신자료인 0800 base_time사용
							#강수량 누적# 00~05 / 06~08 / 09~12 / 13~18 / 19~23
							if bt == '0500' and str(DATE) == today and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'): DAY1_RAIN_COM06 = DAY1_RAIN_COM06 + float(RAIN_AMT)
							if bt == '0800' and str(DATE) == today and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200'): DAY1_RAIN_COM09 = DAY1_RAIN_COM09 + float(RAIN_AMT)
							if bt == '0800' and str(DATE) == today and (str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800'): DAY1_RAIN_COM13 = DAY1_RAIN_COM13 + float(RAIN_AMT)
							if bt == '0800' and str(DATE) == today and (str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'): DAY1_RAIN_COM19 = DAY1_RAIN_COM19 + float(RAIN_AMT)

							if bt == '0800' and str(DATE) == afterday1 and (str(TIME) == '0000' or str(TIME) == '0100' or str(TIME) == '0200' or str(TIME) == '0300' or str(TIME) == '0400' or str(TIME) == '0500'): DAY2_RAIN_COM00 = DAY2_RAIN_COM00 + float(RAIN_AMT)
							if bt == '0800' and str(DATE) == afterday1 and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'): DAY2_RAIN_COM06 = DAY2_RAIN_COM06 + float(RAIN_AMT)
							if bt == '0800' and str(DATE) == afterday1 and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200'): DAY2_RAIN_COM09 = DAY2_RAIN_COM09 + float(RAIN_AMT)
							if bt == '0800' and str(DATE) == afterday1 and (str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800'): DAY2_RAIN_COM13 = DAY2_RAIN_COM13 + float(RAIN_AMT)
							if bt == '0800' and str(DATE) == afterday1 and (str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'): DAY2_RAIN_COM19 = DAY2_RAIN_COM19 + float(RAIN_AMT)

							if bt == '0800' and str(DATE) == afterday2 and (str(TIME) == '0000' or str(TIME) == '0100' or str(TIME) == '0200' or str(TIME) == '0300' or str(TIME) == '0400' or str(TIME) == '0500'): DAY3_RAIN_COM00 = DAY3_RAIN_COM00 + float(RAIN_AMT)
							if bt == '0800' and str(DATE) == afterday2 and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'): DAY3_RAIN_COM06 = DAY3_RAIN_COM06 + float(RAIN_AMT)
							if bt == '0800' and str(DATE) == afterday2 and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200'): DAY3_RAIN_COM09 = DAY3_RAIN_COM09 + float(RAIN_AMT)
							if bt == '0800' and str(DATE) == afterday2 and (str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800'): DAY3_RAIN_COM13 = DAY3_RAIN_COM13 + float(RAIN_AMT)
							if bt == '0800' and str(DATE) == afterday2 and (str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'): DAY3_RAIN_COM19 = DAY3_RAIN_COM19 + float(RAIN_AMT)

							if bt == '0500' and str(DATE) == today and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY1_RAIN_COM06])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200') :
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY1_RAIN_COM09])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY1_RAIN_COM13])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY1_RAIN_COM19])
							
							elif bt == '0800' and str(DATE) == afterday1 and(str(TIME) == '0000' or str(TIME) == '0100' or str(TIME) == '0200' or str(TIME) == '0300' or str(TIME) == '0400' or str(TIME) == '0500'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY2_RAIN_COM00])
							elif bt == '0800' and str(DATE) == afterday1 and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY2_RAIN_COM06])
							elif bt == '0800' and str(DATE) == afterday1 and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200') :
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY2_RAIN_COM09])
							elif bt == '0800' and str(DATE) == afterday1 and (str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY2_RAIN_COM13])
							elif bt == '0800' and str(DATE) == afterday1 and (str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY2_RAIN_COM19])

							elif bt == '0800' and str(DATE) == afterday2 and(str(TIME) == '0000' or str(TIME) == '0100' or str(TIME) == '0200' or str(TIME) == '0300' or str(TIME) == '0400' or str(TIME) == '0500'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY3_RAIN_COM00])
							elif bt == '0800' and str(DATE) == afterday2 and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY3_RAIN_COM06])
							elif bt == '0800' and str(DATE) == afterday2 and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200') :
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY3_RAIN_COM09])
							elif bt == '0800' and str(DATE) == afterday2 and (str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY3_RAIN_COM13])
							elif bt == '0800' and str(DATE) == afterday2 and (str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY3_RAIN_COM19])

						else : # 당일 06시 자료가 있는 0500, 14시 이전자료가 있는 0800,  이후 최신자료인 base_time사용
							#[오늘]
							if bt == '0500' and str(DATE) == today and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'): DAY1_RAIN_COM06 = DAY1_RAIN_COM06 + float(RAIN_AMT)
							if bt == '0800' and str(DATE) == today and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200'): DAY1_RAIN_COM09 = DAY1_RAIN_COM09 + float(RAIN_AMT)
							if bt == '0800' and str(DATE) == today and (str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800'): DAY1_RAIN_COM13 = DAY1_RAIN_COM13 + float(RAIN_AMT)
							if bt == '1400' and str(DATE) == today and (str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'): DAY1_RAIN_COM19 = DAY1_RAIN_COM19 + float(RAIN_AMT)
							#[내일]
							if bt == '1400' and str(DATE) == afterday1 and (str(TIME) == '0000' or str(TIME) == '0100' or str(TIME) == '0200' or str(TIME) == '0300' or str(TIME) == '0400' or str(TIME) == '0500'): DAY2_RAIN_COM00 = DAY2_RAIN_COM00 + float(RAIN_AMT)
							if bt == '1400' and str(DATE) == afterday1 and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'): DAY2_RAIN_COM06 = DAY2_RAIN_COM06 + float(RAIN_AMT)
							if bt == '1400' and str(DATE) == afterday1 and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200'): DAY2_RAIN_COM09 = DAY2_RAIN_COM09 + float(RAIN_AMT)
							if bt == '1400' and str(DATE) == afterday1 and (str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800'): DAY2_RAIN_COM13 = DAY2_RAIN_COM13 + float(RAIN_AMT)
							if bt == '1400' and str(DATE) == afterday1 and (str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'): DAY2_RAIN_COM19 = DAY2_RAIN_COM19 + float(RAIN_AMT)
							#[모레]
							if bt == '1400' and str(DATE) == afterday2 and (str(TIME) == '0000' or str(TIME) == '0100' or str(TIME) == '0200' or str(TIME) == '0300' or str(TIME) == '0400' or str(TIME) == '0500'): DAY3_RAIN_COM00 = DAY3_RAIN_COM00 + float(RAIN_AMT)
							if bt == '1400' and str(DATE) == afterday2 and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'): DAY3_RAIN_COM06 = DAY3_RAIN_COM06 + float(RAIN_AMT)
							if bt == '1400' and str(DATE) == afterday2 and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200'): DAY3_RAIN_COM09 = DAY3_RAIN_COM09 + float(RAIN_AMT)
							if bt == '1400' and str(DATE) == afterday2 and (str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800'): DAY3_RAIN_COM13 = DAY3_RAIN_COM13 + float(RAIN_AMT)
							if bt == '1400' and str(DATE) == afterday2 and (str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'): DAY3_RAIN_COM19 = DAY3_RAIN_COM19 + float(RAIN_AMT)

							#[오늘]
							if bt == '0500' and str(DATE) == today and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY1_RAIN_COM06])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200') :
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY1_RAIN_COM09])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY1_RAIN_COM13])
							elif bt == '1400' and str(DATE) == today and (str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY1_RAIN_COM19])
							#[내일]
							elif bt == '1400' and str(DATE) == afterday1 and(str(TIME) == '0000' or str(TIME) == '0100' or str(TIME) == '0200' or str(TIME) == '0300' or str(TIME) == '0400' or str(TIME) == '0500'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY2_RAIN_COM00])
							elif bt == '1400' and str(DATE) == afterday1 and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY2_RAIN_COM06])
							elif bt == '1400' and str(DATE) == afterday1 and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200') :
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY2_RAIN_COM09])
							elif bt == '1400' and str(DATE) == afterday1 and (str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY2_RAIN_COM13])
							elif bt == '1400' and str(DATE) == afterday1 and (str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY2_RAIN_COM19])
							#[모레]
							elif bt == '1400' and str(DATE) == afterday2 and(str(TIME) == '0000' or str(TIME) == '0100' or str(TIME) == '0200' or str(TIME) == '0300' or str(TIME) == '0400' or str(TIME) == '0500'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY3_RAIN_COM00])
							elif bt == '1400' and str(DATE) == afterday2 and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY3_RAIN_COM06])
							elif bt == '1400' and str(DATE) == afterday2 and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200') :
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY3_RAIN_COM09])
							elif bt == '1400' and str(DATE) == afterday2 and (str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY3_RAIN_COM13])
							elif bt == '1400' and str(DATE) == afterday2 and (str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data5.append([FC_AREA, STN, NAME, DATE, TIME[0:2], RAIN_AMT,DAY3_RAIN_COM19])

					if CATEGORY == 'POP': # 강수확률정보 수집 : 1시간 간격
						DATE = READ4[jjj].get('fcstDate')
						TIME = READ4[jjj].get('fcstTime')
						POP = READ4[jjj].get('fcstValue')

						if int(hr) < 14 : # 당일 06시 자료가 있는 0500과 최신자료인 0800 base_time사용
							if bt == '0500' and str(DATE) == today and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data6.append([FC_AREA, STN, NAME, DATE, TIME[0:2], POP])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200' or str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800' or str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data6.append([FC_AREA, STN, NAME, DATE, TIME[0:2], POP])
							elif bt == '0800' and (str(DATE) == afterday1 or str(DATE) == afterday2):
								data6.append([FC_AREA, STN, NAME, DATE, TIME[0:2], POP])
						else : # 당일 06시 자료가 있는 0500, 14시 이전자료가 있는 0800,  이후 최신자료인 base_time사용
							if bt == '0500' and str(DATE) == today and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data6.append([FC_AREA, STN, NAME, DATE, TIME[0:2], POP])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200' or str(TIME) == '1300' or str(TIME) == '1400'):
								data6.append([FC_AREA, STN, NAME, DATE, TIME[0:2], POP])
							elif bt == '1400' and str(DATE) == today and (str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800' or str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data6.append([FC_AREA, STN, NAME, DATE, TIME[0:2], POP])
							elif bt == '1400' and (str(DATE) == afterday1 or str(DATE) == afterday2):
								data6.append([FC_AREA, STN, NAME, DATE, TIME[0:2], POP])

					if CATEGORY == 'REH': # 풍속정보 수집 : 3시간 간격
						DATE = READ4[jjj].get('fcstDate')
						TIME = READ4[jjj].get('fcstTime')
						REH = READ4[jjj].get('fcstValue')

						if int(hr) < 14 : # 당일 06시 자료가 있는 0500과 최신자료인 0800 base_time사용
							if bt == '0500' and str(DATE) == today and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data7.append([FC_AREA, STN, NAME, DATE, TIME[0:2], REH])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200' or str(TIME) == '1300' or str(TIME) == '1400' or str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800' or str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data7.append([FC_AREA, STN, NAME, DATE, TIME[0:2], REH])
							elif bt == '0800' and (str(DATE) == afterday1 or str(DATE) == afterday2):
								data7.append([FC_AREA, STN, NAME, DATE, TIME[0:2], REH])
						else : # 당일 06시 자료가 있는 0500, 14시 이전자료가 있는 0800,  이후 최신자료인 base_time사용
							if bt == '0500' and str(DATE) == today and (str(TIME) == '0600' or str(TIME) == '0700' or str(TIME) == '0800'):
								data7.append([FC_AREA, STN, NAME, DATE, TIME[0:2], REH])
							elif bt == '0800' and str(DATE) == today and (str(TIME) == '0900' or str(TIME) == '1000' or str(TIME) == '1100' or str(TIME) == '1200' or str(TIME) == '1300' or str(TIME) == '1400'):
								data7.append([FC_AREA, STN, NAME, DATE, TIME[0:2], REH])
							elif bt == '1400' and str(DATE) == today and (str(TIME) == '1500' or str(TIME) == '1600' or str(TIME) == '1700' or str(TIME) == '1800' or str(TIME) == '1900' or str(TIME) == '2000' or str(TIME) == '2100' or str(TIME) == '2200' or str(TIME) == '2300'):
								data7.append([FC_AREA, STN, NAME, DATE, TIME[0:2], REH])
							elif bt == '1400' and (str(DATE) == afterday1 or str(DATE) == afterday2):
								data7.append([FC_AREA, STN, NAME, DATE, TIME[0:2], REH])
					jjj += 1

			#-----------------------------------[중기예보 자료수집]----------------------------------------------------
			#동네예보자료 정상 갱신여부 check 
			if LIST == 'JEJU' : Region_code = '11G00000' # 제주도 중기육상예보구역 코드정보
			if LIST == 'BUSAN' : Region_code = '11H20000' # 부산,울산,경남 중기육상예보구역 코드정보
			if LIST == 'YEOSU' : Region_code = '11F20000' # 광주,전라남도 중기육상예보구역 코드정보
			if LIST == 'INCHEON' : Region_code = '11B00000' # 서울,인천,경기 중기육상예보구역 코드정보
			if LIST == 'GANGNEUNG' : Region_code = '11D20000' # 강원도영동 중기육상예보구역 코드정보
			if LIST == 'TAEAN' : Region_code = '11C20000' # 대전,세종,충남 중기육상예보구역 코드정보
			MURL = MID_URL + MID_API_KEY + "&numOfRows=100&pageNo=1&regId="+Region_code+"&tmFc="+ today+"0600&dataType=JSON"

			#print(MURL)
			MPAGE = urllib.request.urlopen(MURL)
			MREAD = MPAGE.read() ; MJSON = json.loads(MREAD)
			MREAD1 = MJSON.get('response') ; MCHECK1 = MREAD1.get('header') ; MCHECK2 = MCHECK1.get('resultCode')
			if MCHECK2 == '03' :
				print('No Data')
			else : 
				MPAGE = urllib.request.urlopen(MURL)
				MREAD = MPAGE.read() ; MJSON = json.loads(MREAD)
				MREAD1 = MJSON.get('response')#.decode('euc-kr').encode('utf-8')
				MREAD2 = MREAD1.get('body')
				MREAD3 = MREAD2.get('items')
				MREAD4 = MREAD3.get('item')
				ll = 3
				kk = 0
				while ll <= 6 : 
					if kk%2 == 0 : AF = 'A'
					if kk%2 != 0 : AF = 'P'
					TM = 'wf' + str(ll) + AF + 'm' # 날씨 조회 시간 선택
					RTM = 'rnSt' + str(ll) + AF + 'm' # 강수확률 조회 시간 선택
					DAY_SKY = MREAD4[0].get(TM)
					DAY_RPROB = MREAD4[0].get(RTM)
					if DAY_SKY == '맑음' :
						SKY2 = '1'
					elif DAY_SKY == '구름많음' or DAY_SKY == '구름많고 비' or DAY_SKY == '구름많고 눈' or DAY_SKY == '구름많고 비/눈' or DAY_SKY == '구름많고 눈/비':
						SKY2 = '3'
					elif DAY_SKY == '흐림' or DAY_SKY == '흐리고 비' or DAY_SKY == '흐리고 눈' or DAY_SKY == '흐리고 비/눈' or DAY_SKY == '흐리고 눈/비' :
						SKY2 = '4'
					afday = (date.today() + timedelta(ll)).strftime('%Y%m%d')
					if AF == 'A' : 
						HR2 = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
						for HH in HR2 : 
							data1.append([FC_AREA, STN, NAME, afday, HH, 0])         # 동네예보 기온 마지막 시간자료 채우기
							data2.append([FC_AREA, STN, NAME, afday, HH, SKY2])        # 중기예보 날씨 (오전/오후 결과 3시간 단위로 채워 넣기)
							data3.append([FC_AREA, STN, NAME, afday, HH, 0])         # 동네예보 풍속 마지막 시간자료 채우기
							data5.append([FC_AREA, STN, NAME, afday, HH, 0.0, 0.0])         # 동네예보 강수량 0으로 채우기
							data6.append([FC_AREA, STN, NAME, afday, HH, DAY_RPROB])   # 중기예보 강수확률(오전/오후 결과 3시간 단위로 채워 넣기)
							data7.append([FC_AREA, STN, NAME, afday, HH, 0])         # 동네예보 상대습도 마지막 시간자료 채우기
					elif AF == 'P' :
						HR2 = ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
						for HH in HR2 : 
							data1.append([FC_AREA, STN, NAME, afday, HH, 0])         # 동네예보 기온 마지막 시간자료 채우기
							data2.append([FC_AREA, STN, NAME, afday, HH, SKY2])        # 중기예보 날씨 (오전/오후 결과 3시간 단위로 채워 넣기)
							data3.append([FC_AREA, STN, NAME, afday, HH, 0])         # 동네예보 풍속 마지막 시간자료 채우기
							data5.append([FC_AREA, STN, NAME, afday, HH, 0.0, 0.0])         # 동네예보 강수량 0으로 채우기
							data6.append([FC_AREA, STN, NAME, afday, HH, DAY_RPROB])   # 중기예보 강수확률(오전/오후 결과 3시간 단위로 채워 넣기)
							data7.append([FC_AREA, STN, NAME, afday, HH, 0])         # 동네예보 상대습도 마지막 시간자료 채우기
					#print(ii, jjj, ll, kk)
					kk += 1
					if kk%2 == 0 : ll += 1
			ii = ii + 1

		#for PP in data1 : print(PP)		
		#print(len(data1), len(data2), len(data3), len(data4), len(data5), len(data6), len(data7))


		# [시계열용 자료 *_CITY.csv] #3시간 단위 정렬
		ii = 0
		while ii <= len(data1)-1 :
			AIR_TEMP = data1[ii][5]   # 기온(℃)
			SKY_STATUS = data2[ii][5] # 하늘상태[맑음:1, 구름많음:3, 흐림:4]
			WIND_SPD = data3[ii][5]   # 풍속(m/s)
			#WAVE_HGT = data4[ii][4]   # 파고(m)
			RAIN_AMT = data5[ii][5]   # 강수량(mm)
			RAIN_ACC = data5[ii][6]   # 누적 강수량(mm) : 00시~05시, 06시~08시, 09시~12시, 13시~18시, 19시~23시 / 누력자료 사용 시 오전은 12시(09~12 최종 누적값), 오후는 18시(13~18최종 누적값) 자료 활용해야함
			RAIN_PROB = data6[ii][5]  # 강수확률(%)
			REL_HU = data7[ii][5]     # 상대습도(%)

			#           FCST_AREA         STN           지역           날짜          시간                       
			com.append([data1[ii][0], data1[ii][1], data1[ii][2], data1[ii][3], data1[ii][4], AIR_TEMP, WIND_SPD, SKY_STATUS, RAIN_AMT, RAIN_ACC, RAIN_PROB, REL_HU])
			ii += 1
		with open(dir1+'/'+LIST+'_CITY.csv','w',encoding='utf8') as file:
			file.write('FCST_AREA,STN,NAME,DATE,HR,TEMP,WIND_SPD,SKY,RAIN_AMT,RAIN_ACC,RAIN_PROB,REL_HU\n')
			for i in com:
				#print(type(i[0]),type(i[1]),type(i[2]),type(i[3]),type(i[4]),type(i[5]),type(i[6]),type(i[7]))
				file.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}\n'.format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11]))
		del data1[:] ; del data2[:] ;del data3[:] ;del data4[:] ;del data5[:];del data6[:];del data7[:];del com[:]


	print("#KMA Forecast_CITY data collection Complete========")
