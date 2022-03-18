import sys
import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset
from datetime import date, timedelta
from datetime import datetime
from Function.surfing_function import IndexScore
from Function.statistic_function import Statistic

print("#SURFING SERVICE_INDEX CREAT Start==========")

# [Date set] ==============================================================================================

# [Manual date set]
today = str(datetime.today().strftime('%Y%m%d'))
afterday1 = (datetime.strptime(today, "%Y%m%d") +
             timedelta(1)).strftime('%Y%m%d')
afterday2 = (datetime.strptime(today, "%Y%m%d") +
             timedelta(2)).strftime('%Y%m%d')
afterday3 = (datetime.strptime(today, "%Y%m%d") +
             timedelta(3)).strftime('%Y%m%d')
afterday4 = (datetime.strptime(today, "%Y%m%d") +
             timedelta(4)).strftime('%Y%m%d')
afterday5 = (datetime.strptime(today, "%Y%m%d") +
             timedelta(5)).strftime('%Y%m%d')
afterday6 = (datetime.strptime(today, "%Y%m%d") +
             timedelta(6)).strftime('%Y%m%d')

# today = str(date(2021,5,18).strftime('%Y%m%d'))
# afterday1 = (date(2021,5,18) + timedelta(1)).strftime('%Y%m%d')
# afterday2 = (date(2021,5,18) + timedelta(2)).strftime('%Y%m%d')
# afterday3 = (date(2021,5,18) + timedelta(3)).strftime('%Y%m%d')
# afterday4 = (date(2021,5,18) + timedelta(4)).strftime('%Y%m%d')
# afterday5 = (date(2021,5,18) + timedelta(5)).strftime('%Y%m%d')
# afterday6 = (date(2021,5,18) + timedelta(6)).strftime('%Y%m%d')

dir1 = './Result/'+today

mon = date.today().month  # 자료 생산일 기준 월 구분
hr = float(datetime.today().strftime("%H"))

hr = 10  # manual

SURFING_INF = open(dir1+'/SREQ_INDEX_SERVICE_onair_'+today+'.csv', encoding='utf8')
SURFING = [LST for LST in SURFING_INF.read().split()]
SURFING_LEN = len(SURFING)

fdata = []
rawdata = []
ii = 1
while ii < SURFING_LEN:
    DEV = SURFING[ii].split(',')
#   0   1 2   3    4   5    6  7     8    9     10    11   12   13   14   15    16   17   18    19    20    21   22    23  24  25   26
# '코드,권역,지역,예측일자,어종,어종타입,물때,물때점수,최소파고,평균파고,최대파고,파고점수,최소수온,평균수온,최대수온,수온점수,최저기온,평균기온,최대기온,기온점수,최소풍속,평균풍속,최대풍속,풍속점수,특보,특보점수,총점수
    CODE = DEV[20]
    Area = DEV[1]
    Point = DEV[2]
    FDATE = DEV[3]
    #MIN_WHT = DEV[8]; MAX_WHT = DEV[10]
    AVE_WHT = DEV[4]
    AVE_WAVEDIR = DEV[6]
    AVE_R_WAVEDIR = DEV[7]
    AVE_RPEAK = float(DEV[9])
    AVE_WIND = float(DEV[11])
    AVE_WINDDIR = float(DEV[12])
    AVE_SST = float(DEV[14])
    #MIN_SST = DEV[12] ; AVE_SST = DEV[13] ; MAX_SST = DEV[14]
    #MIN_TEMP = DEV[16] ; AVE_TEMP = DEV[17] ; MAX_TEMP = DEV[18]
    #MIN_WIND = DEV[20] ; AVE_WIND = DEV[21] ; MAX_WIND = DEV[22]

    # 칼럼늘어나면 여기 바꿔야됨
    WARN = DEV[16]

    # print(WARN)

    # 파향 들어올 경우 여기 수정해야함
    fdata.append([Point, FDATE, AVE_WHT, AVE_WAVEDIR,
                  AVE_R_WAVEDIR, AVE_SST, AVE_RPEAK])
    rawdata.append([CODE, Area, Point, FDATE, AVE_WHT, AVE_WAVEDIR,
                    AVE_R_WAVEDIR, AVE_RPEAK, AVE_WIND, AVE_WINDDIR, AVE_SST, WARN])
    ii += 1

odata = []
if hr < 12:  # 오전자료 읽기
    AM_DATA = open(dir1+'/SR_POINT_OBS_AM.csv', 'r', encoding='utf8')
    AM = [LST for LST in AM_DATA.read().split()]
    AM_LEN = len(AM)
    check = 'am'

    ii = 0
    while ii < AM_LEN:
        DEV = AM[ii].split(',')
        # print(DEV)
        odata.append(DEV)
        ii = ii + 1
Ver_DATA = open('./Info/Verification.csv', 'r', encoding='utf8')
Ver = Ver_DATA.readlines()
WEST_WHT = Ver[1].split(",")  # 서해 파고 RMSE
SOUTH_WHT = Ver[2].split(",")  # 동해 파고 RMSE
EAST_WHT = Ver[3].split(",")  # 남해 파고 RMSE
# WEST_SST = Ver[4].split(",") # 서해 수온 RMSE
# SOUTH_SST = Ver[5].split(",") # 남해 수온 RMSE
# EAST_SST = Ver[6].split(",") # 동해 수온 RMSE

WEST_RMSE_WHT = float(WEST_WHT[mon])
SOUTH_RMSE_WHT = float(SOUTH_WHT[mon])
EAST_RMSE_WHT = float(EAST_WHT[mon])
#WEST_RMSE_SST = float(WEST_SST[mon]) ; SOUTH_RMSE_SST = float(SOUTH_SST[mon]) ; EAST_RMSE_SST = float(EAST_SST[mon])


POINT_df = pd.read_csv('./Info/SR_Point_Info_2.csv', index_col=['STN'])
for kk in range(len(odata)):
    for nn in range(len(POINT_df)):
        if odata[kk][0] == POINT_df['NAME'][nn]:
            # print(odata[kk][0])
            odata[kk].insert(3, float(odata[kk][2]) -
                             POINT_df['BEACH_DIR'][nn])
            #odata[kk][3] = float(odata[kk][2]) - POINT_df['BEACH_DIR'][nn]
            # print(odata[kk][3])
#     for i in range(len(POINT_df)):
#         BEACH_DIR = POINT_df['BEACH_DIR'][i])

kk = 0
apply1 = []
while kk < int((SURFING_LEN-1)*2/7):
    mm = 0
    while mm < AM_LEN:
        if fdata[kk][0] == odata[mm][0]:  # 예보지역과 관측지역 일치여부
            #print(fdata[kk][0], odata[mm][0])
            Diff_Point = fdata[kk][0]
            # 1일은 그냥 관측자료로 넣기----------------------------------------------------------------
            if fdata[kk][1] == today:
                if odata[mm][4] == '-999.0':
                    apply_SST = round(float(fdata[kk][5]), 2)
                    obj_SST = "fcst"
                else:
                    apply_SST = round(float(odata[mm][4]), 2)
                    obj_SST = "obs"
                if odata[mm][1] == '-999.0':
                    apply_WHT = round(float(fdata[kk][2]), 10)
                    obj_WHT = "fcst"
                    # print(obj_WHT)
                else:
                    apply_WHT = round(float(odata[mm][1]), 2)
                    obj_WHT = "obs"
                    # print(obj_WHT)

                if odata[mm][2] == '-999.0':
                    apply_WDIR = round(float(fdata[kk][3]), 10)
                    obj_WDIR = "fcst"
# 상대파향추가
                    apply_RWDIR = round(float(fdata[kk][4]), 10)
                    obj_RWDIR = "fcst"
                    # print(obj_WDIR)
                else:
                    apply_WDIR = round(float(odata[mm][2]), 2)
                    obj_WDIR = "obs"
                    apply_RWDIR = round(float(odata[mm][3]), 2)
                    obj_RWDIR = "obs"
                    # print(obj_WDIR)
                if odata[mm][5] == '-999.0':
                    apply_RPEAK = round(float(fdata[kk][6]), 10)
                    obj_RPEAK = "fcst"
                    # print(obj_WHT)
                else:
                    apply_RPEAK = round(float(odata[mm][5]), 2)
                    obj_RPEAK = "obs"
            # 2일은 예측값과 비교 후 벗어나면 관측자료로 대체----------------------------------------------------------------
            elif fdata[kk][1] == afterday1:
                # 				if odata[mm][1] == '-999.0' : # Missing value면 차이 0으로 설정
                # 					Diff_SST = 0
                # 				else:
                # 					Diff_SST = abs(round(float(fdata[kk][3]) - float(odata[mm][1]),2))

                # 				#해역별 RMSE 비교  : apply_는 적용할 자료------------------------------------
                # 				if odata[mm][3] == '서해':
                # 					if Diff_SST > WEST_RMSE_SST:
                # 						apply_SST = round(float(odata[mm][1]),2)
                # 						obj_SST = "obs"
                # 					else:
                # 						apply_SST = round(float(fdata[kk][3]),2)
                # 						obj_SST = "fcst"

                # 				elif odata[mm][3] == '남해':
                # 					if Diff_SST > SOUTH_RMSE_SST:
                # 						apply_SST = round(float(odata[mm][1]),2)
                # 						obj_SST = "obs"
                # 					else:
                # 						apply_SST = round(float(fdata[kk][3]),2)
                # 						obj_SST = "fcst"

                # 				elif odata[mm][3] == '동해':
                # 					if Diff_SST > EAST_RMSE_SST:
                # 						apply_SST = round(float(odata[mm][1]),2)
                # 						obj_SST = "obs"
                # 					else:
                # 						apply_SST = round(float(fdata[kk][3]),2)
                # 						obj_SST = "fcst"

                # 				else:#한반도 RMSE
                # 					if Diff_SST > KOR_RMSE_SST:
                # 						apply_SST = round(float(odata[mm][1]),2)
                # 					else:
                # 						apply_SST = round(float(fdata[kk][3]),2)

                apply_WHT = round(float(fdata[kk][2]), 10)
                obj_WHT = "fcst"
                apply_WDIR = round(float(fdata[kk][3]), 10)
                obj_WDIR = "fcst"
                apply_RWDIR = round(float(fdata[kk][4]), 10)
                obj_RWDIR = "fcst"
                apply_SST = round(float(fdata[kk][5]), 10)
                obj_SST = "fcst"
                apply_RPEAK = round(float(fdata[kk][6]), 10)
                obj_RPEAK = "fcst"

            # print(fdata[kk][1])
            apply1.append([Diff_Point, fdata[kk][1], obj_WHT, apply_WHT, obj_WDIR, apply_WDIR,
                           obj_RWDIR, apply_RWDIR, obj_SST, apply_SST, obj_RPEAK, apply_RPEAK])

            # print(kk,Diff_Point,fdata[kk][1],obj_SST,apply_SST,obj_WHT,apply_WHT)
        mm += 1
    kk = kk + 1

kk = int((SURFING_LEN-1)*2/7)
nn = int((SURFING_LEN-1)/7)
# print(kk,nn)
while kk < int((SURFING_LEN-1)*3/7):
    mm = 0
    while mm < AM_LEN:
        if fdata[kk][0] == odata[mm][0]:  # 예보지역과 관측지역 일치여부
            Diff_Point = odata[mm][0]
#            print(fdata[kk][0], odata[mm][0], float(apply1[nn][3]), float(fdata[kk][3]))
#            print(Diff_Point,apply1[nn][0])
            # 3일--------------------------------------------------------------------------
            if fdata[kk][1] == afterday2 and apply1[nn][1] == afterday1:
                #               if odata[mm][1] == '-999.0' : # Missing value면 차이 0으로 설정
                #                    Diff_SST = 0
                #                else:
                #                    Diff_SST = abs(round(float(apply1[nn][3]) - float(fdata[kk][3]),2))
                #
                #                if odata[mm][3] == '서해':
                #                    if Diff_SST > WEST_RMSE_SST:
                #                        apply_SST = round(float(odata[mm][1]),2)
                #                        obj_SST = "obs"
                #                    else:
                #                        apply_SST = round(float(fdata[kk][3]),2)
                #                        obj_SST = "fcst"
                #
                #                elif odata[mm][3] == '남해':
                #                    if Diff_SST > SOUTH_RMSE_SST:
                #                        apply_SST = round(float(odata[mm][1]),2)
                #                        obj_SST = "obs"
                #                    else:
                #                        apply_SST = round(float(fdata[kk][3]),2)
                #                        obj_SST = "fcst"
                #
                #                elif odata[mm][3] == '동해':
                #                    if Diff_SST > EAST_RMSE_SST:
                #                        apply_SST = round(float(odata[mm][1]),2)
                #                        obj_SST = "obs"
                #                    else:
                #                        apply_SST = round(float(fdata[kk][3]),2)
                #                        obj_SST = "fcst"

                apply_WHT = round(float(fdata[kk][2]), 10)
                obj_WHT = "fcst"
                apply_WDIR = round(float(fdata[kk][3]), 10)
                obj_WDIR = "fcst"
                apply_RWDIR = round(float(fdata[kk][4]), 10)
                obj_RWDIR = "fcst"
                apply_SST = round(float(fdata[kk][5]), 10)
                obj_SST = "fcst"
                apply_RPEAK = round(float(fdata[kk][6]), 10)
                obj_RPEAK = "fcst"

            apply1.append([Diff_Point, fdata[kk][1], obj_WHT, apply_WHT, obj_WDIR, apply_WDIR,
                           obj_RWDIR, apply_RWDIR, obj_SST, apply_SST, obj_RPEAK, apply_RPEAK])
            nn += 1
        mm += 1
    kk = kk + 1

while kk < int((SURFING_LEN-1)*4/7):
    #	apply_SST = round(float(fdata[kk][3]),2)
    #	obj_SST = "fcst"
    apply_WHT = round(float(fdata[kk][2]), 10)
    obj_WHT = "fcst"
    apply_WDIR = round(float(fdata[kk][3]), 10)
    obj_WDIR = "fcst"
    apply_RWDIR = round(float(fdata[kk][4]), 10)
    obj_RWDIR = "fcst"
    apply_SST = round(float(fdata[kk][5]), 10)
    obj_SST = "fcst"
    apply_RPEAK = round(float(fdata[kk][6]), 10)
    obj_RPEAK = "fcst"
    apply1.append([Diff_Point, fdata[kk][1], obj_WHT, apply_WHT, obj_WDIR, apply_WDIR,
                   obj_RWDIR, apply_RWDIR, obj_SST, apply_SST, obj_RPEAK, apply_RPEAK])
    kk = kk + 1
# print(kk)
# 5일은 예측값----------------------------------------------------------------

#kk = int((SURFING_LEN-1)*4/7)
while kk < int((SURFING_LEN-1)*5/7):
    #	apply_SST = round(float(fdata[kk][3]),2)
    #	obj_SST = "fcst"
    apply_WHT = round(float(fdata[kk][2]), 10)
    obj_WHT = "fcst"
    apply_WDIR = round(float(fdata[kk][3]), 10)
    obj_WDIR = "fcst"
    apply_RWDIR = round(float(fdata[kk][4]), 10)
    obj_RWDIR = "fcst"
    apply_SST = round(float(fdata[kk][5]), 10)
    obj_SST = "fcst"
    apply_RPEAK = round(float(fdata[kk][6]), 10)
    obj_RPEAK = "fcst"
    apply1.append([Diff_Point, fdata[kk][1], obj_WHT, apply_WHT, obj_WDIR, apply_WDIR,
                   obj_RWDIR, apply_RWDIR, obj_SST, apply_SST, obj_RPEAK, apply_RPEAK])
    kk = kk + 1
# print(kk)
# 6일은 예측값----------------------------------------------------------------

#kk = int((SURFING_LEN-1)*5/7)
while kk < int((SURFING_LEN-1)*6/7):
    #	apply_SST = round(float(fdata[kk][3]),2)
    #	obj_SST = "fcst"
    apply_WHT = round(float(fdata[kk][2]), 10)
    obj_WHT = "fcst"
    apply_WDIR = round(float(fdata[kk][3]), 10)
    obj_WDIR = "fcst"
    apply_RWDIR = round(float(fdata[kk][4]), 10)
    obj_RWDIR = "fcst"
    apply_SST = round(float(fdata[kk][5]), 10)
    obj_SST = "fcst"
    apply_RPEAK = round(float(fdata[kk][6]), 10)
    obj_RPEAK = "fcst"
    apply1.append([Diff_Point, fdata[kk][1], obj_WHT, apply_WHT, obj_WDIR, apply_WDIR,
                   obj_RWDIR, apply_RWDIR, obj_SST, apply_SST, obj_RPEAK, apply_RPEAK])
    kk = kk + 1
# print(kk)
# 7일은 예측값----------------------------------------------------------------

#kk = int((SURFING_LEN-1)*6/7)
while kk < int(SURFING_LEN-1):
    #	apply_SST = round(float(fdata[kk][3]),2)
    #	obj_SST = "fcst"
    apply_WHT = round(float(fdata[kk][2]), 10)
    obj_WHT = "fcst"
    apply_WDIR = round(float(fdata[kk][3]), 10)
    obj_WDIR = "fcst"
    apply_RWDIR = round(float(fdata[kk][4]), 10)
    obj_RWDIR = "fcst"
    apply_SST = round(float(fdata[kk][5]), 10)
    obj_SST = "fcst"
    apply_RPEAK = round(float(fdata[kk][6]), 10)
    obj_RPEAK = "fcst"
    apply1.append([Diff_Point, fdata[kk][1], obj_WHT, apply_WHT, obj_WDIR, apply_WDIR,
                   obj_RWDIR, apply_RWDIR, obj_SST, apply_SST, obj_RPEAK, apply_RPEAK])
    kk = kk + 1

ii = 0
COM = []
while ii < len(apply1):
    # print(ii,rawdata[ii][6],int(rawdata[ii][7]))
    #TIDE_SCRE = IndexScore().tide_score(rawdata[ii][6],int(rawdata[ii][7]))

    # 파랑
    WAVE_SCRE = IndexScore().wave_score(apply1[ii][3])
    RPEAK_SCRE = IndexScore().Rpeak_score(float(apply1[ii][11]))
    R_WAVEDIR_SCRE = IndexScore().wave_dir_score(float(apply1[ii][7]))
    # 수온

    # ppark
    TEMP_SCRE = IndexScore().temp_score(apply1[ii][9])
    # print(ii)
    # 풍속
    WIND_SCRE = IndexScore().wind_score(int(rawdata[ii][8]))
    # 특보점수
    WARN_SCRE = IndexScore().warn_score(rawdata[ii][11])

    # 예보점수 >>> 추후 이부분 다른 지표도 들어가도록 수정해야함
    TOTAL_SCRE2 = IndexScore().total_score(WAVE_SCRE, RPEAK_SCRE,
                                           R_WAVEDIR_SCRE, WIND_SCRE, TEMP_SCRE, WARN_SCRE)[1]
    # 예보지수
    QUOTIENT_SCRE2 = IndexScore().quotient_score(TOTAL_SCRE2)

    #print(WARN_SCRE, TOTAL_SCRE2, QUOTIENT_SCRE2)
    # TOTAL_SCRE1 = IndexScore().total_score(TIDE_SCRE, WAVE_SCRE, SST_SCRE, TEMP_SCRE, WIND_SCRE, WARN_SCRE)[0] # forecast score(no rain, no warning)
    # TOTAL_SCRE2 = IndexScore().total_score(TIDE_SCRE, WAVE_SCRE, SST_SCRE, TEMP_SCRE, WIND_SCRE, WARN_SCRE)[1] # service score(rain, warning)
    # QUOTIENT_SCRE1 = IndexScore().quotient_score(TOTAL_SCRE1) # forecast score(no rain, no warning)
    # QUOTIENT_SCRE2 = IndexScore().quotient_score(TOTAL_SCRE2) # service score(rain, warning)

    #MIN_WHT = round(float(apply1[ii][5])*float(fdata[ii][5])/float(fdata[ii][7]),1)
    AVE_WHT = apply1[ii][3]
    #MIN_SST = int(round(float(apply1[ii][3])*float(fdata[ii][2])/float(fdata[ii][3])))
    #MAX_SST = int(round(float(apply1[ii][3])*float(fdata[ii][4])/float(fdata[ii][3])))

    COM.append([today, rawdata[ii][0], rawdata[ii][1], rawdata[ii][2], rawdata[ii][3], round(AVE_WHT, 1), WAVE_SCRE, round(apply1[ii][5], 0),
                round(apply1[ii][7], 0), R_WAVEDIR_SCRE, round(apply1[ii][11], 1), RPEAK_SCRE, round(rawdata[ii][8], 1), round(rawdata[ii][9], 0), WIND_SCRE, round(apply1[ii][9], 1), TEMP_SCRE, rawdata[ii][11], WARN_SCRE, TOTAL_SCRE2, QUOTIENT_SCRE2])
    ii = ii + 1

COM_INDEX = pd.DataFrame(COM)
COM_INDEX.columns = ['산출날짜', '코드', '구분', '지역', '예측날짜', '유의파고', '파고점수', '파향', '상대파향',
                     '파향점수', '파주기', '파주기점수', '풍속', '풍향', '풍속점수', '수온', '수온점수', '특보', '특보점수', '총점수', '예보지수']
# OUT_FNAME=dir1+'/SURFING_INDEX_SERVICE_last_AM'+today+'.csv'
OUT_FNAME = dir1+'/SREQ_INDEX_SERVICE_onair_'+today+'.csv'
COM_INDEX.to_csv(OUT_FNAME, encoding='euc-kr', index=False)
