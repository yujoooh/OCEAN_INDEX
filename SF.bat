rem

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%
set logfile=./log/%TODAY%.log

python 3_0.SF_POINT_VALUE_EXTRACT.py  >> %logfile%
python 3_1.SF_INDEX_FCST.py  >> %logfile%
python 3_2.SF_INDEX_OBS.py  >> %logfile%
python 3_3.SF_INDEX_SERVICE.py  >> %logfile%
python 3_4.SF_INDEX_timeseries.py  >> %logfile%
python 3_5.SF_DB_UPLOAD.py  >> %logfile%
