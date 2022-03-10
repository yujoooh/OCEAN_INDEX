rem setlocal

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%

rem ROMS, WRF, WW3, CWW3, RWW3

rem scp -P10001 root@10.27.90.57:/home/model/result/YES3K_7d/2020072*00/YES3K_2020072*00.nc ./
rem scp -P10001 root@10.27.90.57:/home/model/result/WRF/2020072*00/wrf_dm2_7d/wrfdm2_2020072*_*.nc ./  
rem scp -P10001 root@10.27.90.57:/home/model/result/WW3_7d/2020072*00/WW3_202007*00.nc ./
rem "C:\Program Files (x86)\GnuWin32\bin\wget.exe" http://10.27.90.53:8080/opendap/external/FORECAST_QUOTIENT/CWW3_%TODAY%00.nc  
rem "C:\Program Files (x86)\GnuWin32\bin\wget.exe" http://10.27.90.53:8080/opendap/external/FORECAST_QUOTIENT/RWW3_%TODAY%00.nc  
rem "C:\Program Files (x86)\GnuWin32\bin\wget.exe" http://10.27.90.53:8080/opendap/application/Tidal_atlas/YES3K/YES3K_2020062700.nc

rem ren  wrfdm2_%TODAY%_*.nc WRF_%TODAY%.nc
copy *.nc Model_data
del  *.nc