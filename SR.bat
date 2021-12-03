rem

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%
set logfile=./log/%TODAY%.log


echo '===[SR Collection start]=====================================================' >> %logfile%
python 7_0.point_value_extract_surfing_am.py  >> %logfile%
python 7_0.point_value_extract_surfing_pm.py  >> %logfile%
python 7_1.SR_INDEX_FCST_AM.py  >> %logfile%
python 7_2.SR_INDEX_SERVICE_AM.py  >> %logfile%
python 7_1.SR_INDEX_FCST_PM.py  >> %logfile%
python 7_2.SR_INDEX_SERVICE_PM.py  >> %logfile%
python 7_1.SR_INDEX_FCST_MID.py  >> %logfile%
python 7_3.SR_INDEX_TOTAL.py  >> %logfile%
rem python 7_5.SR_DB_UPLOAD.py  >> %logfile%
echo '===[SR Collection Complete]==================================================' >> %logfile%