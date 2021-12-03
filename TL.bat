rem

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%
set logfile=./log/%TODAY%.log

python 6_1.TL_INDEX_FCST_and_SERVICE.py  >> %logfile%
python 6_4.TL_INDEX_timeseries.py  >> %logfile%
rem python 6_5.TL_DB_UPLOAD.py  >> %logfile%