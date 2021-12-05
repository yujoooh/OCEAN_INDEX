rem

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%
set logfile=./log/%TODAY%.log

python 4_0.SS_POINT_VALUE_EXTRACT.py  >> %logfile%
python 4_1.SS_INDEX_FCST.py  >> %logfile%
python 4_2.SS_INDEX_OBS.py  >> %logfile%
python 4_3.SS_INDEX_SERVICE.py  >> %logfile%
python 4_4.SS_INDEX_timeseries.py  >> %logfile%
python 4_5.SS_DB_UPLOAD.py  >> %logfile%
