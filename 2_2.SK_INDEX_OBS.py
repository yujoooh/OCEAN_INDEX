#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.04.11] edit 19.08.22
import sys
import os
import numpy as np
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime
from Function.skeq_function import IndexScore
from Function.statistic_function import Statistic
from Function.statistic_function2 import Statistic2

print("#SKEQ OBS_INDEX 1QC CREAT Start==========")

#[Date set] ==============================================================================================
#[Auto date set]
today = str(datetime.today().strftime('%Y%m%d'))
yesterday = (date.today() - timedelta(1)).strftime('%Y%m%d')

#[Manual date set]
#today = str(date(2020,1,20).strftime('%Y%m%d'))
#yesterday = (date(2020,1,20) - timedelta(1)).strftime('%Y%m%d')

dir1 = './Result/'+today

#[Model Data path] =======================================================================================
MPATH = './Model_Data/'
WRF_FNAME = 'WRF_' + str(yesterday) + '.nc'          # WRF_DM2 - KHOA
WW3_FNAME = 'WW3_' + str(yesterday) + '00.nc'        # WW3 - KHOA
CWW3_FNAME = 'CWW3_' + str(yesterday) + '00.nc'      # CWW3 - KMA
RWW3_FNAME = 'RWW3_' + str(yesterday) + '00.nc'     # RWW3 - KMA

INFILE_2 = MPATH+WRF_FNAME
INFILE_3 = MPATH+CWW3_FNAME
INFILE_4 = MPATH+WW3_FNAME
INFILE_5 = MPATH+RWW3_FNAME

#[READ Model_Data] =======================================================================================
#[YES3K]
#DATA = Dataset(INFILE_1, mode='r')
#SST = DATA.variables['temp'][:,:,:]  #[t,y,x]
#U_CURRENT = DATA.variables['u'][:,:,:]  #[t,y,x]
#V_CURRENT = DATA.variables['v'][:,:,:]  #[t,y,x]
#CURRENT= (U_CURRENT**2+V_CURRENT**2)**0.5  #Calculate Current speed
#
#[WRF]
DATA = Dataset(INFILE_2, mode='r')
TEMP = DATA.variables['Tair'][:,:,:]  #[t,y,x]
U_WIND = DATA.variables['Uwind'][:,:,:]  #[t,y,x]
V_WIND = DATA.variables['Vwind'][:,:,:]  #[t,y,x]
WIND = (U_WIND**2+V_WIND**2)**0.5  #Calculate Wind speed

##[CWW3, WW3] not yet RWW3
#if os.path.isfile(INFILE_3):
#	DATA = Dataset(INFILE_3, mode='r')
#	WHT_1 = DATA.variables['hsig1_dajn'][:,:,:]  #[t,y,x]
#	WHT_2 = DATA.variables['hsig2_gwju'][:,:,:]  #[t,y,x]
#	WHT_3 = DATA.variables['hsig3_jeju'][:,:,:]  #[t,y,x]
#	WHT_4 = DATA.variables['hsig4_busn'][:,:,:]  #[t,y,x]
#	WHT_5 = DATA.variables['hsig5_gawn'][:,:,:]  #[t,y,x]
#else :
#	DATA = Dataset(INFILE_4, mode='r')
#	WHT = DATA.variables['Hsig'][:,:,:]  #[t,y,x]


#[Info Data Read]=========================================================================================
POINT_INF = open('./Info/SK_Point_Info.csv','r',encoding='utf8')
INF = [str(INFO) for INFO in POINT_INF.read().split()]
INF_LEN = len(INF)

POINT_INF2 = open('./Info/WEB_SKEC_INFO.csv','r',encoding='utf8')
INF2 = [str(INFO) for INFO in POINT_INF2.read().split()]
INF_LEN2 = len(INF2)

#[OBS Data Read]==========================================================================================
OBS_DATA1 = open(dir1+'/OBS_Daily/OBS_KMA_'+yesterday+'.csv','r',encoding='utf8')
OBS1 = [str(INFO) for INFO in OBS_DATA1.read().split()]
OBS_DATA2 = open(dir1+'/OBS_Daily/OBS_KHOA_'+yesterday+'.csv','r',encoding='utf8')
OBS2 = [str(INFO) for INFO in OBS_DATA2.read().split()]

OBS_COM = OBS1 + OBS2
#print(OBS_COM)


#[SEASICK DATA Extract] ====================================================================================
DAY1 = [] # forecast data list
O_WHT1  = [] ; O_WHT2 = []

ii = 1
while ii <= INF_LEN-1 :
	DEV = INF[ii].split(',')
	STN = DEV[0] ; NAME = DEV[2] ; LON = DEV[3] ; LAT = DEV[4]
	WRF_X = int(DEV[7]) ; WRF_Y = int(DEV[8]) ; WW3_X = int(DEV[9]) ; WW3_Y = int(DEV[10])
	CWW3_X = int(DEV[11]) ; CWW3_Y = int(DEV[12]) ; CWW3_LOC = int(DEV[13])
	RWW3_X = int(DEV[14]) ; RWW3_Y = int(DEV[15])
	REF_AGY1=DEV[19]; REF_STN_WAVE1=DEV[20]; REF_AGY2=DEV[21]; REF_STN_WAVE2=DEV[22]

	M_WIND_S = Statistic().min_max_ave('KHOA', 'ampm', WIND, WRF_X, WRF_Y, 0)
	jj = 1; hr1=0
	while jj < len(OBS_COM)-1:
		DEV2 = OBS_COM[jj].split(',')
		OBS_STNID = DEV2[0] ; OBS_STN = DEV2[1] ; OBS_YMD = DEV2[2] ; OBS_SST = DEV2[3] ; OBS_WHT = DEV2[4]
		OBS_WSPD = DEV2[5] ; OBS_WDIR = DEV2[6] ; OBS_USPD = DEV2[7] ; OBS_VSPD = DEV2[8] ; OBS_AGY = DEV2[9]
		if REF_AGY1 == OBS_AGY and REF_STN_WAVE1 == OBS_STN : 
			hr1 = (f'{hr1:02d}')
			if OBS_YMD[8:10] == hr1 : 
				O_WHT1.append(round(float(OBS_WHT),1))
			else:
				O_WHT1.append(-999); jj = jj - 1
			hr1 = int(hr1) + 1
		if hr1 == 24 : break
		jj = jj + 1

	if(len(O_WHT1) < 24) :
		jj = len(O_WHT1)-1
		while jj < 24 :
			O_WHT1.append(-999)
			jj += 1
	

	jj = 1 ; hr2=0
	while jj < len(OBS_COM)-1:
		DEV2 = OBS_COM[jj].split(',')
		OBS_STNID = DEV2[0] ; OBS_STN = DEV2[1] ; OBS_YMD = DEV2[2] ; OBS_SST = DEV2[3] ; OBS_WHT = DEV2[4]
		OBS_WSPD = DEV2[5] ; OBS_WDIR = DEV2[6] ; OBS_USPD = DEV2[7] ; OBS_VSPD = DEV2[8] ; OBS_AGY = DEV2[9]
		if REF_AGY2 == OBS_AGY and REF_STN_WAVE2 == OBS_STN : 
			hr2 = (f'{hr2:02d}')
			if OBS_YMD[8:10] == hr2 : 
				O_WHT2.append(round(float(OBS_WHT),1))
			else:
				O_WHT2.append(-999); jj = jj - 1
			hr2 = int(hr2) + 1
			if hr2 == 24 : break
		jj = jj + 1					
			
	if(len(O_WHT2) < 24) :
		jj = len(O_WHT2)-1
		while jj < 24 :
			O_WHT2.append(-999)
			jj += 1		

	#관측자료 최대/최소/평균값 산정 및 참고지점 1,2순위의 자료 유무 판단.. 전체 없을 시 -999로
	if len(O_WHT1[9:19]) == 0 or O_WHT1[9:13].count(-999) == 4 or O_WHT1[12:19].count(-999) == 6 or O_WHT1[9:19].count(-999) == 10 :
		#print(NAME, REF_STN_WAVE1,"WAVE REF1 all data missing")
		if len(O_WHT2[9:19]) == 0 or O_WHT2[9:13].count(-999) == 4 or O_WHT2[12:19].count(-999) == 6 or O_WHT2[9:19].count(-999) == 10 :
			#print(NAME, REF_STN_WAVE2,"WAVE REF1/REF2 all data missing")
			WAVE_S = [-999,-999,-999,-999,-999,-999]
		else:
			WAVE_S = Statistic2().min_max_ave('ampm',O_WHT2,9)
	else:
		WAVE_S = Statistic2().min_max_ave('ampm',O_WHT1,9)
	
	#VARS_S ampm [0:am_min 1:am_max, 2:am_ave, 3:pm_min, 4:pm_max, 5:pm_ave] ; VARS_S daily [0:min 1:max, 2:ave]
	DAY1.append([STN, NAME, yesterday, 'AM', M_WIND_S[0], M_WIND_S[2], M_WIND_S[1], WAVE_S[0], WAVE_S[2], WAVE_S[1]])
	DAY1.append([STN, NAME, yesterday, 'PM', M_WIND_S[3], M_WIND_S[5], M_WIND_S[4], WAVE_S[3], WAVE_S[5], WAVE_S[4]])

	O_WHT1.clear(); O_WHT2.clear()
	ii = ii + 1

##[Result Check]
#ii = 0
#while ii < len(DAY1):
#	print(DAY1[ii])
#	ii = ii + 1

COM2=[]
ii = 1
while ii <= INF_LEN2-1 :
	DEV = INF2[ii].split(',')
	STN = DEV[0]; NAME = DEV[2] ; SHIP = DEV[3] ; SAIL_HR = DEV[5] ; SHIP_TON=DEV[8] ; SHIP_TYPE=DEV[4]
	HM = SAIL_HR.split(':')
	SAIL_TIME = float(HM[0])+(float(HM[1])/60)
	#print(HM[0],HM[1], SAIL_TIME)

	jj = 0
	MIN_WIND_AM1 = []; MIN_WIND_PM1 = [] ; AVE_WIND_AM1 = []; AVE_WIND_PM1 = [] ; MAX_WIND_AM1 = []; MAX_WIND_PM1 = []
	AVE_WAVE_AM1 = []; AVE_WAVE_PM1 = [] ; MIN_WAVE_AM1 = []; MIN_WAVE_PM1 = [] ; MAX_WAVE_AM1 = []; MAX_WAVE_PM1 = []
	while jj <= len(DAY1)-1 :
		#print(NAME,DAY1[jj][1],'AM',DAY1[jj][3])
		if NAME == DAY1[jj][1] and 'AM' == DAY1[jj][3]:
			MIN_WIND_AM1.append(DAY1[jj][4]) ; AVE_WIND_AM1.append(DAY1[jj][5]) ; MAX_WIND_AM1.append(DAY1[jj][6])
			MIN_WAVE_AM1.append(DAY1[jj][7]) ; AVE_WAVE_AM1.append(DAY1[jj][8]) ; MAX_WAVE_AM1.append(DAY1[jj][9])
		elif NAME == DAY1[jj][1] and 'PM' == DAY1[jj][3]:
			MIN_WIND_PM1.append(DAY1[jj][4]) ; AVE_WIND_PM1.append(DAY1[jj][5]) ; MAX_WIND_PM1.append(DAY1[jj][6])
			MIN_WAVE_PM1.append(DAY1[jj][7]) ; AVE_WAVE_PM1.append(DAY1[jj][8]) ; MAX_WAVE_PM1.append(DAY1[jj][9])
		jj = jj + 1

	WIND_MIN_AM1 = np.max(MIN_WIND_AM1) ; WIND_AVE_AM1 = np.max(AVE_WIND_AM1) ; WIND_MAX_AM1 = np.max(MAX_WIND_AM1)
	WIND_MIN_PM1 = np.max(MIN_WIND_PM1) ; WIND_AVE_PM1 = np.max(AVE_WIND_PM1) ; WIND_MAX_PM1 = np.max(MAX_WIND_PM1)	
	WAVE_MIN_AM1 = np.max(MIN_WAVE_AM1) ; WAVE_AVE_AM1 = np.max(AVE_WAVE_AM1) ; WAVE_MAX_AM1 = np.max(MAX_WAVE_AM1)	
	WAVE_MIN_PM1 = np.max(MIN_WAVE_PM1) ; WAVE_AVE_PM1 = np.max(AVE_WAVE_PM1) ; WAVE_MAX_PM1 = np.max(MAX_WAVE_PM1)
	
	COM2.append([STN, NAME, SHIP, SHIP_TYPE, yesterday,  'AM',    SAIL_TIME, SHIP_TON, WAVE_MIN_AM1, WAVE_AVE_AM1, WAVE_MAX_AM1, WIND_MIN_AM1, WIND_AVE_AM1, WIND_MAX_AM1])
	COM2.append([STN, NAME, SHIP, SHIP_TYPE, yesterday,  'PM',    SAIL_TIME, SHIP_TON, WAVE_MIN_PM1, WAVE_AVE_PM1, WAVE_MAX_PM1, WIND_MIN_PM1, WIND_AVE_PM1, WIND_MAX_PM1])
	ii = ii + 1

#ii = 0
#while ii <= len(COM2)-1:
#	print(COM2[ii])
#	ii = ii + 1

#[Index Score Calculate] ========================================================================================
ii = 0
while ii <= len(COM2)-1 :
	SAIL_SCRE = IndexScore().sail_score(float(COM2[ii][6]))
	TON_SCRE = IndexScore().ton_score(float(COM2[ii][7]))
	WIND_SCRE = IndexScore().wind_score(float(COM2[ii][13]))
	WAVE_SCRE = IndexScore().wave_score(float(COM2[ii][10]))
	WARN_SCRE = IndexScore().warn_score('-')
	TOTAL_SCRE1 = IndexScore().total_score(SAIL_SCRE, TON_SCRE, WIND_SCRE, WAVE_SCRE, WARN_SCRE)[0] # forecast score(no rain, no warning)

	COM2[ii].insert(7,SAIL_SCRE) ; COM2[ii].insert(9,TON_SCRE) ; COM2[ii].insert(13,WAVE_SCRE) ;COM2[ii].insert(17,WIND_SCRE); COM2[ii].insert(18,TOTAL_SCRE1)
	ii = ii + 1

#[Output Data] ========================================================================================
OUT_FNAME1=dir1+'/SKEQ_INDEX_OBS_1QC_'+today+'.csv'
with open(OUT_FNAME1,'w',encoding='utf8') as file:
	#            0  1    2   3    4    5    6     7       8     9    10   11    12    13   14   15   16   17     18
	file.write('생산일,코드,항로명,선박명,선박종류,예측일자,시간,운항시간,운항시간점수,선박톤수,선박톤수점수,최소파고,평균파고,최대파고,파고점수,최소풍속,평균풍속,최대풍속,풍속점수,총점수\n',)
	ii = 0
	while ii <= len(COM2)-1 :
		#[전체 데이터 Writing]
		file.write(f'{today},{COM2[ii][0]},{COM2[ii][1]},{COM2[ii][2]},{COM2[ii][3]},{COM2[ii][4]},{COM2[ii][5]},{COM2[ii][6]:3.1f},{COM2[ii][7]},{COM2[ii][8]},{COM2[ii][9]},{COM2[ii][10]:3.1f},{COM2[ii][11]:3.1f},{COM2[ii][12]:3.1f},{COM2[ii][13]},{COM2[ii][14]:3.1f},{COM2[ii][15]:3.1f},{COM2[ii][16]:3.1f},{COM2[ii][17]},{COM2[ii][18]:4.2f}\n')
		ii = ii + 1

print("#SKEQ OBS_INDEX 1QC CREAT Complete==========")
