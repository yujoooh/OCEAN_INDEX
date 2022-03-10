rem

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%
set logfile=./log/%TODAY%.log

python 1_0.SP_POINT_VALUE_EXTRACT.py  >> %logfile%
python 1_1.SP_INDEX_FCST.py  >> %logfile%
python 1_3.SP_INDEX_SERVICE.py  >> %logfile%

python 3_0.SF_POINT_VALUE_EXTRACT.py  >> %logfile%
python 3_1.SF_INDEX_FCST.py  >> %logfile%
python 3_3.SF_INDEX_SERVICE.py  >> %logfile%

python 4_0.SS_POINT_VALUE_EXTRACT.py  >> %logfile%
python 4_1.SS_INDEX_FCST.py  >> %logfile%
python 4_3.SS_INDEX_SERVICE.py  >> %logfile%

python 5_1.SD_INDEX_FCST_and_SERVICE.py  >> %logfile%

python 6_1.TL_INDEX_FCST_and_SERVICE.py  >> %logfile%

python 7_0.point_value_extract_surfing_am.py  >> %logfile%
python 7_0.point_value_extract_surfing_pm.py  >> %logfile%
python 7_1.SR_INDEX_FCST_AM.py  >> %logfile%
python 7_2.SR_INDEX_SERVICE_AM.py  >> %logfile%
python 7_1.SR_INDEX_FCST_PM.py  >> %logfile%
python 7_2.SR_INDEX_SERVICE_PM.py  >> %logfile%
python 7_1.SR_INDEX_FCST_MID.py  >> %logfile%
python 7_3.SR_INDEX_TOTAL.py  >> %logfile%
python 7_1.SR_INDEX_FCST_onair.py >> %logfile%
python 7_2.SR_INDEX_SERVICE_onair.py >> %logfile%

python 8_1.ST_INDEX_SERVICE.py  >> %logfile%

