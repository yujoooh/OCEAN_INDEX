#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.04.11] edit 19.08.22
import sys
import os
#os.path.join(os.getcwd(),"Function")
import numpy as np
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime
from Function.speq_function import IndexScore
from Function.statistic_function import Statistic
from Function.statistic_function2 import Statistic2

print("#SPEQ OBS_INDEX 1QC CREAT Start==========")

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
ROMS_FNAME = 'YES3K_'+ str(yesterday) + '00.nc'      # YES3K - KHOA
WRF_FNAME = 'WRF_' + str(yesterday) + '.nc'          # WRF_DM2 - KHOA

INFILE_1 = MPATH+ROMS_FNAME
INFILE_2 = MPATH+WRF_FNAME

#[READ Model_Data] =======================================================================================
##[YES3K]
#DATA = Dataset(INFILE_1, mode='r')
#SST = DATA.variables['temp'][:,:,:]  #[t,y,x]
#U_CURRENT = DATA.variables['u'][:,:,:]  #[t,y,x]
#V_CURRENT = DATA.variables['v'][:,:,:]  #[t,y,x]
#CURRENT= (U_CURRENT**2+V_CURRENT**2)**0.5  #Calculate Current speed

#[WRF]
DATA = Dataset(INFILE_2, mode='r')
TEMP = DATA.variables['Tair'][:,:,:]  #[t,y,x]
U_WIND = DATA.variables['Uwind'][:,:,:]  #[t,y,x]
V_WIND = DATA.variables['Vwind'][:,:,:]  #[t,y,x]
WIND = (U_WIND**2+V_WIND**2)**0.5  #Calculate Wind speed


#[Info Data Read]=========================================================================================
POINT_INF = open('./Info/SP_Point_Info.csv','r',encoding='utf8')
INF = [str(INFO) for INFO in POINT_INF.read().split()]
INF_LEN = len(INF)


OBS_COM = []
DAY1 = [] # yesterday obs data list
#[OBS Data Read]==========================================================================================
OBS_DATA1 = open(dir1+'/OBS_Daily/OBS_KMA_'+yesterday+'.csv','r',encoding='utf8')
OBS1 = [str(INFO) for INFO in OBS_DATA1.read().split()]
OBS_DATA2 = open(dir1+'/OBS_Daily/OBS_KHOA_'+yesterday+'.csv','r',encoding='utf8')
OBS2 = [str(INFO) for INFO in OBS_DATA2.read().split()]

OBS_COM = OBS1 + OBS2
#print(OBS_COM)

##[BEACH DATA Extract] ====================================================================================
O_SST1 = [] ; O_WHT1 = []
O_SST2 = [] ; O_WHT2 = []
DAY1 = [] # yesterday index data list
ii = 1
while ii <= INF_LEN-1 : 
	DEV = INF[ii].split(',')
	POINT = DEV[0] ; AREA = DEV[1] ; NAME = DEV[2] ; LON = DEV[3] ; LAT = DEV[4]
	ROMS_X = int(DEV[5]) ; ROMS_Y = int(DEV[6]) ; WRF_X = int(DEV[7]) ; WRF_Y = int(DEV[8])
	REF_AGY1=DEV[19]; REF_STN_WAVE1=DEV[20]; REF_AGY2=DEV[21]; REF_STN_WAVE2=DEV[22]
	REF_AGY3=DEV[23]; REF_STN_SST1=DEV[24]; REF_AGY4=DEV[25]; REF_STN_SST2=DEV[26]
	#print(POINT,NAME,ii)

	M_WIND_S = Statistic().min_max_ave('KHOA', 'ampm', WIND, WRF_X, WRF_Y, 0)
	M_TEMP_S = Statistic().min_max_ave('KHOA', 'ampm', TEMP, WRF_X, WRF_Y, 0)

	jj = 1 
	hr1=0 ; hr2=0; hr3=0 ; hr4=0
	while jj < len(OBS_COM):
		DEV2 = OBS_COM[jj].split(',')
		OBS_STNID = DEV2[0] ; OBS_STN = DEV2[1] ; OBS_YMD = DEV2[2] ; OBS_SST = DEV2[3] ; OBS_WHT = DEV2[4]
		OBS_WSPD = DEV2[5] ; OBS_WDIR = DEV2[6] ; OBS_USPD = DEV2[7] ; OBS_VSPD = DEV2[8] ; OBS_AGY = DEV2[9]
		#print(OBS_STNID, OBS_STN, OBS_YMD, OBS_SST)
		if REF_AGY1 == OBS_AGY and REF_STN_WAVE1 == OBS_STN : 
			hr1 = (f'{hr1:02d}')
			#print(hr1)			
			#print(REF_AGY1, OBS_AGY, REF_STN_WAVE1, OBS_STN, OBS_YMD[8:10] ,hr)
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
	#print(len(O_WHT1))
	
	jj = 1  ; hr2=0
	while jj < len(OBS_COM):
		DEV2 = OBS_COM[jj].split(',')
		OBS_STNID = DEV2[0] ; OBS_STN = DEV2[1] ; OBS_YMD = DEV2[2] ; OBS_SST = DEV2[3] ; OBS_WHT = DEV2[4]
		OBS_WSPD = DEV2[5] ; OBS_WDIR = DEV2[6] ; OBS_USPD = DEV2[7] ; OBS_VSPD = DEV2[8] ; OBS_AGY = DEV2[9]
		if REF_AGY2 == OBS_AGY and REF_STN_WAVE2 == OBS_STN : 
			hr2 = (f'{hr2:02d}')
			#print(hr2)
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
		
	jj = 1  ; hr3=0	
	while jj < len(OBS_COM):
		DEV2 = OBS_COM[jj].split(',')
		OBS_STNID = DEV2[0] ; OBS_STN = DEV2[1] ; OBS_YMD = DEV2[2] ; OBS_SST = DEV2[3] ; OBS_WHT = DEV2[4]
		OBS_WSPD = DEV2[5] ; OBS_WDIR = DEV2[6] ; OBS_USPD = DEV2[7] ; OBS_VSPD = DEV2[8] ; OBS_AGY = DEV2[9]
		if REF_AGY3 == OBS_AGY and REF_STN_SST1 == OBS_STN : 
			hr3 = (f'{hr3:02d}')
			if OBS_YMD[8:10] == hr3 : 
				O_SST1.append(round(float(OBS_SST),1))
			else:
				O_SST1.append(-999); jj = jj - 1
			hr3 = int(hr3) + 1
		if hr3 == 24 : break
		jj = jj + 1
		
	if(len(O_SST1) < 24) :
		jj = len(O_SST1)-1
		while jj < 24 :
			O_SST1.append(-999)
			jj += 1
			
	jj = 1  ; hr4=0	
	while jj < len(OBS_COM):
		DEV2 = OBS_COM[jj].split(',')
		OBS_STNID = DEV2[0] ; OBS_STN = DEV2[1] ; OBS_YMD = DEV2[2] ; OBS_SST = DEV2[3] ; OBS_WHT = DEV2[4]
		OBS_WSPD = DEV2[5] ; OBS_WDIR = DEV2[6] ; OBS_USPD = DEV2[7] ; OBS_VSPD = DEV2[8] ; OBS_AGY = DEV2[9]
		if REF_AGY4 == OBS_AGY and REF_STN_SST2 == OBS_STN : 
			hr4 = (f'{hr4:02d}')
			if OBS_YMD[8:10] == hr4 : 
				O_SST2.append(round(float(OBS_SST),1))
			else:
				O_SST2.append(-999); jj = jj - 1
			hr4 = int(hr4) + 1
		if hr4 == 24 : break
		jj = jj + 1
		
	if(len(O_SST2) < 24) :
		jj = len(O_SST2)-1
		while jj < 24 :
			O_SST2.append(-999)
			jj += 1

	#관측자료 최대/최소/평균값 산정 및 참고지점 1,2순위의 자료 유무 판단.. 전체 없을 시 -999로
	if len(O_WHT1[9:19]) == 0 or O_WHT1[9:13].count(-999) == 4 or O_WHT1[12:19].count(-999) == 6 or O_WHT1[9:19].count(-999) == 10 :
		print(NAME, REF_STN_WAVE1,"WAVE REF1 all data missing")
		if len(O_WHT2[9:19]) == 0 or O_WHT2[9:13].count(-999) == 4 or O_WHT2[12:19].count(-999) == 6 or O_WHT2[9:19].count(-999) == 10 :
			print(NAME, REF_STN_WAVE2,"WAVE REF1/REF2 all data missing")
			WAVE_S = [-999,-999,-999,-999,-999,-999]
		else:
			WAVE_S = Statistic2().min_max_ave('ampm',O_WHT2,9)
	else:
		WAVE_S = Statistic2().min_max_ave('ampm',O_WHT1,9)

	if len(O_SST1[9:19]) == 0 or O_SST1[9:13].count(-999) == 4 or O_SST1[12:19].count(-999) == 6 or O_SST1[9:19].count(-999) == 10 :
		print(NAME, REF_STN_SST1,"SST REF1 all data missing")
		if len(O_SST2[9:19]) == 0 or O_SST2[9:13].count(-999) == 4 or O_SST2[12:19].count(-999) == 6 or O_SST2[9:19].count(-999) == 10 :
			print(NAME, REF_STN_SST2,"SST REF1/REF2 all data missing")
			SST_S = [-999,-999,-999,-999,-999,-999]
		else:
			SST_S = Statistic2().min_max_ave('ampm',O_SST2,9)
	else:
		SST_S = Statistic2().min_max_ave('ampm',O_SST1,9)

	#VARS_S ampm [0:am_min 1:am_max, 2:am_ave, 3:pm_min, 4:pm_max, 5:pm_ave] ; VARS_S daily [0:min 1:max, 2:ave]
	DAY1.append([POINT, AREA, NAME, yesterday, 'AM', M_TEMP_S[2], SST_S[2], M_WIND_S[1], WAVE_S[1]])
	DAY1.append([POINT, AREA, NAME, yesterday, 'PM', M_TEMP_S[5], SST_S[5], M_WIND_S[4], WAVE_S[4]])

	O_SST1.clear() ;O_SST2.clear() ; O_WHT1.clear(); O_WHT2.clear()
	ii = ii + 1

#[Result Check]
#ii = 0
#while ii < len(DAY1):
#	print(DAY1[ii])
#	ii = ii + 1


#[Index Score Calculate] ========================================================================================
ii = 0
while ii <= len(DAY1)-1 :
	TEMP_SCRE = IndexScore().temp_score(round(DAY1[ii][5],1))
	SST_SCRE = IndexScore().sst_score(round(DAY1[ii][6],1))
	WIND_SCRE = IndexScore().wind_score(round(DAY1[ii][7],1))
	WAVE_SCRE = IndexScore().wave_score(round(DAY1[ii][8],1))
	RAIN_SCRE = IndexScore().rain_score(0)
	WARN_SCRE = IndexScore().warn_score('-')
	TOTAL_SCRE1 = IndexScore().total_score(TEMP_SCRE, round(DAY1[ii][6],1), SST_SCRE, WIND_SCRE, WAVE_SCRE, RAIN_SCRE, WARN_SCRE)[0] # forecast score(no rain, no warning)

	DAY1[ii].insert(6,TEMP_SCRE) ; DAY1[ii].insert(8,SST_SCRE) ; DAY1[ii].insert(10,WIND_SCRE); DAY1[ii].insert(12,WAVE_SCRE);DAY1[ii].insert(13,TOTAL_SCRE1)
	ii = ii + 1

#[Output Data] ========================================================================================
OUT_FNAME1=dir1+'/SPEQ_INDEX_OBS_1QC_'+today+'.csv'
with open(OUT_FNAME1,'w',encoding='utf8') as file:
	file.write('생산일,코드,해수욕장,예측일자,시간,평균기온,기온점수,평균수온,수온점수,최대풍속,풍속점수,최대파고,파고점수,총점수\n',)
	ii = 0
	while ii <= len(DAY1)-1 :
		#[전체 데이터 Writing]
		file.write(f'{today},{DAY1[ii][0]},{DAY1[ii][2]},{DAY1[ii][3]},{DAY1[ii][4]},{DAY1[ii][5]:3.1f},{DAY1[ii][6]},{DAY1[ii][7]:3.1f},{DAY1[ii][8]},{DAY1[ii][9]:3.1f},{DAY1[ii][10]},{DAY1[ii][11]:3.1f},{DAY1[ii][12]},{DAY1[ii][13]:4.2f}\n')
		ii = ii + 1

print("#SPEQ OBS_INDEX 1QC CREAT Complete==========")
