rem setlocal

set YEAR=%date:~0,4%
set MONTH=%date:~5,2%
set DAY=%date:~8,2%
set TODAY=%YEAR%%MONTH%%DAY%

rem ROMS, WRF, WW3, CWW3, RWW3

scp -P10001 root@10.27.90.57:/home/model/result/YES3K_7d/%TODAY%00/YES3K_%TODAY%00.nc ./
scp -P10001 root@10.27.90.57:/home/model/result/WRF/%TODAY%00/wrf_dm2_7d/wrfdm2_%TODAY%_*.nc ./  
scp -P10001 root@10.27.90.57:/home/model/result/WW3_7d/%TODAY%00/WW3_%TODAY%00.nc ./
scp -P10001 root@10.27.90.57://home/geosr/2021/KMA2NC/CWW3_%TODAY%00.nc ./
scp -P10001 root@10.27.90.57://home/geosr/2021/KMA2NC/CWW3_WAVPRD_%TODAY%00.nc ./
scp -P10001 root@10.27.90.50:/DATA/opendap/external/KMA/RWW3/RWW3_%TODAY%00.nc ./

ren  wrfdm2_%TODAY%_*.nc WRF_%TODAY%.nc
copy *.nc Model_data
del  *.nc