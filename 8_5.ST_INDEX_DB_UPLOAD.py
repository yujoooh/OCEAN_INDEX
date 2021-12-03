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
#DBINFO = '192.168.6.190:1521/xe'

#[OCEAN_DB]
DBID = 'ocean'
DBPWD = 'ocean'
DBINFO = '10.27.90.17:1521/mgis'

#[INFO FILE NAME READ]===================================================================
fname1 = dir1+'/ST_INDEX_FCST_BUSAN'+today+'.csv'
file1 = open(fname1, 'r', encoding='utf8')
content1 = [ str(INFO) for INFO in file1.read().split()]

fname2 = dir1+'/ST_INDEX_FCST_JEJU'+today+'.csv'
file2 = open(fname1, 'r', encoding='utf8')
content2 = [ str(INFO) for INFO in file1.read().split()]

fname3 = dir1+'/ST_INDEX_FCST_YEOSU'+today+'.csv'
file3 = open(fname1, 'r', encoding='utf8')
content3 = [ str(INFO) for INFO in file1.read().split()]

con = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cur = con.cursor()

#[중기예보 자료 삭제]===================================================================
conn = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cursor = conn.cursor()
sql = f"delete from WEB_STEQ_SCRE@svclink.nori.go.kr where PRED_TYPE='DY' "
cursor.execute(sql)
sql = f"delete from WEB_STEQ_SCRE_KHOA@svclink.nori.go.kr where PRED_TYPE='DY' "
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
	TIDE = float(DEV[11]) ; TIDE_SCORE = float(DEV[12]) ; AVE_CSPD = float(DEV[13])  ; CSPD_SCORE = float(DEV[14])
	WEATHER = float(DEV[15]) ; WEATHER_SCORE = float(DEV[16]) ; CARNIVAL_NUM = float(DEV[17]) ;  RAIN = float(DEV[18])
	WARN_SEA = DEV[19] ; WARN_LAND = DEV[20] ; TOTAL = float(DEV[21]) ; QUOTIENT = DEV[22].encode('utf8').decode()
#               0     1   2     3         4           5          6           7         8       9          10        11     12          13        14          15        16            17          18      19         20       21    22
	print(CODE, YMD, HR, AVE_TEMP, TEMP_SCORE, AVE_WSPD, WSPD_SCORE, AVE_SST, SST_SCORE, AVE_WHT, WAVE_SCORE, TIDE, TIDE_SCORE, AVE_CSPD, CSPD_SCORE, WEATHER, WEATHER_SCORE, CARNIVAL_NUM, RAIN, WARN_SEA, WARN_LAND, TOTAL, QUOTIENT)
	
	sqlStr  = f"merge into WEB_SFEQ_SCRE@svclink.nori.go.kr    "
	#sqlStr  = f"merge into WEB_SFEQ_SCRE    "
	sqlStr += f"using dual  "
	#sqlStr += f"on (SF_CODE='{CODE}' and SF_FISH_NAME='{NAME}' and SF_FISH_TYPE='{TYPE}' and PRED_DATE='{YR}-{MN}-{DY}')  "
	sqlStr += f"on (SF_CODE='{CODE}' and PRED_DATE='{YR}-{MN}-{DY}' and PRED_TYPE ='{HR}')  "
	sqlStr += f"when matched then  "
	sqlStr += f"update set  "
	sqlStr += f"SF_FISH_NAME='{NAME}',  "
	sqlStr += f"SF_FISH_TYPE='{TYPE}',  "
	sqlStr += f"TIDE_TIME={TIDE},  "
	sqlStr += f"TE_SCORE={TIDE_SCORE},  "
	sqlStr += f"MIN_WAVE_HEIGHT={MIN_WHT},  "
	sqlStr += f"AVG_WAVE_HEIGHT={AVE_WHT},  "
	sqlStr += f"MAX_WAVE_HEIGHT={MAX_WHT},  "
	sqlStr += f"WH_SCORE={WAVE_SCORE},  "
	sqlStr += f"MIN_WATER_TEMP={MIN_SST},  "
	sqlStr += f"AVG_WATER_TEMP={AVE_SST},  "
	sqlStr += f"MAX_WATER_TEMP={MAX_SST},  "
	sqlStr += f"WT_SCORE={SST_SCORE},  "
	sqlStr += f"MIN_AIR_TEMP={MIN_TEMP},  "
	sqlStr += f"AVG_AIR_TEMP={AVE_TEMP},  "
	sqlStr += f"MAX_AIR_TEMP={MAX_TEMP},  "
	sqlStr += f"AT_SCORE={TEMP_SCORE},  "
	sqlStr += f"MIN_WIND_SPEED={MIN_WSPD},  "
	sqlStr += f"AVG_WIND_SPEED={AVE_WSPD},  "
	sqlStr += f"MAX_WIND_SPEED={MAX_WSPD},  "	
	sqlStr += f"WS_SCORE={WSPD_SCORE},  "
	sqlStr += f"TOTAL_SCORE={TOTAL},  "
	sqlStr += f"WARN='{WARN}',  "
	sqlStr += f"WARN_SCORE={WARN_SCORE}  "
	sqlStr += f"when not matched then  "
	sqlStr += f"insert (SF_CODE, PRED_DATE, PRED_TYPE, SF_FISH_NAME, SF_FISH_TYPE, TIDE_TIME, TE_SCORE, MIN_WAVE_HEIGHT, AVG_WAVE_HEIGHT, MAX_WAVE_HEIGHT, WH_SCORE, MIN_WATER_TEMP, AVG_WATER_TEMP, MAX_WATER_TEMP, WT_SCORE, MIN_AIR_TEMP, AVG_AIR_TEMP, MAX_AIR_TEMP, AT_SCORE, MIN_WIND_SPEED, AVG_WIND_SPEED, MAX_WIND_SPEED, WS_SCORE, TOTAL_SCORE, WARN, WARN_SCORE)  "
	sqlStr += f"values ('{CODE}', '{YR}-{MN}-{DY}', '{HR}', '{NAME}', '{TYPE}',{TIDE}, {TIDE_SCORE}, {MIN_WHT}, {AVE_WHT}, {MAX_WHT}, {WAVE_SCORE}, {MIN_SST}, {AVE_SST}, {MAX_SST}, {SST_SCORE}, {MIN_TEMP}, {AVE_TEMP}, {MAX_TEMP}, {TEMP_SCORE}, {MIN_WSPD}, {AVE_WSPD}, {MAX_WSPD}, {WSPD_SCORE}, {TOTAL}, '{WARN}', {WARN_SCORE})  "

	#print(sqlStr)
	#if ii == 2: break
	cur.execute(sqlStr)
	cur.execute('commit')
	ii = ii + 1

cur.close()
con.close()
