rem

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%
set logfile=./log/%TODAY%.log

python 8_1.ST_INDEX_SERVICE.py  >> %logfile% rem 점수 배점구간 20점 간격(매우나쁨 0~20, 나쁨 20~40, 보통 40~60, 좋음 60~80, 매우좋음 80~100)
rem python 8_5.ST_INDEX_DB_UPLOAD.py  >> %logfile% 


