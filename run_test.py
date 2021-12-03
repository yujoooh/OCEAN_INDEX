import sys
import os
#os.path.join(os.getcwd(),"Function")
import numpy as np
from pandas import DataFrame as df
from math import floor
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime
from Function.speq_function import IndexScore
from Function.statistic_function import Statistic

print("#SPEQ FCST_INDEX CREAT Start==========")

#[Date set] ==============================================================================================
#[Auto date set]
today = str(20210709) #str(datetime.today().strftime('%Y%m%d'))
print(today)
print(date.today())
print(datetime.today())
# afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
# afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')
# afterday3 = (date.today() + timedelta(3)).strftime('%Y%m%d')
# afterday4 = (date.today() + timedelta(4)).strftime('%Y%m%d')
# afterday5 = (date.today() + timedelta(5)).strftime('%Y%m%d')
# afterday6 = (date.today() + timedelta(6)).strftime('%Y%m%d')

dir1 = './Result/'+today

#[Info Data Read]=========================================================================================
POINT_INF = open('./Info/SP_Point_Info.csv','r',encoding='utf8')
INF = [str(INFO) for INFO in POINT_INF.read().split()]
INF_LEN = len(INF)

#[KMA CITY and WARNING data read]=========================================================================
if not os.path.exists(dir1+'/SP_CITY.csv'): # 동네예보 수집 에러에 따른 자료 미생성시 그냥 예측자료 사용
	print('CITY_FORECAST DATA Not found') ; CITY_LEN=0
else:
	CITY_INF = open(dir1+'/SP_CITY.csv','r',encoding='utf8')
	CITY = [LST for LST in CITY_INF.read().split()]
	CITY_LEN = len(CITY)

WARN_INF = open(dir1+'/KMA_WARNING.csv','r',encoding='utf8')
WARN = [LST for LST in WARN_INF.read().split()]
WARN_LEN = len(WARN)

#[BEACH DATA Extract] ====================================================================================
DAY1 = [] # today forecast data list
DAY2 = [] # tomorrow forecast data list
DAY3 = [] # the day after tomorrow forecast data list
DAY4 = []
DAY5 = []
DAY6 = []
DAY7 = []
COM  = [] # combine
SST = df(data={'1':[1,2,3],'2':[3,4,5],'3':[7,8,9]})
print(SST)

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
	print('SST_2S: '+SST_2S)
#
print("#SPEQ FCST_INDEX CREAT Complete==========")