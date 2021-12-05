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

##[Manual Set]==================================================================================================
#today = '20210907'
#afterday1 = '20210908'
#afterday2 = '20210909'

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
fname1 = dir1+'/SKEQ_INDEX_SERVICE_'+today+'.csv'

file1 = open(fname1, 'r', encoding='utf8')
content1 = [ str(INFO) for INFO in file1.read().split()]

con = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cur = con.cursor()

#[중기예보 자료 삭제]===================================================================
conn = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cursor = conn.cursor()
sql = f"delete from WEB_SKEQ_SCRE@svclink.nori.go.kr where PRED_TYPE='DY' "
cursor.execute(sql)
cursor.close()
conn.commit()
conn.close()

#[UPLOAD MDCDB]===================================================================
ii = 1
while ii <= len(content1)-1 :
	DEV = content1[ii].split(',')
	#'생산일, 코드,해수욕장,예측년월일,시간,평균기온,기온점수,평균수온,수온점수,최대풍속,풍속점수,최대파고,파고점수,총점수\n',
	#CODE = DEV[1] ; YR = DEV[4][0:4]; MN = DEV[4][4:6] ; DY = DEV[4][6:8] ; HR = DEV[5]
	CODE = DEV[1] ; SHIP_NAME = DEV[3].encode('utf8').decode() ; YMD = DEV[5]
	YR = DEV[5][0:4]; MN = DEV[5][4:6] ; DY = DEV[5][6:8] ; HR = DEV[6]
	SAIL_HOUR = float(DEV[7]) ; SH_SCORE = float(DEV[8]) ; SHIP_TON = float(DEV[9]) ; ST_SCORE=float(DEV[10])
	MIN_WHT = float(DEV[11]) ; AVE_WHT = float(DEV[12]) ; MAX_WHT = float(DEV[13])  ; WAVE_SCORE = float(DEV[14])
	MIN_WSPD = float(DEV[15]) ; AVE_WSPD = float(DEV[16]) ; MAX_WSPD = float(DEV[17])  ; WSPD_SCORE = float(DEV[18])
	WARN = DEV[19] ; WARN_SCORE = float(DEV[20]) ;TOTAL = float(DEV[21])
	#if DEV[6] == 'AM' : HR = '09'
	#if DEV[6] == 'PM' : HR = '16'
	print(CODE, SHIP_NAME, YMD, HR, SAIL_HOUR, SH_SCORE, SHIP_TON, ST_SCORE, MIN_WHT, AVE_WHT, MAX_WHT, WAVE_SCORE, MIN_WSPD, AVE_WSPD, MAX_WSPD, WSPD_SCORE, WARN, WARN_SCORE, TOTAL)
	
	sqlStr  = f"merge into WEB_SKEQ_SCRE@svclink.nori.go.kr    "
	#sqlStr  = f"merge into WEB_SKEQ_SCRE    "
	sqlStr += f"using dual  "
	sqlStr += f"on (SK_CODE='{CODE}' and SHIP_NAME='{SHIP_NAME}' and PRED_DATE='{YR}-{MN}-{DY}' and PRED_TYPE='{HR}')  "
	sqlStr += f"when matched then  "
	sqlStr += f"update set  "
	sqlStr += f"SAIL_HOUR={SAIL_HOUR},  "
	sqlStr += f"SH_SCORE={SH_SCORE},  "
	sqlStr += f"SHIP_TONN={SHIP_TON},  "
	sqlStr += f"ST_SCORE={ST_SCORE},  "
	sqlStr += f"MIN_WAVE_HEIGHT={MIN_WHT},  "
	sqlStr += f"AVG_WAVE_HEIGHT={AVE_WHT},  "
	sqlStr += f"MAX_WAVE_HEIGHT={MAX_WHT},  "
	sqlStr += f"WH_SCORE={WAVE_SCORE},  "
	sqlStr += f"MIN_WIND_SPEED={MIN_WSPD},  "
	sqlStr += f"AVG_WIND_SPEED={AVE_WSPD},  "
	sqlStr += f"MAX_WIND_SPEED={MAX_WSPD},  "	
	sqlStr += f"WS_SCORE={WSPD_SCORE},  "
	sqlStr += f"TOTAL_SCORE={TOTAL},  "
	sqlStr += f"WARN='{WARN}',  "
	sqlStr += f"WARN_SCORE={WARN_SCORE}  "
	sqlStr += f"when not matched then  "
	sqlStr += f"insert (SK_CODE, PRED_DATE, PRED_TYPE, SAIL_HOUR, SH_SCORE, SHIP_TONN,ST_SCORE, MIN_WAVE_HEIGHT, AVG_WAVE_HEIGHT, MAX_WAVE_HEIGHT, WH_SCORE, MIN_WIND_SPEED, AVG_WIND_SPEED, MAX_WIND_SPEED, WS_SCORE, TOTAL_SCORE, SHIP_NAME, WARN, WARN_SCORE)  "
	sqlStr += f"values ('{CODE}', '{YR}-{MN}-{DY}', '{HR}', {SAIL_HOUR}, {SH_SCORE}, {SHIP_TON}, {ST_SCORE}, {MIN_WHT}, {AVE_WHT}, {MAX_WHT}, {WAVE_SCORE}, {MIN_WSPD}, {AVE_WSPD}, {MAX_WSPD}, {WSPD_SCORE}, {TOTAL}, '{SHIP_NAME}', '{WARN}', {WARN_SCORE})  "

	#print(sqlStr)
	#if ii == 2: break
	cur.execute(sqlStr)
	cur.execute('commit')
	ii = ii + 1

cur.close()
con.close()
