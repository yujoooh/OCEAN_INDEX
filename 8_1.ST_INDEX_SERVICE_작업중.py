#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2020.07.30]
import sys
import os
import shutil
import numpy as np
import math
import pandas as pd
import lunardate as lunar 
from netCDF4 import Dataset
from datetime import date, timedelta, datetime
from Function.element_function import Element_extract

print("#Sea Travel FCST_INDEX CREAT Start==========")
#[Date set] ==============================================================================================
#[Auto date set]
today = str(datetime.today().strftime('%Y%m%d'))
afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')
afterday3 = (date.today() + timedelta(3)).strftime('%Y%m%d')
afterday4 = (date.today() + timedelta(4)).strftime('%Y%m%d')
afterday5 = (date.today() + timedelta(5)).strftime('%Y%m%d')
afterday6 = (date.today() + timedelta(6)).strftime('%Y%m%d')
print(today, afterday6)

#[Manual date set1]
#today  = str(date(2020,8,6).strftime('%Y%m%d'))
#afterday1 = (date(2020,8,6) + timedelta(1)).strftime('%Y%m%d')
#afterday2 = (date(2020,8,6) + timedelta(2)).strftime('%Y%m%d')
#afterday3 = (date(2020,8,6) + timedelta(3)).strftime('%Y%m%d')
#afterday4 = (date(2020,8,6) + timedelta(4)).strftime('%Y%m%d')
#afterday5 = (date(2020,8,6) + timedelta(5)).strftime('%Y%m%d')
#afterday6 = (date(2020,8,6) + timedelta(6)).strftime('%Y%m%d')

dir1 = './Result/'+today
#dir2 = 'D:/LIFE_OCEAN_INDEX/Source/Result/'+today

#[Model Data path] =======================================================================================
MPATH = './Model_Data/'
ROMS_FNAME = 'YES3K_'+ str(today) + '00.nc'      # YES3K   - KHOA
WRF_FNAME = 'WRF_' + str(today) + '.nc'          # WRF_DM2 - KHOA
WW3_FNAME = 'WW3_' + str(today) + '00.nc'        # WW3     - KHOA
CWW3_FNAME = 'CWW3_' + str(today) + '00.nc'      # CWW3    - KMA
RWW3_FNAME = 'RWW3_' + str(today) + '00.nc'      # RWW3    - KMA

INFILE_1 = MPATH+ROMS_FNAME #7day forecast data
INFILE_2 = MPATH+WRF_FNAME  #7day forecast data
INFILE_3 = MPATH+CWW3_FNAME #3day forecast data
INFILE_4 = MPATH+WW3_FNAME  #7day forecast data
INFILE_5 = MPATH+RWW3_FNAME #5day forecast data ---  not used

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

#[Sea Travel Index Forecast Area]=========================================================================
#FORECAST_AREA = ['JEJU']
FORECAST_AREA = ['JEJU','BUSAN','YEOSU','INCHEON','GANGNEUNG','TAEAN']
for FCST_AREA in FORECAST_AREA : 
	#[Info Data Read]=========================================================================================
	POINT_INF = open('./Info/'+FCST_AREA+'_Point_Info.csv','r',encoding='utf8')
	INF = [str(INFO) for INFO in POINT_INF.read().split()]
	INF_LEN = len(INF)

	#[KMA CITY and WARNING data read]=========================================================================
	if not os.path.exists(dir1+'/'+FCST_AREA+'_CITY.csv'): # 동네예보 수집 에러에 따른 자료 미생성시 그냥 예측자료 사용
		print('CITY_FORECAST DATA Not found') ; CITY_LEN=0
	else :
		CITY_INF = open(dir1+'/'+FCST_AREA+'_CITY.csv','r',encoding='utf8')
		CITY = [LST for LST in CITY_INF.read().split()]
		CITY_LEN = len(CITY)

	if not os.path.exists(dir1+'/KMA_WARNING.csv') : #기상특보자료 수집 불가시 특보 적용 없이 산출
		print('KMA_WARNING DATA Not found') ; WARN_LEN=0
	else :
		WARN_INF = open(dir1+'/KMA_WARNING.csv','r',encoding='utf8')
		WARN = [LST for LST in WARN_INF.read().split()]
		WARN_LEN = len(WARN)

	#[DATA Extract] ====================================================================================
	COM  = [] ; COM_TIME  = [] # combine

	ii = 1
	while ii < INF_LEN :
		DEV = INF[ii].split(',')
		FC_AREA = DEV[0] ; STN = DEV[1] ; AREA = DEV[2] ; NAME = DEV[3] ; LON = DEV[4] ; LAT = DEV[5]
		ROMS_X = int(DEV[6]) ; ROMS_Y = int(DEV[7]) ; WRF_X = int(DEV[8]) ; WRF_Y = int(DEV[9])
		WW3_X = int(DEV[10]) ; WW3_Y = int(DEV[11]) ; CWW3_X = int(DEV[12]) ; CWW3_Y = int(DEV[13]) ; CWW3_LOC = int(DEV[14])
		RWW3_X = int(DEV[15]) ; RWW3_Y = int(DEV[16]) ; SEA_W_AREA = DEV[19] ; LAND_W_AREA = DEV[20]
		TRAVEL1 = DEV[21] ; TRAVEL2 = DEV[22] ; TRAVEL3 = DEV[23] ; TRAVEL4 = DEV[24] ; TRAVEL5 = DEV[25]

		jj = 0
		while jj <= 158:
			SST_S  = SST[jj, ROMS_Y, ROMS_X]
			WIND_S = WIND[jj, WRF_Y, WRF_X]
			UWIND_S =  U_WIND[jj, WRF_Y, WRF_X]
			VWIND_S =  V_WIND[jj, WRF_Y, WRF_X]
			TEMP_S = TEMP[jj, WRF_Y, WRF_X]
			WIND_DIR = 180+180/math.pi*math.atan2(UWIND_S, VWIND_S) # 풍향 계산 // 유향은 atna2 요소 반전시킬것
			CURRENT_S  = CURRENT[jj, ROMS_Y, ROMS_X]

			if os.path.isfile(INFILE_3): # CWW3 우선적용. 없을경우 WW3로 일괄적용
				if jj <= 57 : # CWW3 최대 예측기간 3일 18시 까지..
					jjj = int(jj/3)+4
					if CWW3_LOC == 1 : WAVE_S = WHT_1[jjj, CWW3_Y, CWW3_X] 
					if CWW3_LOC == 2 : WAVE_S = WHT_2[jjj, CWW3_Y, CWW3_X] 
					if CWW3_LOC == 3 : WAVE_S = WHT_3[jjj, CWW3_Y, CWW3_X] 
					if CWW3_LOC == 4 : WAVE_S = WHT_4[jjj, CWW3_Y, CWW3_X] 
					if CWW3_LOC == 5 : WAVE_S = WHT_5[jjj, CWW3_Y, CWW3_X]

				else : # CWW3 최대 예측기간 이후 WW3로 적용
					WAVE_S = WHT[jj, WW3_Y, WW3_X] 
					#print(WAVE_S)
			else :
				WAVE_S =WHT[jj, WW3_Y, WW3_X]

			#if WAVE_S < '0.1' : WAVE_S == '0.1'			
			if str(SST_S)  == '--' or SST_S > 9999   : SST_S  = -999   # 내륙의 여행요소인 경우 수온 필요 없음
			if str(CURRENT_S)  == '--'  : CURRENT_S  = -999   # 내륙의 여행요소인 경우 유속 필요 없음
			if str(WAVE_S) == 'nan' or str(WAVE_S) == '-9.99': WAVE_S = -999 # 내륙의 여행요소인 경우 파고 필요 없음
			
			tm1, tm2 = divmod(jj+9,24) ; hr = format(tm2, '02') #; print(tm1, tm2, hr) #  시간계산
			afterday = (date.today() + timedelta(tm1)).strftime('%Y%m%d') # 입력날짜 정보
			#print(afterday, hr)
			#[물때정보 생산]----------------------------------------------------------------------------
			yr = int(afterday[0:4]) ; mn = int(afterday[4:6]) ; dy = int(afterday[6:8])
			yr_lunar = lunar.LunarDate.fromSolarDate(yr,mn,dy).year
			mn_lunar = lunar.LunarDate.fromSolarDate(yr,mn,dy).month
			dy_lunar = lunar.LunarDate.fromSolarDate(yr,mn,dy).day
			if dy_lunar + 7 <= 15 : MUL = dy_lunar + 7
			if dy_lunar + 7 > 15 and dy_lunar + 7 <= 30 : MUL = dy_lunar + 7 - 15
			if dy_lunar + 7 > 30 : MUL = dy_lunar + 7 - 30
			#------------------------------------------------------------------------------------------

			COM_TIME.append([FC_AREA, STN, AREA, SEA_W_AREA, LAND_W_AREA, NAME, afterday, hr, TEMP_S, WIND_S, WIND_DIR, SST_S, WAVE_S, CURRENT_S, MUL, TRAVEL1, TRAVEL2, TRAVEL3, TRAVEL4, TRAVEL5])
			jj = jj + 3 #24시간 간격으로 일괄 계산
		ii = ii + 1
	#for PP in COM_TIME : print(PP)

	#[KMA weather forecast : rain amount, sky status]=====================================================================================
	ii = 0
	COM_TIME_LEN = len(COM_TIME)
	#print(COM_TIME_LEN, CITY_LEN)
	while ii < COM_TIME_LEN : 
		DATE2 = COM_TIME[ii][6]
		if CITY_LEN == 0 :
			COM_TIME[ii].insert(15,1)    # SKY [맑음:1, 구름많음:3, 흐림:4]
			COM_TIME[ii].insert(16,0)    # RAIN AMOUNT
			COM_TIME[ii].insert(17,0) # RAIN PROBABILITY
			COM_TIME[ii].insert(18,0) # RELATIVE HUMEDITY
			COM_TIME[ii].insert(19,'-')    # SEA_WARNING
			COM_TIME[ii].insert(20,'-')    # LAND_WARNING
		else :
			COM_TIME[ii].insert(15,1)    # SKY [맑음:1, 구름많음:3, 흐림:4]
			COM_TIME[ii].insert(16,0)    # RAIN AMOUNT
			COM_TIME[ii].insert(17,0) # RAIN PROBABILITY
			COM_TIME[ii].insert(18,0) # RELATIVE HUMEDITY
			COM_TIME[ii].insert(19,'-')    # SEA_WARNING
			COM_TIME[ii].insert(20,'-')    # LAND_WARNING
		ii = ii + 1
	
	ii = 1	
	jj = 1
	while jj < CITY_LEN :              
		DEV = CITY[jj].split(',')
		FC_AREA = DEV[0] ; STN = DEV[1] ; NAME = DEV[2] ; DATE = DEV[3] ; HOUR = DEV[4]; SKY = DEV[7] ; RAIN_AMT = DEV[8] ; RAIN_PROB = DEV[9] ; REL_HU = DEV[10]
		if COM_TIME[ii][1] == STN and COM_TIME[ii][6] == DATE and COM_TIME[ii][7] == str(HOUR):
			COM_TIME[ii][15] == float(SKY)      # SKY [맑음:1, 구름많음:3, 흐림:4]
			COM_TIME[ii][16] == float(RAIN_AMT)  # RAIN AMOUNT
			COM_TIME[ii][17] == float(RAIN_PROB) # RAIN PROBABILITY
			COM_TIME[ii][18] == float(REL_HU)    # RELATIVE HUMEDITY
		jj = jj + 1
		ii = ii + 1
	#for PP in COM_TIME : print(PP)

	#[KMA WARNING INFORAMTION : special weather report]=====================================================================================================
	ii = 0 
	while ii < COM_TIME_LEN :
	#while ii < 2 :
		if WARN_LEN == 0 : 
			COM_TIME[ii][19] = '-'
			COM_TIME[ii][20] = '-'
		else : 
			jj = 1
			while jj < WARN_LEN : 
				DEV = WARN[jj].split(',')
				WARN_AREA = DEV[0] ; WARN_TYPE = DEV[1] ; WARN_SDAY = DEV[2] ; WARN_SHR = DEV[3] ; WARN_EDAY = DEV[4] ; WARN_EHR = DEV[5]
				#print(WARN_AREA, WARN_TYPE)				
				#if WARN_TYPE == 'SR1' or  WARN_TYPE == 'SR2' or  WARN_TYPE == 'SR3' : WARN_TYPE = 'SR'
				#if WARN_TYPE == 'SW1' or  WARN_TYPE == 'SW2' or  WARN_TYPE == 'SW3' : WARN_TYPE = 'SW'
				#if WARN_TYPE == 'CW1' or  WARN_TYPE == 'CW2' or  WARN_TYPE == 'CW3' : WARN_TYPE = 'CW'
				#if WARN_TYPE == 'DR1' or  WARN_TYPE == 'DR2' or  WARN_TYPE == 'DR3' : WARN_TYPE = 'DR'
				#if WARN_TYPE == 'SS1' or  WARN_TYPE == 'SS2' or  WARN_TYPE == 'SS3' : WARN_TYPE = 'SS'
				#if WARN_TYPE == 'WW1' or  WARN_TYPE == 'WW2' or  WARN_TYPE == 'WW3' : WARN_TYPE = 'WW'
				#if WARN_TYPE == 'TY1' or  WARN_TYPE == 'TY2' or  WARN_TYPE == 'TY3' : WARN_TYPE = 'TY'
				#if WARN_TYPE == 'SN1' or  WARN_TYPE == 'SN2' or  WARN_TYPE == 'SN3' : WARN_TYPE = 'SN'
				#if WARN_TYPE == 'YD1' or  WARN_TYPE == 'YD2' or  WARN_TYPE == 'YD3' : WARN_TYPE = 'YD'
				#if WARN_TYPE == 'HW1' : WARN_TYPE = 'HW1'	#폭염경보
				#if WARN_TYPE == 'HW2' or WARN_TYPE == 'HW3' : WARN_TYPE = 'HW'	#폭염주의보/예비특보
				#[해상특보적용]------------------------------------------------------------------------------------------
				if COM_TIME[ii][6] < WARN_EDAY and COM_TIME[ii][6] >= WARN_SDAY and COM_TIME[ii][3] == WARN_AREA : # [해상특보] 해제예고 일보다 전날일 경우 일괄적용
					COM_TIME[ii][19] = WARN_TYPE
					jjj = WARN_LEN
				elif COM_TIME[ii][6] == WARN_EDAY and COM_TIME[ii][6] >= WARN_SDAY and COM_TIME[ii][3] == WARN_AREA : # 해제예고일과 같을 경우 AM이면 오전만 적용, PM이면 오전/오후 모두적용
					if WARN_EHR == 'AM' and (COM_TIME[ii][7] == '00' or COM_TIME[ii][7] == '03' or COM_TIME[ii][7] == '06' or COM_TIME[ii][7] == '09') : 
						COM_TIME[ii][19] = WARN_TYPE
					elif WARN_EHR == 'PM' and (COM_TIME[ii][7] == '00' or COM_TIME[ii][7] == '03' or COM_TIME[ii][7] == '06' or COM_TIME[ii][7] == '09' or COM_TIME[ii][7] == '12' or COM_TIME[ii][7] == '15' or COM_TIME[ii][7] == '18' or COM_TIME[ii][7] == '21') : 
						COM_TIME[ii][19] = WARN_TYPE
					jjj = WARN_LEN
				else : 
					jjj = WARN_LEN + 1
				#[육상특보적용]------------------------------------------------------------------------------------------
				if COM_TIME[ii][6] < WARN_EDAY and COM_TIME[ii][6] >= WARN_SDAY and COM_TIME[ii][4] == WARN_AREA : # 해제예고 일보다 전날일 경우 일괄적용
					COM_TIME[ii][20] = WARN_TYPE
					jj = WARN_LEN
				elif COM_TIME[ii][6] == WARN_EDAY and COM_TIME[ii][6] >= WARN_SDAY and COM_TIME[ii][4] == WARN_AREA : # 해제예고일과 같을 경우 AM이면 오전만 적용, PM이면 오전/오후 모두적용
					if WARN_EHR == 'AM' and (COM_TIME[ii][7] == '00' or COM_TIME[ii][7] == '03' or COM_TIME[ii][7] == '06' or COM_TIME[ii][7] == '09') : 
						COM_TIME[ii][20] = WARN_TYPE
					elif WARN_EHR == 'PM' and (COM_TIME[ii][7] == '00' or COM_TIME[ii][7] == '03' or COM_TIME[ii][7] == '06' or COM_TIME[ii][7] == '09' or COM_TIME[ii][7] == '12' or COM_TIME[ii][7] == '15' or COM_TIME[ii][7] == '18' or COM_TIME[ii][7] == '21') : 
						COM_TIME[ii][20] = WARN_TYPE
					jj = WARN_LEN
				else:
					jj = jj + 1
					if jj == WARN_LEN and jjj == WARN_LEN :
						break
				jj = jj
						#print(COM_TIME[ii][4], 'warning does not exist...')
		ii = ii + 1
	COM_TIME_DF = pd.DataFrame(COM_TIME)
	COM_TIME_DF.columns = ['FC_AREA','STN','AREA','SEA_WARN','LAND_WARN','NAME','DATE','HR','TEMP','WSPD','WDIR','SST','WAVE','CURRENT','MUL','SKY','RAIN','RAIN_PROB','REL_HU','WARN1','WARN2','TRAVEL1','TRAVEL2','TRAVEL3','TRAVEL4','TRAVEL5']
	#print(COM_TIME_DF)

	#[Index Score Calculate] ========================================================================================
	SEA_TRAVEL_INDEX = Element_extract().travel(COM_TIME_DF,FCST_AREA)
	SEA_TRAVEL_INDEX = SEA_TRAVEL_INDEX.sort_values(by = ['DATE', 'FC_AREA'], ascending=True)
	#print(SEA_TRAVEL_INDEX)

	#[Output Data] ========================================================================================
	OUT_FNAME1 = dir1+'/ST_TIMESERIES_'+FCST_AREA+'_'+today+'.csv'   # 시계열
	OUT_FNAME2 = dir1+'/ST_INDEX_FCST_'+FCST_AREA+'_'+today+'.csv'   # 예보지수

	COM_TIME_DF.to_csv(OUT_FNAME1,mode='w',encoding='utf8', index=False)
	SEA_TRAVEL_INDEX.to_csv(OUT_FNAME2,mode='w',encoding='utf8', index=False)

#shutil.copy(dir1+'/ST_INDEX_FCST_BUSAN_'+today+'.csv', dir2+'/ST_INDEX_FCST_BUSAN_'+today+'.csv')
#shutil.copy(dir1+'/ST_INDEX_FCST_JEJU_'+today+'.csv', dir2+'/ST_INDEX_FCST_JEJU_'+today+'.csv')
#shutil.copy(dir1+'/ST_INDEX_FCST_YEOSU_'+today+'.csv', dir2+'/ST_INDEX_FCST_YEOSU_'+today+'.csv')
print("#Sea Travel FCST_INDEX CREAT Complete==========")
