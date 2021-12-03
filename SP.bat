rem

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%
set logfile=./log/%TODAY%.log

python 1_0.SP_POINT_VALUE_EXTRACT.py  >> %logfile%
python 1_1.SP_INDEX_FCST.py  >> %logfile%
python 1_2.SP_INDEX_OBS.py  >> %logfile%
python 1_3.SP_INDEX_SERVICE.py  >> %logfile%
python 1_4.SP_INDEX_timeseries.py  >> %logfile%
python 1_5.SP_DB_UPLOAD.py  >> %logfile%
