import pandas as pd
import time as checktime
from netCDF4 import Dataset
import numpy as np
import lunardate as lunar
from datetime import date, timedelta, datetime
import pandas as pd
import os
import sys
from Function.surfing_function import IndexScore

# auto date set
today = str(datetime.today().strftime('%Y%m%d'))
afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')
afterday3 = (date.today() + timedelta(3)).strftime('%Y%m%d')
afterday4 = (date.today() + timedelta(4)).strftime('%Y%m%d')
afterday5 = (date.today() + timedelta(5)).strftime('%Y%m%d')
afterday6 = (date.today() + timedelta(6)).strftime('%Y%m%d')
#print(today, afterday6)

# manual date set
#yyyymmdd = str(sys.argv[1])
#today = yyyymmdd
# today = str(date(2021,5,18).strftime('%Y%m%d'))
# afterday1 = (date(2021,5,18) + timedelta(1)).strftime('%Y%m%d')
# afterday2 = (date(2021,5,18) + timedelta(2)).strftime('%Y%m%d')
# afterday3 = (date(2021,5,18) + timedelta(3)).strftime('%Y%m%d')
# afterday4 = (date(2021,5,18) + timedelta(4)).strftime('%Y%m%d')
# afterday5 = (date(2021,5,18) + timedelta(5)).strftime('%Y%m%d')
# afterday6 = (date(2021,5,18) + timedelta(6)).strftime('%Y%m%d')
# print(today, afterday6)

COM_INDEX = pd.DataFrame(index=range(0), columns=['구분', '지역', '예측날짜', '유의파고', '파고점수', '파향', '상대파향', '파향점수', '파주기',
                                                  '파주기점수', '풍속', '풍향', '풍속점수', '수온', '수온점수', '특보', '특보점수', '총점수', '예보지수', '코드'])
# 20210628
COM_INDEX2 = pd.DataFrame(index=range(0), columns=['구분', '지역', '예측날짜', '유의파고', '파고점수', '파향', '상대파향', '파향점수', '파주기',
                                                   '파주기점수', '풍속', '풍향', '풍속점수', '수온', '수온점수', '총점수', '예보지수', '코드'])

COM = pd.read_csv('./Result/'+today+'/SR_TMESERIES_'+today+'.csv')

# 서핑포인트 정보 읽어옴
POINT_df = pd.read_csv('./Info/SR_Point_Info_2.csv', index_col=['STN'])

for i in range(len(POINT_df)):
    FCST_AREA = POINT_df['AREA'][i]
    WARN_AREA = POINT_df['WARN_SEA'][i]
    CODE = POINT_df['CODE'][i]
    NAME = POINT_df['NAME'][i]
    BEACH_DIR = POINT_df['BEACH_DIR'][i]
    for date in COM['DATE'].unique().tolist():
        if date >= int(today):
            # [WW3]
            mean_WHT = round(COM['WHT'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (
                COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 9)].mean(), 1)
            mean_WAVEX = COM['Wavex'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (
                COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 9)].mean()
            mean_WAVEY = COM['Wavey'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (
                COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 9)].mean()
            mean_WAVEDIR = round(np.rad2deg(
                np.arctan2(mean_WAVEY, mean_WAVEX)), 0)
            # print(mean_WAVEDIR)
            if mean_WAVEDIR < 0:
                mean_WAVEDIR = mean_WAVEDIR + 360
            #print('1', mean_WAVEDIR)
            #mean_WAVEDIR = COM['Wavedir'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 9) ].mean()
            mean_R_WAVEDIR = round(mean_WAVEDIR - BEACH_DIR, 0)
            mean_RPEAK = round(COM['Rpeak'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (
                COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 9)].mean(), 1)
            # [WRF]
            mean_WINDS = round(COM['풍속'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (
                COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 9)].mean(), 1)
            mean_WINDDIR = COM['풍향'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (
                COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 9)].mean()
            # [YES3K]
            mean_TEMP = round(COM['수온'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (
                COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 9)].mean(), 1)

            warning = COM['특보'][(COM['FCST_AREA'] == FCST_AREA) & (
                COM['NAME'] == NAME) & (COM['DATE'] == date)].unique()
            if len(warning) != 1:
                #print("특보적용이 이상합니다")
                warning = warning[0]
            else:
                warning = warning[0]
                print(warning)
            WAVE_SCRE = IndexScore().wave_score(mean_WHT)
            RPEAK_SCRE = IndexScore().Rpeak_score(mean_RPEAK)
            WAVEDIR_SCRE = IndexScore().wave_dir_score(mean_R_WAVEDIR)
            # [WRF]
            WIND_SCRE = IndexScore().wind_score(mean_WINDS)

            # [YES3K]
            TEMP_SCRE = IndexScore().temp_score(mean_TEMP)

            # [특보점수]
            WARN_SCRE = IndexScore().warn_score(warning)

            TOTAL_SCRE1 = IndexScore().total_score(WAVE_SCRE, RPEAK_SCRE,
                                                   WAVEDIR_SCRE, WIND_SCRE, TEMP_SCRE, WARN_SCRE)[0]
            TOTAL_SCRE2 = IndexScore().total_score(WAVE_SCRE, RPEAK_SCRE,
                                                   WAVEDIR_SCRE, WIND_SCRE, TEMP_SCRE, WARN_SCRE)[1]

            QUOTIENT_SCRE1 = IndexScore().quotient_score(
                TOTAL_SCRE1)  # forecast score(no rain, no warning)
            QUOTIENT_SCRE2 = IndexScore().quotient_score(TOTAL_SCRE2)  # service score

            #row = [FCST_AREA, NAME, date, mean_WHT, WAVE_SCRE, mean_WAVEDIR, mean_R_WAVEDIR, WAVEDIR_SCRE, mean_RPEAK, RPEAK_SCRE, mean_WINDS, mean_WINDDIR, WIND_SCRE, mean_TEMP, TEMP_SCRE, warning, WARN_SCRE, TOTAL_SCRE2,  QUOTIENT_SCRE2]
            #row2 = [FCST_AREA, NAME, date, mean_WHT, WAVE_SCRE, mean_WAVEDIR, mean_R_WAVEDIR, WAVEDIR_SCRE, mean_RPEAK, RPEAK_SCRE, mean_WINDS, mean_WINDDIR, WIND_SCRE, mean_TEMP, TEMP_SCRE, TOTAL_SCRE1,  QUOTIENT_SCRE1]
            print(CODE, NAME)
            # 20210628
            row = [FCST_AREA, NAME, date, round(mean_WHT, 1), WAVE_SCRE, round(mean_WAVEDIR, 0), round(mean_R_WAVEDIR, 0), WAVEDIR_SCRE, round(mean_RPEAK, 1), RPEAK_SCRE, round(
                mean_WINDS, 1), round(mean_WINDDIR, 0), WIND_SCRE, round(mean_TEMP, 1), TEMP_SCRE, warning, WARN_SCRE, TOTAL_SCRE2,  QUOTIENT_SCRE2, CODE]
            row2 = [FCST_AREA, NAME, date, round(mean_WHT, 1), WAVE_SCRE, round(mean_WAVEDIR, 0), round(mean_R_WAVEDIR, 0), WAVEDIR_SCRE, round(
                mean_RPEAK, 1), RPEAK_SCRE, round(mean_WINDS, 1), round(mean_WINDDIR, 0), WIND_SCRE, round(mean_TEMP, 1), TEMP_SCRE, TOTAL_SCRE1,  QUOTIENT_SCRE1, CODE]
            COM_INDEX = COM_INDEX.append(
                pd.Series(row, index=COM_INDEX.columns), ignore_index=True)
            COM_INDEX2 = COM_INDEX2.append(
                pd.Series(row2, index=COM_INDEX2.columns), ignore_index=True)
        else:
            pass

COM_INDEX = COM_INDEX.sort_values(by=['예측날짜'])
COM_INDEX2 = COM_INDEX2.sort_values(by=['예측날짜'])
COM_INDEX.insert(0, '산출날짜', today)
COM_INDEX2.insert(0, '산출날짜', today)

COM_INDEX2.to_csv('./Result/'+today+'/SREQ_INDEX_FCST_onair_'+today+'.csv', encoding='utf8', index=False)
#COM_INDEX2.to_csv('./Result/'+today+'/'+today+'_SURFING_INDEX_FCST_mid_euckr.csv', encoding = 'euc-kr', index=False)
COM_INDEX.to_csv('./Result/'+today+'/SREQ_INDEX_SERVICE_onair_'+today+'.csv', encoding='utf8', index=False)
#COM_INDEX.to_csv('./Result/'+today+'/'+today+'_SURFING_INDEX_SERVICE_mid_euckr.csv', encoding = 'euc-kr', index=False)
