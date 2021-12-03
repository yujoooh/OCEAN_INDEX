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
today = str(datetime.today().strftime('%Y%m%d'))
yesterday = (date.today() - timedelta(1)).strftime('%Y%m%d')
#today='20191107'
dir1 = './Result/'+today

HR = str(datetime.today().strftime('%H'))
#[Manual date set]
#HR = '10'
if int(HR) <12 : AMPM = 'AM'
if int(HR) >= 12 : AMPM = 'PM'

#[Real Time OBS DATA]
if not os.path.exists(dir1+'/KMA_WARNING.csv'):
	f = open('./Info/KMA_WARNING_M.csv', 'r', encoding = 'UTF8')
	f2 = open('./Info/KMA_WARNING.csv', 'w', encoding = 'UTF8')
	line = f.read().replace('YYYYMMDD', today)
	print(line)
	f2.write(line)
	f.close()
	f2.close()
	shutil.copy('./Info/KMA_WARNING.csv', dir1+'/KMA_WARNING.csv') # 특보 자료수집 에러발생 시 Missing 값으로 넣기.
	os.remove('./Info/KMA_WARNING.csv')
	exit()
if not os.path.exists(dir1+'/KMA_OBS_AM.csv'): shutil.copy('./Info/KMA_OBS_MISSING.csv', dir1+'/KMA_OBS_AM.csv') #조사원 자료수집 에러발생시 Missing 값으로 넣기.
if not os.path.exists(dir1+'/KMA_OBS_PM.csv'): shutil.copy('./Info/KMA_OBS_MISSING.csv', dir1+'/KMA_OBS_PM.csv') #조사원 자료수집 에러발생시 Missing 값으로 넣기.
if not os.path.exists(dir1+'/KHOA_OBS_AM.csv'): shutil.copy('./Info/KHOA_OBS_MISSING.csv', dir1+'/KHOA_OBS_AM.csv') #조사원 자료수집 에러발생시 Missing 값으로 넣기.
if not os.path.exists(dir1+'/KHOA_OBS_PM.csv'): shutil.copy('./Info/KHOA_OBS_MISSING.csv', dir1+'/KHOA_OBS_PM.csv') #조사원 자료수집 에러발생시 Missing 값으로 넣기.

##[Yesterday OBS DATA]
#if not os.path.exists(dir1+'/OBS_DAILY/KMA_OBS_'+yesterday+'.csv'): shutil.copy('./Info/KMA_OBS_MISSING.csv', dir1+'/KMA_OBS_'+AMPM+'.csv') #조사원 자료수집 에러발생시 Missing 값으로 넣기.
#if not os.path.exists(dir1+'/OBS_DAILY/KHOA_OBS_'+yesterday+'.csv'): shutil.copy('./Info/KHOA_OBS_MISSING.csv', dir1+'/KHOA_OBS_'+AMPM+'.csv') #조사원 자료수집 에러발생시 Missing 값으로 넣기.

print("#Data Collect error check Complete==========")
