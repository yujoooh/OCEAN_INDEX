#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.04.11] edit 19.08.22
import sys
import os
#os.path.join(os.getcwd(),"Function")
import numpy as np
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime
from Function.skeq_function import IndexScore
from Function.statistic_function import Statistic

print("#SKEQ SERVICE_INDEX CREAT Start==========")

#[Date set] ==============================================================================================
#[Auto date set]
today = str(datetime.today().strftime('%Y%m%d'))
afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')
afterday4 = (date.today() + timedelta(4)).strftime('%Y%m%d')
afterday5 = (date.today() + timedelta(5)).strftime('%Y%m%d')
afterday6 = (date.today() + timedelta(6)).strftime('%Y%m%d')

#[Manual date set]
#today = str(date(2019,10,18).strftime('%Y%m%d'))
#afterday1 = (date(2019,10,18) + timedelta(1)).strftime('%Y%m%d')
#afterday2 = (date(2019,10,18) + timedelta(2)).strftime('%Y%m%d')
#print(today, afterday1, afterday2)

dir1 = './Result/'+today

mon = date.today().month  # 자료 생산일 기준 월 구분
hr = float(datetime.today().strftime("%H"))
#print(hr)

#산출된 예보지수자료 읽기-------------------------------------------------------------------------
SKEQ_INF = open(dir1+'/SKEQ_INDEX_SERVICE_'+today+'.csv',encoding='utf8')
SKEQ = [LST for LST in SKEQ_INF.read().split()]
SKEQ_LEN = len(SKEQ)

fdata = []
rawdata = []
ii = 1
while ii < SKEQ_LEN:
	DEV = SKEQ[ii].split(',')
	Code = DEV[0]; Route = DEV[1] ; Point = DEV[2] ; SHIP_Type = DEV[3] ; FDATE = DEV[4] ; FAMPM = DEV[5]
	SAIL_HR = DEV[6] ; Ton = DEV[8] ; MIN_WHT = DEV[10] ; AVE_WHT = DEV[11] ; MAX_WHT = DEV[12]
	MIN_WIND = DEV[14] ; AVE_WIND = DEV[15] ; MAX_WIND = DEV[16] ; WARN = DEV[18]
	fdata.append([Route,FDATE,FAMPM,MIN_WHT, AVE_WHT, MAX_WHT])
	rawdata.append([ii,Code,Route,Point, SHIP_Type, FDATE, FAMPM, SAIL_HR, Ton,MIN_WHT, AVE_WHT, MAX_WHT, MIN_WIND, AVE_WIND, MAX_WIND, WARN]) 
	ii += 1
#print(fdata)

# 수집된 관측자료 읽기-------------------------------------------------------------------------
odata1 = []
odata2 = []
if hr < 12: # 오전자료 읽기
	AM_DATA = open(dir1+'/SK_POINT_OBS_AM.csv','r',encoding='utf8')
	AM = [LST for LST in AM_DATA.read().split()]
	AM_LEN = len(AM)
	check = 'am'

	ii = 0
	while ii < AM_LEN:
		DEV = AM[ii].split(',')
		#print(DEV)
		odata1.append(DEV)
		ii = ii + 1

else: # 오전/오후자료 읽기-------
	AM_DATA = open(dir1+'/SK_POINT_OBS_AM.csv','r',encoding='utf8')
	AM = [LST for LST in AM_DATA.read().split()]
	AM_LEN = len(AM)
	check = 'am'
	PM_DATA = open(dir1+'/SK_POINT_OBS_PM.csv','r',encoding='utf8')
	PM = [LST for LST in PM_DATA.read().split()]
	PM_LEN = len(PM)
	check = 'pm'

	ii = 0
	while ii < AM_LEN:
		DEV = AM[ii].split(',')
		DEV2 = PM[ii].split(',')
		odata1.append(DEV)
		odata2.append(DEV2)
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

# 예측자료/관측자료 비교하기---------------------------------------------------------------------
kk = 0
apply1 = []
while kk < int((SKEQ_LEN-1)*4/10):
	mm = 0
	ll = 0
	while mm < AM_LEN:
		#print(fdata[kk][0],odata1[mm][0])
		if fdata[kk][0] == odata1[mm][0]:# 예보지역과 관측지역 일치여부
			Diff_Point = fdata[kk][0]
			# 1일은 그냥 관측자료로 넣기----------------------------------------------------------------
			if hr < 12: # 오전자료 읽기
				#print(fdata[kk][1], today, fdata[kk][2], "AM")
				if fdata[kk][1] == today and fdata[kk][2] == "AM":   
					if odata1[mm][2] == '-999.0':
						apply_WHT = round(float(fdata[kk][5]),2)
						obj_WHT = "fcst"
					else:
						apply_WHT = round(float(odata1[mm][2]),2)                    
						obj_WHT = "obs"
			else:
				if fdata[kk][1] == today and fdata[kk][2] == "AM":                
					if odata1[mm][2] == '-999.0':
						apply_WHT = round(float(fdata[kk][5]),2)
						obj_WHT = "fcst"
					else:
						apply_WHT = round(float(odata1[mm][2]),2)                    
						obj_WHT = "obs"
				if fdata[kk][1] == today and fdata[kk][2] == "PM":                
					if odata2[ll][2] == '-999.0':
						apply_WHT = round(float(fdata[kk][5]),2)
						obj_WHT = "fcst"
					else:
						apply_WHT = round(float(odata2[ll][2]),2)                    
						obj_WHT = "obs"
			# 2일은 예측값과 비교 후 벗어나면 관측자료로 대체----------------------------------------------------------------
			if fdata[kk][1]== afterday1:
				apply_WHT = round(float(fdata[kk][5]),2)
				obj_WHT = "fcst"
	
			apply1.append([Diff_Point,fdata[kk][1],obj_WHT,apply_WHT])
			#print(Diff_Point, fdata[kk][1], apply_WHT)
		ll += 1
		mm += 1
	kk = kk + 1


# 3일은 2일 변경값과 비교 후 벗어나면 관측자료로 대체----------------------------------------------------------------
while kk < int((SKEQ_LEN-1)*6/10):
    mm = 0
    while mm < AM_LEN:
        if odata1[mm][0] == fdata[kk][0]:# 예보지역과 관측지역 일치여부
            Diff_Point = fdata[kk][0]
             # 3일--------------------------------------------------------------------------
            apply_WHT = round(float(fdata[kk][5]),2)
            obj_WHT = "fcst"
            apply1.append([Diff_Point,fdata[kk][1],obj_WHT,apply_WHT])
        mm += 1
    kk = kk + 1
# 4일은 3일 변경값과 비교 후 벗어나면 관측자료로 대체----------------------------------------------------------------
while kk < int((SKEQ_LEN-1)*7/10):
    mm = 0
    while mm < AM_LEN:
        if odata1[mm][0] == fdata[kk][0]:# 예보지역과 관측지역 일치여부
            Diff_Point = fdata[kk][0]
             # 3일--------------------------------------------------------------------------
            apply_WHT = round(float(fdata[kk][5]),2)
            obj_WHT = "fcst"
            apply1.append([Diff_Point,fdata[kk][1],obj_WHT,apply_WHT])
        mm += 1
    kk = kk + 1
# 5일은 4일 변경값과 비교 후 벗어나면 관측자료로 대체----------------------------------------------------------------
while kk < int((SKEQ_LEN-1)*8/10):
    mm = 0
    while mm < AM_LEN:
        if odata1[mm][0] == fdata[kk][0]:# 예보지역과 관측지역 일치여부
            Diff_Point = fdata[kk][0]
             # 3일--------------------------------------------------------------------------
            apply_WHT = round(float(fdata[kk][5]),2)
            obj_WHT = "fcst"
            apply1.append([Diff_Point,fdata[kk][1],obj_WHT,apply_WHT])
        mm += 1
    kk = kk + 1
# 6일은 5일 변경값과 비교 후 벗어나면 관측자료로 대체----------------------------------------------------------------
while kk < int((SKEQ_LEN-1)*9/10):
    mm = 0
    while mm < AM_LEN:
        if odata1[mm][0] == fdata[kk][0]:# 예보지역과 관측지역 일치여부
            Diff_Point = fdata[kk][0]
             # 3일--------------------------------------------------------------------------
            apply_WHT = round(float(fdata[kk][5]),2)
            obj_WHT = "fcst"
            apply1.append([Diff_Point,fdata[kk][1],obj_WHT,apply_WHT])
        mm += 1
    kk = kk + 1
# 7일은 6일 변경값과 비교 후 벗어나면 관측자료로 대체----------------------------------------------------------------
while kk < int(SKEQ_LEN-1):
    mm = 0
    while mm < AM_LEN:
        if odata1[mm][0] == fdata[kk][0]:# 예보지역과 관측지역 일치여부
            Diff_Point = fdata[kk][0]
             # 3일--------------------------------------------------------------------------
            apply_WHT = round(float(fdata[kk][5]),2)
            obj_WHT = "fcst"
            apply1.append([Diff_Point,fdata[kk][1],obj_WHT,apply_WHT])
        mm += 1
    kk = kk + 1    

#ii = 0
#while ii < len(apply1) : 
#	print(apply1[ii])
#	ii = ii + 1

ii = 0
COM = []
while ii <= len(apply1)-1 :
	MAX_WHT = float(apply1[ii][3])
	MIN_WHT = round(float(apply1[ii][3])*float(fdata[ii][3])/float(fdata[ii][5]),1)
	AVE_WHT = round(float(apply1[ii][3])*float(fdata[ii][4])/float(fdata[ii][5]),1)
#	if MIN_WHT == MAX_WHT :
#		MAX_WHT = MAX_WHT + 0.1
#	if round(float(MIN_WHT),1) < 0.1 :
#		MIN_WHT = 0.1
	SAIL_SCRE = IndexScore().sail_score(float(rawdata[ii][7]))
	TON_SCRE = IndexScore().ton_score(float(rawdata[ii][8]))
	WIND_SCRE = IndexScore().wind_score(float(rawdata[ii][14]))
	WAVE_SCRE = IndexScore().wave_score(float(apply1[ii][3]))
	WARN_SCRE = IndexScore().warn_score(rawdata[ii][15])
	TOTAL_SCRE1 = IndexScore().total_score(SAIL_SCRE, TON_SCRE, WIND_SCRE, WAVE_SCRE, WARN_SCRE)[0] # forecast score(no rain, no warning)
	TOTAL_SCRE2 = IndexScore().total_score(SAIL_SCRE, TON_SCRE, WIND_SCRE, WAVE_SCRE, WARN_SCRE)[1] # service score(rain, warning)
	QUOTIENT_SCRE1 = IndexScore().quotient_score(TOTAL_SCRE1)
	QUOTIENT_SCRE2 = IndexScore().quotient_score(TOTAL_SCRE2)

#	print(MIN_WHT, AVE_WHT, apply1[ii][3])

	#'코드,항로명,선박명,선박종류,예측일자,시간,운항시간,운항시간점수,선박톤수,선박톤수점수,최소파고,평균파고,최대파고,파고점수,최소풍속,평균풍속,최대풍속,풍속점수,총점수,예보지수\n'
	COM.append([rawdata[ii][1],rawdata[ii][2],rawdata[ii][3],rawdata[ii][4],rawdata[ii][5],rawdata[ii][6],rawdata[ii][7],SAIL_SCRE,rawdata[ii][8],TON_SCRE,MIN_WHT, AVE_WHT,MAX_WHT, WAVE_SCRE,rawdata[ii][12],rawdata[ii][13],rawdata[ii][14],WIND_SCRE,rawdata[ii][15],WARN_SCRE,round(TOTAL_SCRE2,2),QUOTIENT_SCRE2])
	ii = ii + 1

#ii = 0
#while ii < len(COM) : 
#	print(COM[ii])
#	ii = ii + 1
#	
#print(len(COM))


#OUT_FNAME = './Result/SKEQ_INDEX_SERVICE_modify_'+today+'.csv'
OUT_FNAME=dir1+'/SKEQ_INDEX_SERVICE_'+today+'.csv'
with open(OUT_FNAME,'w',encoding='utf8') as file:
	file.write('생산일,코드,항로명,선박명,선박종류,예측일자,시간,운항시간,운항시간점수,선박톤수,선박톤수점수,최소파고,평균파고,최대파고,파고점수,최소풍속,평균풍속,최대풍속,풍속점수,특보,특보점수,총점수,예보지수\n',)
	ii = 0
	while ii < len(COM) :
		#[전체 데이터 Writing]
		file.write(f'{today},{COM[ii][0]},{COM[ii][1]},{COM[ii][2]},{COM[ii][3]},{COM[ii][4]},{COM[ii][5]},{COM[ii][6]},{COM[ii][7]},{COM[ii][8]},{COM[ii][9]},{COM[ii][10]},{COM[ii][11]},{COM[ii][12]},{COM[ii][13]},{COM[ii][14]},{COM[ii][15]},{COM[ii][16]},{COM[ii][17]},{COM[ii][18]},{COM[ii][19]},{COM[ii][20]},{COM[ii][21]}\n')
		ii = ii + 1

print("#SKEQ SERVICE_INDEX CREAT Complete==========")
