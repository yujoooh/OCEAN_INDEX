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
#afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
#afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')


#[DB connect inforamtion]================================================================
#[MDCDB]
DBID = 'ocean_web'
DBPWD = 'infoshfl03'
DBINFO = '192.168.200.16:1521/mgis'

#[OCEAN_DB 접속]
#DBID = 'ocean'
#DBPWD = 'ocean'
#DBINFO = '10.27.90.17:1521/mgis'

con = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cur = con.cursor()


#[UPLOAD]===================================================================
# HS 해수욕
#sql = "CALL PROC_CLONE_RESULT_QUOTIENT@svclink.nori.go.kr('HS', to_date('"
sql = "CALL PROC_CLONE_RESULT_QUOTIENT('TL', to_date('"
Str = "','YYYYMMDD'),6)"
sqlStr = sql + today + Str
print(sqlStr)
cur.execute(sqlStr)

