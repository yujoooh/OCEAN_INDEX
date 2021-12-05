#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.04.11] edit 19.08.22
import sys
import os
import numpy as np
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime
from Function.sfeq_function import IndexScore
from Function.statistic_function import Statistic

print("#SFEQ SERVICE_INDEX CREAT Start==========")

#[Date set] ==============================================================================================
#[Auto date set]
today = str(datetime.today().strftime('%Y%m%d'))
afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')

#[Manual date set]
#today = str(date(2019,10,18).strftime('%Y%m%d'))
#afterday1 = (date(2019,10,18) + timedelta(1)).strftime('%Y%m%d')
#afterday2 = (date(2019,10,18) + timedelta(2)).strftime('%Y%m%d')
#print(today, afterday1, afterday2)

#[Manual date set2] 외부변수 받아오기
var1 = sys.argv[1] ; var2 = sys.argv[2]; var3 = sys.argv[3]
today = str(date(int(var1),int(var2),int(var3)).strftime('%Y%m%d'))
afterday1 = (date(int(var1),int(var2),int(var3)) + timedelta(1)).strftime('%Y%m%d')
afterday2 = (date(int(var1),int(var2),int(var3)) + timedelta(2)).strftime('%Y%m%d')
afterday3 = (date(int(var1),int(var2),int(var3)) + timedelta(3)).strftime('%Y%m%d')
afterday4 = (date(int(var1),int(var2),int(var3)) + timedelta(4)).strftime('%Y%m%d')
afterday5 = (date(int(var1),int(var2),int(var3)) + timedelta(5)).strftime('%Y%m%d')
afterday6 = (date(int(var1),int(var2),int(var3)) + timedelta(6)).strftime('%Y%m%d')
#print(today, afterday1, afterday2)

dir1 = './Result/'+today

mon = date.today().month  # 자료 생산일 기준 월 구분
hr = float(datetime.today().strftime("%H"))
hr = 10
#print(hr)
#print(today, afterday1, afterday2)

#산출된 예보지수자료 읽기-------------------------------------------------------------------------
SFEQ_INF = open(dir1+'/SFEQ_INDEX_SERVICE_'+today+'.csv',encoding='utf8')
SFEQ = [LST for LST in SFEQ_INF.read().split()]
SFEQ_LEN = len(SFEQ)

fdata = []
rawdata = []
ii = 1
while ii < SFEQ_LEN:
	DEV = SFEQ[ii].split(',')
#   0   1 2   3    4   5    6  7     8    9     10    11   12   13   14   15    16   17   18    19    20    21   22    23  24  25   26
#'코드,권역,지역,예측일자,어종,어종타입,물때,물때점수,최소파고,평균파고,최대파고,파고점수,최소수온,평균수온,최대수온,수온점수,최저기온,평균기온,최대기온,기온점수,최소풍속,평균풍속,최대풍속,풍속점수,특보,특보점수,총점수
	Code = DEV[0]; Area = DEV[1] ; Point = DEV[2] ; FDATE = DEV[3] ; FISH_NAME = DEV[4]
	FISH_TYPE = DEV[5] ; MUL = DEV[6] ; MIN_WHT = DEV[8] ; AVE_WHT = DEV[9] ; MAX_WHT = DEV[10]
	MIN_SST = DEV[12] ; AVE_SST = DEV[13] ; MAX_SST = DEV[14]
	MIN_TEMP = DEV[16] ; AVE_TEMP = DEV[17] ; MAX_TEMP = DEV[18]
	MIN_WIND = DEV[20] ; AVE_WIND = DEV[21] ; MAX_WIND = DEV[22]
	WARN = DEV[24]
	
	fdata.append([Point,FDATE, MIN_SST, AVE_SST, MAX_SST, MIN_WHT, AVE_WHT, MAX_WHT])
	rawdata.append([ii,Code,Area,Point, FDATE, FISH_NAME, FISH_TYPE, MUL, MIN_WHT, AVE_WHT, MAX_WHT, MIN_SST, AVE_SST, MAX_SST, MIN_TEMP, AVE_TEMP, MAX_TEMP, MIN_WIND, AVE_WIND, MAX_WIND, WARN])
	ii += 1
# 수집된 관측자료 읽기-------------------------------------------------------------------------
odata = []
if hr < 12: # 오전자료 읽기
	AM_DATA = open(dir1+'/SF_POINT_OBS_AM.csv','r',encoding='utf8')
	AM = [LST for LST in AM_DATA.read().split()]
	AM_LEN = len(AM)
	check = 'am'

	ii = 0
	while ii < AM_LEN:
		DEV = AM[ii].split(',')
		#print(DEV)
		odata.append(DEV)
		ii = ii + 1

#검증결과 자료 읽기--------------------------------------------------------------------------
#[서해,남해,동해]로 구분하기 [뱃멀미는 항로별 구분필요] STN_REF.dat에 해역 구분하고 POINT OBS에 들어가도록 해야할듯.
Ver_DATA = open('./Info/Verification.csv','r',encoding='utf8')
Ver = Ver_DATA.readlines()
WEST_WHT = Ver[1].split(",") # 서해 파고 RMSE
SOUTH_WHT = Ver[2].split(",") # 동해 파고 RMSE
EAST_WHT = Ver[3].split(",") # 남해 파고 RMSE

WEST_SST = Ver[4].split(",") # 서해 수온 RMSE
SOUTH_SST = Ver[5].split(",") # 남해 수온 RMSE
EAST_SST = Ver[6].split(",") # 동해 수온 RMSE

WEST_RMSE_WHT = float(WEST_WHT[mon]) ; SOUTH_RMSE_WHT = float(SOUTH_WHT[mon]) ; EAST_RMSE_WHT = float(EAST_WHT[mon])
WEST_RMSE_SST = float(WEST_SST[mon]) ; SOUTH_RMSE_SST = float(SOUTH_SST[mon]) ; EAST_RMSE_SST = float(EAST_SST[mon])
#print(WEST_RMSE_WHT, SOUTH_RMSE_WHT, EAST_RMSE_WHT, WEST_RMSE_SST, SOUTH_RMSE_SST, EAST_RMSE_SST)

#print(len(fdata),SFEQ_LEN,len(odata))
# 예측자료/관측자료 비교하기---------------------------------------------------------------------
kk = 0
apply1 = []
while kk < int((SFEQ_LEN-1)*2/7):
	mm = 0
	while mm < AM_LEN:
		if fdata[kk][0] == odata[mm][0]:# 예보지역과 관측지역 일치여부
			#print(fdata[kk][0], odata[mm][0])
			Diff_Point = fdata[kk][0]
			# 1일은 그냥 관측자료로 넣기----------------------------------------------------------------
			if fdata[kk][1] == today:                
				if odata[mm][1] == '-999.0':                
					apply_SST = round(float(fdata[kk][3]),2)
					obj_SST = "fcst"
				else:
					apply_SST = round(float(odata[mm][1]),2)
					obj_SST = "obs"
				if odata[mm][2] == '-999.0':
					apply_WHT = round(float(fdata[kk][7]),10)
					obj_WHT = "fcst"
				else:
					apply_WHT = round(float(odata[mm][2]),2)                    
					obj_WHT = "obs"
			# 2일은 예측값과 비교 후 벗어나면 관측자료로 대체----------------------------------------------------------------
			elif fdata[kk][1]== afterday1:
				if odata[mm][1] == '-999.0' : # Missing value면 차이 0으로 설정
					Diff_SST = 0
				else:
					Diff_SST = abs(round(float(fdata[kk][3]) - float(odata[mm][1]),2))
	
				#해역별 RMSE 비교  : apply_는 적용할 자료------------------------------------
				if odata[mm][3] == '서해':
					if Diff_SST > WEST_RMSE_SST:
						apply_SST = round(float(odata[mm][1]),2)
						obj_SST = "obs"
					else:
						apply_SST = round(float(fdata[kk][3]),2)
						obj_SST = "fcst"
	
				elif odata[mm][3] == '남해':
					if Diff_SST > SOUTH_RMSE_SST:
						apply_SST = round(float(odata[mm][1]),2)
						obj_SST = "obs"
					else:
						apply_SST = round(float(fdata[kk][3]),2)
						obj_SST = "fcst"
	
				elif odata[mm][3] == '동해':
					if Diff_SST > EAST_RMSE_SST:
						apply_SST = round(float(odata[mm][1]),2)
						obj_SST = "obs"
					else:
						apply_SST = round(float(fdata[kk][3]),2)
						obj_SST = "fcst"
						
				else:#한반도 RMSE
					if Diff_SST > KOR_RMSE_SST:
						apply_SST = round(float(odata[mm][1]),2)
					else:
						apply_SST = round(float(fdata[kk][3]),2)
	
				apply_WHT = round(float(fdata[kk][7]),10)
				obj_WHT = "fcst"
	
			apply1.append([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
			#print(kk,Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT)
		mm += 1
	kk = kk + 1
#ii = 0
#while ii < len(apply1) : 
#	print(apply1[ii])
#	ii = ii + 1	 

# 3일은 2일 변경값과 비교 후 벗어나면 관측자료로 대체----------------------------------------------------------------

kk = int((SFEQ_LEN-1)*2/7)
nn = int((SFEQ_LEN-1)/7)
#print(kk,nn)
while kk < int((SFEQ_LEN-1)*3/7):
    mm = 0
    while mm < AM_LEN:
        if fdata[kk][0] == odata[mm][0]:# 예보지역과 관측지역 일치여부
            Diff_Point = odata[mm][0]
#            print(fdata[kk][0], odata[mm][0], float(apply1[nn][3]), float(fdata[kk][3])) 
#            print(Diff_Point,apply1[nn][0]) 
             # 3일--------------------------------------------------------------------------
            if fdata[kk][1] == afterday2 and apply1[nn][1] == afterday1:                
                if odata[mm][1] == '-999.0' : # Missing value면 차이 0으로 설정
                    Diff_SST = 0
                else:
                    Diff_SST = abs(round(float(apply1[nn][3]) - float(fdata[kk][3]),2))

                if odata[mm][3] == '서해':
                    if Diff_SST > WEST_RMSE_SST:
                        apply_SST = round(float(odata[mm][1]),2)
                        obj_SST = "obs"                        
                    else:
                        apply_SST = round(float(fdata[kk][3]),2)
                        obj_SST = "fcst"

                elif odata[mm][3] == '남해':
                    if Diff_SST > SOUTH_RMSE_SST:
                        apply_SST = round(float(odata[mm][1]),2)
                        obj_SST = "obs"                        
                    else:
                        apply_SST = round(float(fdata[kk][3]),2)
                        obj_SST = "fcst"
                        
                elif odata[mm][3] == '동해':
                    if Diff_SST > EAST_RMSE_SST:
                        apply_SST = round(float(odata[mm][1]),2)
                        obj_SST = "obs"                        
                    else:
                        apply_SST = round(float(fdata[kk][3]),2)
                        obj_SST = "fcst"

                apply_WHT = round(float(fdata[kk][7]),10)  
                obj_WHT = "fcst"

            apply1.append([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
            nn += 1
        mm += 1
    kk = kk + 1
#print(kk)
# 4일은 예측값----------------------------------------------------------------

#kk = int((SFEQ_LEN-1)*3/7)
while kk < int((SFEQ_LEN-1)*4/7):
	apply_SST = round(float(fdata[kk][3]),2)
	obj_SST = "fcst"
	apply_WHT = round(float(fdata[kk][7]),10)  
	obj_WHT = "fcst"
	apply1.append([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
	kk = kk + 1
#print(kk)	
# 5일은 예측값----------------------------------------------------------------

#kk = int((SFEQ_LEN-1)*4/7)
while kk < int((SFEQ_LEN-1)*5/7):
	apply_SST = round(float(fdata[kk][3]),2)
	obj_SST = "fcst"
	apply_WHT = round(float(fdata[kk][7]),10)  
	obj_WHT = "fcst"
	apply1.append([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
	kk = kk + 1
#print(kk)	
# 6일은 예측값----------------------------------------------------------------

#kk = int((SFEQ_LEN-1)*5/7)
while kk < int((SFEQ_LEN-1)*6/7):
	apply_SST = round(float(fdata[kk][3]),2)
	obj_SST = "fcst"
	apply_WHT = round(float(fdata[kk][7]),10)  
	obj_WHT = "fcst"
	apply1.append([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
	kk = kk + 1
#print(kk)	
# 7일은 예측값----------------------------------------------------------------

#kk = int((SFEQ_LEN-1)*6/7)
while kk < int(SFEQ_LEN-1):
	apply_SST = round(float(fdata[kk][3]),2)
	obj_SST = "fcst"
	apply_WHT = round(float(fdata[kk][7]),10)  
	obj_WHT = "fcst"
	apply1.append([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
	kk = kk + 1
#print(kk)	
#ii = 0
#while ii < len(apply1) : 
#	print(ii, apply1[ii])
#	ii = ii + 1

#print(len(apply1))
ii = 0
COM = []
while ii < len(apply1) :
	#print(ii,rawdata[ii][6],int(rawdata[ii][7]))
	TIDE_SCRE = IndexScore().tide_score(rawdata[ii][6],int(rawdata[ii][7]))
	WAVE_SCRE = IndexScore().wave_score(apply1[ii][5])
	SST_SCRE = IndexScore().sst_score(rawdata[ii][6],round(apply1[ii][3]))
	TEMP_SCRE = IndexScore().temp_score(int(rawdata[ii][15]))
	WIND_SCRE = IndexScore().wind_score(int(rawdata[ii][19]))
	WARN_SCRE = IndexScore().warn_score(rawdata[ii][20])
	TOTAL_SCRE1 = IndexScore().total_score(TIDE_SCRE, WAVE_SCRE, SST_SCRE, TEMP_SCRE, WIND_SCRE, WARN_SCRE)[0] # forecast score(no rain, no warning)
	TOTAL_SCRE2 = IndexScore().total_score(TIDE_SCRE, WAVE_SCRE, SST_SCRE, TEMP_SCRE, WIND_SCRE, WARN_SCRE)[1] # service score(rain, warning)
	QUOTIENT_SCRE1 = IndexScore().quotient_score(TOTAL_SCRE1) # forecast score(no rain, no warning)
	QUOTIENT_SCRE2 = IndexScore().quotient_score(TOTAL_SCRE2) # service score(rain, warning)

	MIN_WHT = round(float(apply1[ii][5])*float(fdata[ii][5])/float(fdata[ii][7]),1)
	AVE_WHT = round(float(apply1[ii][5])*float(fdata[ii][6])/float(fdata[ii][7]),1)
	MIN_SST = int(round(float(apply1[ii][3])*float(fdata[ii][2])/float(fdata[ii][3])))
	MAX_SST = int(round(float(apply1[ii][3])*float(fdata[ii][4])/float(fdata[ii][3])))
	

	COM.append([rawdata[ii][1],rawdata[ii][2],rawdata[ii][3],rawdata[ii][4],rawdata[ii][5],rawdata[ii][6],rawdata[ii][7],TIDE_SCRE,MIN_WHT,AVE_WHT,round(apply1[ii][5],1),WAVE_SCRE, MIN_SST,int(round(apply1[ii][3],0)),MAX_SST,SST_SCRE,rawdata[ii][14],rawdata[ii][15],rawdata[ii][16],TEMP_SCRE,rawdata[ii][17],rawdata[ii][18],rawdata[ii][19],WIND_SCRE,rawdata[ii][20],WARN_SCRE,TOTAL_SCRE2,QUOTIENT_SCRE2])
	ii = ii + 1


#ii = 0
#while ii < len(COM) : 
#	print(COM[ii])
#	ii = ii + 1


#OUT_FNAME = './Result/SFEQ_INDEX_SERVICE_modify_'+today+'.csv'
OUT_FNAME=dir1+'/SFEQ_INDEX_SERVICE_'+today+'.csv'
with open(OUT_FNAME,'w',encoding='utf8') as file:
	file.write('생산일,코드,권역,지역,예측일자,어종,어종타입,물때,물때점수,최소파고,평균파고,최대파고,파고점수,최소수온,평균수온,최대수온,수온점수,최저기온,평균기온,최대기온,기온점수,최소풍속,평균풍속,최대풍속,풍속점수,특보,특보점수,총점수,예보지수\n',)
	ii = 0
	ii = 0
	while ii <= len(COM)-1 :
		#[WEB_~~_SCRE Format]
		file.write(f'{today},{COM[ii][0]},{COM[ii][1]},{COM[ii][2]},{COM[ii][3]},{COM[ii][4]},{COM[ii][5]},{COM[ii][6]},{COM[ii][7]},{COM[ii][8]},{COM[ii][9]},{COM[ii][10]},{COM[ii][11]},{COM[ii][12]},{COM[ii][13]},{COM[ii][14]},{COM[ii][15]},{COM[ii][16]},{COM[ii][17]},{COM[ii][18]},{COM[ii][19]},{COM[ii][20]},{COM[ii][21]},{COM[ii][22]},{COM[ii][23]},{COM[ii][24]},{COM[ii][25]},{COM[ii][26]:4.2f},{COM[ii][27]}\n')
		ii = ii + 1

print("#SFEQ SERVICE_INDEX CREAT Complete==========")
