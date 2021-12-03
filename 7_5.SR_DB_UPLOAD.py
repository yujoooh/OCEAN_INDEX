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
fname1 = dir1+'/SREQ_INDEX_SERVICE_'+today+'.csv'

file1 = open(fname1, 'r', encoding='utf8')
content1 = [ str(INFO) for INFO in file1.read().split()]

con = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cur = con.cursor()

#[UPLOAD MDCDB]===================================================================
ii = 1
while ii <= 6 :
	DEV = content1[ii].split(',')
	#'생산일, 코드,해수욕장,예측년월일,시간,평균기온,기온점수,평균수온,수온점수,최대풍속,풍속점수,최대파고,파고점수,총점수\n',
	#CODE = DEV[1] ; YR = DEV[4][0:4]; MN = DEV[4][4:6] ; DY = DEV[4][6:8] ; HR = DEV[5]
	CODE = DEV[1] ; YMD = DEV[4] ; YR = DEV[4][0:4]; MN = DEV[4][4:6] ; DY = DEV[4][6:8] ; HR = DEV[5]
	WAVE = float(DEV[6]) ; WAVE_SCORE = float(DEV[7]) ; DERECTION = float(DEV[8]) ; REF_DERECTION = float(DEV[9]) ; DERECTION_SCORE = float(DEV[10])
	PERIOD = float(DEV[11]) ; PERIOD_SCORE = float(DEV[12]) ; WSPD = float(DEV[13]) ; WDIR = float(DEV[14]) ; WSPD_SCORE = float(DEV[15])
	SST = float(DEV[16]) ; SST_SCORE=float(DEV[17]) ; WARN = DEV[18] ; WARN_SCORE = float(DEV[19]) ; TOTAL = float(DEV[20]) ; QUOTIENT = DEV[21].encode('utf8').decode()
 
	print(CODE, YMD, HR, WAVE, WAVE_SCORE, DERECTION, REF_DERECTION, DERECTION_SCORE, PERIOD, PERIOD_SCORE, WSPD, WDIR, WSPD_SCORE, SST, SST_SCORE, WARN, WARN_SCORE, TOTAL, QUOTIENT)
	
	sqlStr  = f"merge into WEB_SREQ_SCRE@svclink.nori.go.kr    "
	#sqlStr  = f"merge into WEB_SREQ_SCRE    "
	sqlStr += f"using dual  "
	sqlStr += f"on (SR_CODE='{CODE}' and PRED_DATE='{YR}-{MN}-{DY}' and PRED_TYPE='{HR}')  "
	sqlStr += f"when matched then  "
	sqlStr += f"update set  "
	sqlStr += f"AVG_WAVE_HEIGHT={WAVE},  "
	sqlStr += f"WH_SCORE={WAVE_SCORE},  "
	sqlStr += f"AVG_WAVE_DERECTION={DERECTION},  "	
	sqlStr += f"REF_AVG_WAVE_DERECTION={REF_DERECTION},  "	
	sqlStr += f"WD_SCORE={DERECTION_SCORE},  "
	sqlStr += f"AVG_WAVE_PERIOD={PERIOD},  "
	sqlStr += f"WP_SCORE={PERIOD_SCORE},  "
	sqlStr += f"AVG_WIND_SPEED={WSPD},  "
	sqlStr += f"AVG_WIND_DERECTION={WDIR},  "
	sqlStr += f"WS_SCORE={WSPD_SCORE},  "
	sqlStr += f"AVG_WATER_TEMP={SST},  "
	sqlStr += f"WT_SCORE={SST_SCORE},  "
	sqlStr += f"WARN='{WARN}',  "
	sqlStr += f"WARN_SCORE={WARN_SCORE},  "
	sqlStr += f"TOTAL_SCORE={TOTAL},  "
	sqlStr += f"TOTAL_SCORE_STR='{QUOTIENT}'  "
	sqlStr += f"when not matched then  "
	sqlStr += f"insert (SR_CODE, PRED_DATE, PRED_TYPE, AVG_WAVE_HEIGHT, WH_SCORE, AVG_WAVE_DERECTION, REF_AVG_WAVE_DERECTION, WD_SCORE, AVG_WAVE_PERIOD, WP_SCORE, AVG_WIND_SPEED, AVG_WIND_DERECTION, WS_SCORE, AVG_WATER_TEMP, WT_SCORE, WARN, WARN_SCORE, TOTAL_SCORE, TOTAL_SCORE_STR)  "
	sqlStr += f"values ('{CODE}', '{YR}-{MN}-{DY}', '{HR}', {WAVE}, {WAVE_SCORE}, {DERECTION}, {REF_DERECTION}, {DERECTION_SCORE}, {PERIOD}, {PERIOD_SCORE}, {WSPD}, {WDIR}, {WSPD_SCORE}, {SST}, {SST_SCORE}, '{WARN}', {WARN_SCORE}, {TOTAL}, '{QUOTIENT}')  "

	#print(sqlStr)
	#if ii == 2: break
	cur.execute(sqlStr)
	cur.execute('commit')
	ii = ii + 1

cur.close()
con.close()
