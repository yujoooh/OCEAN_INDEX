import pandas as pd
import numpy as np
import os
import shutil
import sys
from datetime import date, timedelta, datetime

#auto date set
today = str(datetime.today().strftime('%Y%m%d'))
afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')
afterday3 = (date.today() + timedelta(3)).strftime('%Y%m%d')
afterday4 = (date.today() + timedelta(4)).strftime('%Y%m%d')
afterday5 = (date.today() + timedelta(5)).strftime('%Y%m%d')
afterday6 = (date.today() + timedelta(6)).strftime('%Y%m%d')
#print(today, afterday6)

#manual date set 
# today = str(date(2021,5,18).strftime('%Y%m%d'))
# afterday1 = (date(2021,5,18) + timedelta(1)).strftime('%Y%m%d')
# afterday2 = (date(2021,5,18) + timedelta(2)).strftime('%Y%m%d')
# afterday3 = (date(2021,5,18) + timedelta(3)).strftime('%Y%m%d')
# afterday4 = (date(2021,5,18) + timedelta(4)).strftime('%Y%m%d')
# afterday5 = (date(2021,5,18) + timedelta(5)).strftime('%Y%m%d')
# afterday6 = (date(2021,5,18) + timedelta(6)).strftime('%Y%m%d')
# print(today, afterday6)

#산출물 폴더(특보 정보 있음)
dir_result = './Result/'+today
dir1 = './Result/'+today
#dir2 = 'D:/LIFE_OCEAN_INDEX/Source/Result/'+today

# AM_FCST = pd.read_csv(dir_result+'/'+ today+ '_SURFING_INDEX_SERVICE_AM.csv',encoding='utf8')
# PM_FCST = pd.read_csv(dir_result+'/'+ today+ '_SURFING_INDEX_SERVICE_PM.csv',encoding='utf8')
AM_FCST = pd.read_csv(dir_result+'/'+ today+ '_SREQ_INDEX_FCST_AM.csv',encoding='utf8')
PM_FCST = pd.read_csv(dir_result+'/'+ today+ '_SREQ_INDEX_FCST_PM.csv',encoding='utf8')
#FCST_MID = pd.read_csv(dir_result+'/'+ today+ '_SREQ_INDEX_FCST_MID.csv',encoding='utf8')
# AM_SERVICE = pd.read_csv(dir_result+'/SURFING_INDEX_SERVICE_last_AM'+today+'.csv',encoding='euckr')
# PM_SERVICE = pd.read_csv(dir_result+'/SURFING_INDEX_SERVICE_last_PM'+today+'.csv',encoding='euckr')
AM_SERVICE = pd.read_csv(dir_result+'/'+today+'_SREQ_INDEX_SERVICE_AM.csv',encoding='utf8')
PM_SERVICE = pd.read_csv(dir_result+'/'+today+'_SREQ_INDEX_SERVICE_PM.csv',encoding='utf8')
#SERVICE_MID = pd.read_csv(dir_result+'/'+today+'_SREQ_INDEX_SERVICE_MID.csv',encoding='utf8')

#4일이후자료 다 날리기
#AM_FCST = AM_FCST[AM_FCST['예측날짜']<=int(afterday2)].copy()
#PM_FCST = PM_FCST[PM_FCST['예측날짜']<=int(afterday2)].copy()
#AM_SERVICE = AM_SERVICE[AM_SERVICE['예측날짜']<=int(afterday2)].copy()
#PM_SERVICE = PM_SERVICE[PM_SERVICE['예측날짜']<=int(afterday2)].copy()

AM_FCST.insert(4, '오전오후', 'AM')
PM_FCST.insert(4, '오전오후', 'PM')
#FCST_MID.insert(4, '오전오후', 'MID')
AM_SERVICE.insert(4, '오전오후', 'AM')
PM_SERVICE.insert(4, '오전오후', 'PM')

#SERVICE_MID.insert(4, '오전오후', 'MID')

total_fcst = AM_FCST.append(PM_FCST)

#total_fcst = total_fcst.append(FCST_MID)
total_service = AM_SERVICE.append(PM_SERVICE)
#total_service = total_service.append(SERVICE_MID)

total_fcst = total_fcst.sort_values(by=['예측날짜', '오전오후'])
total_service = total_service.sort_values(by=['예측날짜', '오전오후'])


#20210628
column_fcst = ['산출날짜', '코드', '구분','지역', '예측날짜', '오전오후', '유의파고', '파고점수', '파향', '상대파향', '파향점수', '파주기',
                                                      '파주기점수','풍속', '풍향', '풍속점수', '수온', '수온점수', '총점수', '예보지수']

column_service = ['산출날짜', '코드', '구분','지역', '예측날짜', '오전오후', '유의파고', '파고점수', '파향', '상대파향', '파향점수', '파주기',
                                                      '파주기점수','풍속', '풍향', '풍속점수', '수온', '수온점수', '특보', '특보점수', '총점수', '예보지수']

total_fcst = total_fcst.reindex(columns = column_fcst)
total_service = total_service.reindex(columns = column_service)

# 각각 뜯어보고싶을때
# total_fcst.to_csv('./Result/'+today+'/'+today+'_SURFING_FCST_TOTAL.csv', encoding = 'euckr', index=False)
# total_service.to_csv('./Result/'+today+'/'+today+'_SURFING_SERVICE_TOTAL.csv', encoding = 'euckr', index=False)

total_fcst.to_csv('./Result/'+today+'/SREQ_INDEX_FCST_'+today+'.csv', encoding = 'utf8', index=False)
total_service.to_csv('./Result/'+today+'/SREQ_INDEX_SERVICE_'+today+'.csv', encoding = 'utf8', index=False)

shutil.copy(dir1+'/SREQ_INDEX_FCST_'+today+'.csv', dir2+'/SREQ_INDEX_FCST_'+today+'.csv')
shutil.copy(dir1+'/SREQ_INDEX_SERVICE_'+today+'.csv', dir2+'/SREQ_INDEX_SERVICE_'+today+'.csv')

#os.remove('./Result/'+today+'/'+today+'_SREQ_INDEX_FCST_AM.csv')
#os.remove('./Result/'+today+'/'+today+'_SREQ_INDEX_FCST_PM.csv')
#os.remove('./Result/'+today+'/'+today+'_SREQ_INDEX_SERVICE_AM.csv')
#os.remove('./Result/'+today+'/'+today+'_SREQ_INDEX_SERVICE_PM.csv')
#os.remove('./Result/'+today+'/'+today+'_SREQ_INDEX_FCST_MID.csv')
#os.remove('./Result/'+today+'/'+today+'_SREQ_INDEX_SERVICE_MID.csv')
