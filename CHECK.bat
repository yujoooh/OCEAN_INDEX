set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%
set logfile=./log/%TODAY%.log

echo '===[Data Collection start]=====================================================' >> %logfile%
python 0_1.KMA_CITY_FORECAST_API_05.py >> %logfile%
python 0_1.KMA_CITY_FORECAST_API_ST_05.py >> %logfile%
echo '===[Data Collection Complete]==================================================' >> %logfile%