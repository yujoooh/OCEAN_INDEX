rem

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%
set logfile=./log/%TODAY%.log

python 5_1.SD_INDEX_FCST_and_SERVICE.py  >> %logfile%
python 5_4.SD_INDEX_timeseries.py  >> %logfile%
python 5_5.SD_DB_UPLOAD.py  >> %logfile%
