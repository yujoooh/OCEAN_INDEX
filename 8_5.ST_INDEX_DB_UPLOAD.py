#[Geosystem Research : Department of Coastal Management]
#[Created by HGCHOE]
#[EDIT C.K. Park on 2019.11.07]

import cx_Oracle
import os
from pprint import pprint
import sys
from datetime import date, timedelta
from datetime import datetime

os.putenv('NLS_LANG', '.UTF8') # 한글 깨질 때 사용 ㅎㅎ

print("#INDEX result DB upload Start ========")

#[Date Set]==================================================================================================
today = str(datetime.today().strftime('%Y%m%d'))
afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')

#today = str(date(2019,11,7).strftime('%Y%m%d'))
#afterday1 = (date(2019,11,7) + timedelta(1)).strftime('%Y%m%d')
#afterday2 = (date(2019,11,7) + timedelta(2)).strftime('%Y%m%d')

dir1 ='./Result/'+today

#[DB connect inforamtion]================================================================
#[MDCDB]
#DBID = 'ocean_web'
#DBPWD = 'infoshfl03'
#DBINFO = '192.168.200.16:1521/mgis'

#[OCEAN_DB]
DBID = 'ocean'
DBPWD = 'ocean'
DBINFO = '10.27.90.17:1521/mgis'

#[INFO FILE NAME READ]===================================================================
fname1 = dir1+'/ST_INDEX_FCST_BUSAN_'+today+'.csv'
file1 = open(fname1, 'r', encoding='utf8')
content1 = [ str(INFO) for INFO in file1.read().split()]

fname2 = dir1+'/ST_INDEX_FCST_JEJU_'+today+'.csv'
file2 = open(fname2, 'r', encoding='utf8')
content2 = [ str(INFO) for INFO in file2.read().split()]

fname3 = dir1+'/ST_INDEX_FCST_YEOSU_'+today+'.csv'
file3 = open(fname3, 'r', encoding='utf8')
content3 = [ str(INFO) for INFO in file3.read().split()]

con = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cur = con.cursor()

#[중기예보 자료 삭제]===================================================================
conn = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cursor = conn.cursor()
sql = f"delete from WEB_STEQ_SCRE@svclink.nori.go.kr where PRED_TYPE='DY' "
cursor.execute(sql)
cursor.close()
conn.commit()
conn.close()

#[UPLOAD MDCDB]===================================================================
ii = 1
while ii <= len(content1)-1 :
	DEV = content1[ii].split(',')
	CODE = DEV[0] ; YMD = DEV[1] ; YR = DEV[1][0:4]; MN = DEV[1][4:6] ; DY = DEV[1][6:8] ; HR = DEV[2]
	AVE_TEMP = float(DEV[3]) ; TEMP_SCORE = float(DEV[4]) ; AVE_WSPD = float(DEV[5])  ; WSPD_SCORE = float(DEV[6])
	AVE_SST = float(DEV[7])  ; SST_SCORE = float(DEV[8]) ; AVE_WHT = float(DEV[9])  ; WAVE_SCORE = float(DEV[10])
	TIDE = float(DEV[11]) ; TIDE_SCORE = float(DEV[12]) ; AVE_CSPD = DEV[13]  ; CSPD_SCORE = float(DEV[14])
	WEATHER = float(DEV[15]) ; WEATHER_SCORE = float(DEV[16]) ; CARNIVAL_NUM = float(DEV[17]) ;  RAIN = float(DEV[18])
	WARN_SEA = DEV[19] ; WARN_LAND = DEV[20] ; TOTAL = float(DEV[21]) ; QUOTIENT = DEV[22].encode('utf8').decode()
#               0     1   2     3         4           5          6           7         8       9          10        11     12          13        14          15        16            17          18      19         20     21    22
	print(CODE, YMD, HR, AVE_TEMP, TEMP_SCORE, AVE_WSPD, WSPD_SCORE, AVE_SST, SST_SCORE, AVE_WHT, WAVE_SCORE, TIDE, TIDE_SCORE, AVE_CSPD, CSPD_SCORE, WEATHER, WEATHER_SCORE, CARNIVAL_NUM, RAIN, WARN_SEA, WARN_LAND, TOTAL, QUOTIENT)
	
	sqlStr  = f"merge into WEB_STEQ_SCRE@svclink.nori.go.kr    "
	#sqlStr  = f"merge into WEB_STEQ_SCRE    "
	sqlStr += f"using dual  "
	sqlStr += f"on (FCST_AREA='{CODE}' and PRED_DATE='{YR}-{MN}-{DY}' and PRED_TYPE ='{HR}')  "
	sqlStr += f"when matched then  "
	sqlStr += f"update set  "
	sqlStr += f"AVG_AIR_TEMP={AVE_TEMP},  "
	sqlStr += f"AT_SCORE={TEMP_SCORE},  "
	sqlStr += f"AVG_WIND_SPEED={AVE_WSPD},  "
	sqlStr += f"WS_SCORE={WSPD_SCORE},  "
	sqlStr += f"AVG_WATER_TEMP={AVE_SST},  "
	sqlStr += f"WT_SCORE={SST_SCORE},  "
	sqlStr += f"AVG_WAVE_HEIGHT={AVE_WHT},  "
	sqlStr += f"WH_SCORE={WAVE_SCORE},  "
	sqlStr += f"TIDE_TIME={TIDE},  "
	sqlStr += f"TE_SCORE={TIDE_SCORE},  "
	sqlStr += f"AVG_CURRENT_SPEED='{AVE_CSPD}',  "
	sqlStr += f"CS_SCORE={CSPD_SCORE},  "
	sqlStr += f"WEATHER={WEATHER},  "
	sqlStr += f"WR_SCORE={WEATHER_SCORE},  "
	sqlStr += f"CARNIVAL_NUM={CARNIVAL_NUM},  "
	sqlStr += f"AVE_RAIN_AMT={RAIN},  "	
	sqlStr += f"WARN_SEA='{WARN_SEA}',  "
	sqlStr += f"WARN_LAND='{WARN_LAND}',  "
	sqlStr += f"TOTAL_SCORE={TOTAL},  "
	sqlStr += f"TOTAL_SCORE_STR='{QUOTIENT}'  "	
	sqlStr += f"when not matched then  "
	sqlStr += f"insert (FCST_AREA, PRED_DATE, PRED_TYPE, AVG_AIR_TEMP, AT_SCORE, AVG_WIND_SPEED, WS_SCORE, AVG_WATER_TEMP, WT_SCORE, AVG_WAVE_HEIGHT, WH_SCORE, TIDE_TIME, TE_SCORE, AVG_CURRENT_SPEED, CS_SCORE, WEATHER, WR_SCORE, CARNIVAL_NUM, AVE_RAIN_AMT, WARN_SEA, WARN_LAND, TOTAL_SCORE, TOTAL_SCORE_STR)  "
	sqlStr += f"values ('{CODE}', '{YR}-{MN}-{DY}', '{HR}', '{AVE_TEMP}', '{TEMP_SCORE}',{AVE_WSPD}, {WSPD_SCORE}, {AVE_SST}, {SST_SCORE}, {AVE_WHT}, {WAVE_SCORE}, {TIDE}, {TIDE_SCORE}, '{AVE_CSPD}', {CSPD_SCORE}, {WEATHER}, {WEATHER_SCORE}, {CARNIVAL_NUM}, {RAIN}, '{WARN_SEA}', '{WARN_LAND}', {TOTAL}, '{QUOTIENT}')  "

	cur.execute(sqlStr)
	cur.execute('commit')
	ii = ii + 1

ii = 1
while ii <= len(content2)-1 :
	DEV = content2[ii].split(',')
	CODE = DEV[0] ; YMD = DEV[1] ; YR = DEV[1][0:4]; MN = DEV[1][4:6] ; DY = DEV[1][6:8] ; HR = DEV[2]
	AVE_TEMP = float(DEV[3]) ; TEMP_SCORE = float(DEV[4]) ; AVE_WSPD = float(DEV[5])  ; WSPD_SCORE = float(DEV[6])
	AVE_SST = float(DEV[7])  ; SST_SCORE = float(DEV[8]) ; AVE_WHT = float(DEV[9])  ; WAVE_SCORE = float(DEV[10])
	TIDE = float(DEV[11]) ; TIDE_SCORE = float(DEV[12]) ; AVE_CSPD = DEV[13]  ; CSPD_SCORE = float(DEV[14])
	WEATHER = float(DEV[15]) ; WEATHER_SCORE = float(DEV[16]) ; CARNIVAL_NUM = float(DEV[17]) ;  RAIN = float(DEV[18])
	WARN_SEA = DEV[19] ; WARN_LAND = DEV[20] ; TOTAL = float(DEV[21]) ; QUOTIENT = DEV[22].encode('utf8').decode()
#               0     1   2     3         4           5          6           7         8       9          10        11     12          13        14          15        16            17          18      19         20     21    22
	print(CODE, YMD, HR, AVE_TEMP, TEMP_SCORE, AVE_WSPD, WSPD_SCORE, AVE_SST, SST_SCORE, AVE_WHT, WAVE_SCORE, TIDE, TIDE_SCORE, AVE_CSPD, CSPD_SCORE, WEATHER, WEATHER_SCORE, CARNIVAL_NUM, RAIN, WARN_SEA, WARN_LAND, TOTAL, QUOTIENT)
	
	sqlStr  = f"merge into WEB_STEQ_SCRE@svclink.nori.go.kr    "
	#sqlStr  = f"merge into WEB_STEQ_SCRE    "
	sqlStr += f"using dual  "
	sqlStr += f"on (FCST_AREA='{CODE}' and PRED_DATE='{YR}-{MN}-{DY}' and PRED_TYPE ='{HR}')  "
	sqlStr += f"when matched then  "
	sqlStr += f"update set  "
	sqlStr += f"AVG_AIR_TEMP={AVE_TEMP},  "
	sqlStr += f"AT_SCORE={TEMP_SCORE},  "
	sqlStr += f"AVG_WIND_SPEED={AVE_WSPD},  "
	sqlStr += f"WS_SCORE={WSPD_SCORE},  "
	sqlStr += f"AVG_WATER_TEMP={AVE_SST},  "
	sqlStr += f"WT_SCORE={SST_SCORE},  "
	sqlStr += f"AVG_WAVE_HEIGHT={AVE_WHT},  "
	sqlStr += f"WH_SCORE={WAVE_SCORE},  "
	sqlStr += f"TIDE_TIME={TIDE},  "
	sqlStr += f"TE_SCORE={TIDE_SCORE},  "
	sqlStr += f"AVG_CURRENT_SPEED='{AVE_CSPD}',  "
	sqlStr += f"CS_SCORE={CSPD_SCORE},  "
	sqlStr += f"WEATHER={WEATHER},  "
	sqlStr += f"WR_SCORE={WEATHER_SCORE},  "
	sqlStr += f"CARNIVAL_NUM={CARNIVAL_NUM},  "
	sqlStr += f"AVE_RAIN_AMT={RAIN},  "	
	sqlStr += f"WARN_SEA='{WARN_SEA}',  "
	sqlStr += f"WARN_LAND='{WARN_LAND}',  "
	sqlStr += f"TOTAL_SCORE={TOTAL},  "
	sqlStr += f"TOTAL_SCORE_STR='{QUOTIENT}'  "	
	sqlStr += f"when not matched then  "
	sqlStr += f"insert (FCST_AREA, PRED_DATE, PRED_TYPE, AVG_AIR_TEMP, AT_SCORE, AVG_WIND_SPEED, WS_SCORE, AVG_WATER_TEMP, WT_SCORE, AVG_WAVE_HEIGHT, WH_SCORE, TIDE_TIME, TE_SCORE, AVG_CURRENT_SPEED, CS_SCORE, WEATHER, WR_SCORE, CARNIVAL_NUM, AVE_RAIN_AMT, WARN_SEA, WARN_LAND, TOTAL_SCORE, TOTAL_SCORE_STR)  "
	sqlStr += f"values ('{CODE}', '{YR}-{MN}-{DY}', '{HR}', '{AVE_TEMP}', '{TEMP_SCORE}',{AVE_WSPD}, {WSPD_SCORE}, {AVE_SST}, {SST_SCORE}, {AVE_WHT}, {WAVE_SCORE}, {TIDE}, {TIDE_SCORE}, '{AVE_CSPD}', {CSPD_SCORE}, {WEATHER}, {WEATHER_SCORE}, {CARNIVAL_NUM}, {RAIN}, '{WARN_SEA}', '{WARN_LAND}', {TOTAL}, '{QUOTIENT}')  "

	cur.execute(sqlStr)
	cur.execute('commit')
	ii = ii + 1

ii = 1
while ii <= len(content3)-1 :
	DEV = content3[ii].split(',')
	CODE = DEV[0] ; YMD = DEV[1] ; YR = DEV[1][0:4]; MN = DEV[1][4:6] ; DY = DEV[1][6:8] ; HR = DEV[2]
	AVE_TEMP = float(DEV[3]) ; TEMP_SCORE = float(DEV[4]) ; AVE_WSPD = float(DEV[5])  ; WSPD_SCORE = float(DEV[6])
	AVE_SST = float(DEV[7])  ; SST_SCORE = float(DEV[8]) ; AVE_WHT = float(DEV[9])  ; WAVE_SCORE = float(DEV[10])
	TIDE = float(DEV[11]) ; TIDE_SCORE = float(DEV[12]) ; AVE_CSPD = DEV[13] ; CSPD_SCORE = float(DEV[14])
	WEATHER = float(DEV[15]) ; WEATHER_SCORE = float(DEV[16]) ; CARNIVAL_NUM = float(DEV[17]) ;  RAIN = float(DEV[18])
	WARN_SEA = DEV[19] ; WARN_LAND = DEV[20] ; TOTAL = float(DEV[21]) ; QUOTIENT = DEV[22].encode('utf8').decode()
#               0     1   2     3         4           5          6           7         8       9          10        11     12          13        14          15        16            17          18      19         20     21    22
	print(CODE, YMD, HR, AVE_TEMP, TEMP_SCORE, AVE_WSPD, WSPD_SCORE, AVE_SST, SST_SCORE, AVE_WHT, WAVE_SCORE, TIDE, TIDE_SCORE, AVE_CSPD, CSPD_SCORE, WEATHER, WEATHER_SCORE, CARNIVAL_NUM, RAIN, WARN_SEA, WARN_LAND, TOTAL, QUOTIENT)
	
	sqlStr  = f"merge into WEB_STEQ_SCRE@svclink.nori.go.kr    "
	#sqlStr  = f"merge into WEB_STEQ_SCRE    "
	sqlStr += f"using dual  "
	sqlStr += f"on (FCST_AREA='{CODE}' and PRED_DATE='{YR}-{MN}-{DY}' and PRED_TYPE ='{HR}')  "
	sqlStr += f"when matched then  "
	sqlStr += f"update set  "
	sqlStr += f"AVG_AIR_TEMP={AVE_TEMP},  "
	sqlStr += f"AT_SCORE={TEMP_SCORE},  "
	sqlStr += f"AVG_WIND_SPEED={AVE_WSPD},  "
	sqlStr += f"WS_SCORE={WSPD_SCORE},  "
	sqlStr += f"AVG_WATER_TEMP={AVE_SST},  "
	sqlStr += f"WT_SCORE={SST_SCORE},  "
	sqlStr += f"AVG_WAVE_HEIGHT={AVE_WHT},  "
	sqlStr += f"WH_SCORE={WAVE_SCORE},  "
	sqlStr += f"TIDE_TIME={TIDE},  "
	sqlStr += f"TE_SCORE={TIDE_SCORE},  "
	sqlStr += f"AVG_CURRENT_SPEED='{AVE_CSPD}',  "
	sqlStr += f"CS_SCORE={CSPD_SCORE},  "
	sqlStr += f"WEATHER={WEATHER},  "
	sqlStr += f"WR_SCORE={WEATHER_SCORE},  "
	sqlStr += f"CARNIVAL_NUM={CARNIVAL_NUM},  "
	sqlStr += f"AVE_RAIN_AMT={RAIN},  "	
	sqlStr += f"WARN_SEA='{WARN_SEA}',  "
	sqlStr += f"WARN_LAND='{WARN_LAND}',  "
	sqlStr += f"TOTAL_SCORE={TOTAL},  "
	sqlStr += f"TOTAL_SCORE_STR='{QUOTIENT}'  "	
	sqlStr += f"when not matched then  "
	sqlStr += f"insert (FCST_AREA, PRED_DATE, PRED_TYPE, AVG_AIR_TEMP, AT_SCORE, AVG_WIND_SPEED, WS_SCORE, AVG_WATER_TEMP, WT_SCORE, AVG_WAVE_HEIGHT, WH_SCORE, TIDE_TIME, TE_SCORE, AVG_CURRENT_SPEED, CS_SCORE, WEATHER, WR_SCORE, CARNIVAL_NUM, AVE_RAIN_AMT, WARN_SEA, WARN_LAND, TOTAL_SCORE, TOTAL_SCORE_STR)  "
	sqlStr += f"values ('{CODE}', '{YR}-{MN}-{DY}', '{HR}', '{AVE_TEMP}', '{TEMP_SCORE}',{AVE_WSPD}, {WSPD_SCORE}, {AVE_SST}, {SST_SCORE}, {AVE_WHT}, {WAVE_SCORE}, {TIDE}, {TIDE_SCORE}, '{AVE_CSPD}', {CSPD_SCORE}, {WEATHER}, {WEATHER_SCORE}, {CARNIVAL_NUM}, {RAIN}, '{WARN_SEA}', '{WARN_LAND}', {TOTAL}, '{QUOTIENT}')  "

	cur.execute(sqlStr)
	cur.execute('commit')
	ii = ii + 1

cur.close()
con.close()
