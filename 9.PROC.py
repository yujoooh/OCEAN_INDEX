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

#[중기예보 자료 삭제]===================================================================
conn = cx_Oracle.connect(DBID, DBPWD, DBINFO)
cursor = conn.cursor()
sql = f"delete from WEB_STEQ_SCRE_KHOA where PRED_TYPE='DY' "
cursor.execute(sql)
sql = f"delete from WEB_SREQ_SCRE_KHOA where PRED_TYPE='DY' "
cursor.execute(sql)
sql = f"delete from WEB_SSEQ_SCRE_KHOA where PRED_TYPE='DY' "
cursor.execute(sql)
sql = f"delete from WEB_SFEQ_SCRE_KHOA where PRED_TYPE='DY' "
cursor.execute(sql)
sql = f"delete from WEB_SKEQ_SCRE_KHOA where PRED_TYPE='DY' "
cursor.execute(sql)
sql = f"delete from WEB_BEACH_QUOT_SCORE_KHOA where PRED_HOUR='DY' "
cursor.execute(sql)
cursor.close()
conn.commit()
conn.close()

#[UPLOAD]===================================================================
# HS 해수욕
#sql = "CALL PROC_CLONE_RESULT_QUOTIENT@svclink.nori.go.kr('HS', to_date('"
sql = "CALL PROC_CLONE_RESULT_QUOTIENT('HS', to_date('"
Str = "','YYYYMMDD'),6)"
sqlStr = sql + today + Str
print(sqlStr)
cur.execute(sqlStr)
# SK 뱃멀미
#sql = "CALL PROC_CLONE_RESULT_QUOTIENT@svclink.nori.go.kr('SK', to_date('"
sql = "CALL PROC_CLONE_RESULT_QUOTIENT('SK', to_date('"
Str = "','YYYYMMDD'),6)"
sqlStr = sql + today + Str
print(sqlStr)
cur.execute(sqlStr)
# SF 바다낚시
#sql = "CALL PROC_CLONE_RESULT_QUOTIENT@svclink.nori.go.kr('SF', to_date('"
sql = "CALL PROC_CLONE_RESULT_QUOTIENT('SF', to_date('"
Str = "','YYYYMMDD'),6)"
sqlStr = sql + today + Str
print(sqlStr)
cur.execute(sqlStr)
# SD 바다갈라짐체험
#sql = "CALL PROC_CLONE_RESULT_QUOTIENT@svclink.nori.go.kr('SD', to_date('"
sql = "CALL PROC_CLONE_RESULT_QUOTIENT('SD', to_date('"
Str = "','YYYYMMDD'),6)"
sqlStr = sql + today + Str
print(sqlStr)
cur.execute(sqlStr)
# TL 바다갈라짐체험
#sql = "CALL PROC_CLONE_RESULT_QUOTIENT@svclink.nori.go.kr('TL', to_date('"
sql = "CALL PROC_CLONE_RESULT_QUOTIENT('TL', to_date('"
Str = "','YYYYMMDD'),6)"
sqlStr = sql + today + Str
print(sqlStr)
cur.execute(sqlStr)
# SS 스킨스쿠버
#sql = "CALL PROC_CLONE_RESULT_QUOTIENT@svclink.nori.go.kr('SS', to_date('"
sql = "CALL PROC_CLONE_RESULT_QUOTIENT('SS', to_date('"
Str = "','YYYYMMDD'),6)"
sqlStr = sql + today + Str
print(sqlStr)
cur.execute(sqlStr)
# SR 서핑
#sql = "CALL PROC_CLONE_RESULT_QUOTIENT@svclink.nori.go.kr('SS', to_date('"
sql = "CALL PROC_CLONE_RESULT_QUOTIENT('SR', to_date('"
Str = "','YYYYMMDD'),6)"
sqlStr = sql + today + Str
print(sqlStr)
cur.execute(sqlStr)
# ST 바다여행
#sql = "CALL PROC_CLONE_RESULT_QUOTIENT@svclink.nori.go.kr('ST', to_date('"
sql = "CALL PROC_CLONE_RESULT_QUOTIENT('ST', to_date('"
Str = "','YYYYMMDD'),6)"
sqlStr = sql + today + Str
print(sqlStr)
cur.execute(sqlStr)


