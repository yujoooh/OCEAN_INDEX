#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.04.11] edit 19.08.22
import sys
import os
import numpy as np
import calendar
from datetime import date, timedelta
from datetime import datetime
from math import *

print("#KMA Monthly OBS data collection Start==========")

#[Date Set]===============================================================================================================
today = str(datetime.today().strftime('%Y%m%d'))
YY = str(datetime.today().strftime('%Y'))
MM = str(datetime.today().strftime('%m'))

#Manual set
#MM = 12 # 월 설정 만 하고 돌리면 됨

if int(MM) == 1 :
	YY2 = int(YY)
	YY = int(YY) - 1
	print(YY, YY2)
	MM = 12
	MM2 = 1 #마지막일은 다음달 1일 폴더에 쌓임
else : 
	MM2 = int(MM)
	MM = int(MM) - 1
	YY = int(YY)
	YY2 = int(YY)
	
YM1 = str(date(YY,int(MM),1).strftime('%Y%m'))
YM2 = str(date(YY2,int(MM2),1).strftime('%Y%m')) #마지막일자 관측자료는 다음달 1일 폴더에 쌓임
YR1 = int(YM1[0:4]) ; MN1 = int(YM1[4:6])
YR2 = int(YM2[0:4]) ; MN2 = int(YM2[4:6])#1일은 전월 마지막날 폴더에 쌓임

EDAY1 = int(calendar.monthrange(int(YR1), int(MN1))[1])
EDAY2 = int(calendar.monthrange(int(YR2), int(MN2))[1])
#print(YM1, YM2)
#print(YR1, MN1, YR2, MN2, EDAY1, EDAY2)

DAY = 2
COM=[]
while DAY <= EDAY1 + 1 :
	if DAY == EDAY1+1 : 
		MN3 = (f'{MN1:02d}') #폴더용
		DAY1 = (f'{1:02d}') #폴더용
		
		MN4 = (f'{MN2:02d}') #파일용
		DAY2 = (f'{DAY-1:02d}') #파일용
		FNAME = './Result/'+str(YR2)+MN4+DAY1+'/OBS_DAILY/OBS_KMA_'+str(YR1)+MN3+DAY2+'.csv'
	else : 
		MN3 = (f'{MN1:02d}') #폴더용
		DAY1 = (f'{DAY:02d}') #폴더용
		
		MN4 = (f'{MN2:02d}') #파일용
		DAY2 = (f'{DAY-1:02d}') #파일용
		FNAME = './Result/'+str(YR1)+MN3+DAY1+'/OBS_DAILY/OBS_KMA_'+str(YR1)+MN3+DAY2+'.csv'
	print(FNAME)

	OBS_DATA = open(FNAME,'r',encoding='utf8')
	OBS = [str(INFO) for INFO in OBS_DATA.read().split()]
	
	ii = 1
	while ii <= len(OBS)-1:
		DEV = OBS[ii].split(',')
		STN = DEV[0] ; POINT = DEV[1] ; YMDHMS = DEV[2]
		SST = DEV[3] ; WAVE = DEV[4] ; WSPD = DEV[5] ;WDIR = DEV[6]; USPD = DEV[7]; VSPD = DEV[8]; TYPE = DEV[9]
		COM.append([STN,POINT, YMDHMS,SST,WAVE,WSPD,WDIR,USPD,VSPD,TYPE])
		ii = ii + 1
	DAY = DAY + 1

COM.sort()

#ii = 0
#while ii <= len(COM)-1:
#	print(COM[ii])
#	ii = ii + 1

OUT_FNAME='./Result/OBS_Monthly/OBS_KMA_'+YM1+'.csv'
with open(OUT_FNAME,'w',encoding='utf8') as file:
	file.write('지점번호,지점명,년월일시,수온,파고,풍속,풍향,U풍속,V풍속,관측소\n')
	ii = 0
	while ii <= len(COM)-1:
		file.write(f'{COM[ii][0]},{COM[ii][1]},{COM[ii][2]},{COM[ii][3]},{COM[ii][4]},{COM[ii][5]},{COM[ii][6]},{COM[ii][7]},{COM[ii][8]},{COM[ii][9]}\n')
		ii = ii + 1

print("#KMA Monthly OBS data collection Complete==========")