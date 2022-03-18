#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.04.11] edit 19.08.22
import sys
import os
#os.path.join(os.getcwd(),"Function")
import numpy as np
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime
from Function.skeq_function import IndexScore
from Function.statistic_function import Statistic

print("#SKEQ FCST_INDEX CREAT Start==========")

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
POINT_INF = open('./Info/SK_Point_Info.csv','r',encoding='utf8')
INF = [str(INFO) for INFO in POINT_INF.read().split()]
INF_LEN = len(INF)

POINT_INF2 = open('./Info/WEB_SKEC_INFO.csv','r',encoding='utf8')
INF2 = [str(INFO) for INFO in POINT_INF2.read().split()]
INF_LEN2 = len(INF2)

#[KMA CITY and WARNING data read]=========================================================================
if not os.path.exists(dir1+'/SK_CITY.csv'): # 동네예보 수집 에러에 따른 자료 미생성시 그냥 예측자료 사용
	print('CITY_FORECAST DATA Not found') ; CITY_LEN=0
else:
	CITY_INF = open(dir1+'/SK_CITY.csv','r',encoding='utf8')
	CITY = [LST for LST in CITY_INF.read().split()]
	CITY_LEN = len(CITY)


WARN_INF = open(dir1+'/KMA_WARNING.csv','r',encoding='utf8')
WARN = [LST for LST in WARN_INF.read().split()]
WARN_LEN = len(WARN)

#[SEASICK DATA Extract] ====================================================================================
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
	STN = DEV[0] ; NAME = DEV[2] ; LON = DEV[3] ; LAT = DEV[4]
	WRF_X = int(DEV[7]) ; WRF_Y = int(DEV[8]) ; WW3_X = int(DEV[9]) ; WW3_Y = int(DEV[10])
	CWW3_X = int(DEV[11]) ; CWW3_Y = int(DEV[12]) ; CWW3_LOC = int(DEV[13])
	RWW3_X = int(DEV[14]) ; RWW3_Y = int(DEV[15])
	jj = 0 ; jjj = 0

	while jj <= 144:
		WIND_2S = Statistic().min_max_ave('KHOA', 'ampm', WIND, WRF_X, WRF_Y, jj)
		WIND_S = Statistic().min_max_ave('KHOA', 'daily', WIND, WRF_X, WRF_Y, jj)
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
			DAY1.append([STN, NAME, today, 'AM', WIND_2S[0], WIND_2S[2], WIND_2S[1], WAVE_2S[0], WAVE_2S[2], WAVE_2S[1]])
			DAY1.append([STN, NAME, today, 'PM', WIND_2S[3], WIND_2S[5], WIND_2S[4], WAVE_2S[3], WAVE_2S[5], WAVE_2S[4]])
		elif  jj == 24 :
			DAY2.append([STN, NAME, afterday1, 'AM', WIND_2S[0], WIND_2S[2], WIND_2S[1], WAVE_2S[0], WAVE_2S[2], WAVE_2S[1]])
			DAY2.append([STN, NAME, afterday1, 'PM', WIND_2S[3], WIND_2S[5], WIND_2S[4], WAVE_2S[3], WAVE_2S[5], WAVE_2S[4]])
		elif  jj ==48 :
			DAY3.append([STN, NAME, afterday2, 'AM', WIND_2S[0], WIND_2S[2], WIND_2S[1], WAVE_2S[0], WAVE_2S[2], WAVE_2S[1]])
			DAY3.append([STN, NAME, afterday2, 'PM', WIND_2S[3], WIND_2S[5], WIND_2S[4], WAVE_2S[3], WAVE_2S[5], WAVE_2S[4]])
		elif  jj ==72 :
			DAY4.append([STN, NAME, afterday3, 'DY', WIND_S[0], WIND_S[2], WIND_S[1], WAVE_S[0], WAVE_S[2], WAVE_S[1]])
		elif  jj ==96 :
			DAY5.append([STN, NAME, afterday4, 'DY', WIND_S[0], WIND_S[2], WIND_S[1], WAVE_S[0], WAVE_S[2], WAVE_S[1]])
		elif  jj ==120 :
			DAY6.append([STN, NAME, afterday5, 'DY', WIND_S[0], WIND_S[2], WIND_S[1], WAVE_S[0], WAVE_S[2], WAVE_S[1]])
		elif  jj ==144 :
			DAY7.append([STN, NAME, afterday6, 'DY', WIND_S[0], WIND_S[2], WIND_S[1], WAVE_S[0], WAVE_S[2], WAVE_S[1]])
		jj = jj + 24 #24시간 간격으로 일괄 계산

	ii = ii + 1

LEN_DAY= len(DAY1) # AM/PM 1day data length 
LEN_DAY2= len(DAY4)# DAILY 1day data length 
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

COM2=[] ; DAY1=[] ; DAY2=[] ; DAY3=[] ; DAY4=[] ; DAY5=[] ; DAY6=[] ; DAY7 =[]
ii = 1
while ii <= INF_LEN2-1 :
	DEV = INF2[ii].split(',')
	STN = DEV[0]; NAME = DEV[2] ; SHIP = DEV[3] ; SAIL_HR = DEV[5] ; SHIP_TON=DEV[8] ; SHIP_TYPE=DEV[4]
	W_AREA1 = DEV[18] ; W_AREA2 = DEV[19] ; W_AREA3 = DEV[20] ; W_AREA4 = DEV[21]
	HM = SAIL_HR.split(':')
	SAIL_TIME = float(HM[0])+(float(HM[1])/60)
	#print(HM[0],HM[1], SAIL_TIME)

	jj = 0
	MIN_WIND_AM1 = [] ; MIN_WIND_AM2 = [] ; MIN_WIND_AM3 = [] ; MIN_WIND_PM1 = [] ; MIN_WIND_PM2 = [] ; MIN_WIND_PM3 = [] ; MIN_WIND_DAY4 = [] ; MIN_WIND_DAY5 = [] ; MIN_WIND_DAY6 = [] ; MIN_WIND_DAY7 = []
	MIN_WAVE_AM1 = [] ; MIN_WAVE_AM2 = [] ; MIN_WAVE_AM3 = [] ; MIN_WAVE_PM1 = [] ; MIN_WAVE_PM2 = [] ; MIN_WAVE_PM3 = [] ; MIN_WAVE_DAY4 = [] ; MIN_WAVE_DAY5 = [] ; MIN_WAVE_DAY6 = [] ; MIN_WAVE_DAY7 = [] 
	AVE_WIND_AM1 = [] ; AVE_WIND_AM2 = [] ; AVE_WIND_AM3 = [] ; AVE_WIND_PM1 = [] ; AVE_WIND_PM2 = [] ; AVE_WIND_PM3 = [] ; AVE_WIND_DAY4 = [] ; AVE_WIND_DAY5 = [] ; AVE_WIND_DAY6 = [] ; AVE_WIND_DAY7 = []
	AVE_WAVE_AM1 = [] ; AVE_WAVE_AM2 = [] ; AVE_WAVE_AM3 = [] ; AVE_WAVE_PM1 = [] ; AVE_WAVE_PM2 = [] ; AVE_WAVE_PM3 = [] ; AVE_WAVE_DAY4 = [] ; AVE_WAVE_DAY5 = [] ; AVE_WAVE_DAY6 = [] ; AVE_WAVE_DAY7 = []
	MAX_WIND_AM1 = [] ; MAX_WIND_AM2 = [] ; MAX_WIND_AM3 = [] ; MAX_WIND_PM1 = [] ; MAX_WIND_PM2 = [] ; MAX_WIND_PM3 = [] ; MAX_WIND_DAY4 = [] ; MAX_WIND_DAY5 = [] ; MAX_WIND_DAY6 = [] ; MAX_WIND_DAY7 = []
	MAX_WAVE_AM1 = [] ; MAX_WAVE_AM2 = [] ; MAX_WAVE_AM3 = [] ; MAX_WAVE_PM1 = [] ; MAX_WAVE_PM2 = [] ; MAX_WAVE_PM3 = [] ; MAX_WAVE_DAY4 = [] ; MAX_WAVE_DAY5 = [] ; MAX_WAVE_DAY6 = [] ; MAX_WAVE_DAY7 = []
	while jj <= COM_LEN-1 :
		if NAME == COM[jj][1] and today == COM[jj][2] and 'AM' == COM[jj][3]:
			MIN_WIND_AM1.append(COM[jj][4]) ; AVE_WIND_AM1.append(COM[jj][5]) ; MAX_WIND_AM1.append(COM[jj][6])
			MIN_WAVE_AM1.append(COM[jj][7]) ; AVE_WAVE_AM1.append(COM[jj][8]) ; MAX_WAVE_AM1.append(COM[jj][9])
		elif NAME == COM[jj][1] and today == COM[jj][2] and 'PM' == COM[jj][3]:
			MIN_WIND_PM1.append(COM[jj][4]) ; AVE_WIND_PM1.append(COM[jj][5]) ; MAX_WIND_PM1.append(COM[jj][6])
			MIN_WAVE_PM1.append(COM[jj][7]) ; AVE_WAVE_PM1.append(COM[jj][8]) ; MAX_WAVE_PM1.append(COM[jj][9])
		elif NAME == COM[jj][1] and afterday1 == COM[jj][2] and 'AM' == COM[jj][3]:
			MIN_WIND_AM2.append(COM[jj][4]) ; AVE_WIND_AM2.append(COM[jj][5]) ; MAX_WIND_AM2.append(COM[jj][6])
			MIN_WAVE_AM2.append(COM[jj][7]) ; AVE_WAVE_AM2.append(COM[jj][8]) ; MAX_WAVE_AM2.append(COM[jj][9])
		elif NAME == COM[jj][1] and afterday1 == COM[jj][2] and 'PM' == COM[jj][3]:
			MIN_WIND_PM2.append(COM[jj][4]) ; AVE_WIND_PM2.append(COM[jj][5]) ; MAX_WIND_PM2.append(COM[jj][6])
			MIN_WAVE_PM2.append(COM[jj][7]) ; AVE_WAVE_PM2.append(COM[jj][8]) ; MAX_WAVE_PM2.append(COM[jj][9])
		elif NAME == COM[jj][1] and afterday2 == COM[jj][2] and 'AM' == COM[jj][3]:
			MIN_WIND_AM3.append(COM[jj][4]) ; AVE_WIND_AM3.append(COM[jj][5]) ; MAX_WIND_AM3.append(COM[jj][6])
			MIN_WAVE_AM3.append(COM[jj][7]) ; AVE_WAVE_AM3.append(COM[jj][8]) ; MAX_WAVE_AM3.append(COM[jj][9])
		elif NAME == COM[jj][1] and afterday2 == COM[jj][2] and 'PM' == COM[jj][3]:
			MIN_WIND_PM3.append(COM[jj][4]) ; AVE_WIND_PM3.append(COM[jj][5]) ; MAX_WIND_PM3.append(COM[jj][6])
			MIN_WAVE_PM3.append(COM[jj][7]) ; AVE_WAVE_PM3.append(COM[jj][8]) ; MAX_WAVE_PM3.append(COM[jj][9])
		elif NAME == COM[jj][1] and afterday3 == COM[jj][2] and 'DY' == COM[jj][3]:
			MIN_WIND_DAY4.append(COM[jj][4]) ; AVE_WIND_DAY4.append(COM[jj][5]) ; MAX_WIND_DAY4.append(COM[jj][6])
			MIN_WAVE_DAY4.append(COM[jj][7]) ; AVE_WAVE_DAY4.append(COM[jj][8]) ; MAX_WAVE_DAY4.append(COM[jj][9])
		elif NAME == COM[jj][1] and afterday4 == COM[jj][2] and 'DY' == COM[jj][3]:
			MIN_WIND_DAY5.append(COM[jj][4]) ; AVE_WIND_DAY5.append(COM[jj][5]) ; MAX_WIND_DAY5.append(COM[jj][6])
			MIN_WAVE_DAY5.append(COM[jj][7]) ; AVE_WAVE_DAY5.append(COM[jj][8]) ; MAX_WAVE_DAY5.append(COM[jj][9])
		elif NAME == COM[jj][1] and afterday5 == COM[jj][2] and 'DY' == COM[jj][3]:
			MIN_WIND_DAY6.append(COM[jj][4]) ; AVE_WIND_DAY6.append(COM[jj][5]) ; MAX_WIND_DAY6.append(COM[jj][6])
			MIN_WAVE_DAY6.append(COM[jj][7]) ; AVE_WAVE_DAY6.append(COM[jj][8]) ; MAX_WAVE_DAY6.append(COM[jj][9])
		elif NAME == COM[jj][1] and afterday6 == COM[jj][2] and 'DY' == COM[jj][3]:
			MIN_WIND_DAY7.append(COM[jj][4]) ; AVE_WIND_DAY7.append(COM[jj][5]) ; MAX_WIND_DAY7.append(COM[jj][6])
			MIN_WAVE_DAY7.append(COM[jj][7]) ; AVE_WAVE_DAY7.append(COM[jj][8]) ; MAX_WAVE_DAY7.append(COM[jj][9])
		
		
		jj = jj + 1
	WIND_MIN_AM1 = np.min(MIN_WIND_AM1) ; WIND_MIN_AM2 = np.min(MIN_WIND_AM2) ; WIND_MIN_AM3 = np.min(MIN_WIND_AM3) 
	WIND_AVE_AM1 = np.mean(AVE_WIND_AM1) ; WIND_AVE_AM2 = np.mean(AVE_WIND_AM2) ; WIND_AVE_AM3 = np.mean(AVE_WIND_AM3)	
	WIND_MAX_AM1 = np.max(MAX_WIND_AM1) ; WIND_MAX_AM2 = np.max(MAX_WIND_AM2) ; WIND_MAX_AM3 = np.max(MAX_WIND_AM3) 

	WIND_MIN_PM1 = np.min(MIN_WIND_PM1) ; WIND_MIN_PM2 = np.min(MIN_WIND_PM2) ; WIND_MIN_PM3 = np.min(MIN_WIND_PM3) 
	WIND_AVE_PM1 = np.mean(AVE_WIND_PM1) ; WIND_AVE_PM2 = np.mean(AVE_WIND_PM2) ; WIND_AVE_PM3 = np.mean(AVE_WIND_PM3) 
	WIND_MAX_PM1 = np.max(MAX_WIND_PM1) ; WIND_MAX_PM2 = np.max(MAX_WIND_PM2) ; WIND_MAX_PM3 = np.max(MAX_WIND_PM3)

	WIND_MIN_DAY4 = np.min(MIN_WIND_DAY4) ; WIND_MIN_DAY5 = np.min(MIN_WIND_DAY5) ; WIND_MIN_DAY6 = np.min(MIN_WIND_DAY6) ; WIND_MIN_DAY7 = np.min(MIN_WIND_DAY7) 
	WIND_AVE_DAY4 = np.mean(AVE_WIND_DAY4) ; WIND_AVE_DAY5 = np.mean(AVE_WIND_DAY5) ; WIND_AVE_DAY6 = np.mean(AVE_WIND_DAY6) ; WIND_AVE_DAY7 = np.mean(AVE_WIND_DAY7) 
	WIND_MAX_DAY4 = np.max(MAX_WIND_DAY4) ; WIND_MAX_DAY5 = np.max(MAX_WIND_DAY5) ; WIND_MAX_DAY6 = np.max(MAX_WIND_DAY6) ; WIND_MAX_DAY7 = np.max(MAX_WIND_DAY7)


	WAVE_MIN_AM1 = np.min(MIN_WAVE_AM1) ; WAVE_MIN_AM2 = np.min(MIN_WAVE_AM2) ; WAVE_MIN_AM3 = np.min(MIN_WAVE_AM3) 
	WAVE_AVE_AM1 = np.mean(AVE_WAVE_AM1) ; WAVE_AVE_AM2 = np.mean(AVE_WAVE_AM2) ; WAVE_AVE_AM3 = np.mean(AVE_WAVE_AM3)	
	WAVE_MAX_AM1 = np.max(MAX_WAVE_AM1) ; WAVE_MAX_AM2 = np.max(MAX_WAVE_AM2) ; WAVE_MAX_AM3 = np.max(MAX_WAVE_AM3)	

	WAVE_MIN_PM1 = np.min(MIN_WAVE_PM1) ; WAVE_MIN_PM2 = np.min(MIN_WAVE_PM2) ; WAVE_MIN_PM3 = np.min(MIN_WAVE_PM3) 
	WAVE_AVE_PM1 = np.mean(AVE_WAVE_PM1) ; WAVE_AVE_PM2 = np.mean(AVE_WAVE_PM2) ; WAVE_AVE_PM3 = np.mean(AVE_WAVE_PM3) 
	WAVE_MAX_PM1 = np.max(MAX_WAVE_PM1) ; WAVE_MAX_PM2 = np.max(MAX_WAVE_PM2) ; WAVE_MAX_PM3 = np.max(MAX_WAVE_PM3)

	WAVE_MIN_DAY4 = np.min(MIN_WAVE_DAY4) ; WAVE_MIN_DAY5 = np.min(MIN_WAVE_DAY5) ; WAVE_MIN_DAY6 = np.min(MIN_WAVE_DAY6) ; WAVE_MIN_DAY7 = np.min(MIN_WAVE_DAY7) 
	WAVE_AVE_DAY4 = np.mean(AVE_WAVE_DAY4) ; WAVE_AVE_DAY5 = np.mean(AVE_WAVE_DAY5) ; WAVE_AVE_DAY6 = np.mean(AVE_WAVE_DAY6) ; WAVE_AVE_DAY7 = np.mean(AVE_WAVE_DAY7) 
	WAVE_MAX_DAY4 = np.max(MAX_WAVE_DAY4) ; WAVE_MAX_DAY5 = np.max(MAX_WAVE_DAY5) ; WAVE_MAX_DAY6 = np.max(MAX_WAVE_DAY6) ; WAVE_MAX_DAY7 = np.max(MAX_WAVE_DAY7) 

	
	DAY1.append([STN, NAME, W_AREA1, W_AREA2, W_AREA3, W_AREA4, SHIP, SHIP_TYPE, today,  'AM',    SAIL_TIME, SHIP_TON, WAVE_MIN_AM1, WAVE_AVE_AM1, WAVE_MAX_AM1, WIND_MIN_AM1, WIND_AVE_AM1, WIND_MAX_AM1])
	DAY1.append([STN, NAME, W_AREA1, W_AREA2, W_AREA3, W_AREA4, SHIP, SHIP_TYPE, today,  'PM',    SAIL_TIME, SHIP_TON, WAVE_MIN_PM1, WAVE_AVE_PM1, WAVE_MAX_PM1, WIND_MIN_PM1, WIND_AVE_PM1, WIND_MAX_PM1])
	DAY2.append([STN, NAME, W_AREA1, W_AREA2, W_AREA3, W_AREA4, SHIP, SHIP_TYPE, afterday1, 'AM', SAIL_TIME, SHIP_TON, WAVE_MIN_AM2, WAVE_AVE_AM2, WAVE_MAX_AM2, WIND_MIN_AM2, WIND_AVE_AM2, WIND_MAX_AM2])
	DAY2.append([STN, NAME, W_AREA1, W_AREA2, W_AREA3, W_AREA4, SHIP, SHIP_TYPE, afterday1, 'PM', SAIL_TIME, SHIP_TON, WAVE_MIN_PM2, WAVE_AVE_PM2, WAVE_MAX_PM2, WIND_MIN_PM2, WIND_AVE_PM2, WIND_MAX_PM2])
	DAY3.append([STN, NAME, W_AREA1, W_AREA2, W_AREA3, W_AREA4, SHIP, SHIP_TYPE, afterday2, 'AM', SAIL_TIME, SHIP_TON, WAVE_MIN_AM3, WAVE_AVE_AM3, WAVE_MAX_AM3, WIND_MIN_AM3, WIND_AVE_AM3, WIND_MAX_AM3])
	DAY3.append([STN, NAME, W_AREA1, W_AREA2, W_AREA3, W_AREA4, SHIP, SHIP_TYPE, afterday2, 'PM', SAIL_TIME, SHIP_TON, WAVE_MIN_PM3, WAVE_AVE_PM3, WAVE_MAX_PM3, WIND_MIN_PM3, WIND_AVE_PM3, WIND_MAX_PM3])
	DAY4.append([STN, NAME, W_AREA1, W_AREA2, W_AREA3, W_AREA4, SHIP, SHIP_TYPE, afterday3, 'DY', SAIL_TIME, SHIP_TON, WAVE_MIN_DAY4, WAVE_AVE_DAY4, WAVE_MAX_DAY4, WIND_MIN_DAY4, WIND_AVE_DAY4, WIND_MAX_DAY4])
	DAY5.append([STN, NAME, W_AREA1, W_AREA2, W_AREA3, W_AREA4, SHIP, SHIP_TYPE, afterday4, 'DY', SAIL_TIME, SHIP_TON, WAVE_MIN_DAY5, WAVE_AVE_DAY5, WAVE_MAX_DAY5, WIND_MIN_DAY5, WIND_AVE_DAY5, WIND_MAX_DAY5])
	DAY6.append([STN, NAME, W_AREA1, W_AREA2, W_AREA3, W_AREA4, SHIP, SHIP_TYPE, afterday5, 'DY', SAIL_TIME, SHIP_TON, WAVE_MIN_DAY6, WAVE_AVE_DAY6, WAVE_MAX_DAY6, WIND_MIN_DAY6, WIND_AVE_DAY6, WIND_MAX_DAY6])
	DAY7.append([STN, NAME, W_AREA1, W_AREA2, W_AREA3, W_AREA4, SHIP, SHIP_TYPE, afterday6, 'DY', SAIL_TIME, SHIP_TON, WAVE_MIN_DAY7, WAVE_AVE_DAY7, WAVE_MAX_DAY7, WIND_MIN_DAY7, WIND_AVE_DAY7, WIND_MAX_DAY7])
	
	ii = ii + 1

#[Combine and sorting] date > am/pm > stn ============================================================================
LEN_DAY= len(DAY1)
LEN_DAY2= len(DAY4)
ii = 0
while ii <= LEN_DAY-1 : COM2.append(DAY1[ii]); COM2.append(DAY1[ii+1]); ii = ii + 2
ii = 0
while ii <= LEN_DAY-1 : COM2.append(DAY2[ii]); COM2.append(DAY2[ii+1]); ii = ii + 2
ii = 0
while ii <= LEN_DAY-1 : COM2.append(DAY3[ii]); COM2.append(DAY3[ii+1]); ii = ii + 2
ii = 0
while ii <= LEN_DAY2-1 : COM2.append(DAY4[ii]) ; ii = ii + 1
ii = 0
while ii <= LEN_DAY2-1 : COM2.append(DAY5[ii]); ii = ii + 1
ii = 0
while ii <= LEN_DAY2-1 : COM2.append(DAY6[ii]); ii = ii + 1
ii = 0
while ii <= LEN_DAY2-1 : COM2.append(DAY7[ii]); ii = ii + 1

COM2_LEN = len(COM2)

#[KMA WARNING INFORAMTION : special weather report]=====================================================================================================
ii = 0 
while ii <= COM2_LEN-1:
	jj = 1
	while jj <= WARN_LEN-1:
		DEV = WARN[jj].split(',')
		WARN_AREA = DEV[0] ; WARN_TYPE = DEV[1] ; WARN_SDAY = DEV[2] ; WARN_SHR = DEV[3] ; WARN_EDAY = DEV[4] ; WARN_EHR = DEV[5]
		#print(WARN_AREA, WARN_TYPE)
		if int(COM2[ii][8]) < int(WARN_EDAY) and int(COM2[ii][8]) >= int(WARN_SDAY) and (COM2[ii][2] == WARN_AREA or COM2[ii][3] == WARN_AREA or COM2[ii][4] == WARN_AREA or COM2[ii][5] == WARN_AREA): #해제예고 일보다 전날일 경우 일괄적용
			if int(WARN_SDAY) == int(COM2[ii][8]) and WARN_SHR == 'PM':
				if COM2[ii][9] == 'AM' :
					COM2[ii].insert(18,'-')
				elif COM2[ii][9] == 'PM' or COM2[ii][9] == 'DY' :
					COM2[ii].insert(18,WARN_TYPE)					
			else :
				COM2[ii].insert(18,WARN_TYPE)				
			jj = WARN_LEN
			
		elif int(COM2[ii][8]) == int(WARN_EDAY) and int(COM2[ii][8]) > int(WARN_SDAY) and (COM2[ii][2] == WARN_AREA or COM2[ii][3] == WARN_AREA or COM2[ii][4] == WARN_AREA or COM2[ii][5] == WARN_AREA) : #해제예고일과 같을 경우 AM이면 오전만 적용, PM이면 오전/오후 모두적용
			if WARN_EHR == 'PM' :
				COM2[ii].insert(18,WARN_TYPE)
			elif WARN_EHR == 'AM' :
				if COM2[ii][9] == 'AM' or COM2[ii][9] == 'DY' :
					COM2[ii].insert(18,WARN_TYPE)
				else :
					COM2[ii].insert(18,'-')
			jj = WARN_LEN

		elif int(COM2[ii][8]) == int(WARN_EDAY) and int(COM2[ii][8]) == int(WARN_SDAY) and (COM2[ii][2] == WARN_AREA or COM2[ii][3] == WARN_AREA or COM2[ii][4] == WARN_AREA or COM2[ii][5] == WARN_AREA) : #해제예고일과 같을 경우 AM이면 오전만 적용, PM이면 오전/오후 모두적용
			if WARN_SHR == 'PM' :
				if COM2[ii][9] == 'PM' or COM2[ii][9] == 'DY' :
					COM2[ii].insert(18,WARN_TYPE)
				elif COM2[ii][5] == 'AM':
					COM2[ii].insert(18,'-')					
			else :
				COM2[ii].insert(18,WARN_TYPE)
			jj = WARN_LEN

		else:
			jj = jj + 1
			if jj == WARN_LEN :
				COM2[ii].insert(18,'-')
		jj = jj
	ii = ii + 1
	
#[Index Score Calculate] ========================================================================================
ii = 0
while ii <= len(COM2)-1 :
	SAIL_SCRE = IndexScore().sail_score(float(COM2[ii][10]))
	TON_SCRE = IndexScore().ton_score(float(COM2[ii][11]))
	WIND_SCRE = IndexScore().wind_score(round(float(COM2[ii][17]),1))
	WAVE_SCRE = IndexScore().wave_score(round(float(COM2[ii][14]),1))
	WARN_SCRE = IndexScore().warn_score(COM2[ii][18])
	TOTAL_SCRE1 = IndexScore().total_score(SAIL_SCRE, TON_SCRE, WIND_SCRE, WAVE_SCRE, WARN_SCRE)[0] # forecast score(no rain, no warning)
	TOTAL_SCRE2 = IndexScore().total_score(SAIL_SCRE, TON_SCRE, WIND_SCRE, WAVE_SCRE, WARN_SCRE)[1] # service score(rain, warning)
	QUOTIENT_SCRE1 = IndexScore().quotient_score(TOTAL_SCRE1)
	QUOTIENT_SCRE2 = IndexScore().quotient_score(TOTAL_SCRE2) # service score(rain, warning)

	COM2[ii].insert(11,SAIL_SCRE) ; COM2[ii].insert(13,TON_SCRE) ; COM2[ii].insert(17,WAVE_SCRE) ; COM2[ii].insert(21,WIND_SCRE) ; COM2[ii].insert(23,WARN_SCRE) ; COM2[ii].insert(24,TOTAL_SCRE1) ; COM2[ii].insert(25,TOTAL_SCRE2) ; COM2[ii].insert(26,QUOTIENT_SCRE1) ; COM2[ii].insert(27,QUOTIENT_SCRE2)
	ii = ii + 1

#[Output Data] ========================================================================================
OUT_FNAME1=dir1+'/SKEQ_INDEX_FCST_'+today+'.csv'
with open(OUT_FNAME1,'w',encoding='utf8') as file:
	#            0       1    2      3       4         5      6     7       8             9            10      11      12         13     14         15     16        17     18         19   20
	file.write('생산일,코드,항로명,선박명,선박종류,예측일자,시간,운항시간,운항시간점수,선박톤수,선박톤수점수,최소파고,평균파고,최대파고,파고점수,최소풍속,평균풍속,최대풍속,풍속점수,총점수,예보지수\n',)
	ii = 0
	while ii <= len(COM2)-1 :
		#[전체 데이터 Writing]
		file.write(f'{today},{COM2[ii][0]},{COM2[ii][1]},{COM2[ii][6]},{COM2[ii][7]},{COM2[ii][8]},{COM2[ii][9]},{COM2[ii][10]:3.1f},{COM2[ii][11]},{COM2[ii][12]},{COM2[ii][13]},{COM2[ii][14]:3.1f},{COM2[ii][15]:3.1f},{COM2[ii][16]:3.1f},{COM2[ii][17]},{COM2[ii][18]:3.1f},{COM2[ii][19]:3.1f},{COM2[ii][20]:3.1f},{COM2[ii][21]},{COM2[ii][24]:4.2f},{COM2[ii][26]}\n')
		ii = ii + 1

OUT_FNAME2=dir1+'/SKEQ_INDEX_SERVICE_'+today+'.csv'
with open(OUT_FNAME2,'w',encoding='utf8') as file:
	#            0  1    2   3    4    5    6     7       8     9    10   11    12    13   14   15   16   17     18
	file.write('코드,항로명,선박명,선박종류,예측일자,시간,운항시간,운항시간점수,선박톤수,선박톤수점수,최소파고,평균파고,최대파고,파고점수,최소풍속,평균풍속,최대풍속,풍속점수,특보,특보점수,총점수,예보지수\n',)
	ii = 0
	while ii <= len(COM2)-1 :
		file.write(f'{COM2[ii][0]},{COM2[ii][1]},{COM2[ii][6]},{COM2[ii][7]},{COM2[ii][8]},{COM2[ii][9]},{COM2[ii][10]:3.1f},{COM2[ii][11]},{COM2[ii][12]},{COM2[ii][13]},{COM2[ii][14]:3.1f},{COM2[ii][15]:3.1f},{COM2[ii][16]:3.1f},{COM2[ii][17]},{COM2[ii][18]:3.1f},{COM2[ii][19]:3.1f},{COM2[ii][20]:3.1f},{COM2[ii][21]},{COM2[ii][22]},{COM2[ii][23]},{COM2[ii][25]:4.2f},{COM2[ii][27]}\n')
		ii = ii + 1

print("#SKEQ FCST_INDEX CREAT Complete==========")

