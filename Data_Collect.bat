erem Data_Correct

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%
set logfile=./log/%TODAY%.log

echo '===[Data Collection start]=====================================================' >> %logfile%
python 0_1.KMA_CITY_FORECAST_API.py >> %logfile%
rem python 0_1.KMA_CITY_FORECAST_API_ST.py >> %logfile%
python 0_2.KMA_WARNING.py >> %logfile%
python 0_3.KMA_OBS_API_REALTIME.py >> %logfile%
python 0_4.KHOA_OBS_REALTIME_DB.py  >> %logfile% rem OPeNDAP에서 자료 받는 부분까지 해당 프로그램에 포함되어있음 python 0_4.KHOA_OBS_API_REALTIME.py >> %logfile%
python 0_4.KHOA_OBS_REALTIME_DB_surf.py  >> %logfile%
python 0_5.KMA_OBS_API_DAILY.py >> %logfile%
python 0_6.KHOA_OBS_DAILY_DBTXT.py >> %logfile% rem OPeNDAP에서 자료 받는 부분까지 해당 프로그램에 포함되어있음  rem [python 0_6.KHOA_OBS_API_DAILY.py >> %logfile% rem API는 임시로..]
python 0_9.REALTIME_DATA_COLLECT_ERROR_CHECK.py >> %logfile% rem API 정상여부 체크 및 없을 경우 전체 MISSING 자료로 저장
echo '===[Data Collection Complete]==================================================' >> %logfile%