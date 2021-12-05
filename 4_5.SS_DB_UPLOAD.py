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
fname1 = dir1+'/SSEQ_INDEX_SERVICE_'+today+'.csv'

file1 = open(fname1, 'r', encoding='utf8')
content1 = [ str(INFO) for INFO in file1.read().split()]

con = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cur = con.cursor()

#[중기예보 자료 삭제]===================================================================
conn = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cursor = conn.cursor()
sql = f"delete from WEB_SSEQ_SCRE@svclink.nori.go.kr where PRED_TYPE='DY' "
cursor.execute(sql)
cursor.close()
conn.commit()
conn.close()

#[UPLOAD MDCDB]===================================================================
ii = 1
while ii <= len(content1)-1 :
	DEV = content1[ii].split(',')
	CODE = DEV[1] ; YMD = DEV[4] ;YR = DEV[4][0:4]; MN = DEV[4][4:6] ; DY = DEV[4][6:8] ; HR = DEV[5]
	TIDE = float(DEV[6]) ; TIDE_SCORE = float(DEV[7]) ; 
	MIN_WHT = float(DEV[8]) ; AVE_WHT = float(DEV[9]) ; MAX_WHT = float(DEV[10])  ; WAVE_SCORE = float(DEV[11])
	MIN_CSPD = float(DEV[12]) ; AVE_CSPD = float(DEV[13]) ; MAX_CSPD = float(DEV[14])  ; CSPD_SCORE = float(DEV[15])
	MIN_SST = float(DEV[16]) ; AVE_SST = float(DEV[17]) ; MAX_SST = float(DEV[18])  ; SST_SCORE = float(DEV[19])
	WARN = DEV[20] ; WARN_SCORE = float(DEV[21]) ; TOTAL = float(DEV[22])
	if MN == '06' and MN == '07' and MN == '08' and MN == '09' and MN == '10' :
	#	        0     1   2     3       4       5       6         7             8       9             10        11      12      13       14        15           16      17    18         19 
		print(CODE, YMD, HR, TIDE, TIDE_SCORE, MIN_WHT, AVE_WHT, MAX_WHT, WAVE_SCORE, MIN_CSPD, AVE_CSPD, MAX_CSPD, CSPD_SCORE, MIN_SST, AVE_SST, MAX_SST, SST_SCORE, WARN, WARN_SCORE, TOTAL)

		sqlStr  = f"merge into WEB_SSEQ_SCRE@svclink.nori.go.kr    "
		#sqlStr  = f"merge into WEB_SSEQ_SCRE    "
		sqlStr += f"using dual  "
		sqlStr += f"on (SS_CODE='{CODE}' and PRED_DATE='{YR}-{MN}-{DY}' and PRED_TYPE ='{HR}')  "
		sqlStr += f"when matched then  "
		sqlStr += f"update set  "
		sqlStr += f"TIDE_TIME={TIDE},  "
		sqlStr += f"TE_SCORE={TIDE_SCORE},  "
		sqlStr += f"MIN_WAVE_HEIGHT={MIN_WHT},  "
		sqlStr += f"AVG_WAVE_HEIGHT={AVE_WHT},  "
		sqlStr += f"MAX_WAVE_HEIGHT={MAX_WHT},  "
		sqlStr += f"WH_SCORE={WAVE_SCORE},  "
		sqlStr += f"MIN_CURRENT_SPEED={MIN_CSPD},  "
		sqlStr += f"AVG_CURRENT_SPEED={AVE_CSPD},  "
		sqlStr += f"MAX_CURRENT_SPEED={MAX_CSPD},  "
		sqlStr += f"CS_SCORE={CSPD_SCORE},  "
		sqlStr += f"MIN_WATER_TEMP={MIN_SST},  "
		sqlStr += f"AVG_WATER_TEMP={AVE_SST},  "
		sqlStr += f"MAX_WATER_TEMP={MAX_SST},  "
		sqlStr += f"WT_SCORE={SST_SCORE},  "
		sqlStr += f"TOTAL_SCORE={TOTAL},  "
		sqlStr += f"WARN='{WARN}',  "
		sqlStr += f"WARN_SCORE={WARN_SCORE}  "
		sqlStr += f"when not matched then  "
		sqlStr += f"insert (SS_CODE, PRED_DATE, PRED_TYPE, TIDE_TIME, TE_SCORE, MIN_WAVE_HEIGHT, AVG_WAVE_HEIGHT, MAX_WAVE_HEIGHT, WH_SCORE, MIN_CURRENT_SPEED, AVG_CURRENT_SPEED, MAX_CURRENT_SPEED, CS_SCORE, MIN_WATER_TEMP, AVG_WATER_TEMP, MAX_WATER_TEMP, WT_SCORE, TOTAL_SCORE, WARN, WARN_SCORE)  "
		sqlStr += f"values ('{CODE}', '{YR}-{MN}-{DY}', '{HR}', {TIDE}, {TIDE_SCORE}, {MIN_WHT}, {AVE_WHT}, {MAX_WHT}, {WAVE_SCORE}, {MIN_CSPD}, {AVE_CSPD}, {MAX_CSPD}, {CSPD_SCORE}, {MIN_SST}, {AVE_SST}, {MAX_SST}, {SST_SCORE}, {TOTAL}, '{WARN}', {WARN_SCORE})  "

		#print(sqlStr)
		#if ii == 2: break
		cur.execute(sqlStr)
		cur.execute('commit')
		ii = ii + 1
	else :
		TOTAL = 6.0
	#	        0     1   2     3       4       5       6         7             8       9             10        11      12      13       14        15           16      17    18         19 
		print(CODE, YMD, HR, TIDE, TIDE_SCORE, MIN_WHT, AVE_WHT, MAX_WHT, WAVE_SCORE, MIN_CSPD, AVE_CSPD, MAX_CSPD, CSPD_SCORE, MIN_SST, AVE_SST, MAX_SST, SST_SCORE, WARN, WARN_SCORE, TOTAL)

		sqlStr  = f"merge into WEB_SSEQ_SCRE@svclink.nori.go.kr    "
		#sqlStr  = f"merge into WEB_SSEQ_SCRE    "
		sqlStr += f"using dual  "
		sqlStr += f"on (SS_CODE='{CODE}' and PRED_DATE='{YR}-{MN}-{DY}' and PRED_TYPE ='{HR}')  "
		sqlStr += f"when matched then  "
		sqlStr += f"update set  "
		sqlStr += f"TIDE_TIME={TIDE},  "
		sqlStr += f"TE_SCORE={TIDE_SCORE},  "
		sqlStr += f"MIN_WAVE_HEIGHT={MIN_WHT},  "
		sqlStr += f"AVG_WAVE_HEIGHT={AVE_WHT},  "
		sqlStr += f"MAX_WAVE_HEIGHT={MAX_WHT},  "
		sqlStr += f"WH_SCORE={WAVE_SCORE},  "
		sqlStr += f"MIN_CURRENT_SPEED={MIN_CSPD},  "
		sqlStr += f"AVG_CURRENT_SPEED={AVE_CSPD},  "
		sqlStr += f"MAX_CURRENT_SPEED={MAX_CSPD},  "
		sqlStr += f"CS_SCORE={CSPD_SCORE},  "
		sqlStr += f"MIN_WATER_TEMP={MIN_SST},  "
		sqlStr += f"AVG_WATER_TEMP={AVE_SST},  "
		sqlStr += f"MAX_WATER_TEMP={MAX_SST},  "
		sqlStr += f"WT_SCORE={SST_SCORE},  "
		sqlStr += f"TOTAL_SCORE={TOTAL},  "
		sqlStr += f"WARN='{WARN}',  "
		sqlStr += f"WARN_SCORE={WARN_SCORE}  "
		sqlStr += f"when not matched then  "
		sqlStr += f"insert (SS_CODE, PRED_DATE, PRED_TYPE, TIDE_TIME, TE_SCORE, MIN_WAVE_HEIGHT, AVG_WAVE_HEIGHT, MAX_WAVE_HEIGHT, WH_SCORE, MIN_CURRENT_SPEED, AVG_CURRENT_SPEED, MAX_CURRENT_SPEED, CS_SCORE, MIN_WATER_TEMP, AVG_WATER_TEMP, MAX_WATER_TEMP, WT_SCORE, TOTAL_SCORE, WARN, WARN_SCORE)  "
		sqlStr += f"values ('{CODE}', '{YR}-{MN}-{DY}', '{HR}', {TIDE}, {TIDE_SCORE}, {MIN_WHT}, {AVE_WHT}, {MAX_WHT}, {WAVE_SCORE}, {MIN_CSPD}, {AVE_CSPD}, {MAX_CSPD}, {CSPD_SCORE}, {MIN_SST}, {AVE_SST}, {MAX_SST}, {SST_SCORE}, {TOTAL}, '{WARN}', {WARN_SCORE})  "

		#print(sqlStr)
		#if ii == 2: break
		cur.execute(sqlStr)
		cur.execute('commit')
		ii = ii + 1

cur.close()
con.close()
