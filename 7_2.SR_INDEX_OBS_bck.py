#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.04.11] edit 19.08.22
import time as checktime
from netCDF4 import Dataset
import sys
import os
import numpy as np
import lunardate as lunar
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime
from Function.speq_function import IndexScore
from Function.statistic_function import Statistic
from Function.statistic_function2 import Statistic2

print("#SREQ OBS_INDEX 1QC CREAT Start==========")

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
WW3_FNAME = 'WW3_' + str(yesterday) + '00.nc'        # WW3 - KHOA
CWW3_FNAME = 'CWW3_' + str(yesterday) + '00.nc'      # CWW3 - KMA
CWW3_P_FNAME = 'CWW3_WAVPRD_' + str(yesterday) + '00.nc'      # CWW3_WAVPRD - KMA
RWW3_FNAME = 'RWW3_' + str(yesterday) + '00.nc'     # RWW3 - KMA

INFILE_1 = MPATH+ROMS_FNAME
INFILE_2 = MPATH+WRF_FNAME
INFILE_3 = MPATH+CWW3_FNAME
INFILE_4 = MPATH+WW3_FNAME
INFILE_5 = MPATH+RWW3_FNAME
INFILE_6 = MPATH+CWW3_P_FNAME

#[READ Model_Data] =======================================================================================
##[YES3K]
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
WDEG = np.rad2deg(np.arctan2(V_WIND,U_WIND))
WDEG[WDEG<0]+= 360

#[CWW3, WW3] not yet RWW3
if os.path.isfile(INFILE_3):
    #print('Use CWW3')
    DATA = Dataset(INFILE_3, mode='r')
    #파고
    WHT_1 = DATA.variables['hsig1_dajn'][:,:,:]  #[t,y,x]
    WHT_2 = DATA.variables['hsig2_gwju'][:,:,:]  #[t,y,x]
    WHT_3 = DATA.variables['hsig3_jeju'][:,:,:]  #[t,y,x]
    WHT_4 = DATA.variables['hsig4_busn'][:,:,:]  #[t,y,x]
    WHT_5 = DATA.variables['hsig5_gawn'][:,:,:]  #[t,y,x]
    #파향
    Wdir_1 = DATA.variables['wavdir1_dajn'][:,:,:]  #[t,y,x]
    Wdir_2 = DATA.variables['wavdir2_gwju'][:,:,:]  #[t,y,x]
    Wdir_3 = DATA.variables['wavdir3_jeju'][:,:,:]  #[t,y,x]
    Wdir_4 = DATA.variables['wavdir4_busn'][:,:,:]  #[t,y,x]
    Wdir_5 = DATA.variables['wavdir5_gawn'][:,:,:]  #[t,y,x]

    #전처리
    Wdir_1[Wdir_1<-180] = np.nan
    Wdir_2[Wdir_2<-180] = np.nan
    Wdir_3[Wdir_3<-180] = np.nan
    Wdir_4[Wdir_4<-180] = np.nan
    Wdir_5[Wdir_5<-180] = np.nan

    Wdir_1[Wdir_1>0] = -Wdir_1[Wdir_1>0] - 90
    Wdir_2[Wdir_2>0] = -Wdir_2[Wdir_2>0] - 90
    Wdir_3[Wdir_3>0] = -Wdir_3[Wdir_3>0] - 90
    Wdir_4[Wdir_4>0] = -Wdir_4[Wdir_4>0] - 90
    Wdir_5[Wdir_5>0] = -Wdir_5[Wdir_5>0] - 90

    Wdir_1[Wdir_1<0] += 360
    Wdir_2[Wdir_2<0] += 360
    Wdir_3[Wdir_3<0] += 360
    Wdir_4[Wdir_4<0] += 360
    Wdir_5[Wdir_5<0] += 360

    Wx_1 = np.cos(np.deg2rad(Wdir_1))
    Wy_1 = np.sin(np.deg2rad(Wdir_1))
    Wx_2 = np.cos(np.deg2rad(Wdir_2))
    Wy_2 = np.sin(np.deg2rad(Wdir_2))
    Wx_3 = np.cos(np.deg2rad(Wdir_3))
    Wy_3 = np.sin(np.deg2rad(Wdir_3))
    Wx_4 = np.cos(np.deg2rad(Wdir_4))
    Wy_4 = np.sin(np.deg2rad(Wdir_4))
    Wx_5 = np.cos(np.deg2rad(Wdir_5))
    Wy_5 = np.sin(np.deg2rad(Wdir_5))
     
    #파주기도 추가 곧 해야함

    #20210628
    DATA2 = Dataset(INFILE_6, mode='r')
    print('Use Rpeak CWW3_wavprd')
    Rpeak_1 = DATA2.variables['wavprd1_dajn'][:,:,:]  #[t,y,x]
    Rpeak_2 = DATA2.variables['wavprd2_gwju'][:,:,:]  #[t,y,x]
    Rpeak_3 = DATA2.variables['wavprd3_jeju'][:,:,:]  #[t,y,x]
    Rpeak_4 = DATA2.variables['wavprd4_busn'][:,:,:]  #[t,y,x]
    Rpeak_5 = DATA2.variables['wavprd5_gawn'][:,:,:]  #[t,y,x]

    DATA3 = Dataset(INFILE_4, mode='r')
    print('Use Rpeak WW3')
    WHT = DATA3.variables['Hsig'][:,:,:]  #유의파고 [t,y,x]
    Wdir = DATA3.variables['Wdir'][:,:,:] # 파향
    Rpeak = DATA3.variables['Rpeak'][:,:,:]  #[t,y,x]	

    Wdir[Wdir<-180] = np.nan
    # 0보다 작은값 + 값으로 만들기
    Wdir[Wdir<0] += 360
    
    #각도를 라디안으로 바꾸고, 그것에 대한 코사인, 사인 성분 구함(x방향, y방향)
    Wx = np.cos(np.deg2rad(Wdir))   
    Wy = np.sin(np.deg2rad(Wdir))

else :
    #print("There is no CWW3, Use WW3")

    #WW3의 파고, 파향 불러오기
    DATA = Dataset(INFILE_4, mode='r')
    WHT = DATA.variables['Hsig'][:,:,:]  #유의파고 [t,y,x]
    Wdir = DATA.variables['Wdir'][:,:,:] # 파향
    Rpeak = DATA.variables['Rpeak'][:,:,:] #파주기

    # -180보다 작은 값 전처리 
    Wdir[Wdir<-180] = np.nan
    # 0보다 작은값 + 값으로 만들기
    Wdir[Wdir<0] += 360

    #각도를 라디안으로 바꾸고, 그것에 대한 코사인, 사인 성분 구함(x방향, y방향)
    Wx = np.cos(np.deg2rad(Wdir))
    Wy = np.sin(np.deg2rad(Wdir))

#[Info Data Read]=========================================================================================
POINT_INF = open('./Info/SR_Point_Info_2.csv','r',encoding='utf8')
INF = [str(INFO) for INFO in POINT_INF.read().split()]
INF_LEN = len(INF)

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
	POINT = DEV[1] ; AREA = DEV[2] ; NAME = DEV[3] ; LON = DEV[4] ; LAT = DEV[5]
	ROMS_X = int(DEV[6]) ; ROMS_Y = int(DEV[7]) ; WRF_X = int(DEV[8]) ; WRF_Y = int(DEV[9])
	WW3_X = int(DEV[10]) ; WW3_Y = int(DEV[11]) ; CWW3_X = int(DEV[12]) ; CWW3_Y = int(DEV[13]) ; CWW3_LOC = int(DEV[14])
	RWW3_X = int(DEV[15]) ; RWW3_Y = int(DEV[16]) ; W_AREA = DEV[19]	
	REF_AGY1=DEV[21]; REF_STN_WAVE1=DEV[22]; REF_AGY2=DEV[23]; REF_STN_WAVE2=DEV[24]
	REF_AGY3=DEV[25]; REF_STN_SST1=DEV[26]; REF_AGY4=DEV[27]; REF_STN_SST2=DEV[28]
	#print(POINT,NAME,ii)

	M_WIND_S = Statistic().min_max_ave('KHOA', 'ampm', WIND, WRF_X, WRF_Y, 0)


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
