#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.04.11] edit 19.08.22
import sys
import os
import numpy as np
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime
from Function.sdeq_function import IndexScore, SD_time_cal
from Function.statistic_function import Statistic

print("#SDEQ FCST_INDEX and SERVICE INDEX CREAT Start==========")

#[Date set] ==============================================================================================
#[Auto date set]
today = str(datetime.today().strftime('%Y%m%d'))
afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')
afterday3 = (date.today() + timedelta(3)).strftime('%Y%m%d')
afterday4 = (date.today() + timedelta(4)).strftime('%Y%m%d')
afterday5 = (date.today() + timedelta(5)).strftime('%Y%m%d')
afterday6 = (date.today() + timedelta(6)).strftime('%Y%m%d')

#[Manual date set]
#today = str(date(2019,11,29).strftime('%Y%m%d'))
#afterday1 = (date(2019,11,29) + timedelta(1)).strftime('%Y%m%d')
#afterday2 = (date(2019,11,29) + timedelta(2)).strftime('%Y%m%d')
#print(today, afterday1, afterday2)

dir1 = './Result/'+today

#[Model Data path] =======================================================================================
MPATH = './Model_Data/'
WRF_FNAME = 'WRF_' + str(today) + '.nc'          # WRF_DM2 - KHOA

INFILE_2 = MPATH+WRF_FNAME

#[READ Model_Data] =======================================================================================
#[WRF]
DATA = Dataset(INFILE_2, mode='r')
TEMP = DATA.variables['Tair'][:,:,:]  #[t,y,x]
U_WIND = DATA.variables['Uwind'][:,:,:]  #[t,y,x]
V_WIND = DATA.variables['Vwind'][:,:,:]  #[t,y,x]
WIND = (U_WIND**2+V_WIND**2)**0.5  #Calculate Wind speed

#[Info Data Read]=========================================================================================
POINT_INF = open('./Info/SD_Point_Info.csv','r',encoding='utf8')
INF = [str(INFO) for INFO in POINT_INF.read().split()]
INF_LEN = len(INF)

#[SD Split data read]=========================================================================
SDTIME_INF = open('./Info/SD_Split_time.csv','r',encoding='utf8')
SDTIME = [LST for LST in SDTIME_INF.read().split()]
SDTIME_LEN = len(SDTIME)

#[KMA CITY and WARNING data read]=========================================================================
if not os.path.exists(dir1+'/SD_CITY.csv'): # 동네예보 수집 에러에 따른 자료 미생성시 그냥 예측자료 사용
	print('CITY_FORECAST DATA Not found') ; CITY_LEN=0
else:
	CITY_INF = open(dir1+'/SD_CITY.csv','r',encoding='utf8')
	CITY = [LST for LST in CITY_INF.read().split()]
	CITY_LEN = len(CITY)

WARN_INF = open(dir1+'/KMA_WARNING.csv','r',encoding='utf8')
WARN = [LST for LST in WARN_INF.read().split()]
WARN_LEN = len(WARN)

#[SD DATA Extract] ====================================================================================
DAY1 = [] # today forecast data list
DAY2 = [] # tomorrow forecast data list
DAY3 = [] # the day after tomorrow forecast data list
DAY4 = []
DAY5 = []
DAY6 = []
DAY7 = []
COM  = [] # combine

for SDT_DATA in SDTIME :
	DEV = SDT_DATA.split(',')
	SPLIT_NAME = DEV[0] ; YMD = DEV[1] ; START_TIME = DEV[2] ; END_TIME = DEV[3]

	if YMD == today :
		#SD_TIME[0] = SD_START_TIME, [1] = SD_END_TIME, [2] = exp_hr 
		SD_TIME = SD_time_cal().split_time(YMD, START_TIME, END_TIME)
		#print(SD_TIME)

		ii = 1
		while ii <= INF_LEN-1 :
			DEV = INF[ii].split(',')
			STN = DEV[0] ; AREA = DEV[1] ; NAME = DEV[2] ; LON = DEV[3] ; LAT = DEV[4]
			WRF_X = int(DEV[7]) ; WRF_Y = int(DEV[8]) ; W_AREA = DEV[18]
			
			if SPLIT_NAME == NAME :
				if SD_TIME[3] == 'daily' or SD_TIME[3] == 'AM' or SD_TIME[3] =='PM':
					WIND_S  = Statistic().min_max_ave('KHOA', 'daily', WIND, WRF_X, WRF_Y, 0)
					TEMP_S  = Statistic().min_max_ave('KHOA', 'daily', TEMP, WRF_X, WRF_Y, 0)
					DAY1.append([STN, AREA, W_AREA, NAME, today, SD_TIME[0], SD_TIME[1], SD_TIME[2], SD_TIME[3], round(TEMP_S[0],1), round(TEMP_S[2],1), round(TEMP_S[1],1), round(WIND_S[0],1), round(WIND_S[2],1), round(WIND_S[1],1)])	
			ii = ii + 1
		

	elif YMD == afterday1 :
		#SD_time_cal().split_time(YMD, START_TIME, END_TIME)
		SD_TIME = SD_time_cal().split_time(YMD, START_TIME, END_TIME)

		ii = 1
		while ii <= INF_LEN-1 :
			DEV = INF[ii].split(',')
			STN = DEV[0] ; AREA = DEV[1] ; NAME = DEV[2] ; LON = DEV[3] ; LAT = DEV[4]
			WRF_X = int(DEV[7]) ; WRF_Y = int(DEV[8]) ; W_AREA = DEV[18]
			if SPLIT_NAME == NAME :
				if SD_TIME[3] == 'daily' or SD_TIME[3] == 'AM' or SD_TIME[3] =='PM':
					WIND_S  = Statistic().min_max_ave('KHOA', 'daily', WIND, WRF_X, WRF_Y, 24)
					TEMP_S  = Statistic().min_max_ave('KHOA', 'daily', TEMP, WRF_X, WRF_Y, 24)
					DAY2.append([STN, AREA, W_AREA, NAME, afterday1, SD_TIME[0], SD_TIME[1], SD_TIME[2], SD_TIME[3], round(TEMP_S[0],1), round(TEMP_S[2],1), round(TEMP_S[1],1), round(WIND_S[0],1), round(WIND_S[2],1), round(WIND_S[1],1)])	
			ii = ii + 1
	elif YMD == afterday2 :
		#SD_time_cal().split_time(YMD, START_TIME, END_TIME)
		SD_TIME = SD_time_cal().split_time(YMD, START_TIME, END_TIME)

		ii = 1
		while ii <= INF_LEN-1 :
			DEV = INF[ii].split(',')
			STN = DEV[0] ; AREA = DEV[1] ; NAME = DEV[2] ; LON = DEV[3] ; LAT = DEV[4]
			WRF_X = int(DEV[7]) ; WRF_Y = int(DEV[8]) ; W_AREA = DEV[18]
			if SPLIT_NAME == NAME :
				if SD_TIME[3] == 'daily' or SD_TIME[3] == 'AM' or SD_TIME[3] =='PM':
					WIND_S  = Statistic().min_max_ave('KHOA', 'daily', WIND, WRF_X, WRF_Y, 48)
					TEMP_S  = Statistic().min_max_ave('KHOA', 'daily', TEMP, WRF_X, WRF_Y, 48)
					DAY3.append([STN, AREA, W_AREA, NAME, afterday2, SD_TIME[0], SD_TIME[1], SD_TIME[2], SD_TIME[3], round(TEMP_S[0],1), round(TEMP_S[2],1), round(TEMP_S[1],1), round(WIND_S[0],1), round(WIND_S[2],1), round(WIND_S[1],1)])	
			ii = ii + 1
	elif YMD == afterday3 :
		#SD_time_cal().split_time(YMD, START_TIME, END_TIME)
		SD_TIME = SD_time_cal().split_time(YMD, START_TIME, END_TIME)

		ii = 1
		while ii <= INF_LEN-1 :
			DEV = INF[ii].split(',')
			STN = DEV[0] ; AREA = DEV[1] ; NAME = DEV[2] ; LON = DEV[3] ; LAT = DEV[4]
			WRF_X = int(DEV[7]) ; WRF_Y = int(DEV[8]) ; W_AREA = DEV[18]
			if SPLIT_NAME == NAME :
				if SD_TIME[3] == 'daily' or SD_TIME[3] == 'AM' or SD_TIME[3] =='PM':
					WIND_S  = Statistic().min_max_ave('KHOA', 'daily', WIND, WRF_X, WRF_Y, 72)
					TEMP_S  = Statistic().min_max_ave('KHOA', 'daily', TEMP, WRF_X, WRF_Y, 72)
					DAY4.append([STN, AREA, W_AREA, NAME, afterday3, SD_TIME[0], SD_TIME[1], SD_TIME[2], SD_TIME[3], round(TEMP_S[0],1), round(TEMP_S[2],1), round(TEMP_S[1],1), round(WIND_S[0],1), round(WIND_S[2],1), round(WIND_S[1],1)])	
			ii = ii + 1	
	elif YMD == afterday4 :
		#SD_time_cal().split_time(YMD, START_TIME, END_TIME)
		SD_TIME = SD_time_cal().split_time(YMD, START_TIME, END_TIME)

		ii = 1
		while ii <= INF_LEN-1 :
			DEV = INF[ii].split(',')
			STN = DEV[0] ; AREA = DEV[1] ; NAME = DEV[2] ; LON = DEV[3] ; LAT = DEV[4]
			WRF_X = int(DEV[7]) ; WRF_Y = int(DEV[8]) ; W_AREA = DEV[18]
			if SPLIT_NAME == NAME :
				if SD_TIME[3] == 'daily' or SD_TIME[3] == 'AM' or SD_TIME[3] =='PM':
					WIND_S  = Statistic().min_max_ave('KHOA', 'daily', WIND, WRF_X, WRF_Y, 96)
					TEMP_S  = Statistic().min_max_ave('KHOA', 'daily', TEMP, WRF_X, WRF_Y, 96)
					DAY5.append([STN, AREA, W_AREA, NAME, afterday4, SD_TIME[0], SD_TIME[1], SD_TIME[2], SD_TIME[3], round(TEMP_S[0],1), round(TEMP_S[2],1), round(TEMP_S[1],1), round(WIND_S[0],1), round(WIND_S[2],1), round(WIND_S[1],1)])	
			ii = ii + 1
	elif YMD == afterday5 :
		#SD_time_cal().split_time(YMD, START_TIME, END_TIME)
		SD_TIME = SD_time_cal().split_time(YMD, START_TIME, END_TIME)

		ii = 1
		while ii <= INF_LEN-1 :
			DEV = INF[ii].split(',')
			STN = DEV[0] ; AREA = DEV[1] ; NAME = DEV[2] ; LON = DEV[3] ; LAT = DEV[4]
			WRF_X = int(DEV[7]) ; WRF_Y = int(DEV[8]) ; W_AREA = DEV[18]
			if SPLIT_NAME == NAME :
				if SD_TIME[3] == 'daily' or SD_TIME[3] == 'AM' or SD_TIME[3] =='PM':
					WIND_S  = Statistic().min_max_ave('KHOA', 'daily', WIND, WRF_X, WRF_Y, 120)
					TEMP_S  = Statistic().min_max_ave('KHOA', 'daily', TEMP, WRF_X, WRF_Y, 120)
					DAY6.append([STN, AREA, W_AREA, NAME, afterday5, SD_TIME[0], SD_TIME[1], SD_TIME[2], SD_TIME[3], round(TEMP_S[0],1), round(TEMP_S[2],1), round(TEMP_S[1],1), round(WIND_S[0],1), round(WIND_S[2],1), round(WIND_S[1],1)])	
			ii = ii + 1
	elif YMD == afterday6 :
		#SD_time_cal().split_time(YMD, START_TIME, END_TIME)
		SD_TIME = SD_time_cal().split_time(YMD, START_TIME, END_TIME)

		ii = 1
		while ii <= INF_LEN-1 :
			DEV = INF[ii].split(',')
			STN = DEV[0] ; AREA = DEV[1] ; NAME = DEV[2] ; LON = DEV[3] ; LAT = DEV[4]
			WRF_X = int(DEV[7]) ; WRF_Y = int(DEV[8]) ; W_AREA = DEV[18]
			if SPLIT_NAME == NAME :
				WIND_S  = Statistic().min_max_ave('KHOA', 'daily', WIND, WRF_X, WRF_Y, 144)
				TEMP_S  = Statistic().min_max_ave('KHOA', 'daily', TEMP, WRF_X, WRF_Y, 144)
				DAY7.append([STN, AREA, W_AREA, NAME, afterday6, SD_TIME[0], SD_TIME[1], SD_TIME[2], SD_TIME[3], round(TEMP_S[0],1), round(TEMP_S[2],1), round(TEMP_S[1],1), round(WIND_S[0],1), round(WIND_S[2],1), round(WIND_S[1],1)])	
			ii = ii + 1
				

#[Combine and sorting] date > am/pm > stn ============================================================================
DAY1.sort() ; DAY2.sort() ; DAY3.sort() ; DAY4.sort() ; DAY5.sort() ; DAY6.sort() ; DAY7.sort() 
ii = 0
while ii <= len(DAY1)-1 : COM.append(DAY1[ii]); ii = ii + 1
ii = 0                                                                          
while ii <= len(DAY2)-1 : COM.append(DAY2[ii]); ii = ii + 1
ii = 0                                                                          
while ii <= len(DAY3)-1 : COM.append(DAY3[ii]); ii = ii + 1
ii = 0
while ii <= len(DAY4)-1 : COM.append(DAY4[ii]); ii = ii + 1
ii = 0                                                                          
while ii <= len(DAY5)-1 : COM.append(DAY5[ii]); ii = ii + 1
ii = 0                                                                          
while ii <= len(DAY6)-1 : COM.append(DAY6[ii]); ii = ii + 1
ii = 0                                                                          
while ii <= len(DAY7)-1 : COM.append(DAY7[ii]); ii = ii + 1

COM_LEN = len(COM)
#print(COM_LEN)

#ii = 0
#while ii <= COM_LEN-1 :
#	print(COM[ii])
#	ii += 1
#print(len(DAY1), COM_LEN, INF_LEN )

#[KMA weather forecast : rain amount, sky status]=====================================================================================
#print(CITY_LEN, COM_LEN)
ii = 0
while ii <= COM_LEN-1:
	if CITY_LEN == 0 :
		COM[ii].insert(15,0)
		COM[ii].insert(16,1)
	else:        
		jj = 1 
		while jj <= CITY_LEN-1:
			DEV = CITY[jj].split(',')
			if jj != CITY_LEN-1 : DEV2 = CITY[jj+1].split(',')
			STN = DEV[0] ; NAME = DEV[1] ; DATE = DEV[2] ; AMPM = DEV[3] ; RAIN_AMT = float(DEV[11]) ; SKY = DEV[10]
			if COM[ii][0] == STN and COM[ii][4] == DATE and COM[ii][8] == AMPM :
				COM[ii].insert(15,RAIN_AMT)
				COM[ii].insert(16,SKY)
				print(NAME, DATE, int(SKY), int(DEV2[10]))
			elif COM[ii][0] == STN and COM[ii][4] == DATE and COM[ii][8] == 'daily' and DEV[2] == DEV2[2] :
				COM[ii].insert(15,(RAIN_AMT + float(DEV2[11])))
				if int(SKY) >= int(DEV2[10]) : COM[ii].insert(16,SKY)
				else : COM[ii].insert(16,DEV2[10])
				print(NAME, DATE, int(SKY), int(DEV2[10]))
			elif COM[ii][0] == STN and COM[ii][4] == DATE and DEV[3] == 'DY' :
				COM[ii].insert(15,0)
				COM[ii].insert(16,SKY)
				print(NAME, DATE, int(SKY), int(DEV2[10]))				
			jj = jj + 1
	ii = ii + 1
#[KMA WARNING INFORAMTION : special weather report]=====================================================================================================
ii = 0 
while ii <= COM_LEN-1:
	jj = 1
	while jj <= WARN_LEN-1:
		DEV = WARN[jj].split(',')
		WARN_AREA = DEV[0] ; WARN_TYPE = DEV[1] ; WARN_SDAY = DEV[2] ; WARN_SHR = DEV[3] ; WARN_EDAY = DEV[4] ; WARN_EHR = DEV[5]
		#print(WARN_AREA, WARN_TYPE)
		
		#print(COM[ii][4], int(WARN_SDAY), COM[ii][5],WARN_SHR)
		if int(COM[ii][4]) < int(WARN_EDAY) and int(COM[ii][4]) >= int(WARN_SDAY) and COM[ii][2] == WARN_AREA: #해제예고 일보다 전날일 경우 일괄적용
			COM[ii].insert(17,WARN_TYPE)
			jj = WARN_LEN
		elif int(COM[ii][4]) == int(WARN_EDAY) and int(COM[ii][4]) >= int(WARN_SDAY) and COM[ii][2] == WARN_AREA: #해제예고일과 같을 경우 AM이면 오전만 적용, PM이면 오전/오후 모두적용
			if WARN_EHR == 'PM': 
				COM[ii].insert(17,WARN_TYPE)
			elif WARN_EHR == 'AM' :
				if COM[ii][5] == 'AM' :
					COM[ii].insert(17,WARN_TYPE)
				else :
					COM[ii].insert(17,'-')
			jj = WARN_LEN
		else:
			jj = jj + 1
			if jj == WARN_LEN :
				COM[ii].insert(17,'-')
		jj = jj
	ii = ii + 1
ii = 0
#while ii < len(COM)-1:
	#print(COM[ii][15], COM[ii][16], COM[ii][17])
	#print(COM[ii])
#	ii = ii + 1
#[Index Score Calculate] ========================================================================================
COM_LEN = len(COM)
ii = 0
while ii <= COM_LEN-1 :
               #0   1       2     3      4              5       6			7			8				9						10						11						12						13						14				                 
#DAY3.append([STN, AREA, W_AREA, NAME, afterday2, SD_TIME[0], SD_TIME[1], SD_TIME[2], SD_TIME[3], int(round(TEMP_S[0])),  int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])),int(round(WIND_S[2])), int(round(WIND_S[1]))])
	#print(ii)
	MIN_TEMP = COM[ii][9] ; AVE_TEMP = COM[ii][10] ; MAX_TEMP = COM[ii][11]
#	if MIN_TEMP == MAX_TEMP :
#		MIN_TEMP = AVE_TEMP - 1
#		MAX_TEMP = AVE_TEMP + 1	
	EXPHR_SCRE = IndexScore().exphr_score(COM[ii][7])
	TEMP_SCRE = IndexScore().temp_score(COM[ii][10])
	WIND_SCRE = IndexScore().wind_score(COM[ii][14])
	SKY_SCRE = IndexScore().sky_score(int(COM[ii][16]))
	RAIN_SCRE = IndexScore().rain_score(float(COM[ii][15]))
	WARN_SCRE = IndexScore().warn_score(COM[ii][17])
	TOTAL_SCRE1 = IndexScore().total_score(EXPHR_SCRE, TEMP_SCRE, WIND_SCRE, SKY_SCRE, RAIN_SCRE, WARN_SCRE)[0] # forecast score(no rain, no warning)
	TOTAL_SCRE2 = IndexScore().total_score(EXPHR_SCRE, TEMP_SCRE, WIND_SCRE, SKY_SCRE, RAIN_SCRE, WARN_SCRE)[1] # service score(rain, warning)
	QUOTIENT_SCRE1 = IndexScore().quotient_score(TOTAL_SCRE1) # forecast score(no rain, no warning)
	QUOTIENT_SCRE2 = IndexScore().quotient_score(TOTAL_SCRE2) # service score(rain, warning)

	COM[ii][9] = MIN_TEMP ; COM[ii][11] = MAX_TEMP
	COM[ii].insert(8,EXPHR_SCRE) ; COM[ii].insert(13,TEMP_SCRE) ; COM[ii].insert(17,WIND_SCRE); COM[ii].insert(19,RAIN_SCRE) ; COM[ii].insert(21,SKY_SCRE) ; COM[ii].insert(23,WARN_SCRE);COM[ii].insert(24,TOTAL_SCRE1) ; COM[ii].insert(25,TOTAL_SCRE2) ; COM[ii].insert(26,QUOTIENT_SCRE1) ; COM[ii].insert(27,QUOTIENT_SCRE2)
	ii = ii + 1

#ii = 0
#while ii <= COM_LEN-1:
#	print(COM[ii])
#	ii = ii + 1

#[Output Data] ========================================================================================
OUT_FNAME1=dir1+'/SDEQ_INDEX_FCST_'+today+'.csv'
with open(OUT_FNAME1,'w',encoding='utf8') as file:
	file.write('생산일,코드,권역,지역,예측일자,갈라짐시작시간,갈라짐종료시간,체험시간,체험시간점수,최저기온,평균기온,최고기온,기온점수,최저풍속,평균풍속,최대풍속,풍속점수,날씨,날씨점수,총점수,예보지수\n',)
	ii = 0
	while ii <= COM_LEN-1 :
		#[전체 데이터 Writing]
		if COM[ii][8] != 0 :
			file.write(f'{today},{COM[ii][0]},{COM[ii][1]},{COM[ii][3]},{COM[ii][4]},{COM[ii][5]},{COM[ii][6]},{COM[ii][7]:3.2f},{COM[ii][8]},{COM[ii][10]:3.1f},{COM[ii][11]:3.1f},{COM[ii][12]:3.1f},{COM[ii][13]},{COM[ii][14]:3.2f},{COM[ii][15]:3.2f},{COM[ii][16]:3.2f},{COM[ii][17]},{COM[ii][20]},{COM[ii][21]},{COM[ii][24]:4.2f},{COM[ii][26]}\n')
			ii = ii + 1
		else :
			ii = ii + 1
			continue
OUT_FNAME2=dir1+'/SDEQ_INDEX_SERVICE_'+today+'.csv'
with open(OUT_FNAME2,'w',encoding='utf8') as file:
	file.write('생산일,코드,권역,지역,예측일자,갈라짐시작시간,갈라짐종료시간,체험시간,체험시간점수,최저기온,평균기온,최고기온,기온점수,최저풍속,평균풍속,최대풍속,풍속점수,날씨,날씨점수,강수량,강수점수,특보,특보점수,총점수,예보지수\n',)
	ii = 0
	while ii <= COM_LEN-1 :
		#[WEB_~~_SCRE Format]
		if COM[ii][8] != 0 :
			file.write(f'{today},{COM[ii][0]},{COM[ii][1]},{COM[ii][3]},{COM[ii][4]},{COM[ii][5]},{COM[ii][6]},{COM[ii][7]:3.2f},{COM[ii][8]},{COM[ii][10]:3.1f},{COM[ii][11]:3.1f},{COM[ii][12]:3.1f},{COM[ii][13]},{COM[ii][14]:3.1f},{COM[ii][15]:3.1f},{COM[ii][16]:3.1f},{COM[ii][17]},{COM[ii][20]},{COM[ii][21]},{COM[ii][18]},{COM[ii][19]},{COM[ii][22]},{COM[ii][23]},{COM[ii][25]:4.2f},{COM[ii][27]}\n')
			ii = ii + 1
		else :
			ii = ii + 1
			continue
print("#SDEQ FCST_INDEX and SERVICE INDEX CREAT Complete==========")
