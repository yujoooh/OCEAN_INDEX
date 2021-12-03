#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.04.11] edit 19.08.22
import sys
import os
import numpy as np
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime
from Function.sseq_function import IndexScore, Tide_time_lunar
from Function.statistic_function import Statistic

print("#SSEQ FCST_INDEX CREAT Start==========")

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
POINT_INF = open('./Info/SS_Point_Info.csv','r',encoding='utf8')
INF = [str(INFO) for INFO in POINT_INF.read().split()]
INF_LEN = len(INF)

#[KMA CITY and WARNING data read]=========================================================================
if not os.path.exists(dir1+'/SS_CITY.csv'): # 동네예보 수집 에러에 따른 자료 미생성시 그냥 예측자료 사용
	print('CITY_FORECAST DATA Not found') ; CITY_LEN=0
else:
	CITY_INF = open(dir1+'/SS_CITY.csv','r',encoding='utf8')
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
	RWW3_X = int(DEV[14]) ; RWW3_Y = int(DEV[15]) ; W_AREA = DEV[18]

	jj = 0 ; jjj = 0
	while jj <= 144:
		SST_2S  = Statistic().min_max_ave('KHOA', 'ampm', SST, ROMS_X, ROMS_Y, jj)
		SST_S  = Statistic().min_max_ave('KHOA', 'daily', SST, ROMS_X, ROMS_Y, jj)
		CURRENT_2S = Statistic().min_max_ave('KHOA', 'ampm', CURRENT, ROMS_X, ROMS_Y, jj)
		CURRENT_S = Statistic().min_max_ave('KHOA', 'daily', CURRENT, ROMS_X, ROMS_Y, jj)

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
				
		#VARS_S ampm [0:am_min 1:am_max, 2:am_ave, 3:pm_min, 4:pm_max, 5:pm_ave] ; VARS_S daily [0:min 1:max, 2:ave]
		if jj == 0  :
			DAY1.append([STN, AREA, W_AREA, NAME, today, 'AM' ,TODAY_MUL, round(WAVE_2S[0],1), round(WAVE_2S[2],1), round(WAVE_2S[1],1), round(CURRENT_2S[0],1), round(CURRENT_2S[2],1), round(CURRENT_2S[1],1), round(SST_2S[0],1), round(SST_2S[2],1), round(SST_2S[1],1)])
			DAY1.append([STN, AREA, W_AREA, NAME, today, 'PM' ,TODAY_MUL, round(WAVE_2S[3],1), round(WAVE_2S[5],1), round(WAVE_2S[4],1), round(CURRENT_2S[3],1), round(CURRENT_2S[5],1), round(CURRENT_2S[4],1), round(SST_2S[3],1), round(SST_2S[5],1), round(SST_2S[4],1)])
		if jj == 24 :
			DAY2.append([STN, AREA, W_AREA, NAME, afterday1, 'AM' ,AFTERDAY1_MUL, round(WAVE_2S[0],1), round(WAVE_2S[2],1), round(WAVE_2S[1],1), round(CURRENT_2S[0],1), round(CURRENT_2S[2],1), round(CURRENT_2S[1],1), round(SST_2S[0],1), round(SST_2S[2],1), round(SST_2S[1],1)])
			DAY2.append([STN, AREA, W_AREA, NAME, afterday1, 'PM' ,AFTERDAY1_MUL, round(WAVE_2S[3],1), round(WAVE_2S[5],1), round(WAVE_2S[4],1), round(CURRENT_2S[3],1), round(CURRENT_2S[5],1), round(CURRENT_2S[4],1), round(SST_2S[3],1), round(SST_2S[5],1), round(SST_2S[4],1)])
		if jj == 48 :
			DAY3.append([STN, AREA, W_AREA, NAME, afterday2, 'AM' ,AFTERDAY2_MUL, round(WAVE_2S[0],1), round(WAVE_2S[2],1), round(WAVE_2S[1],1), round(CURRENT_2S[0],1), round(CURRENT_2S[2],1), round(CURRENT_2S[1],1), round(SST_2S[0],1), round(SST_2S[2],1), round(SST_2S[1],1)])
			DAY3.append([STN, AREA, W_AREA, NAME, afterday2, 'PM' ,AFTERDAY2_MUL, round(WAVE_2S[3],1), round(WAVE_2S[5],1), round(WAVE_2S[4],1), round(CURRENT_2S[3],1), round(CURRENT_2S[5],1), round(CURRENT_2S[4],1), round(SST_2S[3],1), round(SST_2S[5],1), round(SST_2S[4],1)])
		if jj == 72 :
			DAY4.append([STN, AREA, W_AREA, NAME, afterday3, 'DY', AFTERDAY3_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), round(CURRENT_S[0],1), round(CURRENT_S[2],1), round(CURRENT_S[1],1), round(SST_S[0],1), round(SST_S[2],1), round(SST_S[1],1)])
		if jj == 96 :
			DAY5.append([STN, AREA, W_AREA, NAME, afterday4, 'DY', AFTERDAY4_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), round(CURRENT_S[0],1), round(CURRENT_S[2],1), round(CURRENT_S[1],1), round(SST_S[0],1), round(SST_S[2],1), round(SST_S[1],1)])
		if jj == 120 :
			DAY6.append([STN, AREA, W_AREA, NAME, afterday5, 'DY', AFTERDAY5_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), round(CURRENT_S[0],1), round(CURRENT_S[2],1), round(CURRENT_S[1],1), round(SST_S[0],1), round(SST_S[2],1), round(SST_S[1],1)])
		if jj == 144 :
			DAY7.append([STN, AREA, W_AREA, NAME, afterday6, 'DY', AFTERDAY6_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), round(CURRENT_S[0],1), round(CURRENT_S[2],1), round(CURRENT_S[1],1), round(SST_S[0],1), round(SST_S[2],1), round(SST_S[1],1)])
		
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

#ii = 0
#while ii <= COM_LEN-1 :
#	print(COM[ii])
#	ii += 1
#print(len(DAY1), COM_LEN, INF_LEN )

#[KMA WARNING INFORAMTION : special weather report]=====================================================================================================
ii = 0 
while ii <= COM_LEN-1:
	jj = 1
	while jj <= WARN_LEN-1:
		DEV = WARN[jj].split(',')
		WARN_AREA = DEV[0] ; WARN_TYPE = DEV[1] ; WARN_SDAY = DEV[2] ; WARN_SHR = DEV[3] ; WARN_EDAY = DEV[4] ; WARN_EHR = DEV[5]
		#print(WARN_AREA, WARN_TYPE)
		if WARN_TYPE == 'WW2' : WARN_TYPE = 'WW'
		if WARN_TYPE == 'TY2' : WARN_TYPE = 'TY'
		if WARN_TYPE == 'SS2' : WARN_TYPE = 'SS'
		
		#print(COM[ii][4], int(WARN_SDAY), COM[ii][5],WARN_SHR)
		if int(COM[ii][4]) < int(WARN_EDAY) and int(COM[ii][4]) >= int(WARN_SDAY) and COM[ii][2] == WARN_AREA: #해제예고 일보다 전날일 경우 일괄적용
			COM[ii].insert(21,WARN_TYPE)
			jj = WARN_LEN
		elif int(COM[ii][4]) == int(WARN_EDAY) and int(COM[ii][4]) >= int(WARN_SDAY) and COM[ii][2] == WARN_AREA: #해제예고일과 같을 경우 AM이면 오전만 적용, PM이면 오전/오후 모두적용
			if WARN_EHR == 'PM' : 
				COM[ii].insert(21,WARN_TYPE)
			elif WARN_EHR == 'AM' :
				if COM[ii][5] == 'AM' or COM[ii][5] == 'DY' :
					COM[ii].insert(21,WARN_TYPE)
				else :
					COM[ii].insert(21,'-')
			jj = WARN_LEN
		else:
			jj = jj + 1
			if jj == WARN_LEN :
				COM[ii].insert(21,'-')
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
                    #0   1     2      3       4        5             6                     7                 8                     9                      10                    11                   12                  13                      14              15
	#DAY1.append([STN, AREA, W_AREA, NAME, today, TODAY_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), round(CURRENT_S[0],1), round(CURRENT_S[2],1), round(CURRENT_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), WARN])
	TIDE_SCRE = IndexScore().tide_score(COM[ii][6])
	WAVE_SCRE = IndexScore().wave_score(round(float(COM[ii][9]),1))
	CURRENT_SCRE = IndexScore().current_score(round(COM[ii][12],1))
	SST_SCRE = IndexScore().sst_score(round(COM[ii][14],1))
	WARN_SCRE = IndexScore().warn_score(COM[ii][16])
	TOTAL_SCRE1 = IndexScore().total_score(TIDE_SCRE, WAVE_SCRE, CURRENT_SCRE, SST_SCRE, WARN_SCRE)[0] # forecast score(no rain, no warning)
	TOTAL_SCRE2 = IndexScore().total_score(TIDE_SCRE, WAVE_SCRE, CURRENT_SCRE, SST_SCRE, WARN_SCRE)[1] # service score(rain, warning)
	QUOTIENT_SCRE1 = IndexScore().quotient_score(TOTAL_SCRE1) # forecast score(no rain, no warning)
	QUOTIENT_SCRE2 = IndexScore().quotient_score(TOTAL_SCRE2) # service score(rain, warning)

	COM[ii].insert(7,TIDE_SCRE) ; COM[ii].insert(11,WAVE_SCRE) ; COM[ii].insert(15,CURRENT_SCRE); COM[ii].insert(19,SST_SCRE) ; COM[ii].insert(21,WARN_SCRE) ;COM[ii].insert(22,TOTAL_SCRE1) ; COM[ii].insert(23,TOTAL_SCRE2) ; COM[ii].insert(24,QUOTIENT_SCRE1) ; COM[ii].insert(25,QUOTIENT_SCRE2)
	ii = ii + 1

#ii = 0
#while ii <= COM_LEN-1:
#	print(COM[ii])
#	ii = ii + 1

#[Output Data] ========================================================================================
OUT_FNAME1=dir1+'/SSEQ_INDEX_FCST_'+today+'.csv'
with open(OUT_FNAME1,'w',encoding='utf8') as file:
	file.write('생산일,코드,권역,지역,예측일자,시간,물때,물때점수,최소파고,평균파고,최대파고,파고점수,최소유속,평균유속,최대유속,유속점수,최소수온,평균수온,최대수온,수온점수,총점수,예보지수\n',)
	ii = 0
	while ii <= COM_LEN-1 :
		#[전체 데이터 Writing]
		file.write(f'{today},{COM[ii][0]},{COM[ii][1]},{COM[ii][3]},{COM[ii][4]},{COM[ii][5]},{COM[ii][6]},{COM[ii][7]},{COM[ii][8]:2.1f},{COM[ii][9]:2.1f},{COM[ii][10]:2.1f},{COM[ii][11]},{COM[ii][12]:2.1f},{COM[ii][13]:2.1f},{COM[ii][14]:2.1f},{COM[ii][15]},{COM[ii][16]:2.1f},{COM[ii][17]:2.1f},{COM[ii][18]:2.1f},{COM[ii][19]},{COM[ii][22]:4.2f},{COM[ii][24]}\n')
		ii = ii + 1

OUT_FNAME2=dir1+'/SSEQ_INDEX_SERVICE_'+today+'.csv'
with open(OUT_FNAME2,'w',encoding='utf8') as file:
	file.write('코드,권역,지역,예측일자,시간,물때,물때점수,최소파고,평균파고,최대파고,파고점수,최소유속,평균유속,최대유속,유속점수,최소수온,평균수온,최대수온,수온점수,특보,특보점수,총점수,예보지수\n',)
	ii = 0
	while ii <= COM_LEN-1 :
		#[WEB_~~_SCRE Format]
		file.write(f'{COM[ii][0]},{COM[ii][1]},{COM[ii][3]},{COM[ii][4]},{COM[ii][5]},{COM[ii][6]},{COM[ii][7]},{COM[ii][8]:2.1f},{COM[ii][9]:2.1f},{COM[ii][10]:2.1f},{COM[ii][11]:2.1f},{COM[ii][12]:2.1f},{COM[ii][13]:2.1f},{COM[ii][14]:2.1f},{COM[ii][15]},{COM[ii][16]:2.1f},{COM[ii][17]:2.1f},{COM[ii][18]:2.1f},{COM[ii][19]},{COM[ii][20]},{COM[ii][21]},{COM[ii][23]:4.2f},{COM[ii][25]}\n')
		ii = ii + 1

print("#SSEQ FCST_INDEX CREAT Complete==========")
