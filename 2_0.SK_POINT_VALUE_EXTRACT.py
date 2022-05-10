#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.08.08]
import sys
import os
import shutil
import numpy as np
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime

print("#SKEQ OBS data extract Start==========")

#[Date set] ==============================================================================================
#[Auto date set]
HR = str(datetime.today().strftime('%H'))
today = str(datetime.today().strftime('%Y%m%d'))
dir1 = './Result/'+today

#[Manual date set]
#HR = '10'
if int(HR) <12 : AMPM = 'AM'
if int(HR) >= 12 : AMPM = 'PM'
	
KMA_OBS_DATA = open(dir1+'/KMA_OBS_'+AMPM+'.csv','r',encoding='utf8')
KMA_OBS = [LST for LST in KMA_OBS_DATA.read().split()]
KMA_LEN = len(KMA_OBS)
#print(KMA_OBS[0], KMA_OBS[1], KMA_OBS[2],KMA_OBS[3])

KHOA_OBS_DATA = open(dir1+'/KHOA_OBS_'+AMPM+'.csv','r',encoding='utf8')
KHOA_OBS = [LST for LST in KHOA_OBS_DATA.read().split()]
KHOA_LEN = len(KHOA_OBS)



#for 문으로 다른 지수의 관측자료도 반복적으로 추출하도록 수정
#[READ Info Data] ========================================================================================
INDEX_LIST = ['SK']

data=[] #저장 list 생성
MWHT1=-999 ; MWHT2=-999
#INDEX_LIST = ['SP','SF','SK','SF','SD','TL']
for LIST in INDEX_LIST:
	POINT_INF = open('./Info/'+LIST+'_Point_Info.csv','r',encoding='utf8')  
	INF = [str(INFO) for INFO in POINT_INF.read().split()]
	INF_LEN = len(INF)
	
	ii = 1
	while ii <= INF_LEN-1 :
		DEV = INF[ii].split(',')
		if ii != 1 :DEV2 = INF[ii-1].split(',')
		STN = DEV[0] ; AREA = DEV[1]; NAME = DEV[2] ; LON = DEV[3] ; LAT = DEV[4]
		WRF_X = int(DEV[7]) ; WRF_Y = int(DEV[8]) ; WW3_X = int(DEV[9]) ; WW3_Y = int(DEV[10])
		CWW3_X = int(DEV[11]) ; CWW3_Y = int(DEV[12]) ; CWW3_LOC = int(DEV[13])
		RWW3_X = int(DEV[14]) ; RWW3_Y = int(DEV[15]) ; MOHID_X = int(DEV[16]) ; MOHID_X = int(DEV[17])
		AGY1 = DEV[21]; MWHT_STN1 = DEV[22]; AGY2 = DEV[23]; MWHT_STN2 = DEV[24]
		#print(AGY1, MWHT_STN1, AGY2, MWHT_STN2)
		# 1/2순위를 결픅 값으로 초기화
		MWHT1 = '-999.0' ; MWHT2 = '-999.0'
		
		if ii == 1 :
			jj = 4
			while jj <= KMA_LEN-1 :# 지점별 1/2순위 선택(기상청)
				DEV2 = KMA_OBS[jj].split(',')
				KMA_AGY = DEV2[0] ; KMA_STN = DEV2[1] ; KMA_SST = DEV2[2] ; KMA_MWHT = DEV2[3]
				#print(KMA_AGY, KMA_STN, KMA_SST, KMA_MWHT)
				if AGY1 == KMA_AGY and MWHT_STN1 == KMA_STN :
					MWHT1 = KMA_MWHT
				elif AGY2 == KMA_AGY and MWHT_STN2 == KMA_STN :
					MWHT2 = KMA_MWHT
				jj = jj + 1		
		
			kk = 7
			while kk <= KHOA_LEN-1 :# 지점별 1/2순위 선택(조사원)
				DEV3 = KHOA_OBS[kk].split(',')
				KHOA_AGY = DEV3[0] ; KHOA_STN = DEV3[1] ; KHOA_SST = DEV3[2] ; KHOA_MWHT = DEV3[3]
				#print(KHOA_AGY, KHOA_STN, KHOA_SST, KHOA_MWHT)
				if AGY1 == KHOA_AGY and MWHT_STN1 == KHOA_STN :
					MWHT1 = KHOA_MWHT
				elif AGY2 == KHOA_AGY and MWHT_STN2 == KHOA_STN :
					MWHT2 = KHOA_MWHT
				kk = kk + 1	
		
			# 결측을 제외하고 우선 순위에 따른 적용 
			if MWHT1 != '-999.0' :
				MWHT = MWHT1
			elif MWHT2 != '-999.0' :
				MWHT = MWHT2
			else:
				MWHT = -999

			#print(NAME, '-999', MWHT)
			data.append([NAME, '-999', round(float(MWHT),1)])
		elif STN == DEV2[0] : 
			DUMY = 1
			#print(STN, DEV2[0],"same_loc")
		elif STN != DEV2[0]:
			jj = 4
			while jj <= KMA_LEN-1 :# 지점별 1/2순위 선택(기상청)
				DEV2 = KMA_OBS[jj].split(',')
				KMA_AGY = DEV2[0] ; KMA_STN = DEV2[1] ; KMA_SST = DEV2[2] ; KMA_MWHT = DEV2[3]
				#print(KMA_AGY, KMA_STN, KMA_SST, KMA_MWHT)
				if AGY1 == KMA_AGY and MWHT_STN1 == KMA_STN :
					MWHT1 = KMA_MWHT
				elif AGY2 == KMA_AGY and MWHT_STN2 == KMA_STN :
					MWHT2 = KMA_MWHT
				jj = jj + 1		
		
			kk = 7
			while kk <= KHOA_LEN-1 :# 지점별 1/2순위 선택(조사원)
				DEV3 = KHOA_OBS[kk].split(',')
				KHOA_AGY = DEV3[0] ; KHOA_STN = DEV3[1] ; KHOA_SST = DEV3[2] ; KHOA_MWHT = DEV3[3]
				#print(KHOA_AGY, KHOA_STN, KHOA_SST, KHOA_MWHT)
				if AGY1 == KHOA_AGY and MWHT_STN1 == KHOA_STN :
					MWHT1 = KHOA_MWHT
				elif AGY2 == KHOA_AGY and MWHT_STN2 == KHOA_STN :
					MWHT2 = KHOA_MWHT
				kk = kk + 1	
		
			# 결측을 제외하고 우선 순위에 따른 적용 
			if MWHT1 != '-999.0' :
				MWHT = MWHT1
			elif MWHT2 != '-999.0' :
				MWHT = MWHT2
			else:
				MWHT = -999

			if AREA == '황해중부' or AREA =='황해남부' : VR_AREA = '서해'
			if AREA == '남해서부' or AREA =='남해동부' or AREA == '제주도': VR_AREA = '남해'
			if AREA == '동해중부' or AREA =='동해남부' : VR_AREA = '동해'
			
			print(NAME, '-999', MWHT)
			data.append([NAME, '-999', round(float(MWHT),1)])
		ii = ii + 1

	with open(dir1+'/'+LIST+'_POINT_OBS_'+AMPM+'.csv','w',encoding='utf8') as file:
		#file.write('NAME, SST, MWHT, VR_AREA\n')
		for i in data:
			file.write('{0},{1},{2}\n'.format(i[0],i[1],i[2]))
	del data[:]
if not os.path.exists(dir1+'/'+LIST+'_POINT_OBS_AM.csv'): shutil.copy(dir1+'/'+LIST+'_POINT_OBS_PM.csv', dir1+'/'+LIST+'_POINT_OBS_AM.csv') #12시 이후에 AM자료가 없으면 PM자료 복사해서 이름 바꾸기

print("#SKEQ OBS data extract Complete==========")
