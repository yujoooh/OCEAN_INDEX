#[Geosystem Research : Department of Coastal Management]
#[Created by HGCHOE]
#[EDIT C.K. Park on 2019.11.07]

import cx_Oracle
#import pymysql
from pprint import pprint
import sys
from datetime import date, timedelta
from datetime import datetime

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
fname1 = dir1+'/SPEQ_INDEX_SERVICE_'+today+'.csv'

file1 = open(fname1, 'r', encoding='utf8')
content1 = [ str(INFO) for INFO in file1.read().split()]

con = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cur = con.cursor()

#[중기예보 자료 삭제]===================================================================
conn = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cursor = conn.cursor()
sql = f"delete from WEB_BEACH_QUOTIENT_SCORE@svclink.nori.go.kr where PRED_HOUR='DY' "
cursor.execute(sql)
conn.commit()
conn.close()

#[UPLOAD MDCDB]===================================================================
ii = 1
while ii <= len(content1)-1 :
	DEV = content1[ii].split(',')
	#'생산일, 코드,해수욕장,예측년월일,시간,평균기온,기온점수,평균수온,수온점수,최대풍속,풍속점수,최대파고,파고점수,총점수\n',
	CODE = DEV[1] ; YR = DEV[4][0:4]; MN = DEV[4][4:6] ; DY = DEV[4][6:8]
	TEMP = float(DEV[6]) ; TEMP_SCORE = float(DEV[7]) ; SST = float(DEV[8]) ; SST_SCORE=float(DEV[9])
	WIND = float(DEV[10]) ; WIND_SCORE = float(DEV[11]) ; WAVE = float(DEV[12]) ; WAVE_SCORE = float(DEV[13])
	RAIN = float(DEV[14]) ; RAIN_SCORE = float(DEV[15]) ; WARN = DEV[16] ; WARN_SCORE = float(DEV[17]) ; TOTAL = float(DEV[18])
	if DEV[5] == 'AM' : HR = '12'
	if DEV[5] == 'PM' : HR = '18'
	if DEV[5] == 'DY' : HR = 'DY'
	if MN == '06' and MN == '07' and MN == '08' :
		print(CODE, YR, MN, DY, HR, TEMP, TEMP_SCORE, SST, SST_SCORE, WIND, WIND_SCORE, WAVE, WAVE_SCORE, RAIN, RAIN_SCORE, WARN, WARN_SCORE, TOTAL)
		print(DEV)
		sqlStr  = f"merge into WEB_BEACH_QUOTIENT_SCORE@svclink.nori.go.kr  "
		#sqlStr  = f"merge into WEB_BEACH_QUOTIENT_SCORE  "
		sqlStr += f"using dual  "
		sqlStr += f"on (BEACH_CODE='{CODE}' and PRED_YEAR={YR} and PRED_MONTH={MN} and PRED_DAY={DY} and PRED_HOUR='{HR}')  "
		sqlStr += f"when matched then  "
		sqlStr += f"update set  "
		sqlStr += f"AVG_AIR_TEMP={TEMP},  "
		sqlStr += f"SCORE_AIR_TEMP={TEMP_SCORE},  "
		sqlStr += f"AVG_WATER_TEMP={SST},  "
		sqlStr += f"SCORE_WATER_TEMP={SST_SCORE},  "
		sqlStr += f"MAX_WIND_SPEED={WIND},  "
		sqlStr += f"SCORE_WIND_SPEED={WIND_SCORE},  "
		sqlStr += f"MAX_WAVE_HEIGHT={WAVE},  "
		sqlStr += f"SCORE_WAVE_HEIGHT={WAVE_SCORE},  "
		sqlStr += f"TOTAL_SCORE={TOTAL},  "
		sqlStr += f"MAX_RAIN_AMT={RAIN},  "
		sqlStr += f"SCORE_RAIN_AMT={RAIN_SCORE},  "
		sqlStr += f"WARN='{WARN}',  "
		sqlStr += f"WARN_SCORE={WARN_SCORE}  "
		sqlStr += f"when not matched then  "
		sqlStr += f"insert (BEACH_CODE, PRED_YEAR, PRED_MONTH, PRED_DAY, PRED_HOUR, AVG_AIR_TEMP, SCORE_AIR_TEMP, AVG_WATER_TEMP, SCORE_WATER_TEMP, MAX_WIND_SPEED, SCORE_WIND_SPEED, MAX_WAVE_HEIGHT, SCORE_WAVE_HEIGHT, TOTAL_SCORE, MAX_RAIN_AMT, SCORE_RAIN_AMT, WARN, WARN_SCORE)  "
		sqlStr += f"values ('{CODE}', '{YR}', '{MN.zfill(2)}', '{DY.zfill(2)}', '{HR}', {TEMP}, {TEMP_SCORE}, {SST}, {SST_SCORE}, {WIND}, {WIND_SCORE}, {WAVE}, {WAVE_SCORE}, {TOTAL}, {RAIN}, {RAIN_SCORE}, '{WARN}', {WARN_SCORE})  "
	

		#print(sqlStr)
		#if ii == 2: break
		cur.execute(sqlStr)
		cur.execute('commit')
		ii = ii + 1
	else :
		TOTAL = 6.0
		print(CODE, YR, MN, DY, HR, TEMP, TEMP_SCORE, SST, SST_SCORE, WIND, WIND_SCORE, WAVE, WAVE_SCORE, RAIN, RAIN_SCORE, WARN, WARN_SCORE, TOTAL)
		#print(DEV)
		sqlStr  = f"merge into WEB_BEACH_QUOTIENT_SCORE@svclink.nori.go.kr  "
		#sqlStr  = f"merge into WEB_BEACH_QUOTIENT_SCORE  "
		sqlStr += f"using dual  "
		sqlStr += f"on (BEACH_CODE='{CODE}' and PRED_YEAR={YR} and PRED_MONTH={MN} and PRED_DAY={DY} and PRED_HOUR='{HR}')  "
		sqlStr += f"when matched then  "
		sqlStr += f"update set  "
		sqlStr += f"AVG_AIR_TEMP={TEMP},  "
		sqlStr += f"SCORE_AIR_TEMP={TEMP_SCORE},  "
		sqlStr += f"AVG_WATER_TEMP={SST},  "
		sqlStr += f"SCORE_WATER_TEMP={SST_SCORE},  "
		sqlStr += f"MAX_WIND_SPEED={WIND},  "
		sqlStr += f"SCORE_WIND_SPEED={WIND_SCORE},  "
		sqlStr += f"MAX_WAVE_HEIGHT={WAVE},  "
		sqlStr += f"SCORE_WAVE_HEIGHT={WAVE_SCORE},  "
		sqlStr += f"TOTAL_SCORE={TOTAL},  "
		sqlStr += f"MAX_RAIN_AMT={RAIN},  "
		sqlStr += f"SCORE_RAIN_AMT={RAIN_SCORE},  "
		sqlStr += f"WARN='{WARN}',  "
		sqlStr += f"WARN_SCORE={WARN_SCORE}  "
		sqlStr += f"when not matched then  "
		sqlStr += f"insert (BEACH_CODE, PRED_YEAR, PRED_MONTH, PRED_DAY, PRED_HOUR, AVG_AIR_TEMP, SCORE_AIR_TEMP, AVG_WATER_TEMP, SCORE_WATER_TEMP, MAX_WIND_SPEED, SCORE_WIND_SPEED, MAX_WAVE_HEIGHT, SCORE_WAVE_HEIGHT, TOTAL_SCORE, MAX_RAIN_AMT, SCORE_RAIN_AMT, WARN, WARN_SCORE)  "
		sqlStr += f"values ('{CODE}', '{YR}', '{MN.zfill(2)}', '{DY.zfill(2)}', '{HR}', {TEMP}, {TEMP_SCORE}, {SST}, {SST_SCORE}, {WIND}, {WIND_SCORE}, {WAVE}, {WAVE_SCORE}, {TOTAL}, {RAIN}, {RAIN_SCORE}, '{WARN}', {WARN_SCORE})  "
		cur.execute(sqlStr)
		cur.execute('commit')
		ii = ii + 1
cur.close()
con.close()
