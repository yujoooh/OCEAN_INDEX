#[Geosystem Research : Department of Marine Forecast ]
#[Created by C.K. Park on 2018.10.23]
import json
import urllib.request
import os
import numpy as np
from collections import OrderedDict
from datetime import date, timedelta
from datetime import datetime
from math import *

os.putenv('NLS_LANG', '.UTF8') # 한글 깨질 때 사용 ㅎㅎ

print("#KHOA Yesterday OBS data collection Start==========")

#[Date Set]===============================================================================================================
today = str(datetime.today().strftime('%Y%m%d'))
yesterday = (date.today() - timedelta(1)).strftime('%Y%m%d')
hr = str(datetime.today().strftime("%H"))
h = 0
#today = str(date(2019,11,7).strftime('%Y%m%d'))
#yesterday = (date(2019,11,7) - timedelta(1)).strftime('%Y%m%d')


#[REALTIME DATA DOWNLOAD]================================================================================================
if not os.path.exists('./Result/'+today+'/OBS_DAILY/OBS_KHOA_'+yesterday+'.txt'): os.system(r'"C:\Program Files (x86)\GnuWin32\bin\wget.exe" -P ./Result/'+today+'/OBS_DAILY/ http://10.27.90.53:8080/opendap/external/FORECAST_QUOTIENT/OBS/OBS_KHOA_'+yesterday+'.txt')


#[Info Data Read]=========================================================================================
OBS_INF = open('./Info/KHOA_OBS_INFO.csv','r',encoding='utf8')
OBS_STN = [str(INFO) for INFO in OBS_INF.read().split()]
print(len(OBS_STN), len(OBS_STN)-1)
#ii = 1
#while ii <= len(OBS_STN)-1 :
#	print(OBS_STN[ii])
#	ii = ii + 1


#[OBS Data Read]==========================================================================================
OBS_DATA = open('./Result/'+today+'/OBS_DAILY/OBS_KHOA_'+yesterday+'.txt','r',encoding='utf8')
OBS = [str(INFO) for INFO in OBS_DATA.read().split()]

Miss = -999
ii = 0
qc_data = []
last_YMDHMS = ''
while ii <= len(OBS)-1 : 
	DEV = OBS[ii].split(',')
	POINT = DEV[0] ; YMDHMS = DEV[1] ; SST = DEV[6] ; WSPD = DEV[16] ; WDIR = DEV[17] ; WHT = DEV[32]
	#print(YMDHMS, YMDHMS[10:14])
	if YMDHMS[10:14] == '0000' and YMDHMS != last_YMDHMS:
		#print(POINT, YMDHMS[0:10], SST, WSPD, WDIR)
		if WHT == 'NAN' : WHT = Miss
		if SST == 'NAN' : SST = Miss
		if WDIR == 'NAN' : WDIR = Miss
		if WSPD == 'NAN' :
			WSPD = Miss ; USPD = Miss ; VSPD = Miss
		else :
			USPD = round(-abs(float(WSPD))*sin(np.deg2rad(float(WDIR))),1)
			VSPD = round(-abs(float(WSPD))*cos(np.deg2rad(float(WDIR))),1)
			
		jj = 0
		while jj < len(OBS_STN)-1:
			DEV2 = OBS_STN[jj].split(',')
			POINT2 = DEV2[0] ; NAME = DEV2[1] ; TYPE = DEV2[2]
			#print(POINT, POINT2, NAME, TYPE)
			
			if POINT == POINT2 :
				OBS_POINT = POINT ; OBS_NAME = NAME ; OBS_TYPE = TYPE
				qc_data.append([OBS_POINT, OBS_NAME, YMDHMS[0:10], SST, WHT, WSPD, WDIR, USPD, VSPD, OBS_TYPE])
			jj = jj + 1
	last_YMDHMS = YMDHMS
	ii = ii + 1
	
#ii = 0
#while ii <= len(qc_data)-1 :
#	print(qc_data[ii])
#	ii = ii + 1
	
qc_data_len = len(qc_data)
OUT_FNAME='./Result/'+today+'/OBS_DAILY/OBS_KHOA_'+yesterday+'.csv'
with open(OUT_FNAME,'w',encoding='utf8') as file:
	file.write('지점번호,지점명,년월일시,수온,파고,풍속,풍향,U풍속,V풍속,관측소\n')
	ii = 0
	while ii <= qc_data_len-1:
		file.write(f'{qc_data[ii][0]},{qc_data[ii][1]},{qc_data[ii][2]},{qc_data[ii][3]},{qc_data[ii][4]},{qc_data[ii][5]},{qc_data[ii][6]},{qc_data[ii][7]},{qc_data[ii][8]},{qc_data[ii][9]}\n')
		ii = ii + 1

print("#KHOA Yesterday OBS data collection Complete==========")
