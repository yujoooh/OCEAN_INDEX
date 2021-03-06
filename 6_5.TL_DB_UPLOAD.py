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
fname1 = dir1+'/TLEQ_INDEX_SERVICE_'+today+'.csv'

file1 = open(fname1, 'r', encoding='utf8')
content1 = [ str(INFO) for INFO in file1.read().split()]

con = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cur = con.cursor()

#[UPLOAD MDCDB]===================================================================
ii = 1
while ii <= len(content1)-1 :
	DEV = content1[ii].split(',')
	CODE = DEV[1] ; YMD = DEV[4]; YR = DEV[4][0:4]; MN = DEV[4][4:6] ; DY = DEV[4][6:8]
	TL_STIME = DEV[5] ; TL_ETIME = DEV[6] ; TL_TIME = float(DEV[7]); TL_SCORE = float(DEV[8])
	MIN_TEMP = float(DEV[9]) ; AVE_TEMP = float(DEV[10]) ; MAX_TEMP = float(DEV[11])  ; TEMP_SCORE = float(DEV[12])
	MIN_WSPD = float(DEV[13]) ; AVE_WSPD = float(DEV[14]) ; MAX_WSPD = float(DEV[15])  ; WSPD_SCORE = float(DEV[16])
	WEATHER = float(DEV[17]) ; WEATHER_SCORE = float(DEV[18]) ; RAIN = float(DEV[19])  ; RAIN_SCORE = float(DEV[20])
	WARN = DEV[21] ; WARN_SCORE = float(DEV[22]) ; TOTAL = float(DEV[23])
	if MN == '05' and MN == '06' and MN == '07' and MN == '08' and MN == '09' and MN == '10' :	
		print(CODE, YMD, TL_STIME, TL_ETIME, TL_TIME, TL_SCORE, MIN_TEMP, AVE_TEMP, MAX_TEMP, TEMP_SCORE, MIN_WSPD, AVE_WSPD, MAX_WSPD, WSPD_SCORE, WEATHER, WEATHER_SCORE, RAIN, RAIN_SCORE, WARN, WARN_SCORE, TOTAL)

		sqlStr  = f"merge into WEB_TLEQ_SCRE@svclink.nori.go.kr    "
		#sqlStr  = f"merge into WEB_TLEQ_SCRE    "
		sqlStr += f"using dual  "
		sqlStr += f"on (TL_CODE='{CODE}' and PRED_DATE='{YR}-{MN}-{DY}' and TL_EXP_STIME='{TL_STIME}' and TL_EXP_ETIME='{TL_ETIME}')  "
		sqlStr += f"when matched then  "
		sqlStr += f"update set  "
		sqlStr += f"TL_SCORE={TL_SCORE},  "
		sqlStr += f"MIN_AIR_TEMP={MIN_TEMP},  "
		sqlStr += f"AVG_AIR_TEMP={AVE_TEMP},  "
		sqlStr += f"MAX_AIR_TEMP={MAX_TEMP},  "
		sqlStr += f"AT_SCORE={TEMP_SCORE},  "
		sqlStr += f"MIN_WIND_SPEED={MIN_WSPD},  "
		sqlStr += f"AVG_WIND_SPEED={AVE_WSPD},  "
		sqlStr += f"MAX_WIND_SPEED={MAX_WSPD},  "	
		sqlStr += f"WS_SCORE={WSPD_SCORE},  "
		sqlStr += f"WEATHER={WEATHER},  "
		sqlStr += f"WT_SCORE={WEATHER_SCORE},  "
		sqlStr += f"TOTAL_SCORE={TOTAL},  "
		sqlStr += f"MAX_RAIN_AMT={RAIN},  "
		sqlStr += f"RAIN_AMT_SCORE={RAIN_SCORE},  "
		sqlStr += f"WARN='{WARN}',  "
		sqlStr += f"WARN_SCORE={WARN_SCORE}  "
		sqlStr += f"when not matched then  "
		sqlStr += f"insert (TL_CODE, PRED_DATE, TL_EXP_STIME, TL_EXP_ETIME, TL_EXP_HOUR, TL_SCORE, MIN_AIR_TEMP, AVG_AIR_TEMP, MAX_AIR_TEMP, AT_SCORE, MIN_WIND_SPEED, AVG_WIND_SPEED, MAX_WIND_SPEED, WS_SCORE, WEATHER, WT_SCORE, TOTAL_SCORE, MAX_RAIN_AMT, RAIN_AMT_SCORE, WARN, WARN_SCORE)  "
		sqlStr += f"values ('{CODE}', '{YR}-{MN}-{DY}', '{TL_STIME}', '{TL_ETIME}', {TL_TIME}, {TL_SCORE}, {MIN_TEMP}, {AVE_TEMP}, {MAX_TEMP}, {TEMP_SCORE}, {MIN_WSPD}, {AVE_WSPD}, {MAX_WSPD}, {WSPD_SCORE}, {WEATHER}, {WEATHER_SCORE}, {TOTAL}, {RAIN}, {RAIN_SCORE}, '{WARN}', {WARN_SCORE})  "

		print(sqlStr)
		#if ii == 2: break
		cur.execute(sqlStr)
		cur.execute('commit')
		ii = ii + 1

	else :
		TOTAL = 6.0                
		print(CODE, YMD, TL_STIME, TL_ETIME, TL_TIME, TL_SCORE, MIN_TEMP, AVE_TEMP, MAX_TEMP, TEMP_SCORE, MIN_WSPD, AVE_WSPD, MAX_WSPD, WSPD_SCORE, WEATHER, WEATHER_SCORE, RAIN, RAIN_SCORE, WARN, WARN_SCORE, TOTAL)

		sqlStr  = f"merge into WEB_TLEQ_SCRE@svclink.nori.go.kr    "
		#sqlStr  = f"merge into WEB_TLEQ_SCRE    "
		sqlStr += f"using dual  "
		sqlStr += f"on (TL_CODE='{CODE}' and PRED_DATE='{YR}-{MN}-{DY}' and TL_EXP_STIME='{TL_STIME}' and TL_EXP_ETIME='{TL_ETIME}')  "
		sqlStr += f"when matched then  "
		sqlStr += f"update set  "
		sqlStr += f"TL_SCORE={TL_SCORE},  "
		sqlStr += f"MIN_AIR_TEMP={MIN_TEMP},  "
		sqlStr += f"AVG_AIR_TEMP={AVE_TEMP},  "
		sqlStr += f"MAX_AIR_TEMP={MAX_TEMP},  "
		sqlStr += f"AT_SCORE={TEMP_SCORE},  "
		sqlStr += f"MIN_WIND_SPEED={MIN_WSPD},  "
		sqlStr += f"AVG_WIND_SPEED={AVE_WSPD},  "
		sqlStr += f"MAX_WIND_SPEED={MAX_WSPD},  "	
		sqlStr += f"WS_SCORE={WSPD_SCORE},  "
		sqlStr += f"WEATHER={WEATHER},  "
		sqlStr += f"WT_SCORE={WEATHER_SCORE},  "
		sqlStr += f"TOTAL_SCORE={TOTAL},  "
		sqlStr += f"MAX_RAIN_AMT={RAIN},  "
		sqlStr += f"RAIN_AMT_SCORE={RAIN_SCORE},  "
		sqlStr += f"WARN='{WARN}',  "
		sqlStr += f"WARN_SCORE={WARN_SCORE}  "
		sqlStr += f"when not matched then  "
		sqlStr += f"insert (TL_CODE, PRED_DATE, TL_EXP_STIME, TL_EXP_ETIME, TL_EXP_HOUR, TL_SCORE, MIN_AIR_TEMP, AVG_AIR_TEMP, MAX_AIR_TEMP, AT_SCORE, MIN_WIND_SPEED, AVG_WIND_SPEED, MAX_WIND_SPEED, WS_SCORE, WEATHER, WT_SCORE, TOTAL_SCORE, MAX_RAIN_AMT, RAIN_AMT_SCORE, WARN, WARN_SCORE)  "
		sqlStr += f"values ('{CODE}', '{YR}-{MN}-{DY}', '{TL_STIME}', '{TL_ETIME}', {TL_TIME}, {TL_SCORE}, {MIN_TEMP}, {AVE_TEMP}, {MAX_TEMP}, {TEMP_SCORE}, {MIN_WSPD}, {AVE_WSPD}, {MAX_WSPD}, {WSPD_SCORE}, {WEATHER}, {WEATHER_SCORE}, {TOTAL}, {RAIN}, {RAIN_SCORE}, '{WARN}', {WARN_SCORE})  "

		print(sqlStr)
		#if ii == 2: break
		cur.execute(sqlStr)
		cur.execute('commit')
		ii = ii + 1		

cur.close()
con.close()
