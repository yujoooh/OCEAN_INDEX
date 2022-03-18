#[Geosystem Research : Department of Coastal Management]
#[Created by C.K. Park on 2019.04.11] edit 19.08.22
import sys
import os
#os.path.join(os.getcwd(),"Function")
from datetime import date, timedelta
from datetime import datetime
import calendar


YMD = str(date(2019,9,1).strftime('%Y%m%d'))
#print(type(int(YMD[4:6])))
eday = calendar.monthrange(int(YMD[0:4]),int(YMD[4:6]))[1]
print(YMD[0:4],YMD[4:6],YMD[6:8],eday, type(eday))

dd = int(YMD[6:8])
while dd <= eday:
	dd2 = (f'{dd:02d}')
	YMD2 = YMD[0:4]+YMD[4:6]+dd2
	print(dd, YMD[4:6],dd2, day)
	dd = dd + 1