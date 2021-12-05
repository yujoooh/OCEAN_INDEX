#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.08.08]
import sys
import os
import shutil
import numpy as np
from datetime import date, timedelta
from datetime import datetime

print("#Data Collect error check  Start==========")
#[Date set] ==============================================================================================
#today = str(datetime.today().strftime('%Y%m%d'))
#yesterday = (date.today() - timedelta(1)).strftime('%Y%m%d')

#[Manual date set2] 외부변수 받아오기
var1 = sys.argv[1] ; var2 = sys.argv[2]; var3 = sys.argv[3]
today = str(date(int(var1),int(var2),int(var3)).strftime('%Y%m%d'))
yesterday = (date(int(var1),int(var2),int(var3)) - timedelta(1)).strftime('%Y%m%d')
#print(today, afterday1, afterday2)

#today='20191107'
dir1 = './Result/'+today

HR = str(datetime.today().strftime('%H'))
#[Manual date set]
#HR = '10'
if int(HR) <12 : AMPM = 'AM'
if int(HR) >= 12 : AMPM = 'PM'

#[Real Time OBS DATA]
if not os.path.exists(dir1+'/KMA_OBS_AM.csv'): shutil.copy('./Info/KMA_OBS_MISSING.csv', dir1+'/KMA_OBS_AM.csv') #조사원 자료수집 에러발생시 Missing 값으로 넣기.
if not os.path.exists(dir1+'/KMA_OBS_PM.csv'): shutil.copy('./Info/KMA_OBS_MISSING.csv', dir1+'/KMA_OBS_PM.csv') #조사원 자료수집 에러발생시 Missing 값으로 넣기.
if not os.path.exists(dir1+'/KHOA_OBS_AM.csv'): shutil.copy('./Info/KHOA_OBS_MISSING.csv', dir1+'/KHOA_OBS_AM.csv') #조사원 자료수집 에러발생시 Missing 값으로 넣기.
if not os.path.exists(dir1+'/KHOA_OBS_PM.csv'): shutil.copy('./Info/KHOA_OBS_MISSING.csv', dir1+'/KHOA_OBS_PM.csv') #조사원 자료수집 에러발생시 Missing 값으로 넣기.

##[Yesterday OBS DATA]
#if not os.path.exists(dir1+'/OBS_DAILY/KMA_OBS_'+yesterday+'.csv'): shutil.copy('./Info/KMA_OBS_MISSING.csv', dir1+'/KMA_OBS_'+AMPM+'.csv') #조사원 자료수집 에러발생시 Missing 값으로 넣기.
#if not os.path.exists(dir1+'/OBS_DAILY/KHOA_OBS_'+yesterday+'.csv'): shutil.copy('./Info/KHOA_OBS_MISSING.csv', dir1+'/KHOA_OBS_'+AMPM+'.csv') #조사원 자료수집 에러발생시 Missing 값으로 넣기.

print("#Data Collect error check Complete==========")