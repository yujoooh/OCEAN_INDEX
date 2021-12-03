rem
set YEAR=2019
set MONTH=12
set DAY=1

python 0_9.REALTIME_DATA_COLLECT_ERROR_CHECK_manual.py %YEAR% %MONTH% %DAY%

python 1_0.SP_POINT_VALUE_EXTRACT_manual.py %YEAR% %MONTH% %DAY%
python 1_1.SP_INDEX_FCST_manual.py %YEAR% %MONTH% %DAY%
python 1_2.SP_INDEX_OBS_manual.py %YEAR% %MONTH% %DAY%
python 1_3.SP_INDEX_SERVICE_manual.py %YEAR% %MONTH% %DAY%
python 1_5.SP_DB_UPLOAD_manual.py %YEAR% %MONTH% %DAY%

python 2_0.SK_POINT_VALUE_EXTRACT_manual.py %YEAR% %MONTH% %DAY%
python 2_1.SK_INDEX_FCST_manual.py %YEAR% %MONTH% %DAY%
python 2_2.SK_INDEX_OBS_manual.py %YEAR% %MONTH% %DAY%
python 2_3.SK_INDEX_SERVICE_manual.py %YEAR% %MONTH% %DAY%
python 2_5.SK_DB_UPLOAD_manual.py %YEAR% %MONTH% %DAY%

python 3_0.SF_POINT_VALUE_EXTRACT_manual.py %YEAR% %MONTH% %DAY%
python 3_1.SF_INDEX_FCST_manual.py %YEAR% %MONTH% %DAY%
python 3_2.SF_INDEX_OBS_manual.py %YEAR% %MONTH% %DAY%
python 3_3.SF_INDEX_SERVICE_manual.py %YEAR% %MONTH% %DAY%
python 3_5.SF_DB_UPLOAD_manual.py %YEAR% %MONTH% %DAY%

python 4_0.SS_POINT_VALUE_EXTRACT_manual.py %YEAR% %MONTH% %DAY%
python 4_1.SS_INDEX_FCST_manual.py %YEAR% %MONTH% %DAY%
python 4_2.SS_INDEX_OBS_manual.py %YEAR% %MONTH% %DAY%
python 4_3.SS_INDEX_SERVICE_manual.py %YEAR% %MONTH% %DAY%
python 4_5.SS_DB_UPLOAD_manual.py %YEAR% %MONTH% %DAY%

python 5_1.SD_INDEX_FCST_and_SERVICE_manual.py %YEAR% %MONTH% %DAY%
python 5_5.SD_DB_UPLOAD_manual.py %YEAR% %MONTH% %DAY%

python 6_1.TL_INDEX_FCST_and_SERVICE_manual.py %YEAR% %MONTH% %DAY%
python 6_5.TL_DB_UPLOAD_manual.py %YEAR% %MONTH% %DAY%