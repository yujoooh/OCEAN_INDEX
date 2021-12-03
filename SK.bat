rem

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%
set logfile=./log/%TODAY%.log

python 2_0.SK_POINT_VALUE_EXTRACT.py  >> %logfile%
python 2_1.SK_INDEX_FCST.py  >> %logfile%
rem python 2_2.SK_INDEX_OBS.py  >> %logfile%
python 2_3.SK_INDEX_SERVICE.py  >> %logfile%
python 2_4.SK_INDEX_timeseries.py  >> %logfile%
rem python 2_5.SK_DB_UPLOAD.py  >> %logfile%