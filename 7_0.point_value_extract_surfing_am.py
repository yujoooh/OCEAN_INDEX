#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.08.08]
import sys
import os
import shutil
import numpy as np
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime

print("#SURFING OBS data extract Start==========")

#[Date set] ==============================================================================================
#[Auto date set]
#HR = str(datetime.today().strftime('%H'))
today = str(datetime.today().strftime('%Y%m%d'))
dir1 = './Result/'+today

#[Manual date set]
HR = '10'
if int(HR) <12 : AMPM = 'AM'
if int(HR) >= 12 : AMPM = 'PM'
	
KHOA_OBS_DATA = open(dir1+'/KHOA_OBS_'+AMPM+'.csv','r',encoding='utf8')
KHOA_OBS = [LST for LST in KHOA_OBS_DATA.read().split()]
KHOA_LEN = len(KHOA_OBS)

#for 문으로 다른 지수의 관측자료도 반복적으로 추출하도록 수정
#[READ Info Data] ========================================================================================
INDEX_LIST = ['SR']

data=[] #저장 list 생성
for LIST in INDEX_LIST:
	POINT_INF = open('./Info/'+LIST+'_Point_Info.csv','r',encoding='utf8')  
	INF = [str(INFO) for INFO in POINT_INF.read().split()]
	INF_LEN = len(INF)
	
	ii = 1
	while ii <= INF_LEN-1 :
	#while ii <= 1 :
		DEV = INF[ii].split(',')
		STN = DEV[1] ; AREA = DEV[2] ; NAME = DEV[3] ; W_AREA = DEV[19];
		AGY1 = DEV[20]; MWHT_STN1 = DEV[21]; AGY2 = DEV[22]; MWHT_STN2 = DEV[23]
		AGY3 = DEV[25]; SST_STN1 = DEV[26]; AGY4 = DEV[27]; SST_STN2 = DEV[28]
		#print(AGY1, MWHT_STN1, AGY2, MWHT_STN2)
		# 1/2순위를 결픅 값으로 초기화
		MWHT1 = '-999.0' ; MWHT2 = '-999.0' ; SST1 = '-999.0' ; SST2 = '-999.0'
		WHDIR1 = '-999.0'; WHDIR2 = '-999.0'

		#5월 20일이전
		#kk = 6
		#5월 20일 이후
		kk = 7
		while kk <= KHOA_LEN-1 :# 지점별 1/2순위 선택(조사원)
			DEV3 = KHOA_OBS[kk].split(',')
			KHOA_AGY = DEV3[0] ; KHOA_STN = DEV3[1] ; KHOA_SST = DEV3[2] ; KHOA_MWHT = DEV3[3]; KHOA_WHDIR = DEV3[4]; KHOA_RPEAK = DEV3[6]
			print(KHOA_AGY, KHOA_STN, KHOA_SST, KHOA_MWHT, KHOA_RPEAK)
			if AGY1 == KHOA_AGY and MWHT_STN1 == KHOA_STN :
				MWHT1 = KHOA_MWHT
				WHDIR1 = KHOA_WHDIR
				RPEAK1 = KHOA_RPEAK
			elif AGY2 == KHOA_AGY and MWHT_STN2 == KHOA_STN :
				MWHT2 = KHOA_MWHT
				WHDIR2 = KHOA_WHDIR
				RPEAK2 = KHOA_RPEAK
			if AGY3 == KHOA_AGY and SST_STN1 == KHOA_STN :
				SST1 = KHOA_SST
			elif AGY4 == KHOA_AGY and SST_STN2 == KHOA_STN :
				SST2 = KHOA_SST
			kk = kk + 1	
		
		# 결측을 제외하고 우선 순위에 따른 적용 
		if MWHT1 != '-999.0' :
			MWHT = MWHT1
		elif MWHT2 != '-999.0' :
			MWHT = MWHT2
		else:
			MWHT = -999
		print(NAME, MWHT)
        
		if SST1 != '-999.0' :
			SST = SST1
		elif SST2 != '-999.0' :
			SST = SST2
		else:
			SST = -999
		print(NAME, SST)
        
		if WHDIR1 != '-999' :
			WHDIR = float(WHDIR1)
			WHDIR = -WHDIR -90
			if WHDIR <0:
				# print('변환잘되고 있음')
				WHDIR += 360
				if WHDIR <0:
					WHDIR += 360				
			
		elif WHDIR2 != '-999' :
			WHDIR = float(WHDIR2)
			WHDIR = -WHDIR -90
			if WHDIR <0:
				# print('변환잘되고 있음')
				WHDIR += 360
				if WHDIR <0:
					WHDIR += 360								
		else:
			WHDIR = -999
		print(NAME, WHDIR)

		if RPEAK1 != '-999.0' :
			RPEAK = RPEAK1
		elif RPEAK2 != '-999.0' :
			RPEAK = RPEAK2
		else:
			RPEAK = -999
		print(NAME, RPEAK)
			
		if AREA == '황해중부' or AREA =='황해남부' : VR_AREA = '서해'
		if AREA == '남해서부' or AREA =='남해동부' or AREA == '제주도': VR_AREA = '남해'
		if AREA == '동해중부' or AREA =='동해남부' : VR_AREA = '동해'
		
		#print(NAME, SST, MWHT, VR_AREA)
		data.append([NAME, round(float(MWHT),1), round(float(WHDIR),1), round(float(SST),1), round(float(RPEAK),1), AREA])
		ii = ii + 1

	#print(list(set(map(tuple,data))))
	data = list(set(map(tuple,data)))
	print(data)

print("#SFEQ OBS data extract Complete==========")


with open(dir1+'/'+LIST+'_POINT_OBS_'+AMPM+'.csv','w',encoding='utf8') as file:
    #file.write('NAME, SST, MWHT, VR_AREA\n')
    for i in data:
        file.write('{0},{1},{2},{3},{4}\n'.format(i[0],i[1],i[2],i[3],i[4]))
    del data[:]
if not os.path.exists(dir1+'/'+LIST+'_POINT_OBS_AM.csv'): shutil.copy(dir1+'/'+LIST+'_POINT_OBS_PM.csv', dir1+'/'+LIST+'_POINT_OBS_AM.csv') #12시 이후에 AM자료가 없으면 PM자료 복사해서 이름 바꾸기
