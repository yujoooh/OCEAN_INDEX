#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.04.11] edit 19.08.22
import sys
import os
import numpy as np
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime
from Function.sseq_function import IndexScore, Tide_time_lunar
from Function.statistic_function import Statistic

print("#SSEQ SERVICE_INDEX CREAT Start==========")

#[Date set] ==============================================================================================
#[Auto date set]
today = str(datetime.today().strftime('%Y%m%d'))
afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')
afterday3 = (date.today() + timedelta(3)).strftime('%Y%m%d')
afterday4 = (date.today() + timedelta(4)).strftime('%Y%m%d')
afterday5 = (date.today() + timedelta(5)).strftime('%Y%m%d')
afterday6 = (date.today() + timedelta(6)).strftime('%Y%m%d')

#[Manual date set]
#today = str(date(2019,10,18).strftime('%Y%m%d'))
#afterday1 = (date(2019,10,18) + timedelta(1)).strftime('%Y%m%d')
#afterday2 = (date(2019,10,18) + timedelta(2)).strftime('%Y%m%d')

dir1 = './Result/'+today

mon = date.today().month  # 자료 생산일 기준 월 구분
hr = float(datetime.today().strftime("%H"))
# hr = 10    # 오전 자료만 뽑을시 시간 고정

#산출된 예보지수자료 읽기-------------------------------------------------------------------------
SSEQ_INF = open(dir1+'/SSEQ_INDEX_SERVICE_'+today+'.csv',encoding='utf8')
SSEQ = [LST for LST in SSEQ_INF.read().split()]
SSEQ_LEN = len(SSEQ)

fdata = []
rawdata = []
ii = 1
while ii <= SSEQ_LEN-1 :
	DEV = SSEQ[ii].split(',')
	Code = DEV[0]; Area = DEV[1] ; Point = DEV[2] ; FDATE = DEV[3] ; FAMPM = DEV[4] ; MUL = DEV[5]
	MIN_WHT = DEV[7] ; AVE_WHT = DEV[8] ; MAX_WHT = DEV[9]
	MIN_CURRENT = DEV[11] ; AVE_CURRENT = DEV[12] ; MAX_CURRENT = DEV[13]
	MIN_SST = DEV[15] ; AVE_SST = DEV[16] ; MAX_SST = DEV[17]
	WARN = DEV[19]

#                       0       1    2       3       4       5       6           7        8
	fdata.append([Point,FDATE, FAMPM, MIN_SST, AVE_SST, MAX_SST, MIN_WHT, AVE_WHT, MAX_WHT])
	rawdata.append([ii,Code,Area,Point, FDATE, FAMPM, MUL, MIN_WHT, AVE_WHT, MAX_WHT, MIN_CURRENT, AVE_CURRENT, MAX_CURRENT, MIN_SST, AVE_SST, MAX_SST, WARN])
	ii = ii + 1
	
#ii = 0
#while ii <= len(rawdata)-1:
#	print(ii,rawdata[ii])
#	ii = ii + 1

# 수집된 관측자료 읽기-------------------------------------------------------------------------
odata1 = []
odata2 = []
if hr < 12: # 오전자료 읽기
	AM_DATA = open(dir1+'/SS_POINT_OBS_AM.csv','r',encoding='utf8')
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
	AM_DATA = open(dir1+'/SS_POINT_OBS_AM.csv','r',encoding='utf8')
	AM = [LST for LST in AM_DATA.read().split()]
	AM_LEN = len(AM)
	check = 'am'
	PM_DATA = open(dir1+'/SS_POINT_OBS_PM.csv','r',encoding='utf8')
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
while kk < int((SSEQ_LEN-1)*2/10):
	mm = 0
	ll = 0
	while mm < AM_LEN:
		if odata1[mm][0] == fdata[kk][0]:# 예보지역과 관측지역 일치여부
			#print(fdata[kk][0], odata[mm][0])
			Diff_Point = fdata[kk][0]
			# 1일은 그냥 관측자료로 넣기----------------------------------------------------------------
			if hr < 12 :
				if fdata[kk][1] == today and fdata[kk][2] == 'AM' :
					if odata1[mm][1] == '-999.0':                
						apply_SST = float(fdata[kk][4])
						obj_SST = "fcst"
					else:
						apply_SST = round(float(odata1[mm][1]),2)
						obj_SST = "obs"
					if odata1[mm][2] == '-999.0' :
						apply_WHT = float(fdata[kk][8])
						obj_WHT = "fcst"
					else:
						apply_WHT = round(float(odata1[mm][2]),2)                    
						obj_WHT = "obs"
				elif fdata[kk][1] == today and fdata[kk][2] =="PM":
					if obj_SST == "obs" :
						apply_SST = round(float(odata1[mm][1]),2)
						obj_SST = "obs"
					elif obj_SST == "fcst" :
						apply_SST = float(fdata[kk][4])
						obj_SST = "fcst"
				
					if obj_WHT == "obs":
						apply_WHT = round(float(odata1[mm][2]),2)
						obj_WHT = "obs"
					elif obj_WHT == "fcst":
						apply_WHT = float(fdata[kk][8])
						obj_WHT = "fcst"
				apply1.append([Diff_Point,fdata[kk][1],obj_SST, apply_SST, obj_WHT,apply_WHT])  
				
			else:
				if fdata[kk][1] == today and fdata[kk][2] == "AM":                
					if odata1[mm][1] == '-999.0':
						apply_SST = float(fdata[kk][4])
						obj_SST = "fcst"
					else:
						apply_SST = round(float(odata1[mm][1]),2)                    
						obj_SST = "obs"
					if odata1[mm][2] == '-999.0':
						apply_WHT = float(fdata[kk][8])
						obj_WHT = "fcst"
					else:
						apply_WHT = round(float(odata1[mm][2]),2)                    
						obj_WHT = "obs"
				elif fdata[kk][1] == today and fdata[kk][2] == "PM":
					if obj_SST == "fcst" : 
						apply_SST = float(fdata[kk][4])
						obj_SST = "fcst"
					elif obj_SST == "obs" and odata2[ll][1] != '-999.0':
						apply_SST = round(float(odata2[ll][1]),2)                    
						obj_SST = "obs"
					elif obj_SST == "obs" and odata2[ll][1] == '-999.0':
						apply_SST = round(float(odata1[ll][1]),2)                    
						obj_SST = "obs"
			
			
					if obj_WHT == "fcst" : 
						apply_WHT = float(fdata[kk][8])
						obj_WHT = "fcst"
					elif obj_WHT == "obs" and odata2[ll][2] != '-999.0':
						apply_WHT = round(float(odata2[ll][2]),2)                    
						obj_WHT = "obs"					
					elif obj_WHT == "obs" and odata2[ll][2] == '-999.0':
						apply_WHT = round(float(odata1[ll][2]),2)
						obj_WHT = "obs"
				apply1.append([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
		ll += 1
		mm += 1
	kk = kk + 1
while kk < int((SSEQ_LEN-1)*4/10):
	mm = 0
	ll = 0
	while mm < AM_LEN:
		if fdata[kk][0] == odata1[mm][0]:# 예보지역과 관측지역 일치여부
			Diff_Point = fdata[kk][0]
			# 2일은 예측값과 비교 후 벗어나면 관측자료로 대체----------------------------------------------------------------
			if hr < 12 :
				if fdata[kk][1]== afterday1 and fdata[kk][2] == 'AM' :
					if odata1[mm][1] == '-999.0' : # Missing value면 차이 0으로 설정
						Diff_SST = 0
					else:
						Diff_SST = abs(round(float(fdata[kk][4]) - float(odata1[mm][1]),2))
	
				#해역별 RMSE 비교  : apply_는 적용할 자료------------------------------------
					if odata1[mm][3] == '서해':
						if Diff_SST > WEST_RMSE_SST:
							apply_SST = round(float(odata1[mm][1]),2)
							obj_SST = "obs"
						else:
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
	
					elif odata1[mm][3] == '남해':
						if Diff_SST > SOUTH_RMSE_SST:
							apply_SST = round(float(odata1[mm][1]),2)
							obj_SST = "obs"
						else:
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
	
					elif odata1[mm][3] == '동해':
						if Diff_SST > EAST_RMSE_SST:
							apply_SST = round(float(odata1[mm][1]),2)
							obj_SST = "obs"
						else:
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
						
					else:#한반도 RMSE
						if Diff_SST > KOR_RMSE_SST:
							apply_SST = round(float(odata1[mm][1]),2)
						else:
							apply_SST = float(fdata[kk][4])
	
					apply_WHT = float(fdata[kk][8])
					obj_WHT = "fcst"
				elif fdata[kk][1]== afterday1 and fdata[kk][2] == 'PM' :
					if obj_SST == "fcst" :
						apply_SST = float(fdata[kk][4])
						obj_SST = "fcst"
					elif obj_SST == "obs" :
						apply_SST = round(float(odata1[mm][1]),2)
						obj_SST = "obs"
				apply_WHT = float(fdata[kk][8])
				obj_WHT = "fcst"	
				apply1.append([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
				#print(kk,Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT)

			else:
				if fdata[kk][1]== afterday1 and fdata[kk][2] == "AM":
					#print(fdata[kk][1],afterday1)
					if odata1[mm][1] == '-999.0':
						Diff_SST = 0
					else:
						Diff_SST = abs(round(float(fdata[kk][4]) - float(odata1[mm][1]),2))
	
					#해역별 RMSE 비교  : apply_는 적용할 자료------------------------------------
					if odata1[mm][3] == '서해':
						if Diff_SST > WEST_RMSE_SST:
							apply_SST = round(float(odata1[mm][1]),2)
							obj_SST = "obs"
						else:
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
	
					elif odata1[mm][3] == '남해':
						if Diff_SST > SOUTH_RMSE_SST:
							apply_SST = round(float(odata1[mm][1]),2)
							obj_SST = "obs"
						else:
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
	
					elif odata1[mm][3] == '동해':
						if Diff_SST > EAST_RMSE_SST:
							apply_SST = round(float(odata1[mm][1]),2)
							obj_SST = "obs"
						else:
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
	
				elif fdata[kk][1]== afterday1 and fdata[kk][2] == "PM":
					if odata2[ll][1] == '-999.0':
						Diff_SST = 0
					else:
						Diff_SST = abs(round(float(fdata[kk][4]) - float(odata2[ll][1]),2))
	
					#해역별 RMSE 비교  : apply_는 적용할 자료------------------------------------
					if odata2[ll][3] == '서해':
						if obj_SST == "fcst" :
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
						elif obj_SST == "obs" : 
							if Diff_SST > WEST_RMSE_SST:
								apply_SST =round(float(odata2[ll][1]),2)
								obj_SST = "obs"
							else :
								apply_SST =round(float(odata1[ll][1]),2)
								obj_SST = "obs"
	
					elif odata2[ll][3] == '남해':
						if obj_SST == "fcst" :
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
						elif obj_SST == "obs" : 
							if Diff_SST > SOUTH_RMSE_SST:
								apply_SST = round(float(odata2[ll][1]),2)
								obj_SST = "obs"
							else :
								apply_SST =round(float(odata1[ll][1]),2)
								obj_SST = "obs"
	
					elif odata2[ll][3] == '동해':
						if obj_SST == "fcst" :
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
						elif obj_SST == "obs" : 
							if Diff_SST > EAST_RMSE_SST:
								apply_SST = round(float(odata2[ll][1]),2)
								obj_SST = "obs"
							else :
								apply_SST =round(float(odata1[ll][1]),2)
								obj_SST = "obs"
	
				apply_WHT = float(fdata[kk][8])
				obj_WHT = "fcst"
				#print([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
				apply1.append([Diff_Point,fdata[kk][1],obj_SST, apply_SST, obj_WHT,apply_WHT])
				#print(Diff_Point, fdata[kk][1], diff_SST, apply_WHT)
		ll += 1
		mm += 1
	kk = kk + 1
# 3일은 2일 변경값과 비교 후 벗어나면 관측자료로 대체----------------------------------------------------------------
nn = int((SSEQ_LEN-1)*2/10)
while kk < int((SSEQ_LEN-1)*6/10):
	mm = 0
	ll = 0
	while mm < AM_LEN:
		if fdata[kk][0] == odata1[mm][0] and fdata[kk][1] == afterday2:# 예보지역과 관측지역 일치여부
			Diff_Point = odata1[mm][0]
             		# 3일--------------------------------------------------------------------------
			if hr < 12:
				if fdata[kk][1] == afterday2 and apply1[nn][1] == afterday1 and fdata[kk][2] == "AM":
					if odata1[mm][1] == '-999.0':
						Diff_SST = 0
						obj_SST = "fcst"                        
					else:
						Diff_SST = abs(round(float(apply1[nn][3]) - float(fdata[kk][4]),2))
					#print(apply1[nn][3], fdata[kk][4], Diff_SST)
						
					if odata1[mm][3] == '서해':
						if Diff_SST > WEST_RMSE_SST:
							apply_SST = round(float(odata1[mm][1]),2)
							obj_SST = "obs"
						else:
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
	
					elif odata1[mm][3] == '남해':
						if Diff_SST > SOUTH_RMSE_SST:
							apply_SST = round(float(odata1[mm][1]),2)
							obj_SST = "obs"
						else:
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
						
					elif odata1[mm][3] == '동해':
						if Diff_SST > EAST_RMSE_SST:
							apply_SST = round(float(odata1[mm][1]),2)
							obj_SST = "obs"
						else:
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
					apply_WHT = float(fdata[kk][8])
					obj_WHT = "fcst"
				elif fdata[kk][1] == afterday2 and apply1[nn][1] == afterday1 and fdata[kk][2] == "PM":
					if obj_SST == "fcst" :
						apply_SST = float(fdata[kk][4])
						obj_SST = "fcst"
					elif obj_SST =="obs" :
						apply_SST = round(float(odata1[mm][1]),2)
						obj_SST = "obs"
	
				apply_WHT = float(fdata[kk][8])
				obj_WHT = "fcst"
	
				apply1.append([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
				#print([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])								
				
	
			else:
				if fdata[kk][1] == afterday2 and apply1[nn][1] == afterday1 and fdata[kk][2] == "AM":
					if odata1[mm][1] == '-999.0':
						Diff_SST = 0
					else:
						Diff_SST = abs(round(float(apply1[nn][3]) - float(fdata[kk][4]),2))
					#print(apply1[nn][3], fdata[kk][4], Diff_SST)												
	
					if odata1[mm][3] == '서해':
						if Diff_SST > WEST_RMSE_SST:
							apply_SST = round(float(odata1[mm][1]),2)
							obj_SST = "obs"
						else:
							apply_SST = round(float(fdata[kk][4]),2)
							obj_SST = "fcst"
	
					elif odata1[mm][3] == '남해':
						if Diff_SST > SOUTH_RMSE_SST:
							apply_SST = round(float(odata1[mm][1]),2)
							obj_SST = "obs"
						else:
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
						
					elif odata1[mm][3] == '동해':
						if Diff_SST > EAST_RMSE_SST:
							apply_SST = round(float(odata1[mm][1]),2)
							obj_SST = "obs"
						else:
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
					
			
				if fdata[kk][1] == afterday2 and apply1[nn][1] == afterday1 and fdata[kk][2] == "PM":                
					if odata2[ll][1] == '-999.0':
						Diff_SST = 0                   
					else:
						Diff_SST = abs(round(float(apply1[nn][3]) - float(fdata[kk][4]),2))
					#print(apply1[nn][3], fdata[kk][4], Diff_SST)												
	
					#해역별 RMSE 비교  : apply_는 적용할 자료------------------------------------
					if odata2[ll][3] == '서해':
						if obj_SST == "fcst" :
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
						elif obj_SST == "obs" : 
							if Diff_SST > WEST_RMSE_SST:
								apply_SST =round(float(odata2[ll][1]),2)
								obj_SST = "obs"
							else :
								apply_SST =round(float(odata1[ll][1]),2)
								obj_SST = "obs"
	
					elif odata2[ll][3] == '남해':
						if obj_SST == "fcst" :
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
						elif obj_SST == "obs" : 
							if Diff_SST > SOUTH_RMSE_SST:
								apply_SST = round(float(odata2[ll][1]),2)
								obj_SST = "obs"
							else :
								apply_SST =round(float(odata1[ll][1]),2)
								obj_SST = "obs"
	
					elif odata2[ll][3] == '동해':
						if obj_SST == "fcst" :
							apply_SST = float(fdata[kk][4])
							obj_SST = "fcst"
						elif obj_SST == "obs" : 
							if Diff_SST > EAST_RMSE_SST:
								apply_SST = round(float(odata2[ll][1]),2)
								obj_SST = "obs"
							else :
								apply_SST =round(float(odata1[ll][1]),2)
								obj_SST = "obs"
	
				apply_WHT = float(fdata[kk][8])
				obj_WHT = "fcst"
				apply1.append([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
				#print([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])				
			nn += 1
		ll += 1
		#if Diff_Point == apply1[nn][0] :
		#	nn += 1
		mm += 1
	kk = kk + 1
#print(kk)
# 4일은 예측값----------------------------------------------------------------

while kk < int((SSEQ_LEN-1)*7/10):
	apply_SST = float(fdata[kk][4])
	obj_SST = "fcst"
	apply_WHT = float(fdata[kk][8])
	obj_WHT = "fcst"
	apply1.append([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
	kk = kk + 1
#print(kk)
# 5일은 예측값----------------------------------------------------------------

while kk < int((SSEQ_LEN-1)*8/10):
	apply_SST = float(fdata[kk][4])
	obj_SST = "fcst"
	apply_WHT = float(fdata[kk][8])
	obj_WHT = "fcst"
	apply1.append([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
	kk = kk + 1
#print(kk)
# 6일은 예측값----------------------------------------------------------------

while kk < int((SSEQ_LEN-1)*9/10):
	apply_SST = float(fdata[kk][4])
	obj_SST = "fcst"
	apply_WHT = float(fdata[kk][8])
	obj_WHT = "fcst"
	apply1.append([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
	kk = kk + 1
#print(kk)
# 7일은 예측값----------------------------------------------------------------

while kk < int(SSEQ_LEN-1):
	apply_SST = float(fdata[kk][4])
	obj_SST = "fcst"
	apply_WHT = float(fdata[kk][8])
	obj_WHT = "fcst"
	apply1.append([Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT])
	kk = kk + 1
#print(kk)

#print(len(apply1))
#ii = 0
#while ii < len(apply1) : 
#	print(ii, apply1[ii])
#	ii = ii + 1

#[Index Score Calculate] ========================================================================================
ii = 0
COM = []
while ii <= len(apply1)-1 :
	MAX_WHT = round(apply1[ii][5],1)
	AVE_SST = round(apply1[ii][3],1)
	MAX_CURRENT = round(float(rawdata[ii][12]),1); MIN_CURRENT = round(float(rawdata[ii][10]),1); AVE_CURRENT = round(float(rawdata[ii][11]),1)
	MIN_WHT = round(float(apply1[ii][5])*float(fdata[ii][6])/float(fdata[ii][8]),1)
	AVE_WHT = round(float(apply1[ii][5])*float(fdata[ii][7])/float(fdata[ii][8]),1)
	MIN_SST = round(float(apply1[ii][3])*float(fdata[ii][3])/float(fdata[ii][4]),1)
	MAX_SST = round(float(apply1[ii][3])*float(fdata[ii][5])/float(fdata[ii][4]),1)
#	if MIN_WHT == MAX_WHT :
#		MAX_WHT = MAX_WHT + 0.1
#	if MIN_CURRENT == MAX_CURRENT :
#		MAX_CURRENT = MAX_CURRENT + 0.1	
	
	TIDE_SCRE = IndexScore().tide_score(int(rawdata[ii][6]))
	WAVE_SCRE = IndexScore().wave_score(apply1[ii][5])
	CURRENT_SCRE = IndexScore().current_score(float(rawdata[ii][12]))
	SST_SCRE = IndexScore().sst_score(float(apply1[ii][3]))
	WARN_SCRE = IndexScore().warn_score(rawdata[ii][16])
	TOTAL_SCRE1 = IndexScore().total_score(TIDE_SCRE, WAVE_SCRE, CURRENT_SCRE, SST_SCRE, WARN_SCRE)[0] # forecast score(no rain, no warning)
	TOTAL_SCRE2 = IndexScore().total_score(TIDE_SCRE, WAVE_SCRE, CURRENT_SCRE, SST_SCRE, WARN_SCRE)[1] # service score(rain, warning)
	QUOTIENT_SCRE1 = IndexScore().quotient_score(TOTAL_SCRE1) # forecast score(no rain, no warning)
	QUOTIENT_SCRE2 = IndexScore().quotient_score(TOTAL_SCRE2) # service score(rain, warning)

	COM.append([rawdata[ii][1],rawdata[ii][2],rawdata[ii][3],rawdata[ii][4],rawdata[ii][5],rawdata[ii][6],TIDE_SCRE,MIN_WHT,AVE_WHT,MAX_WHT,WAVE_SCRE, MIN_CURRENT,AVE_CURRENT,MAX_CURRENT,CURRENT_SCRE,MIN_SST,round(apply1[ii][3],1),MAX_SST,SST_SCRE,rawdata[ii][16],WARN_SCRE,TOTAL_SCRE2,QUOTIENT_SCRE2])
	ii = ii + 1

#ii = 0
#while ii <= len(COM)-1:
#	print(COM[ii])
#	ii = ii + 1

#[Output Data] ========================================================================================
#OUT_FNAME = './Result/SSEQ_INDEX_SERVICE_modify_'+today+'.csv'
OUT_FNAME=dir1+'/SSEQ_INDEX_SERVICE_'+today+'.csv'
with open(OUT_FNAME,'w',encoding='utf8') as file:
	file.write('생산일,코드,권역,지역,예측일자,시간,물때,물때점수,최소파고,평균파고,최대파고,파고점수,최소유속,평균유속,최대유속,유속점수,최소수온,평균수온,최대수온,수온점수,특보,특보점수,총점수,예보지수\n',)
	ii = 0
	while ii <= len(COM)-1 :
		#[WEB_~~_SCRE Format]
		file.write(f'{today},{COM[ii][0]},{COM[ii][1]},{COM[ii][2]},{COM[ii][3]},{COM[ii][4]},{COM[ii][5]},{COM[ii][6]},{COM[ii][7]},{COM[ii][8]},{COM[ii][9]},{COM[ii][10]},{COM[ii][11]},{COM[ii][12]},{COM[ii][13]},{COM[ii][14]},{COM[ii][15]},{COM[ii][16]},{COM[ii][17]},{COM[ii][18]},{COM[ii][19]},{COM[ii][20]},{COM[ii][21]:4.2f},{COM[ii][22]}\n')
		ii = ii + 1

print("#SSEQ SERVICE_INDEX CREAT Complete==========")
