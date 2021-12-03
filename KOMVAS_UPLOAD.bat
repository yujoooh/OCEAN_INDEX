rem setlocal

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%

set logfile=./log/%TODAY%.log
echo '===[KOMVAS Data Upload Process start]=================================================='  >> %logfile%
scp -r -P 10001 ./Result/%TODAY% root@10.27.90.53:/usr/local/data/opendap/external/FORECAST_QUOTIENT/KOMVAS/
echo '===[KOMVAS Data Upload Process Complete]=================================================='  >> %logfile%
