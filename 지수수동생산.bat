rem

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%
set logfile=./log/%TODAY%.log

rem call SP.bat
call SK.bat
call SF.bat
call SS.bat
rem call SD.bat
rem call TL.bat
rem call ST.bat
call SR.bat