import datetime
import os

today     =  datetime.datetime.today().strftime('%Y%m%d')
lastmonth = (datetime.datetime.today().replace(day=1) - datetime.timedelta(days=1)).strftime('%Y%m')

os.system(f"echo '===[KOMVAS Data Upload Process start]=================================================='     >> ./log/{today}.log")
os.system(f"scp -r -P 10001 ./Result/TSD_Monthly/{lastmonth} root@10.27.90.53:/usr/local/data/opendap/external/FORECAST_QUOTIENT/KOMVAS/")
os.system(f"echo '===[KOMVAS Data Upload Process Complete]=================================================='  >> ./log/{today}.log")
