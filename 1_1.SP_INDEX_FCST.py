#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.04.11] edit 19.08.22
import sys
import os
#os.path.join(os.getcwd(),"Function")
import numpy as np
from math import floor
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime
from Function.speq_function import IndexScore
from Function.statistic_function import Statistic

print("#SPEQ FCST_INDEX CREAT Start==========")

#[Date set] ==============================================================================================
#[Auto date set]
today = str(datetime.today().strftime('%Y%m%d'))
afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')
afterday3 = (date.today() + timedelta(3)).strftime('%Y%m%d')
afterday4 = (date.today() + timedelta(4)).strftime('%Y%m%d')
afterday5 = (date.today() + timedelta(5)).strftime('%Y%m%d')
afterday6 = (date.today() + timedelta(6)).strftime('%Y%m%d')
#print(today,afterday1,afterday2,afterday3,afterday4,afterday5,afterday6)

#[Manual date set]
#today = str(date(2019,10,18).strftime('%Y%m%d'))
#afterday1 = (date(2019,10,18) + timedelta(1)).strftime('%Y%m%d')
#afterday2 = (date(2019,10,18) + timedelta(2)).strftime('%Y%m%d')
#print(today, afterday1, afterday2)

dir1 = './Result/'+today

#[Model Data path] =======================================================================================
MPATH = './Model_Data/'
ROMS_FNAME = 'YES3K_'+ str(today) + '00.nc'      # YES3K - KHOA
WRF_FNAME = 'WRF_' + str(today) + '.nc'          # WRF_DM2 - KHOA
WW3_FNAME = 'WW3_' + str(today) + '00.nc'        # WW3 - KHOA
CWW3_FNAME = 'CWW3_' + str(today) + '00.nc'      # CWW3 - KMA
RWW3_FNAME = 'RWW3_' + str(today) + '00.nc'     # RWW3 - KMA

INFILE_1 = MPATH+ROMS_FNAME
INFILE_2 = MPATH+WRF_FNAME
INFILE_3 = MPATH+CWW3_FNAME
INFILE_4 = MPATH+WW3_FNAME
INFILE_5 = MPATH+RWW3_FNAME

#[READ Model_Data] =======================================================================================
#[YES3K]
DATA = Dataset(INFILE_1, mode='r')
SST = DATA.variables['temp'][:,:,:]  #[t,y,x]
U_CURRENT = DATA.variables['u'][:,:,:]  #[t,y,x]
V_CURRENT = DATA.variables['v'][:,:,:]  #[t,y,x]
CURRENT= (U_CURRENT**2+V_CURRENT**2)**0.5  #Calculate Current speed

#[WRF]
DATA = Dataset(INFILE_2, mode='r')
TEMP = DATA.variables['Tair'][:,:,:]  #[t,y,x]
U_WIND = DATA.variables['Uwind'][:,:,:]  #[t,y,x]
V_WIND = DATA.variables['Vwind'][:,:,:]  #[t,y,x]
WIND = (U_WIND**2+V_WIND**2)**0.5  #Calculate Wind speed

#[CWW3, WW3] not yet RWW3
if os.path.isfile(INFILE_3):
	DATA = Dataset(INFILE_3, mode='r')
	WHT_1 = DATA.variables['hsig1_dajn'][:,:,:]  #[t,y,x]
	WHT_2 = DATA.variables['hsig2_gwju'][:,:,:]  #[t,y,x]
	WHT_3 = DATA.variables['hsig3_jeju'][:,:,:]  #[t,y,x]
	WHT_4 = DATA.variables['hsig4_busn'][:,:,:]  #[t,y,x]
	WHT_5 = DATA.variables['hsig5_gawn'][:,:,:]  #[t,y,x]
	DATA2 = Dataset(INFILE_4, mode='r')
	WHT = DATA2.variables['Hsig'][:,:,:]  #[t,y,x]	
else :
	DATA = Dataset(INFILE_4, mode='r')
	WHT = DATA.variables['Hsig'][:,:,:]  #[t,y,x]


#[Info Data Read]=========================================================================================
POINT_INF = open('./Info/SP_Point_Info.csv','r',encoding='utf8')
INF = [str(INFO) for INFO in POINT_INF.read().split()]
INF_LEN = len(INF)

#[KMA CITY and WARNING data read]=========================================================================
if not os.path.exists(dir1+'/SP_CITY.csv'): # 동네예보 수집 에러에 따른 자료 미생성시 그냥 예측자료 사용
	print('CITY_FORECAST DATA Not found') ; CITY_LEN=0
else:
	CITY_INF = open(dir1+'/SP_CITY.csv','r',encoding='utf8')
	CITY = [LST for LST in CITY_INF.read().split()]
	CITY_LEN = len(CITY)

WARN_INF = open(dir1+'/KMA_WARNING.csv','r',encoding='utf8')
WARN = [LST for LST in WARN_INF.read().split()]
WARN_LEN = len(WARN)

#[BEACH DATA Extract] ====================================================================================
DAY1 = [] # today forecast data list
DAY2 = [] # tomorrow forecast data list
DAY3 = [] # the day after tomorrow forecast data list
DAY4 = []
DAY5 = []
DAY6 = []
DAY7 = []
COM  = [] # combine

ii = 1
while ii <= INF_LEN-1 :
	DEV = INF[ii].split(',')
	STN = DEV[0] ; AREA = DEV[1] ; NAME = DEV[2] ; LON = DEV[3] ; LAT = DEV[4]
	ROMS_X = int(DEV[5]) ; ROMS_Y = int(DEV[6]) ; WRF_X = int(DEV[7]) ; WRF_Y = int(DEV[8])
	WW3_X = int(DEV[9]) ; WW3_Y = int(DEV[10]) ; CWW3_X = int(DEV[11]) ; CWW3_Y = int(DEV[12]) ; CWW3_LOC = int(DEV[13]) ;
	RWW3_X = int(DEV[14]) ; RWW3_Y = int(DEV[15]) ; W_AREA = DEV[18]

	jj = 0 ; jjj = 0
	while jj <= 144:
		SST_2S  = Statistic().min_max_ave('KHOA', 'ampm', SST, ROMS_X, ROMS_Y, jj)
		SST_S  = Statistic().min_max_ave('KHOA', 'daily', SST, ROMS_X, ROMS_Y, jj)
		WIND_2S = Statistic().min_max_ave('KHOA', 'ampm', WIND, WRF_X, WRF_Y, jj)
		WIND_S = Statistic().min_max_ave('KHOA', 'daily', WIND, WRF_X, WRF_Y, jj)
		TEMP_2S = Statistic().min_max_ave('KHOA', 'ampm', TEMP, WRF_X, WRF_Y, jj)
		TEMP_S = Statistic().min_max_ave('KHOA', 'daily', TEMP, WRF_X, WRF_Y, jj)
	
		if os.path.isfile(INFILE_3):
			if jj <= 48 :
				jjj = int(jj / 3) #3시간 자료
				if CWW3_LOC == 1 :
					WAVE_2S = Statistic().min_max_ave('KMA', 'ampm', WHT_1, CWW3_X, CWW3_Y, jjj)
					WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_1, CWW3_X, CWW3_Y, jjj)
				if CWW3_LOC == 2 :
					WAVE_2S = Statistic().min_max_ave('KMA', 'ampm', WHT_2, CWW3_X, CWW3_Y, jjj)
					WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_2, CWW3_X, CWW3_Y, jjj)
				if CWW3_LOC == 3 :
					WAVE_2S = Statistic().min_max_ave('KMA', 'ampm', WHT_3, CWW3_X, CWW3_Y, jjj)
					WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_3, CWW3_X, CWW3_Y, jjj)
				if CWW3_LOC == 4 :
					WAVE_2S = Statistic().min_max_ave('KMA', 'ampm', WHT_4, CWW3_X, CWW3_Y, jjj)
					WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_4, CWW3_X, CWW3_Y, jjj)
				if CWW3_LOC == 5 :
					WAVE_2S = Statistic().min_max_ave('KMA', 'ampm', WHT_5, CWW3_X, CWW3_Y, jjj)
					WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_5, CWW3_X, CWW3_Y, jjj)
			else :
				WAVE_2S = Statistic().min_max_ave('KHOA', 'ampm', WHT, WW3_X, WW3_Y, jj)
				WAVE_S = Statistic().min_max_ave('KHOA', 'daily', WHT, WW3_X, WW3_Y, jj)
		else : 
			WAVE_2S = Statistic().min_max_ave('KHOA', 'ampm', WHT, WW3_X, WW3_Y, jj)
			WAVE_S = Statistic().min_max_ave('KHOA', 'daily', WHT, WW3_X, WW3_Y, jj)

		if WAVE_S[0] < 0.1 : WAVE_S[0] = 0.1
		if WAVE_S[1] < 0.1 : WAVE_S[1] = 0.1
		if WAVE_S[2] < 0.1 : WAVE_S[2] = 0.1
		if WAVE_2S[0] < 0.1 : WAVE_2S[0] = 0.1
		if WAVE_2S[1] < 0.1 : WAVE_2S[1] = 0.1
		if WAVE_2S[2] < 0.1 : WAVE_2S[2] = 0.1
		if WAVE_2S[3] < 0.1 : WAVE_2S[3] = 0.1		
		if WAVE_2S[4] < 0.1 : WAVE_2S[4] = 0.1
		if WAVE_2S[5] < 0.1 : WAVE_2S[5] = 0.1		
		
		#VARS_S ampm [0:am_min 1:am_max, 2:am_ave, 3:pm_min, 4:pm_max, 5:pm_ave] ; VARS_S daily [0:min 1:max, 2:ave]
		if jj == 0 : # today am/pm data 
			DAY1.append([STN, AREA, W_AREA, NAME, today, 'AM', TEMP_2S[2], SST_2S[2], WIND_2S[1], WAVE_2S[1]])
			DAY1.append([STN, AREA, W_AREA, NAME, today, 'PM', TEMP_2S[5], SST_2S[5], WIND_2S[4], WAVE_2S[4]])
			#print(WAVE_S[1],WAVE_S[4])
		elif jj == 24 :
			DAY2.append([STN, AREA, W_AREA, NAME, afterday1, 'AM', TEMP_2S[2], SST_2S[2], WIND_2S[1], WAVE_2S[1]])
			DAY2.append([STN, AREA, W_AREA, NAME, afterday1, 'PM', TEMP_2S[5], SST_2S[5], WIND_2S[4], WAVE_2S[4]])
		elif jj == 48 :
			DAY3.append([STN, AREA, W_AREA, NAME, afterday2, 'AM', TEMP_2S[2], SST_2S[2], WIND_2S[1], WAVE_2S[1]])
			DAY3.append([STN, AREA, W_AREA, NAME, afterday2, 'PM', TEMP_2S[5], SST_2S[5], WIND_2S[4], WAVE_2S[4]])
		elif jj == 72 :
			DAY4.append([STN, AREA, W_AREA, NAME, afterday3, 'DY', TEMP_S[2], SST_S[2], WIND_S[1], WAVE_S[1]])
		elif jj == 96 :
			DAY5.append([STN, AREA, W_AREA, NAME, afterday4, 'DY', TEMP_S[2], SST_S[2], WIND_S[1], WAVE_S[1]])
		elif jj == 120 :
			DAY6.append([STN, AREA, W_AREA, NAME, afterday5, 'DY', TEMP_S[2], SST_S[2], WIND_S[1], WAVE_S[1]])
		elif jj == 144 :
			DAY7.append([STN, AREA, W_AREA, NAME, afterday6, 'DY', TEMP_S[2], SST_S[2], WIND_S[1], WAVE_S[1]])
			
		jj = jj + 24 #24시간 간격으로 일괄 계산
	ii = ii + 1
	
        
        
LEN_DAY= len(DAY1) # AM/PM 1day data length 
LEN_DAY2= len(DAY4)# DAILY 1day data length 
#print(len(DAY1),len(DAY2),len(DAY3),len(DAY4),len(DAY5),len(DAY6),len(DAY7))
#[Combine and sorting] date > am/pm > stn ============================================================================
ii = 0
while ii <= LEN_DAY-1 : COM.append(DAY1[ii]); COM.append(DAY1[ii+1]); ii = ii + 2
ii = 0
while ii <= LEN_DAY-1 : COM.append(DAY2[ii]); COM.append(DAY2[ii+1]); ii = ii + 2
ii = 0
while ii <= LEN_DAY-1 : COM.append(DAY3[ii]); COM.append(DAY3[ii+1]); ii = ii + 2
ii = 0
while ii <= LEN_DAY2-1 : COM.append(DAY4[ii]); ii = ii + 1
ii = 0
while ii <= LEN_DAY2-1 : COM.append(DAY5[ii]); ii = ii + 1
ii = 0
while ii <= LEN_DAY2-1 : COM.append(DAY6[ii]); ii = ii + 1
ii = 0
while ii <= LEN_DAY2-1 : COM.append(DAY7[ii]); ii = ii + 1

COM_LEN = len(COM)
#print(len(DAY1), COM_LEN, INF_LEN )

#[KMA weather forecast : rain amount, sky status]=====================================================================================
ii = 0
while ii <= CITY_LEN-2:
	#jj = 12 # 0~11 column next data read 
	if CITY_LEN == 0 :
		COM[ii].insert(10,0)
		COM[ii].insert(11,1)
	else :
		jj = 1
		while jj <= CITY_LEN-1:
			DEV = CITY[jj].split(',')
			STN = DEV[0] ; NAME = DEV[1] ; DATE = DEV[2] ; AMPM = DEV[3] ; RAIN_AMT = float(DEV[11]) ; SKY = DEV[10]
			if COM[ii][0] == STN and COM[ii][4] == DATE and COM[ii][5] == AMPM:
				COM[ii].insert(10,RAIN_AMT)
				COM[ii].insert(11,SKY)
			elif COM[ii][0] == STN and COM[ii][4] == DATE and COM[ii][5] == 'DY':
				COM[ii].insert(10,RAIN_AMT)
				COM[ii].insert(11,SKY)
			jj = jj + 1
		#print(COM[ii][10])
	ii = ii + 1
while ii <= COM_LEN-1:
	jj = CITY_LEN
	while jj <= COM_LEN-1:
		COM[ii].insert(10,0)
		COM[ii].insert(11,1)
		jj = jj + 1
	#print(COM[ii][10])
	ii = ii +1

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
			COM[ii].insert(12,WARN_TYPE)
			jj = WARN_LEN
		elif int(COM[ii][4]) == int(WARN_EDAY) and int(COM[ii][4]) >= int(WARN_SDAY) and COM[ii][2] == WARN_AREA: #해제예고일과 같을 경우 AM이면 오전만 적용, PM이면 오전/오후 모두적용
			if WARN_EHR == 'PM' : 
				COM[ii].insert(12,WARN_TYPE)
			elif WARN_EHR == 'AM' :
				if COM[ii][5] == 'AM' or COM[ii][5] == 'DY' :
					COM[ii].insert(12,WARN_TYPE)
				else :
					COM[ii].insert(12,'-')
			jj = WARN_LEN
		else:
			jj = jj + 1
			if jj == WARN_LEN :
				COM[ii].insert(12,'-')
		jj = jj
	ii = ii + 1

#ii = 0
#while ii <= COM_LEN-1:
#	print(COM[ii])
#	ii = ii + 1
#[Index Score Calculate] ========================================================================================
COM_LEN = len(COM)
ii = 0
while ii <= COM_LEN-1 :
	TEMP_SCRE = IndexScore().temp_score(round(COM[ii][6],1))
	SST_SCRE = IndexScore().sst_score(round(COM[ii][7],1))
	WIND_SCRE = IndexScore().wind_score(round(COM[ii][8],1))
	WAVE_SCRE = IndexScore().wave_score(round(float(COM[ii][9]),1))
	RAIN_SCRE = IndexScore().rain_score(float(COM[ii][10]))
	WARN_SCRE = IndexScore().warn_score(COM[ii][12])
	TOTAL_SCRE1 = IndexScore().total_score(TEMP_SCRE, round(COM[ii][7],1), SST_SCRE, WIND_SCRE, WAVE_SCRE, RAIN_SCRE, WARN_SCRE)[0] # forecast score(no rain, no warning)
	TOTAL_SCRE2 = IndexScore().total_score(TEMP_SCRE, round(COM[ii][7],1), SST_SCRE, WIND_SCRE, WAVE_SCRE, RAIN_SCRE, WARN_SCRE)[1] # service score(rain, warning)
	QUOTIENT_SCRE1 = IndexScore().quotient_score(TOTAL_SCRE1)
	QUOTIENT_SCRE2 = IndexScore().quotient_score(TOTAL_SCRE2)

	COM[ii].insert(7,TEMP_SCRE) ; COM[ii].insert(9,SST_SCRE) ; COM[ii].insert(11,WIND_SCRE); COM[ii].insert(13,WAVE_SCRE) ; COM[ii].insert(15,RAIN_SCRE) ; COM[ii].insert(18,WARN_SCRE) ;COM[ii].insert(19,TOTAL_SCRE1) ; COM[ii].insert(20,TOTAL_SCRE2) ; COM[ii].insert(21,QUOTIENT_SCRE1) ; COM[ii].insert(22,QUOTIENT_SCRE2)
	ii = ii + 1

#[Output Data] ========================================================================================
OUT_FNAME1=dir1+'/SPEQ_INDEX_FCST_'+today+'.csv'
with open(OUT_FNAME1,'w',encoding='utf8') as file:
	file.write('생산일,코드,권역,해수욕장,예측년월일,시간,평균기온,기온점수,평균수온,수온점수,최대풍속,풍속점수,최대파고,파고점수,총점수,예보지수\n',)
	ii = 0
	while ii <= COM_LEN-1 :
		#[전체 데이터 Writing]
		file.write(f'{today},{COM[ii][0]},{COM[ii][1]},{COM[ii][3]},{COM[ii][4]},{COM[ii][5]},{COM[ii][6]:3.1f},{COM[ii][7]},{COM[ii][8]:3.1f},{COM[ii][9]},{COM[ii][10]:3.1f},{COM[ii][11]},{COM[ii][12]:3.1f},{COM[ii][13]},{COM[ii][19]:4.2f},{COM[ii][21]}\n')
		ii = ii + 1

OUT_FNAME2=dir1+'/SPEQ_INDEX_SERVICE_'+today+'.csv'
with open(OUT_FNAME2,'w',encoding='utf8') as file:
	file.write('코드,권역,해수욕장,예측일자,시간,평균기온,기온점수,평균수온,수온점수,최대풍속,풍속점수,최대파고,파고점수,강수량,강수량점수,특보,특보점수,총점수,예보지수\n')
	ii = 0
	while ii <= COM_LEN-1 :
		#[WEB_~~_SCRE Format]
		#file.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(COM[ii][0],COM[ii][3],COM[ii][4],COM[ii][5],COM[ii][6],COM[ii][7],COM[ii][8],COM[ii][9],COM[ii][10],COM[ii][11],COM[ii][12],COM[ii][13],COM[ii][14],COM[ii][15],COM[ii][17],COM[ii][18],COM[ii][20]))
		file.write(f'{COM[ii][0]},{COM[ii][1]},{COM[ii][3]},{COM[ii][4]},{COM[ii][5]},{COM[ii][6]:3.1f},{COM[ii][7]},{COM[ii][8]:3.1f},{COM[ii][9]},{COM[ii][10]:3.1f},{COM[ii][11]},{COM[ii][12]:3.1f},{COM[ii][13]},{COM[ii][14]:3.1f},{COM[ii][15]},{COM[ii][17]},{COM[ii][18]},{COM[ii][20]:4.2f},{COM[ii][22]}\n')
		ii = ii + 1

print("#SPEQ FCST_INDEX CREAT Complete==========")
