#[Geosystem Research : Department of Marine Forecast ]
#[Created by C.K. Park on 2018.10.23]
#[191206:HGChoe:From API To DB]
import json
import os
import urllib.request
import shutil
from collections import OrderedDict
from datetime import datetime, timedelta
import cx_Oracle
import pandas as pd

print("#KOHA OBS data collection Start==========")

#[Date Set]===============================================================================================================
today = str(datetime.today().strftime('%Y%m%d'))
hr = str(datetime.today().strftime("%H"))

#[폴더]
dir1 = './Result/'+today

#[DB Connect]
CONID = "OCEAN"
CONPW = "ocean"
CONINFO = "10.27.90.17:1521/mgis"
con = cx_Oracle.connect(CONID, CONPW, CONINFO)
cur = con.cursor()

#[Data Collecting]
data1 = [] # 조위관측소 데이터 저장 리스트 생성
data2 = [] # 해양관측부이 데이터 저장 리스트 생성
Miss = '-999.0'
obsdf = pd.read_csv('./Info/KHOA_OBS_INFO.csv', sep=',', header=None, encoding='utf8', index_col=0)
obsdf.columns = [ 'NAME', 'TYPE' ]
obsdf.index.name = 'CODE'

#-----------------------------------[조위관측소 자료수집]-----------------------------------------
TIDE_INF = open('./Info/TIDE_STATION_INFO.csv','r',encoding='utf8')
TIDE_STN = [str(INFO) for INFO in TIDE_INF.read().split()]
print(today,"KHOA Tide-station obs data collection...","correction time", hr)

for code in TIDE_STN:
    if len(code) < 5:
        continue
    else:
        STN  = obsdf.NAME[code]
        TYPE = obsdf.TYPE[code]
    ## SST
    if   code[0:2] == 'DT':
        sqlStr  = f"select OBS_VALUE from GD_OBS_ST where OBS_POST_ID = '{code}'  "
        sqlStr += f"and OBS_TIME >= sysdate-1  "
        sqlStr += f"and OBS_ITEM_CODE = 'WATER_TEMP'  "
        sqlStr += f"and ROWNUM = 1  "
        sqlStr += f"order by OBS_TIME desc"
    elif code == 'IE_0060': #이어도
        sqlStr  = f"select OBS_VALUE from GD_OBS_ST where OBS_POST_ID = '{code}'  "
        sqlStr += f"and OBS_TIME >= sysdate-1  "
        sqlStr += f"and OBS_ITEM_CODE = 'ICT.L1T'  "
        sqlStr += f"and ROWNUM = 1  "
        sqlStr += f"order by OBS_TIME desc"
    elif code == 'IE_0061': #신안가거초
        sqlStr  = f"select OBS_VALUE from GR_OBS_ST where OBS_POST_ID = '{code}'  "
        sqlStr += f"and OBS_TIME >= sysdate-1  "
        sqlStr += f"and OBS_ITEM_CODE = 'SC_CT_TEMP'  "
        sqlStr += f"and ROWNUM = 1  "
        sqlStr += f"order by OBS_TIME desc"
    elif code == 'IE_0062': #웅진소청초
        sqlStr  = f"select OBS_VALUE from GR_OBS_ST where OBS_POST_ID = '{code}'  "
        sqlStr += f"and OBS_TIME >= sysdate-1  "
        sqlStr += f"and OBS_ITEM_CODE = 'SC_CT_TEMP'  "
        sqlStr += f"and ROWNUM = 1  "
        sqlStr += f"order by OBS_TIME desc"
    cur.execute(sqlStr)
    row = cur.fetchall()
    if len(row):
        SST = row[0][0]
        if SST == 0 :
            SST = Miss
        else :
            SST = SST
    else:
        SST = Miss
    ## MWHT
    if code == 'DT_0039' : #왕돌초
            sqlStr  = f"select OBS_VALUE from GD_OBS_ST where OBS_POST_ID = '{code}'  "
            sqlStr += f"and OBS_TIME >= sysdate-1  "
            sqlStr += f"and OBS_ITEM_CODE = 'SIGNIFI_WAVE_HEIGHT'  "
            sqlStr += f"and ROWNUM = 1  "
            sqlStr += f"order by OBS_TIME desc"
    elif code[0:2] == 'DT':
        sqlStr  = f"select OBS_VALUE from GD_OBS_ST where OBS_POST_ID = '{code}'  "
        sqlStr += f"and OBS_TIME >= sysdate-1  "
        sqlStr += f"and OBS_ITEM_CODE = 'NOT_FOUND_WAVE_HEIGHT'  "
        sqlStr += f"and ROWNUM = 1  "
        sqlStr += f"order by OBS_TIME desc"
    elif code == 'IE_0060': #이어도
        sqlStr  = f"select OBS_VALUE from GD_OBS_ST where OBS_POST_ID = '{code}'  "
        sqlStr += f"and OBS_TIME >= sysdate-1  "
        sqlStr += f"and OBS_ITEM_CODE = 'IOMWR.HM0'  "
        sqlStr += f"and ROWNUM = 1  "
        sqlStr += f"order by OBS_TIME desc"
    elif code == 'IE_0061': #신안가거초
        sqlStr  = f"select OBS_VALUE from GR_OBS_ST where OBS_POST_ID = '{code}'  "
        sqlStr += f"and OBS_TIME >= sysdate-1  "
        sqlStr += f"and OBS_ITEM_CODE = 'Hm0'  "
        sqlStr += f"and ROWNUM = 1  "
        sqlStr += f"order by OBS_TIME desc"
    elif code == 'IE_0062': #웅진소청초
        sqlStr  = f"select OBS_VALUE from GR_OBS_ST where OBS_POST_ID = '{code}'  "
        sqlStr += f"and OBS_TIME >= sysdate-1  "
        sqlStr += f"and OBS_ITEM_CODE = 'SOMWR_Hm0'  "
        sqlStr += f"and ROWNUM = 1  "
        sqlStr += f"order by OBS_TIME desc"
    cur.execute(sqlStr)
    row = cur.fetchall()
    if len(row):
        MWHT = row[0][0]
        if MWHT == 0 :
            MWHT = Miss
        else :
            MWHT = MWHT
    else:
        MWHT = Miss
    print(TYPE, STN, SST, MWHT)
    data1.append([TYPE, STN, SST, MWHT])              # data1[]에 자료 붙여넣기

#-----------------------------------[해양관측부이 자료수집]-----------------------------------------
BUOY_INF = open('./Info/BUOY_STATION_INFO.csv','r',encoding='utf8')
BUOY_STN = [str(INFO) for INFO in BUOY_INF.read().split()]
print(BUOY_STN)
print(today,"KHOA Ocean-buoy obs data collection...","correction time", hr)

for code in BUOY_STN:
    if len(code) < 5:
        continue
    else:
        STN  = obsdf.NAME[code]
        TYPE = obsdf.TYPE[code]
    ## SST
    if   code[0:2] == 'TW':
        sqlStr  = f"select OBS_VALUE from GD_OBS_BU where OBS_POST_ID = '{code}'  "
        sqlStr += f"and OBS_TIME >= sysdate-1  "
        sqlStr += f"and OBS_ITEM_CODE = 'WATER_TEMP'  "
        sqlStr += f"and ROWNUM = 1  "
        sqlStr += f"order by OBS_TIME desc"
    elif code[0:2] == 'KG':
        sqlStr  = f"select OBS_VALUE from GD_OBS_VBU where OBS_POST_ID = '{code}'  "
        sqlStr += f"and OBS_TIME >= sysdate-1  "
        sqlStr += f"and OBS_ITEM_CODE = 'WATER_TEMP'  "
        sqlStr += f"and ROWNUM = 1  "
        sqlStr += f"order by OBS_TIME desc"
    cur.execute(sqlStr)
    row = cur.fetchall()
    if len(row):
        SST = row[0][0]
        if SST == 0 :
            SST = Miss
        else :
            SST=SST
    else:
        SST = Miss
    ## MWHT
    if   code[0:2] == 'TW':
        sqlStr  = f"select OBS_VALUE from GD_OBS_BU where OBS_POST_ID = '{code}'  "
        sqlStr += f"and OBS_TIME >= sysdate-1  "
        sqlStr += f"and OBS_ITEM_CODE = 'SIGNIFI_WAVE_HEIGHT'  "
        sqlStr += f"and ROWNUM = 1  "
        sqlStr += f"order by OBS_TIME desc"
    elif code[0:2] == 'KG':
        sqlStr  = f"select 0.01*OBS_VALUE from GD_OBS_VBU where OBS_POST_ID = '{code}'  "
        sqlStr += f"and OBS_TIME >= sysdate-1  "
        sqlStr += f"and OBS_ITEM_CODE = 'MOSE_HF_SIGNIFI_WAVE_HEIGHT'  "
        sqlStr += f"and ROWNUM = 1  "
        sqlStr += f"order by OBS_TIME desc"
    cur.execute(sqlStr)
    row = cur.fetchall()
    if len(row):
        MWHT = row[0][0]
        if MWHT == 0 :
            MWHT = Miss
        else :
            MWHT = MWHT
    else:
        MWHT = Miss
    print(TYPE, STN, SST, MWHT)
    data2.append([TYPE, STN, SST, MWHT])              # data2[]에 자료 붙여넣기
    
#[DB Close]
cur.close()
con.close()

#[Writing Results]
if hr < '12':
    with open(dir1+'/KHOA_OBS_AM.csv','w',encoding='utf8') as file:
        file.write('OBS, STN, SST, MWHT\n')
        for i in data1:
            file.write('{0},{1},{2},{3}\n'.format(i[0], i[1], i[2], i[3]))
        for i in data2:
            file.write('{0},{1},{2},{3}\n'.format(i[0], i[1], i[2],i[3]))      
    #    for i in data3:
    #        file.write('국내등표,{0},{1},{2}\n'.format(i[0], i[1], i[2]))         
else:
    with open(dir1+'/KHOA_OBS_PM.csv','w',encoding='utf8') as file:
        file.write('OBS, STN, SST, MWHT\n')
        for i in data1:
            file.write('{0},{1},{2},{3}\n'.format(i[0], i[1], i[2],i[3]))      
        for i in data2:
            file.write('{0},{1},{2},{3}\n'.format(i[0], i[1], i[2],i[3]))      
    #    for i in data3:
    #        file.write('국내등표,{0},{1},{2}\n'.format(i[0], i[1], i[2]))
    if not os.path.exists(dir1+'/KHOA_OBS_AM.csv'): shutil.copy(dir1+'/KHOA_OBS_PM.csv', dir1+'/KHOA_OBS_AM.csv') #12시 이후에 AM자료가 없으면 PM자료 복사해서 이름 바꾸기

print("#KOHA OBS data collection Complete==========")
