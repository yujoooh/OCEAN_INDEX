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
fname1 = dir1+'/SFEQ_INDEX_SERVICE_'+today+'.csv'

file1 = open(fname1, 'r', encoding='utf8')
content1 = [ str(INFO) for INFO in file1.read().split()]

con = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cur = con.cursor()

#[중기예보 자료 삭제]===================================================================
conn = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cursor = conn.cursor()
sql = f"delete from WEB_SFEQ_SCRE@svclink.nori.go.kr where PRED_TYPE='DY' "
cursor.execute(sql)
cursor.close()
conn.commit()
conn.close()

#[UPLOAD MDCDB]===================================================================
ii = 1
while ii <= len(content1)-1 :
	DEV = content1[ii].split(',')
	CODE = DEV[1] ; YMD = DEV[4] ; NAME = DEV[6] ; TYPE = DEV[7]
	YR = DEV[4][0:4]; MN = DEV[4][4:6] ; DY = DEV[4][6:8] ; HR = DEV[5]
	TIDE = float(DEV[8]) ; TIDE_SCORE = float(DEV[9]) ; 
	MIN_WHT = float(DEV[10]) ; AVE_WHT = float(DEV[11]) ; MAX_WHT = float(DEV[12])  ; WAVE_SCORE = float(DEV[13])
	MIN_SST = float(DEV[14]) ; AVE_SST = float(DEV[15]) ; MAX_SST = float(DEV[16])  ; SST_SCORE = float(DEV[17])
	MIN_TEMP = float(DEV[18]) ; AVE_TEMP = float(DEV[19]) ; MAX_TEMP = float(DEV[20])  ; TEMP_SCORE = float(DEV[21])
	MIN_WSPD = float(DEV[22]) ; AVE_WSPD = float(DEV[23]) ; MAX_WSPD = float(DEV[24])  ; WSPD_SCORE = float(DEV[25])
	WARN = DEV[26] ; WARN_SCORE = float(DEV[27]) ; TOTAL = float(DEV[28])
	print(CODE, YMD, HR, TIDE, TIDE_SCORE, MIN_WHT, AVE_WHT, MAX_WHT, WAVE_SCORE, MIN_SST, AVE_SST, MAX_SST, SST_SCORE, MIN_TEMP, AVE_TEMP, MAX_TEMP, TEMP_SCORE, MIN_WSPD, AVE_WSPD, MAX_WSPD, WSPD_SCORE, WARN, WARN_SCORE, TOTAL)
	
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
