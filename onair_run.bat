rem

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%
set logfile=./log/%TODAY%.log

rem python 0_1.KMA_CITY_FORECAST_API_ONAIR.py >> %logfile%
rem python 0_1.KMA_CITY_FORECAST_API_ST_ONAIR.py >> %logfile%

python 1_1.SP_INDEX_FCST_ONAIR.py  >> %logfile%
python 1_3.SP_INDEX_SERVICE_ONAIR.py  >> %logfile%

python 3_1.SF_INDEX_FCST_ONAIR.py  >> %logfile%
python 3_3.SF_INDEX_SERVICE_ONAIR.py  >> %logfile%

python 4_1.SS_INDEX_FCST_ONAIR.py  >> %logfile%
python 4_3.SS_INDEX_SERVICE_ONAIR.py  >> %logfile%

python 5_1.SD_INDEX_FCST_and_SERVICE_ONAIR.py  >> %logfile%

python 6_1.TL_INDEX_FCST_and_SERVICE_ONAIR.py  >> %logfile%

python 7_1.SR_INDEX_FCST_onair.py >> %logfile%
python 7_2.SR_INDEX_SERVICE_onair.py >> %logfile%

python 8_1.ST_INDEX_SERVICE_ONAIR.py  >> %logfile%

