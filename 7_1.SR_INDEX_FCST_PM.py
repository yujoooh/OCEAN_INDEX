import time as checktime
from netCDF4 import Dataset
import numpy as np
import lunardate as lunar
from datetime import date, timedelta, datetime
import pandas as pd
import os
import sys
from Function.surfing_function import IndexScore
#Made by PPARK

#실행시간 측정
startTime = checktime.time()

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
# today = str(date(2021,4,6).strftime('%Y%m%d'))
# afterday1 = (date(2021,4,6) + timedelta(1)).strftime('%Y%m%d')
# afterday2 = (date(2021,4,6) + timedelta(2)).strftime('%Y%m%d')
# afterday3 = (date(2021,4,6) + timedelta(3)).strftime('%Y%m%d')
# afterday4 = (date(2021,4,6) + timedelta(4)).strftime('%Y%m%d')
# afterday5 = (date(2021,4,6) + timedelta(5)).strftime('%Y%m%d')
# afterday6 = (date(2021,4,6) + timedelta(6)).strftime('%Y%m%d')
# print(today, afterday6)

#산출물 폴더(특보 정보 있음)
dir_result = './Result/'+today

#모델데이터 불러오기, WW3만 써서 일단 나머지 주석처리
MPATH = './Model_Data/'
ROMS_FNAME = 'YES3K_'+ str(today) + '00.nc'      # YES3K   - KHOA
WRF_FNAME = 'WRF_' + str(today) + '.nc'          # WRF_DM2 - KHOA
WW3_FNAME = 'WW3_' + str(today) + '00.nc'        # WW3     - KHOA
CWW3_FNAME = 'CWW3_' + str(today) + '00.nc'      # CWW3    - KMA
RWW3_FNAME = 'RWW3_' + str(today) + '00.nc'      # RWW3    - KMA
#20210628
CWW3_WAVPRD_FNAME = 'CWW3_WAVPRD_' + str(today) + '00.nc'

INFILE_1 = MPATH+ROMS_FNAME #7day forecast data
INFILE_2 = MPATH+WRF_FNAME  #7day forecast data
INFILE_3 = MPATH+CWW3_FNAME #3day forecast data
INFILE_4 = MPATH+WW3_FNAME  #7day forecast data
INFILE_5 = MPATH+RWW3_FNAME #5day forecast data ---  not used
INFILE_6 = MPATH+CWW3_WAVPRD_FNAME #파주기데이터

#[YES3K]
DATA = Dataset(INFILE_1, mode='r')
SST = DATA.variables['temp'][:,:,:]  #[t,y,x]
#U_CURRENT = DATA.variables['u'][:,:,:]  #[t,y,x]
#V_CURRENT = DATA.variables['v'][:,:,:]  #[t,y,x]
#CURRENT= (U_CURRENT**2+V_CURRENT**2)**0.5  #Calculate Current speed

#[WRF]
DATA = Dataset(INFILE_2, mode='r')
#TEMP = DATA.variables['Tair'][:,:,:]  #[t,y,x]
U_WIND = DATA.variables['Uwind'][:,:,:]  #[t,y,x]
V_WIND = DATA.variables['Vwind'][:,:,:]  #[t,y,x]
WIND = (U_WIND**2+V_WIND**2)**0.5  #Calculate Wind speed
WDEG = np.rad2deg(np.arctan2(V_WIND,U_WIND))
WDEG[WDEG<0]+= 360

#[CWW3, WW3] not yet RWW3
if os.path.isfile(INFILE_3):
    #print('Use CWW3')
    DATA = Dataset(INFILE_3, mode='r')
    #파고
    WHT_1 = DATA.variables['hsig1_dajn'][:,:,:]  #[t,y,x]
    WHT_2 = DATA.variables['hsig2_gwju'][:,:,:]  #[t,y,x]
    WHT_3 = DATA.variables['hsig3_jeju'][:,:,:]  #[t,y,x]
    WHT_4 = DATA.variables['hsig4_busn'][:,:,:]  #[t,y,x]
    WHT_5 = DATA.variables['hsig5_gawn'][:,:,:]  #[t,y,x]
    #파향
    Wdir_1 = DATA.variables['wavdir1_dajn'][:,:,:]  #[t,y,x]
    Wdir_2 = DATA.variables['wavdir2_gwju'][:,:,:]  #[t,y,x]
    Wdir_3 = DATA.variables['wavdir3_jeju'][:,:,:]  #[t,y,x]
    Wdir_4 = DATA.variables['wavdir4_busn'][:,:,:]  #[t,y,x]
    Wdir_5 = DATA.variables['wavdir5_gawn'][:,:,:]  #[t,y,x]

    #전처리
    Wdir_1[Wdir_1<-180] = np.nan
    Wdir_2[Wdir_2<-180] = np.nan
    Wdir_3[Wdir_3<-180] = np.nan
    Wdir_4[Wdir_4<-180] = np.nan
    Wdir_5[Wdir_5<-180] = np.nan
    
    Wdir_1[Wdir_1>0] = -Wdir_1[Wdir_1>0] - 90
    Wdir_2[Wdir_2>0] = -Wdir_2[Wdir_2>0] - 90
    Wdir_3[Wdir_3>0] = -Wdir_3[Wdir_3>0] - 90
    Wdir_4[Wdir_4>0] = -Wdir_4[Wdir_4>0] - 90
    Wdir_5[Wdir_5>0] = -Wdir_5[Wdir_5>0] - 90

    Wdir_1[Wdir_1<0] += 360
    Wdir_2[Wdir_2<0] += 360
    Wdir_3[Wdir_3<0] += 360
    Wdir_4[Wdir_4<0] += 360
    Wdir_5[Wdir_5<0] += 360

    Wx_1 = np.cos(np.deg2rad(Wdir_1))
    Wy_1 = np.sin(np.deg2rad(Wdir_1))
    Wx_2 = np.cos(np.deg2rad(Wdir_2))
    Wy_2 = np.sin(np.deg2rad(Wdir_2))
    Wx_3 = np.cos(np.deg2rad(Wdir_3))
    Wy_3 = np.sin(np.deg2rad(Wdir_3))
    Wx_4 = np.cos(np.deg2rad(Wdir_4))
    Wy_4 = np.sin(np.deg2rad(Wdir_4))
    Wx_5 = np.cos(np.deg2rad(Wdir_5))
    Wy_5 = np.sin(np.deg2rad(Wdir_5))

    #파주기도 추가 곧 해야함

     #20210628
    DATA2 = Dataset(INFILE_6, mode='r')
    print('Use Rpeak CWW3_wavprd')
    Rpeak_1 = DATA2.variables['wavprd1_dajn'][:,:,:]  #[t,y,x]
    Rpeak_2 = DATA2.variables['wavprd2_gwju'][:,:,:]  #[t,y,x]
    Rpeak_3 = DATA2.variables['wavprd3_jeju'][:,:,:]  #[t,y,x]
    Rpeak_4 = DATA2.variables['wavprd4_busn'][:,:,:]  #[t,y,x]
    Rpeak_5 = DATA2.variables['wavprd5_gawn'][:,:,:]  #[t,y,x]

    DATA3 = Dataset(INFILE_4, mode='r')
    print('Use Rpeak WW3')
    WHT = DATA3.variables['Hsig'][:,:,:]  #유의파고 [t,y,x]
    Wdir = DATA3.variables['Wdir'][:,:,:] # 파향
    Rpeak = DATA3.variables['Rpeak'][:,:,:]  #[t,y,x]	

    Wdir[Wdir<-180] = np.nan
    # 0보다 작은값 + 값으로 만들기
    Wdir[Wdir<0] += 360
    
    #각도를 라디안으로 바꾸고, 그것에 대한 코사인, 사인 성분 구함(x방향, y방향)
    Wx = np.cos(np.deg2rad(Wdir))   
    Wy = np.sin(np.deg2rad(Wdir))

else :
    #print("There is no CWW3, Use WW3")
    
#WW3의 파고, 파향 불러오기
    DATA = Dataset(INFILE_4, mode='r')
    WHT = DATA.variables['Hsig'][:,:,:]  #유의파고 [t,y,x]
    Wdir = DATA.variables['Wdir'][:,:,:] # 파향
    Rpeak = DATA.variables['Rpeak'][:,:,:] #파주기
    
    # -180보다 작은 값 전처리 
    Wdir[Wdir<-180] = np.nan
    # 0보다 작은값 + 값으로 만들기
    Wdir[Wdir<0] += 360
    
    #각도를 라디안으로 바꾸고, 그것에 대한 코사인, 사인 성분 구함(x방향, y방향)
    Wx = np.cos(np.deg2rad(Wdir))   
    Wy = np.sin(np.deg2rad(Wdir))


#서핑포인트 정보 읽어옴
POINT_df = pd.read_csv('./Info/SR_Point_Info_2.csv', index_col=['STN'])

#COM은 전체 시계열 데이터, COM_INDEX는 예보지수 데이터
COM = pd.DataFrame(index = range(0), columns = ['FCST_DATE','FCST_AREA','NAME', 'WARN_AREA','DATE', 'HR', 'WHT', 'Wavedir', 'Wavex', 'Wavey', 'Rpeak',
                                                '풍속','풍향','수온','SKY','RAIN_AMT','RAIN_PROB','REL_HU','특보'])

# COM_INDEX = pd.DataFrame(index = range(0), columns = ['구분','지역', '예측날짜', '유의파고', '파고점수', '파향', '상대파향', '파향점수', '파주기',
#                                                       '파주기점수','풍속', '풍향', '풍속점수', '수온', '수온점수', '특보', '특보점수', '총점수', '예보지수'])

# COM_INDEX2 = pd.DataFrame(index = range(0), columns = ['구분','지역', '예측날짜', '유의파고', '파고점수', '파향', '상대파향', '파향점수', '파주기',
#                                                       '파주기점수','풍속', '풍향', '풍속점수', '수온', '수온점수', '총점수', '예보지수'])

#20210628
COM_INDEX = pd.DataFrame(index = range(0), columns = ['구분','지역', '예측날짜', '유의파고', '파고점수', '파향', '상대파향', '파향점수', '파주기',
                                                      '파주기점수','풍속', '풍향', '풍속점수', '수온', '수온점수', '특보', '특보점수', '총점수', '예보지수', '코드'])
#20210628
COM_INDEX2 = pd.DataFrame(index = range(0), columns = ['구분','지역', '예측날짜', '유의파고', '파고점수', '파향', '상대파향', '파향점수', '파주기',
                                                      '파주기점수','풍속', '풍향', '풍속점수', '수온', '수온점수', '총점수', '예보지수', '코드'])
#auto date set
#today_date = datetime.today()

#manual date set
today_date = datetime.strptime(today,"%Y%m%d")
#today_date = date(2021,4,6)

#타임스텝 7일 기간으로 잡아놓기
timestep = range(0, 158, 3)

#시게열 자료 뽑아내기
for i in range(len(POINT_df)):
    #20210628
    CODE = POINT_df['CODE'][i]
    #print(CODE)
    #20210628
    FCST_AREA = POINT_df['AREA'][i]
    WARN_AREA = POINT_df['WARN_SEA'][i]
    NAME = POINT_df['NAME'][i]
    LON = POINT_df['LON'][i]
    LAT = POINT_df['LAT'][i]
    CWW3_LOC = int(POINT_df['CWWR_LOC'][i])
    CWW3_X = int(POINT_df['CWW3_X'][i])
    CWW3_Y = int(POINT_df['CWW3_Y'][i]) 
    WW3_X = int(POINT_df['WW3_X'][i])
    WW3_Y = int(POINT_df['WW3_Y'][i])
    WRF_X = int(POINT_df['WRF_X'][i])
    WRF_Y = int(POINT_df['WRF_Y'][i])
    ROMS_X = int(POINT_df['ROMS_X'][i])
    ROMS_Y = int(POINT_df['ROMS_Y'][i])
    for time in timestep:
        #추가하기 원하는 요소들 추가..
        if os.path.isfile(INFILE_3):
            #print('use CWW3 data')
            if time <=57 :
                #RPEAK = Rpeak[time, WW3_Y, WW3_X]
                if CWW3_LOC == 1 :
                    #print('use loc 1') 
                    WAVE_S = WHT_1[int(time/3)+4, CWW3_Y, CWW3_X]; WAVE_DIR = Wdir_1[int(time/3)+4,CWW3_Y, CWW3_X] ; WAVE_X = Wx_1[int(time/3)+4, CWW3_Y, CWW3_X]; WAVE_Y = Wy_1[int(time/3)+4, CWW3_Y, CWW3_X];\
                        RPEAK = Rpeak_1[int(time/3)+4, CWW3_Y, CWW3_X]
                if CWW3_LOC == 2 :
                    #print('use loc 2') 
                    WAVE_S = WHT_2[int(time/3)+4, CWW3_Y, CWW3_X]; WAVE_DIR = Wdir_2[int(time/3)+4,CWW3_Y, CWW3_X] ; WAVE_X = Wx_2[int(time/3)+4, CWW3_Y, CWW3_X]; WAVE_Y = Wy_2[int(time/3)+4, CWW3_Y, CWW3_X];\
                        RPEAK = Rpeak_2[int(time/3)+4, CWW3_Y, CWW3_X]
                if CWW3_LOC == 3 :
                    #print('use loc 3') 
                    WAVE_S = WHT_3[int(time/3)+4, CWW3_Y, CWW3_X]; WAVE_DIR = Wdir_3[int(time/3)+4,CWW3_Y, CWW3_X] ; WAVE_X = Wx_3[int(time/3)+4, CWW3_Y, CWW3_X]; WAVE_Y = Wy_3[int(time/3)+4, CWW3_Y, CWW3_X];\
                        RPEAK = Rpeak_3[int(time/3)+4, CWW3_Y, CWW3_X]
                if CWW3_LOC == 4 : 
                    #print('use loc 4')
                    WAVE_S = WHT_4[int(time/3)+4, CWW3_Y, CWW3_X]; WAVE_DIR = Wdir_4[int(time/3)+4,CWW3_Y, CWW3_X] ; WAVE_X = Wx_4[int(time/3)+4, CWW3_Y, CWW3_X]; WAVE_Y = Wy_4[int(time/3)+4, CWW3_Y, CWW3_X];\
                        RPEAK = Rpeak_4[int(time/3)+4, CWW3_Y, CWW3_X]
                if CWW3_LOC == 5 :
                    #print('use loc 5') 
                    WAVE_S = WHT_5[int(time/3)+4, CWW3_Y, CWW3_X]; WAVE_DIR = Wdir_5[int(time/3)+4,CWW3_Y, CWW3_X] ; WAVE_X = Wx_5[int(time/3)+4, CWW3_Y, CWW3_X]; WAVE_Y = Wy_5[int(time/3)+4, CWW3_Y, CWW3_X];\
                        RPEAK = Rpeak_5[int(time/3)+4, CWW3_Y, CWW3_X]
            else : # CWW3 최대 예측기간 이후 WW3로 적용
                print("CWW3 최대 예측기간 지나 WW3사용합니다")
                #[WW3]
                WAVE_S = WHT[time, WW3_Y, WW3_X]
                WAVE_DIR = Wdir[time,WW3_Y, WW3_X]
                WAVE_X = Wx[time, WW3_Y, WW3_X]
                WAVE_Y = Wy[time, WW3_Y, WW3_X]
                RPEAK = Rpeak[time, WW3_Y, WW3_X]
        else:
            WAVE_S = WHT[time, WW3_Y, WW3_X]
            WAVE_DIR = Wdir[time,WW3_Y, WW3_X]
            WAVE_X = Wx[time, WW3_Y, WW3_X]
            WAVE_Y = Wy[time, WW3_Y, WW3_X]
            RPEAK = Rpeak[time, WW3_Y, WW3_X]

        #[WRF]
        WIND_S = WIND[time, WRF_Y, WRF_X]  #Calculate Wind speed
        WIND_DIR = WDEG[time, WRF_Y, WRF_X]

        #[YES3K]
        TEMP = SST[time, ROMS_Y, ROMS_X]

        row = [today, FCST_AREA, NAME, WARN_AREA , (today_date + timedelta(divmod(time+9,24)[0])).strftime('%Y%m%d') , \
               divmod(time+9, 24)[1] , WAVE_S, WAVE_DIR ,WAVE_X, WAVE_Y, RPEAK, WIND_S, WIND_DIR, TEMP, np.nan, np.nan, np.nan, np.nan, np.nan]
        #print(row)
        COM = COM.append(pd.Series(row, index = COM.columns), ignore_index=True)
        #print(COM)

#동네예보 적용
if not os.path.exists(dir_result+'/SR_CITY.csv'): # 동네예보 수집 에러에 따른 자료 미생성시 그냥 예측자료 사용
    print('CITY_FORECAST DATA Not found') ; CITY_LEN=0
else :
    CITY = pd.read_csv(dir_result+'/SR_CITY.csv')
    CITY_LEN = len(CITY)
    for i in range(len(COM)):
        COM['SKY'][i] = CITY['SKY'][i]
        COM['RAIN_AMT'][i] = CITY['RAIN_AMT'][i]
        COM['RAIN_PROB'][i] = CITY['RAIN_PROB'][i]
        COM['REL_HU'][i] = CITY['REL_HU'][i]
        
#특보자료 처리 함수 정의_1
def convertWARNTYPE(TYPE):
    if TYPE == 'SR2' : return 'SR'
    if TYPE == 'SW2' : return 'SW'
    if TYPE == 'CW2' : return 'CW'
    if TYPE == 'DR2' : return 'DR'
    if TYPE == 'SS2' : return 'SS'
    if TYPE == 'WW2' : return 'WW'
    if TYPE == 'TY2' : return 'TY'
    if TYPE == 'SN2' : return 'SN'
    if TYPE == 'YD2' : return 'YD'
    if TYPE == 'HW2' : return 'HW'
    return TYPE
# 특보없이 산출하고 싶을때
# WARN_LEN = 0

if not os.path.exists(dir_result+'/KMA_WARNING.csv') : #기상특보자료 수집 불가시 특보 적용 없이 산출
    print('KMA_WARNING DATA Not found') ; WARN_LEN=0
else :
    WARN= pd.read_csv(dir_result+'/KMA_WARNING.csv')
    WARN_LEN = len(WARN)
if WARN_LEN==0:
    COM['특보'] = '-'
else:
    WARN['CONVERT_TYPE']=WARN['TYPE'].apply(convertWARNTYPE)
    WARN = WARN.astype({'START_DAY': 'str'})
    WARN = WARN.astype({'END_DAY': 'str'})
    for j in range(len(COM)):
        for i in range(len(WARN)):
            if COM['WARN_AREA'][j] == WARN['WARNING_AREA'][i] and  COM['DATE'][j] >= WARN['START_DAY'][i] and COM['DATE'][j] <= WARN['END_DAY'][i] :
                COM['특보'][j] =WARN['CONVERT_TYPE'][i]
    COM['특보'][COM['특보'].isnull()] = '-'

for i in range(len(POINT_df)):
    FCST_AREA = POINT_df['AREA'][i]
    WARN_AREA = POINT_df['WARN_SEA'][i]
    CODE = POINT_df['CODE'][i]
    NAME = POINT_df['NAME'][i]
    BEACH_DIR = POINT_df['BEACH_DIR'][i]
    for date in COM['DATE'].unique().tolist():
        #[WW3]
        mean_WHT = round(COM['WHT'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 12) ].mean(),1)
        mean_WAVEX = COM['Wavex'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 12) ].mean()
        mean_WAVEY = COM['Wavey'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 12) ].mean()
        mean_WAVEDIR = round(np.rad2deg(np.arctan2(mean_WAVEY, mean_WAVEX)),0)
        #print(mean_WAVEDIR)
        if mean_WAVEDIR < 0:
            mean_WAVEDIR = mean_WAVEDIR + 360
        #print('1', mean_WAVEDIR)
        #mean_WAVEDIR = COM['Wavedir'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 9) ].mean()
        mean_R_WAVEDIR = round(mean_WAVEDIR - BEACH_DIR,0)
        mean_RPEAK = round(COM['Rpeak'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 12) ].mean(),1)
        #[WRF]
        mean_WINDS = COM['풍속'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 12) ].mean()
        mean_WINDDIR = COM['풍향'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 12) ].mean()
        #[YES3K]
        mean_TEMP = round(COM['수온'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (COM['DATE'] == date) & (COM['HR'] <= 18) & (COM['HR'] >= 12) ].mean(),1)
        
        warning = COM['특보'][(COM['FCST_AREA'] == FCST_AREA) & (COM['NAME'] == NAME) & (COM['DATE'] == date)].unique()
        if len(warning) != 1:
            #print("특보적용이 이상합니다")
            warning = warning[0]
        else:
            warning = warning[0]
        
        WAVE_SCRE = IndexScore().wave_score(mean_WHT)
        RPEAK_SCRE = IndexScore().Rpeak_score(mean_RPEAK)
        WAVEDIR_SCRE = IndexScore().wave_dir_score(mean_R_WAVEDIR)
        #[WRF]
        WIND_SCRE = IndexScore().wind_score(mean_WINDS)
        
        #[YES3K]
        TEMP_SCRE = IndexScore().temp_score(mean_TEMP)

        #[특보점수]
        WARN_SCRE = IndexScore().warn_score(warning)
        
        TOTAL_SCRE1 = IndexScore().total_score(WAVE_SCRE, RPEAK_SCRE, WAVEDIR_SCRE, WIND_SCRE, TEMP_SCRE, WARN_SCRE)[0]
        TOTAL_SCRE2 = IndexScore().total_score(WAVE_SCRE, RPEAK_SCRE, WAVEDIR_SCRE, WIND_SCRE, TEMP_SCRE, WARN_SCRE)[1]
        
        QUOTIENT_SCRE1 = IndexScore().quotient_score(TOTAL_SCRE1) # forecast score(no rain, no warning)
        QUOTIENT_SCRE2 = IndexScore().quotient_score(TOTAL_SCRE2) # service score
        

        #row = [FCST_AREA, NAME, date, mean_WHT, WAVE_SCRE, mean_WAVEDIR, mean_R_WAVEDIR, WAVEDIR_SCRE, mean_RPEAK, RPEAK_SCRE, mean_WINDS, mean_WINDDIR, WIND_SCRE, mean_TEMP, TEMP_SCRE, warning, WARN_SCRE, TOTAL_SCRE2,  QUOTIENT_SCRE2]
        #row2 = [FCST_AREA, NAME, date, mean_WHT, WAVE_SCRE, mean_WAVEDIR, mean_R_WAVEDIR, WAVEDIR_SCRE, mean_RPEAK, RPEAK_SCRE, mean_WINDS, mean_WINDDIR, WIND_SCRE, mean_TEMP, TEMP_SCRE, TOTAL_SCRE1,  QUOTIENT_SCRE1]
        print(CODE, NAME)
        #20210628
        row = [FCST_AREA, NAME, date, round(mean_WHT,1), WAVE_SCRE, round(mean_WAVEDIR,0), round(mean_R_WAVEDIR,0), WAVEDIR_SCRE, round(mean_RPEAK,1), RPEAK_SCRE, round(mean_WINDS,1), round(mean_WINDDIR,0), WIND_SCRE, round(mean_TEMP,1), TEMP_SCRE, warning, WARN_SCRE, TOTAL_SCRE2,  QUOTIENT_SCRE2, CODE]
        row2 = [FCST_AREA, NAME, date, round(mean_WHT,1), WAVE_SCRE, round(mean_WAVEDIR,0), round(mean_R_WAVEDIR,0), WAVEDIR_SCRE, round(mean_RPEAK,1), RPEAK_SCRE, round(mean_WINDS,1), round(mean_WINDDIR,0), WIND_SCRE, round(mean_TEMP,1), TEMP_SCRE, TOTAL_SCRE1,  QUOTIENT_SCRE1, CODE]
        COM_INDEX = COM_INDEX.append(pd.Series(row, index = COM_INDEX.columns), ignore_index=True)
        COM_INDEX2 = COM_INDEX2.append(pd.Series(row2, index = COM_INDEX2.columns), ignore_index=True)

#날짜순으로 정렬
COM_INDEX = COM_INDEX.sort_values(by=['예측날짜'])
COM_INDEX2 = COM_INDEX2.sort_values(by=['예측날짜'])
COM_INDEX.insert(0, '산출날짜', today)
COM_INDEX2.insert(0, '산출날짜', today)


# COM.to_csv('./data/test/'+today+'_SURFING_TMESERIES.csv', encoding = 'utf8', index=False)
# COM.to_csv('./data/test/'+today+'_SURFING_TMESERIES_euckr.csv', encoding = 'euc-kr', index=False)
# COM.to_csv('./Result/'+today+'_SURFING_TMESERIES.csv', encoding = 'utf8', index=False)
# COM.to_csv('./Result/'+today+'_SURFING_TMESERIES_euckr.csv', encoding = 'euc-kr', index=False)

COM.to_csv('./Result/'+today+'/SR_TMESERIES_'+today+'.csv', encoding = 'utf8', index=False)
#COM.to_csv('./Result/'+today+'/'+ today+'_SURFING_TMESERIES_euckr.csv', encoding = 'euc-kr', index=False)

#지수 저장
#COM_INDEX.to_csv('./data/test/'+today+'_SURFING_FCST_INDEX_test_1.csv', encoding = 'utf8', index=False)
#COM_INDEX.to_csv('./data/test/'+today+'_SURFING_FCST_INDEX_euckr_test_1.csv', encoding = 'euc-kr', index=False)
COM_INDEX2.to_csv('./Result/'+today+'/'+today+'_SREQ_INDEX_FCST_PM.csv', encoding = 'utf8', index=False)
#COM_INDEX2.to_csv('./Result/'+today+'/'+today+'_SURFING_INDEX_FCST_PM_euckr.csv', encoding = 'euc-kr', index=False)
COM_INDEX.to_csv('./Result/'+today+'/'+today+'_SREQ_INDEX_SERVICE_PM.csv', encoding = 'utf8', index=False)
#COM_INDEX.to_csv('./Result/'+today+'/'+today+'_SURFING_INDEX_SERVICE_PM_euckr.csv', encoding = 'euc-kr', index=False)
#최종실행시간 체크
endTime = checktime.time() - startTime
print(endTime) 
## COM_INDEX 칼럼에 특보 적용하는 코드 짜야됨
