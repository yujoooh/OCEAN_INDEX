#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.04.11] edit 19.08.22
import sys
import os
#os.path.join(os.getcwd(),"Function")
import numpy as np
from datetime import date, timedelta
from datetime import datetime
from math import *

print("#KHOA Monthly OBS data collection Start==========")

#[Date Set]===============================================================================================================
today = str(datetime.today().strftime('%Y%m%d'))
MM = int(datetime.today().strftime('%m'))
if MM == 1 :
	MM = 12
	YR = int(datetime.today().strftime('%Y'))-1
else : 
	MM = MM - 1
	YR = int(datetime.today().strftime('%Y'))

YM = str(date(YR,MM,1).strftime('%Y%m'))
print(YM,YR,MM)

#[Monthly QC_DATA DOWNLOAD]================================================================================================
os.system(r'"C:\Program Files (x86)\GnuWin32\bin\wget.exe" -P ./Result/OBS_Monthly/ http://10.27.90.53:8080/opendap/external/FORECAST_QUOTIENT/OBS/OBS_KHOA_'+YM+'.txt')

#[Info Data Read]=========================================================================================
OBS_INF = open('./Info/KHOA_OBS_INFO.csv','r',encoding='utf8')
OBS_STN = [str(INFO) for INFO in OBS_INF.read().split()]
#print(len(OBS_STN), len(OBS_STN)-1)

#[OBS Data Read]==========================================================================================
OBS_DATA = open('./Result/OBS_Monthly/OBS_KHOA_'+YM+'.txt','r',encoding='utf8')
OBS = [str(INFO) for INFO in OBS_DATA.read().split()]

Miss = -999
ii = 0
qc_data = []
while ii <= len(OBS)-1 : 
	DEV = OBS[ii].split(',')
	POINT = DEV[0] ; YMDHMS = DEV[1] ; SST = DEV[6] ; WSPD = DEV[16] ; WDIR = DEV[17] ; WHT = DEV[32]
	#print(YMDHMS, YMDHMS[10:14])
	if YMDHMS[10:14] == '0000' :
		#print(POINT, YMDHMS[0:10], SST, WSPD, WDIR)
		if WHT == 'NAN': WHT = Miss
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
				qc_data.append([OBS_POINT, OBS_NAME, YMDHMS[0:10], SST, float(WHT), WSPD, WDIR, USPD, VSPD, OBS_TYPE])
			jj = jj + 1
	ii = ii + 1
	
#ii = 0
#while ii <= len(qc_data)-1 :
#	print(qc_data[ii])
#	ii = ii + 1
	
qc_data_len = len(qc_data)
OUT_FNAME='./Result/OBS_Monthly/OBS_KHOA_'+YM+'.csv'
with open(OUT_FNAME,'w',encoding='utf8') as file:
	file.write('지점번호,지점명,년월일시,수온,파고,풍속,풍향,U풍속,V풍속,관측소\n')
	ii = 0
	while ii <= qc_data_len-1:
		file.write(f'{qc_data[ii][0]},{qc_data[ii][1]},{qc_data[ii][2]},{qc_data[ii][3]},{qc_data[ii][4]},{qc_data[ii][5]},{qc_data[ii][6]},{qc_data[ii][7]},{qc_data[ii][8]},{qc_data[ii][9]}\n')
		ii = ii + 1

print("#KHOA Monthly OBS data collection Complete==========")