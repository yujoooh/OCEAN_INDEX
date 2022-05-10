#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.04.11] edit 19.08.22
import sys
import os
#os.path.join(os.getcwd(),"Function")
import numpy as np
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime
from Function.sfeq_function import IndexScore, Tide_time_lunar
from Function.statistic_function import Statistic

print("#SFEQ FCST_INDEX CREAT Start==========")

#[Date set] ==============================================================================================
#[Auto date set]
today = str(datetime.today().strftime('%Y%m%d'))
yesterday = str((date.today() - timedelta(1)).strftime('%Y%m%d'))
afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')

#[Manual date set2] 외부변수 받아오기
var1 = sys.argv[1] ; var2 = sys.argv[2]; var3 = sys.argv[3]
today = str(date(int(var1),int(var2),int(var3)).strftime('%Y%m%d'))
afterday1 = (date(int(var1),int(var2),int(var3)) + timedelta(1)).strftime('%Y%m%d')
afterday2 = (date(int(var1),int(var2),int(var3)) + timedelta(2)).strftime('%Y%m%d')
afterday3 = (date(int(var1),int(var2),int(var3)) + timedelta(3)).strftime('%Y%m%d')
afterday4 = (date(int(var1),int(var2),int(var3)) + timedelta(4)).strftime('%Y%m%d')
afterday5 = (date(int(var1),int(var2),int(var3)) + timedelta(5)).strftime('%Y%m%d')
afterday6 = (date(int(var1),int(var2),int(var3)) + timedelta(6)).strftime('%Y%m%d')
#print(today, afterday1, afterday2)

#[Manual date set2] 외부변수 받아오기
#var1 = sys.argv[1] ; var2 = sys.argv[2]; var3 = sys.argv[3]
#today = str(date(int(var1),int(var2),int(var3)).strftime('%Y%m%d'))
#afterday1 = (date(int(var1),int(var2),int(var3)) + timedelta(1)).strftime('%Y%m%d')
#afterday2 = (date(int(var1),int(var2),int(var3)) + timedelta(2)).strftime('%Y%m%d')
#print(today, afterday1, afterday2)

dir1 = './Result/'+today

#[Model Data path] =======================================================================================
MPATH = './Model_Data/'
ROMS_FNAME = 'YES3K_'+ str(today) + '00.nc'      # YES3K - KHOA
MOHID_FNAME = 'L4_OC_' + str(yesterday) + '12.nc'      # MOHID - KHOA
WRF_FNAME = 'WRF_' + str(today) + '.nc'          # WRF_DM2 - KHOA
WW3_FNAME = 'WW3_' + str(today) + '00.nc'        # WW3 - KHOA
CWW3_FNAME = 'CWW3_' + str(today) + '00.nc'      # CWW3 - KMA
RWW3_FNAME = 'RWW3_' + str(today) + '00.nc'      # RWW3 - KMA

INFILE_1 = MPATH+ROMS_FNAME
INFILE_2 = MPATH+WRF_FNAME
INFILE_3 = MPATH+CWW3_FNAME
INFILE_4 = MPATH+WW3_FNAME
INFILE_5 = MPATH+RWW3_FNAME
INFILE_6 = MPATH+MOHID_FNAME

#[READ Model_Data] =======================================================================================
#[YES3K, MOHID]
if os.path.isfile(INFILE_6):
	DATA = Dataset(INFILE_6, mode='r')
	SST = DATA.variables['temp'][12:,:,:]  #[t,y,x]
	U_CURRENT = DATA.variables['u'][12:,:,:]  #[t,y,x]
	V_CURRENT = DATA.variables['v'][12:,:,:]  #[t,y,x]
	CURRENT= (U_CURRENT**2+V_CURRENT**2)**0.5  #Calculate Current speed

	DATA2 = Dataset(INFILE_1, mode='r')
	SST2 = DATA2.variables['temp'][:,:,:]  #[t,y,x]
	U_CURRENT2 = DATA2.variables['u'][:,:,:]  #[t,y,x]
	V_CURRENT2 = DATA2.variables['v'][:,:,:]  #[t,y,x]
	CURRENT2= (U_CURRENT2**2+V_CURRENT2**2)**0.5  #Calculate Current speed
else : 
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
POINT_INF = open('./Info/SF_Point_Info.csv','r',encoding='utf8')
INF = [str(INFO) for INFO in POINT_INF.read().split()]
INF_LEN = len(INF)

#[KMA CITY and WARNING data read]=========================================================================
if not os.path.exists(dir1+'/SF_CITY.csv'): # 동네예보 수집 에러에 따른 자료 미생성시 그냥 예측자료 사용
	print('CITY_FORECAST DATA Not found') ; CITY_LEN=0
else:
	CITY_INF = open(dir1+'/SF_CITY.csv','r',encoding='utf8')
	CITY = [LST for LST in CITY_INF.read().split()]
	CITY_LEN = len(CITY)

WARN_INF = open(dir1+'/KMA_WARNING.csv','r',encoding='utf8')
WARN = [LST for LST in WARN_INF.read().split()]
WARN_LEN = len(WARN)

#[Tide Time : mul]=========================================================================================
TODAY_MUL = Tide_time_lunar().lunar_to_mul(today)
AFTERDAY1_MUL = Tide_time_lunar().lunar_to_mul(afterday1)
AFTERDAY2_MUL = Tide_time_lunar().lunar_to_mul(afterday2)
AFTERDAY3_MUL = Tide_time_lunar().lunar_to_mul(afterday3)
AFTERDAY4_MUL = Tide_time_lunar().lunar_to_mul(afterday4)
AFTERDAY5_MUL = Tide_time_lunar().lunar_to_mul(afterday5)
AFTERDAY6_MUL = Tide_time_lunar().lunar_to_mul(afterday6)
#print(TIDE_MUL1, TIDE_MUL2, TIDE_MUL3, TIDE_MOON1, TIDE_MOON2, TIDE_MOON3)

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
	RWW3_X = int(DEV[14]) ; RWW3_Y = int(DEV[15]) ;  MOHID_X = int(DEV[16]) ; MOHID_Y = int(DEV[17]) ;
	W_AREA = DEV[20] ; FISH_NAME = DEV[29] ; FISH_TYPE = DEV[30]


	if today[4:6] == '01' or today[4:6] =='02' or today[4:6] =='03' or today[4:6] =='11' or today[4:6] =='12' : 
		#print(today[4:6], 'winter')
	#if today[4:6] == '01' or today[4:6] == '02' or today[4:6] == '03' or today[4:6] == '11' or today[4:6] == '12' : 
		jj = 0 ; jjj = 0
		while jj <= 144:
			WIND_S = Statistic().min_max_ave('KHOA', 'daily', WIND, WRF_X, WRF_Y, jj)
			TEMP_S = Statistic().min_max_ave('KHOA', 'daily', TEMP, WRF_X, WRF_Y, jj)

			if os.path.isfile(INFILE_6):
				if jj <= 48 : #0~2day
					SST_S  = Statistic().min_max_ave('KHOA', 'daily', SST, MOHID_X, MOHID_Y, jj)
				else :        #3~6days
					SST_S  = Statistic().min_max_ave('KHOA', 'daily', SST2, ROMS_X, ROMS_Y, jj)
			else : 
				SST_S  = Statistic().min_max_ave('KHOA', 'daily', SST, ROMS_X, ROMS_Y, jj)

			if os.path.isfile(INFILE_3):
				if jj <= 48 :
					jjj = int(jj / 3) #3시간 자료
					if CWW3_LOC == 1 : WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_1, CWW3_X, CWW3_Y, jjj)
					if CWW3_LOC == 2 : WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_2, CWW3_X, CWW3_Y, jjj)
					if CWW3_LOC == 3 : WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_3, CWW3_X, CWW3_Y, jjj)
					if CWW3_LOC == 4 : WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_4, CWW3_X, CWW3_Y, jjj)
					if CWW3_LOC == 5 : WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_5, CWW3_X, CWW3_Y, jjj)
				else :
					WAVE_S = Statistic().min_max_ave('KHOA', 'daily', WHT, WW3_X, WW3_Y, jj)
			else : 
				WAVE_S = Statistic().min_max_ave('KHOA', 'daily', WHT, WW3_X, WW3_Y, jj)
				
			#VARS_S ampm [0:am_min 1:am_max, 2:am_ave, 3:pm_min, 4:pm_max, 5:pm_ave] ; VARS_S daily [0:min 1:max, 2:ave]
			if jj == 0  : DAY1.append([STN, AREA, W_AREA, NAME, today, FISH_NAME, FISH_TYPE, TODAY_MUL,         round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(TEMP_S[0])), int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])), int(round(WIND_S[2])), int(round(WIND_S[1]))])
			if jj == 24 : DAY2.append([STN, AREA, W_AREA, NAME, afterday1, FISH_NAME, FISH_TYPE, AFTERDAY1_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(TEMP_S[0])), int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])), int(round(WIND_S[2])), int(round(WIND_S[1]))])
			if jj == 48 : DAY3.append([STN, AREA, W_AREA, NAME, afterday2, FISH_NAME, FISH_TYPE, AFTERDAY2_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(TEMP_S[0])), int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])), int(round(WIND_S[2])), int(round(WIND_S[1]))])
			if jj == 72 : DAY4.append([STN, AREA, W_AREA, NAME, afterday3, FISH_NAME, FISH_TYPE, AFTERDAY3_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(TEMP_S[0])), int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])), int(round(WIND_S[2])), int(round(WIND_S[1]))])
			if jj == 96 : DAY5.append([STN, AREA, W_AREA, NAME, afterday4, FISH_NAME, FISH_TYPE, AFTERDAY4_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(TEMP_S[0])), int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])), int(round(WIND_S[2])), int(round(WIND_S[1]))])
			if jj == 120 : DAY6.append([STN, AREA, W_AREA, NAME, afterday5, FISH_NAME, FISH_TYPE, AFTERDAY5_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(TEMP_S[0])), int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])), int(round(WIND_S[2])), int(round(WIND_S[1]))])
			if jj == 144 : DAY7.append([STN, AREA, W_AREA, NAME, afterday6, FISH_NAME, FISH_TYPE, AFTERDAY6_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(TEMP_S[0])), int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])), int(round(WIND_S[2])), int(round(WIND_S[1]))])
			jj = jj + 24 #24시간 간격으로 일괄 계산
			
	else :
		if FISH_TYPE == 'GR' or FISH_TYPE =='GP':
			MSG = 'No service this season ... GR and GP'
			print(MSG)
		else :
			jj = 0 ; jjj = 0
			while jj <= 144:
				WIND_S = Statistic().min_max_ave('KHOA', 'daily', WIND, WRF_X, WRF_Y, jj)
				TEMP_S = Statistic().min_max_ave('KHOA', 'daily', TEMP, WRF_X, WRF_Y, jj)
				
				if os.path.isfile(INFILE_6):
					if jj <= 48 :
						SST_S  = Statistic().min_max_ave('KHOA', 'daily', SST, MOHID_X, MOHID_Y, jj)
					else :
						SST_S  = Statistic().min_max_ave('KHOA', 'daily', SST2, ROMS_X, ROMS_Y, jj)	
				else : 
					SST_S  = Statistic().min_max_ave('KHOA', 'daily', SST, ROMS_X, ROMS_Y, jj)

				if os.path.isfile(INFILE_3):
					if jj <= 48 :
						jjj = int(jj / 3) #3시간 자료
						if CWW3_LOC == 1 : WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_1, CWW3_X, CWW3_Y, jjj)
						if CWW3_LOC == 2 : WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_2, CWW3_X, CWW3_Y, jjj)
						if CWW3_LOC == 3 : WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_3, CWW3_X, CWW3_Y, jjj)
						if CWW3_LOC == 4 : WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_4, CWW3_X, CWW3_Y, jjj)
						if CWW3_LOC == 5 : WAVE_S = Statistic().min_max_ave('KMA', 'daily', WHT_5, CWW3_X, CWW3_Y, jjj)
					else :
						WAVE_S = Statistic().min_max_ave('KHOA', 'daily', WHT, WW3_X, WW3_Y, jj)
				else : 
					WAVE_S = Statistic().min_max_ave('KHOA', 'daily', WHT, WW3_X, WW3_Y, jj)

				#VARS_S ampm [0:am_min 1:am_max, 2:am_ave, 3:pm_min, 4:pm_max, 5:pm_ave] ; VARS_S daily [0:min 1:max, 2:ave]
				if jj == 0  : DAY1.append([STN, AREA, W_AREA, NAME, today, FISH_NAME, FISH_TYPE, TODAY_MUL,         round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(TEMP_S[0])), int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])), int(round(WIND_S[2])), int(round(WIND_S[1]))])
				if jj == 24 : DAY2.append([STN, AREA, W_AREA, NAME, afterday1, FISH_NAME, FISH_TYPE, AFTERDAY1_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(TEMP_S[0])), int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])), int(round(WIND_S[2])), int(round(WIND_S[1]))])
				if jj == 48 : DAY3.append([STN, AREA, W_AREA, NAME, afterday2, FISH_NAME, FISH_TYPE, AFTERDAY2_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(TEMP_S[0])), int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])), int(round(WIND_S[2])), int(round(WIND_S[1]))])
				if jj == 72 : DAY4.append([STN, AREA, W_AREA, NAME, afterday3, FISH_NAME, FISH_TYPE, AFTERDAY3_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(TEMP_S[0])), int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])), int(round(WIND_S[2])), int(round(WIND_S[1]))])
				if jj == 96 : DAY5.append([STN, AREA, W_AREA, NAME, afterday4, FISH_NAME, FISH_TYPE, AFTERDAY4_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(TEMP_S[0])), int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])), int(round(WIND_S[2])), int(round(WIND_S[1]))])
				if jj == 120 : DAY6.append([STN, AREA, W_AREA, NAME, afterday5, FISH_NAME, FISH_TYPE, AFTERDAY5_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(TEMP_S[0])), int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])), int(round(WIND_S[2])), int(round(WIND_S[1]))])
				if jj == 144 : DAY7.append([STN, AREA, W_AREA, NAME, afterday6, FISH_NAME, FISH_TYPE, AFTERDAY6_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(TEMP_S[0])), int(round(TEMP_S[2])), int(round(TEMP_S[1])), int(round(WIND_S[0])), int(round(WIND_S[2])), int(round(WIND_S[1]))])
				jj = jj + 24 #24시간 간격으로 일괄 계산
	ii = ii + 1

LEN_DAY= len(DAY1) # 1day data length 
#[Combine and sorting] date > am/pm > stn ============================================================================
ii = 0
while ii <= LEN_DAY-1 : COM.append(DAY1[ii]); ii = ii + 1
ii = 0                                                                          
while ii <= LEN_DAY-1 : COM.append(DAY2[ii]); ii = ii + 1
ii = 0                                                                          
while ii <= LEN_DAY-1 : COM.append(DAY3[ii]); ii = ii + 1
ii = 0                                                                          
while ii <= LEN_DAY-1 : COM.append(DAY4[ii]); ii = ii + 1
ii = 0                                                                          
while ii <= LEN_DAY-1 : COM.append(DAY5[ii]); ii = ii + 1
ii = 0                                                                          
while ii <= LEN_DAY-1 : COM.append(DAY6[ii]); ii = ii + 1
ii = 0                                                                          
while ii <= LEN_DAY-1 : COM.append(DAY7[ii]); ii = ii + 1
COM_LEN = len(COM)
#print(len(DAY1), COM_LEN, INF_LEN )

#[KMA WARNING INFORAMTION : special weather report]=====================================================================================================
ii = 0 
while ii <= COM_LEN-1:
	jj = 1
	while jj <= WARN_LEN-1:
		DEV = WARN[jj].split(',')
		WARN_AREA = DEV[0] ; WARN_TYPE = DEV[1] ; WARN_SDAY = DEV[2] ; WARN_SHR = DEV[3]
		#print(WARN_AREA, WARN_TYPE, WARN_SDAY , WARN_SHR)
		if WARN_TYPE == 'WW2' : WARN_TYPE = 'WW'
		if WARN_TYPE == 'TY2' : WARN_TYPE = 'TY'
		if WARN_TYPE == 'SS2' : WARN_TYPE = 'SS'
		
		if int(COM[ii][4]) >= int(WARN_SDAY) and COM[ii][2] == WARN_AREA :
			if COM[ii][4] == today or COM[ii][4] == afterday1 or COM[ii][4] == afterday2:
				COM[ii].insert(20,WARN_TYPE)
			else :
				COM[ii].insert(20,'-')
				#print(COM[ii][12], len(COM[ii]))

			jj = WARN_LEN
		else:
			jj = jj + 1
			if jj == (WARN_LEN-1) :
				COM[ii].insert(20,'-')
		jj = jj
	ii = ii + 1

#ii = 0
#while ii <= COM_LEN-1:
#	print(COM[ii],ii)
#	ii = ii + 1
#[Index Score Calculate] ========================================================================================
COM_LEN = len(COM)
ii = 0
while ii <= COM_LEN-1 :
	#print(ii)
                    #0   1     2      3       4           5          6           7            8          9         10         11         12      13         14       15          16           17       18         19         20
    #DAY3.append([STN, AREA, W_AREA, NAME, afterday2, FISH_NAME, FISH_TYPE, AFTERDAY2_MUL, WAVE_S[0], WAVE_S[2], WAVES_[1], SST_S[0], SST_S[2], SST_S[1], TEMP_S[0], TEMP_S[2], TEMP_S[1], WIND_S[0], WIND_S[2], WIND_S[1]], WARN])
	TIDE_SCRE = IndexScore().tide_score(COM[ii][6],COM[ii][7])
	WAVE_SCRE = IndexScore().wave_score(round(float(COM[ii][10]),1))
	SST_SCRE = IndexScore().sst_score(COM[ii][6],COM[ii][12])
	TEMP_SCRE = IndexScore().temp_score(COM[ii][15])
	WIND_SCRE = IndexScore().wind_score(COM[ii][19])
	WARN_SCRE = IndexScore().warn_score(COM[ii][20])
	TOTAL_SCRE1 = IndexScore().total_score(TIDE_SCRE, WAVE_SCRE, SST_SCRE, TEMP_SCRE, WIND_SCRE, WARN_SCRE)[0] # forecast score(no rain, no warning)
	TOTAL_SCRE2 = IndexScore().total_score(TIDE_SCRE, WAVE_SCRE, SST_SCRE, TEMP_SCRE, WIND_SCRE, WARN_SCRE)[1] # service score(rain, warning)
	QUOTIENT_SCRE1 = IndexScore().quotient_score(TOTAL_SCRE1) # forecast score(no rain, no warning)
	QUOTIENT_SCRE2 = IndexScore().quotient_score(TOTAL_SCRE2) # service score(rain, warning)

    #              0    1       2      3       4           5          6           7            8          9         10         11         12      13         14       15          16           17       18         19         20     21          22          23            24    25       26          27          28        29                  30
    #DAY3.append([STN, AREA, W_AREA, NAME, afterday2, FISH_NAME, FISH_TYPE, AFTERDAY2_MUL, TIDE_SCRE, WAVE_S[0], WAVE_S[2], WAVES_[1], WAVE_SCRE, SST_S[0], SST_S[2], SST_S[1],SST_SCRE, TEMP_S[0], TEMP_S[2], TEMP_S[1],TEMP_SCRE, WIND_S[0], WIND_S[2], WIND_S[1]], WIND_SCRE, WARN, WARN_SCRE, TOTAL_SCRE1, TOTAL_SCRE2, QUOTIENT_SCRE1, QUOTIENT_SCRE2 ])
	COM[ii].insert(8,TIDE_SCRE) ; COM[ii].insert(12,WAVE_SCRE) ; COM[ii].insert(16,SST_SCRE); COM[ii].insert(20,TEMP_SCRE) ; COM[ii].insert(24,WIND_SCRE) ; COM[ii].insert(26,WARN_SCRE) ;COM[ii].insert(27,TOTAL_SCRE1) ; COM[ii].insert(28,TOTAL_SCRE2) ; COM[ii].insert(29,QUOTIENT_SCRE1) ; COM[ii].insert(30,QUOTIENT_SCRE2)
	ii = ii + 1

#ii = 0
#while ii <= COM_LEN-1:
#	print(COM[ii])
#	ii = ii + 1

#[Output Data] ========================================================================================
OUT_FNAME1=dir1+'/SFEQ_INDEX_FCST_'+today+'.csv'
with open(OUT_FNAME1,'w',encoding='utf8') as file:
	file.write('생산일,코드,권역,지역,예측일자,어종,어종타입,물때,물때점수,최소파고,평균파고,최대파고,파고점수,최소수온,평균수온,최대수온,수온점수,최저기온,평균기온,최대기온,기온점수,최소풍속,평균풍속,최대풍속,풍속점수,총점수,예보지수\n',)
	ii = 0
	while ii <= COM_LEN-1 :
		#[전체 데이터 Writing]
		file.write(f'{today},{COM[ii][0]},{COM[ii][1]},{COM[ii][3]},{COM[ii][4]},{COM[ii][5]},{COM[ii][6]},{COM[ii][7]},{COM[ii][8]},{COM[ii][9]:2.1f},{COM[ii][10]:2.1f},{COM[ii][11]:2.1f},{COM[ii][12]},{COM[ii][13]},{COM[ii][14]},{COM[ii][15]},{COM[ii][16]},{COM[ii][17]},{COM[ii][18]},{COM[ii][19]},{COM[ii][20]},{COM[ii][21]},{COM[ii][22]},{COM[ii][23]},{COM[ii][24]},{COM[ii][27]:4.2f},{COM[ii][29]}\n')
		ii = ii + 1

OUT_FNAME2=dir1+'/SFEQ_INDEX_SERVICE_'+today+'.csv'
with open(OUT_FNAME2,'w',encoding='utf8') as file:
	file.write('코드,권역,지역,예측일자,어종,어종타입,물때,물때점수,최소파고,평균파고,최대파고,파고점수,최소수온,평균수온,최대수온,수온점수,최저기온,평균기온,최대기온,기온점수,최소풍속,평균풍속,최대풍속,풍속점수,특보,특보점수,총점수,예보지수\n',)
	ii = 0
	while ii <= COM_LEN-1 :
		#[WEB_~~_SCRE Format]
		file.write(f'{COM[ii][0]},{COM[ii][1]},{COM[ii][3]},{COM[ii][4]},{COM[ii][5]},{COM[ii][6]},{COM[ii][7]},{COM[ii][8]},{COM[ii][9]:2.1f},{COM[ii][10]:2.1f},{COM[ii][11]:2.1f},{COM[ii][12]},{COM[ii][13]},{COM[ii][14]},{COM[ii][15]},{COM[ii][16]},{COM[ii][17]},{COM[ii][18]},{COM[ii][19]},{COM[ii][20]},{COM[ii][21]},{COM[ii][22]},{COM[ii][23]},{COM[ii][24]},{COM[ii][25]},{COM[ii][26]},{COM[ii][28]:4.2f},{COM[ii][30]}\n')
		ii = ii + 1

print("#SFEQ FCST_INDEX CREAT Complete==========")
