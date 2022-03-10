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
from Function.statistic_function2 import Statistic2

print("#SFEQ OBS_INDEX 1QC CREAT Start==========")

#[Date set] ==============================================================================================
#[Auto date set]
today = str(datetime.today().strftime('%Y%m%d'))
yesterday = (date.today() - timedelta(1)).strftime('%Y%m%d')

#[Manual date set]
#today = str(date(2020,1,20).strftime('%Y%m%d'))
#yesterday = (date(2020,1,20) - timedelta(1)).strftime('%Y%m%d')
#print(today, afterday1, afterday2)

dir1 = './Result/'+today

#[Model Data path] =======================================================================================
MPATH = './Model_Data/'
ROMS_FNAME = 'YES3K_'+ str(yesterday) + '00.nc'      # YES3K - KHOA
WRF_FNAME = 'WRF_' + str(yesterday) + '.nc'          # WRF_DM2 - KHOA
WW3_FNAME = 'WW3_' + str(yesterday) + '00.nc'        # WW3 - KHOA
CWW3_FNAME = 'CWW3_' + str(yesterday) + '00.nc'      # CWW3 - KMA
RWW3_FNAME = 'RWW3_' + str(yesterday) + '00.nc'     # RWW3 - KMA

INFILE_1 = MPATH+ROMS_FNAME
INFILE_2 = MPATH+WRF_FNAME
INFILE_3 = MPATH+CWW3_FNAME
INFILE_4 = MPATH+WW3_FNAME
INFILE_5 = MPATH+RWW3_FNAME

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
POINT_INF = open('./Info/SF_Point_Info.csv','r',encoding='utf8')
INF = [str(INFO) for INFO in POINT_INF.read().split()]
INF_LEN = len(INF)

#[OBS Data Read]==========================================================================================
OBS_DATA1 = open(dir1+'/OBS_Daily/OBS_KMA_'+yesterday+'.csv','r',encoding='utf8')
OBS1 = [str(INFO) for INFO in OBS_DATA1.read().split()]
OBS_DATA2 = open(dir1+'/OBS_Daily/OBS_KHOA_'+yesterday+'.csv','r',encoding='utf8')
OBS2 = [str(INFO) for INFO in OBS_DATA2.read().split()]

OBS_COM = OBS1 + OBS2
#print(OBS_COM)

#[Tide Time : mul]=========================================================================================
YESTERDAY_MUL = Tide_time_lunar().lunar_to_mul(yesterday)
#print(TIDE_MUL1, TIDE_MUL2, TIDE_MUL3, TIDE_MOON1, TIDE_MOON2, TIDE_MOON3)

#[BEACH DATA Extract] ====================================================================================
DAY1 = [] # forecast data list
O_WHT1 = [] ; O_WHT2 = [] ; O_SST1 = [] ; O_SST2 = []

ii = 1
while ii <= INF_LEN-1 :
	DEV = INF[ii].split(',')
	STN = DEV[0] ; AREA = DEV[1] ; NAME = DEV[2] ; LON = DEV[3] ; LAT = DEV[4]
	ROMS_X = int(DEV[5]) ; ROMS_Y = int(DEV[6]) ; WRF_X = int(DEV[7]) ; WRF_Y = int(DEV[8])
	WW3_X = int(DEV[9]) ; WW3_Y = int(DEV[10]) ; CWW3_X = int(DEV[11]) ; CWW3_Y = int(DEV[12]) ; CWW3_LOC = int(DEV[13])
	RWW3_X = int(DEV[14]) ; RWW3_Y = int(DEV[15]) ; W_AREA = DEV[18] ; FISH_NAME = DEV[27] ; FISH_TYPE = DEV[28]
	REF_AGY1=DEV[19]; REF_STN_WAVE1=DEV[20]; REF_AGY2=DEV[21]; REF_STN_WAVE2=DEV[22]
	REF_AGY3=DEV[23]; REF_STN_SST1=DEV[24]; REF_AGY4=DEV[25]; REF_STN_SST2=DEV[26]

	if yesterday[4:6] == '01' or yesterday[4:6] =='02' or yesterday[4:6] =='03' or yesterday[4:6] =='11' or yesterday[4:6] =='12' : 
		M_WIND_S = Statistic().min_max_ave('KHOA', 'ampm', WIND, WRF_X, WRF_Y, 0)
		M_TEMP_S = Statistic().min_max_ave('KHOA', 'ampm', TEMP, WRF_X, WRF_Y, 0)

		jj = 1 ; hr1=0 
		while jj < len(OBS_COM):
			DEV2 = OBS_COM[jj].split(',')
			OBS_STNID = DEV2[0] ; OBS_STN = DEV2[1] ; OBS_YMD = DEV2[2] ; OBS_SST = DEV2[3] ; OBS_WHT = DEV2[4]
			OBS_WSPD = DEV2[5] ; OBS_WDIR = DEV2[6] ; OBS_USPD = DEV2[7] ; OBS_VSPD = DEV2[8] ; OBS_AGY = DEV2[9]
			#print(OBS_STNID, OBS_STN, OBS_YMD, OBS_SST)
			if REF_AGY1 == OBS_AGY and REF_STN_WAVE1 == OBS_STN : 
				hr1 = (f'{hr1:02d}')
				#print(REF_AGY1, OBS_AGY, REF_STN_WAVE1, OBS_STN, OBS_YMD[8:10] ,hr)
				if OBS_YMD[8:10] == hr1 : 
					O_WHT1.append(round(float(OBS_WHT),1))
				else:
					O_WHT1.append(-999); jj = jj - 1
				hr1 = int(hr1) + 1
			jj = jj + 1
			if hr1 == 24 : break

		if(len(O_WHT1) < 24) :
			jj = len(O_WHT1)-1
			while jj < 24 :
				O_WHT1.append(-999)
				jj += 1
			
		jj = 1 ; hr2=0
		while jj < len(OBS_COM):
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
			jj = jj + 1
			if hr2 == 24 : break		
		
		if(len(O_WHT2) < 24) :
			jj = len(O_WHT2)-1
			while jj < 24 :
				O_WHT2.append(-999)
				jj += 1	
				
		jj = 1 ;hr3=0
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
			jj = jj + 1
			if hr3 == 24 : break
	
		if(len(O_SST1) < 24) :
			jj = len(O_SST1)-1
			while jj < 24 :
				O_SST1.append(-999)
				jj += 1	

		jj = 1 ; hr4=0
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
			jj = jj + 1
			if hr4 == 24 : break			

		if len(O_WHT1) == 0 : O_WHT1.append([-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999])
		if len(O_WHT2) == 0 : O_WHT2.append([-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999])
		if len(O_SST1) == 0 : O_SST1.append([-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999])
		if len(O_SST2) == 0 : O_SST2.append([-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999])                        
		
		#관측자료 최대/최소/평균값 산정 및 참고지점 1,2순위의 자료 유무 판단.. 전체 없을 시 -999로
		#if len(O_WHT1[9:19]) == 0 or O_WHT1[9:19].count(-999) == 10 or len(O_WHT1) == 0:
		if len(O_WHT1[9:19]) == 0 or O_WHT1[9:13].count(-999) == 4 or O_WHT1[12:19].count(-999) == 6 or O_WHT1[9:19].count(-999) == 10 :
			print(NAME, REF_STN_WAVE1,"WAVE REF1 all data missing")
			#if len(O_WHT2[9:19]) == 0 or O_WHT2[9:19].count(-999) == 10 or len(O_WHT2) == 0:
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
		#print(STN, AREA, W_AREA, NAME,round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1))
		DAY1.append([STN, AREA, W_AREA, NAME, yesterday, 'AM', FISH_NAME, FISH_TYPE, YESTERDAY_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(M_TEMP_S[0])), int(round(M_TEMP_S[2])), int(round(M_TEMP_S[1])), int(round(M_WIND_S[0])), int(round(M_WIND_S[2])), int(round(M_WIND_S[1]))])
		DAY1.append([STN, AREA, W_AREA, NAME, yesterday, 'PM', FISH_NAME, FISH_TYPE, YESTERDAY_MUL, round(WAVE_S[3],1), round(WAVE_S[5],1), round(WAVE_S[4],1), int(round(SST_S[3])), int(round(SST_S[5])), int(round(SST_S[4])), int(round(M_TEMP_S[3])), int(round(M_TEMP_S[5])), int(round(M_TEMP_S[4])), int(round(M_WIND_S[3])), int(round(M_WIND_S[5])), int(round(M_WIND_S[4]))])
		O_SST1.clear() ;O_SST2.clear() ; O_WHT1.clear(); O_WHT2.clear()
	
	else :
		if FISH_TYPE == 'GR' or FISH_TYPE =='GP':
			MSG = 'No service this season ... GR and GP'
		else :
			M_WIND_S = Statistic().min_max_ave('KHOA', 'ampm', WIND, WRF_X, WRF_Y, 0)
			M_TEMP_S = Statistic().min_max_ave('KHOA', 'ampm', TEMP, WRF_X, WRF_Y, 0)

			jj = 1 ; hr1=0 
			while jj < len(OBS_COM):
				DEV2 = OBS_COM[jj].split(',')
				OBS_STNID = DEV2[0] ; OBS_STN = DEV2[1] ; OBS_YMD = DEV2[2] ; OBS_SST = DEV2[3] ; OBS_WHT = DEV2[4]
				OBS_WSPD = DEV2[5] ; OBS_WDIR = DEV2[6] ; OBS_USPD = DEV2[7] ; OBS_VSPD = DEV2[8] ; OBS_AGY = DEV2[9]
				#print(OBS_STNID, OBS_STN, OBS_YMD, OBS_SST)
				if REF_AGY1 == OBS_AGY and REF_STN_WAVE1 == OBS_STN : 
					hr1 = (f'{hr1:02d}')
					#print(REF_AGY1, OBS_AGY, REF_STN_WAVE1, OBS_STN, OBS_YMD[8:10] ,hr)
					if OBS_YMD[8:10] == hr1 : 
						O_WHT1.append(round(float(OBS_WHT),1))
					else:
						O_WHT1.append(-999); jj = jj - 1
					hr1 = int(hr1) + 1
				jj = jj + 1
				if hr1 == 24 : break
				
			jj = 1 ; hr2=0
			while jj < len(OBS_COM):
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
				jj = jj + 1
				if hr2 == 24 : break		
		
			jj = 1 ;hr3=0
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
				jj = jj + 1
				if hr3 == 24 : break

			jj = 1 ; hr4=0
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
				jj = jj + 1
				if hr4 == 24 : break	
			
			if len(O_WHT1) == 0 : O_WHT1.append([-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999])
			if len(O_WHT2) == 0 : O_WHT2.append([-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999])
			if len(O_SST1) == 0 : O_SST1.append([-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999])
			if len(O_SST2) == 0 : O_SST2.append([-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999,-999])
		
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
			DAY1.append([STN, AREA, W_AREA, NAME, yesterday, 'AM', FISH_NAME, FISH_TYPE, YESTERDAY_MUL, round(WAVE_S[0],1), round(WAVE_S[2],1), round(WAVE_S[1],1), int(round(SST_S[0])), int(round(SST_S[2])), int(round(SST_S[1])), int(round(M_TEMP_S[0])), int(round(M_TEMP_S[2])), int(round(M_TEMP_S[1])), int(round(M_WIND_S[0])), int(round(M_WIND_S[2])), int(round(M_WIND_S[1]))])
			DAY1.append([STN, AREA, W_AREA, NAME, yesterday, 'PM', FISH_NAME, FISH_TYPE, YESTERDAY_MUL, round(WAVE_S[3],1), round(WAVE_S[5],1), round(WAVE_S[4],1), int(round(SST_S[3])), int(round(SST_S[5])), int(round(SST_S[4])), int(round(M_TEMP_S[3])), int(round(M_TEMP_S[5])), int(round(M_TEMP_S[4])), int(round(M_WIND_S[3])), int(round(M_WIND_S[5])), int(round(M_WIND_S[4]))])
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
	#print(ii)
                    #0   1     2      3       4           5          6           7            8          9         10         11         12      13         14       15          16           17       18         19    
    #DAY3.append([STN, AREA, W_AREA, NAME, afterday2, FISH_NAME, FISH_TYPE, AFTERDAY2_MUL, WAVE_S[0], WAVE_S[2], WAVES_[1], SST_S[0], SST_S[2], SST_S[1], TEMP_S[0], TEMP_S[2], TEMP_S[1], WIND_S[0], WIND_S[2], WIND_S[1]])
	TIDE_SCRE = IndexScore().tide_score(DAY1[ii][7],DAY1[ii][8])
	WAVE_SCRE = IndexScore().wave_score(round(float(DAY1[ii][11]),1))
	SST_SCRE = IndexScore().sst_score(DAY1[ii][7],DAY1[ii][13])
	TEMP_SCRE = IndexScore().temp_score(DAY1[ii][16])
	WIND_SCRE = IndexScore().wind_score(DAY1[ii][20])
	WARN_SCRE = IndexScore().warn_score('-')
	TOTAL_SCRE1 = IndexScore().total_score(TIDE_SCRE, WAVE_SCRE, SST_SCRE, TEMP_SCRE, WIND_SCRE, WARN_SCRE)[0] # forecast score(no rain, no warning)

    #              0    1       2      3       4           5          6           7            8          9         10         11         12      13         14       15          16           17       18         19         20     21          22          23            24         25    
    #DAY3.append([STN, AREA, W_AREA, NAME, afterday2, FISH_NAME, FISH_TYPE, AFTERDAY2_MUL, TIDE_SCRE, WAVE_S[0], WAVE_S[2], WAVES_[1], WAVE_SCRE, SST_S[0], SST_S[2], SST_S[1],SST_SCRE, TEMP_S[0], TEMP_S[2], TEMP_S[1],TEMP_SCRE, WIND_S[0], WIND_S[2], WIND_S[1]], WIND_SCRE, TOTAL_SCRE1])
	DAY1[ii].insert(9,TIDE_SCRE) ; DAY1[ii].insert(13,WAVE_SCRE) ; DAY1[ii].insert(17,SST_SCRE); DAY1[ii].insert(21,TEMP_SCRE) ; DAY1[ii].insert(25,WIND_SCRE) ; DAY1[ii].insert(26,TOTAL_SCRE1)
	ii = ii + 1

#[Output Data] ========================================================================================
OUT_FNAME1=dir1+'/SFEQ_INDEX_OBS_1QC_'+today+'.csv'
with open(OUT_FNAME1,'w',encoding='utf8') as file:
	file.write('생산일,코드,권역,지역,예측일자,시간,어종,어종타입,물때,물때점수,최소파고,평균파고,최대파고,파고점수,최소수온,평균수온,최대수온,수온점수,최저기온,평균기온,최대기온,기온점수,최소풍속,평균풍속,최대풍속,풍속점수,총점수\n',)
	ii = 0
	while ii <= len(DAY1)-1 :
		#[전체 데이터 Writing]
		file.write(f'{today},{DAY1[ii][0]},{DAY1[ii][1]},{DAY1[ii][3]},{DAY1[ii][4]},{DAY1[ii][5]},{DAY1[ii][6]},{DAY1[ii][7]},{DAY1[ii][8]},{DAY1[ii][9]},{DAY1[ii][10]:2.1f},{DAY1[ii][11]:2.1f},{DAY1[ii][12]:2.1f},{DAY1[ii][13]},{DAY1[ii][14]},{DAY1[ii][15]},{DAY1[ii][16]},{DAY1[ii][17]},{DAY1[ii][18]},{DAY1[ii][19]},{DAY1[ii][20]},{DAY1[ii][21]},{DAY1[ii][22]},{DAY1[ii][23]},{DAY1[ii][24]},{DAY1[ii][25]},{DAY1[ii][26]:4.2f}\n')
		ii = ii + 1

print("#SFEQ OBS_INDEX 1QC CREAT Complete==========")
