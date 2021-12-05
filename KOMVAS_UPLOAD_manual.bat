rem
set YEAR=2020
set MONTH=04
set DAY=21
set TODAY=%YEAR%%MONTH%%DAY%

set logfile=./log/%TODAY%.log
echo '===[KOMVAS Data Upload Process start]=================================================='  >> %logfile%
scp -r -P 10001 ./Result/%TODAY% root@10.27.90.53:/usr/local/data/opendap/external/FORECAST_QUOTIENT/KOMVAS/
echo '===[KOMVAS Data Upload Process Complete]=================================================='  >> %logfile%
