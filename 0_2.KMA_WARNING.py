#[Geosystem Research : Department of Marine Forecast ]
#[Created by C.K. Park on 2018.10.23] edit 2019.04
import os
import sys
import json
import re
import urllib.request
from collections import OrderedDict
from datetime import date, timedelta
from datetime import datetime
from Function.warn_function import RESERVE_WARN
from Function.warn_area_function import WARN_AREA_FN

print("#KMA Warning data collection Start========")

#[Date Set]===============================================================================================================
today = str(datetime.today().strftime('%Y%m%d'))
today2 = str(datetime.today().strftime('%Y%m%d%H'))
afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')
#ago7day = str((date.today() - timedelta(1)).strftime('%Y%m%d'))
#ago7day = str((date.today() - timedelta(2)).strftime('%Y%m%d'))

YR = today[0:4]
HR = str(datetime.today().strftime("%H"))
#print(today, hr, ago7day)

#[폴더]
dir1 = './Result/'+today
if not os.path.exists(dir1): os.makedirs(dir1)
#[KMA API KEY and URL]] ==================================================================================================
API_KEY = "SKRp1p8kIX9Nx%2FG9VonGemNtI09JHVLPcgGtTTiH72auPDE5aVx8iwHLydskKf9zTKj9I2dDniDwuKjovXXdFA%3D%3D"
#API_KEY = "SKRp1p8kIX9Nx%2FG9VonGemNtI09JHVLPcgGtTTiH72auPDE5aVx8iwHLydskKf9zTKj9I2dDniDwuKjovXXdFA=="

#Check KMA API access
#기상특보(전체목록) http://apis.data.go.kr/1360000/WthrWrnInfoService/getWthrWrnMsg?serviceKey=SKRp1p8kIX9Nx%2FG9VonGemNtI09JHVLPcgGtTTiH72auPDE5aVx8iwHLydskKf9zTKj9I2dDniDwuKjovXXdFA%3D%3D&numOfRows=1&pageNo=1&fromTmFc=20201005&toTmFc=20201005&stnId=108&dataType=JSON

#WARNING1_URL = "http://apis.data.go.kr/1360000/WthrWrnInfoService/getPwnStatus?serviceKey="  #기상특보현황 <-------- 특보현황에서 스플릿으로...
WARNING1_URL = "http://apis.data.go.kr/1360000/WthrWrnInfoService/getWthrWrnMsg?serviceKey=" #기상특보통보문조회 <---- 해제예고

data2 = []
data4 = []

#-----------------------------------[기상특보 자료수집]----------------------------------------------------
WURL1 = WARNING1_URL + API_KEY + "&numOfRows=1&pageNo=1&fromTmFc="+today+"&toTmFc="+today+"&stnId=108&dataType=JSON"
print(WURL1)
WPAGE1 = urllib.request.urlopen(WURL1)
WREAD1 = WPAGE1.read()
WJSON1 = json.loads(WREAD1)

READ1 = WJSON1.get('response') ; CHECK2 = READ1.get('header') ; CHECK3 = CHECK2.get('resultCode')
if CHECK3 == '03' :
	print('No data')
	with open(dir1+'/KMA_WARNING.csv','w',encoding='utf8') as file:
		file.write('WARNING_AREA,TYPE,START_DAY,START_TIME,END_DAY,END_TIME\n')
		file.write('-,SR,{},AM,{},AM\n'.format(today,today))
		file.write('-,CW,{},AM,{},AM\n'.format(today,today))
		file.write('-,DR,{},AM,{},AM\n'.format(today,today))
		file.write('-,SS,{},AM,{},AM\n'.format(today,today))
		file.write('-,WW,{},AM,{},AM\n'.format(today,today))
		file.write('-,TY,{},AM,{},AM\n'.format(today,today))
		file.write('-,SN,{},AM,{},AM\n'.format(today,today))
		file.write('-,YD,{},AM,{},AM\n'.format(today,today))
		file.write('-,HW,{},AM,{},AM\n'.format(today,today))

else : 
	READ2 = READ1.get('body')
	READ3 = READ2.get('items')
	READ4 = READ3.get('item')

	WARNING1 = READ4[0]['t6'] #[특보현황]
	WARNING2 = READ4[0]['t7'] #[예비특보현황]
	WARNING3 = READ4[0]['t4'] #[해제예고]

	#[특보현황]---------------------------------------------------------------------------------------------
	WARNLIST = WARNING1.split('o') # 글머리기호 o 를 기준으로 주의보 나눔.
	warnType = ['강풍', '호우', '한파', '건조', '폭풍해일', '풍랑', '태풍', '대설', '황사', '폭염']
	ii = 0

	for WRT in warnType :
		if WRT not in WARNING1 :
			if WRT == '호우' : warnTy  = 'SR'
			if WRT == '강풍' : warnTy  = 'SW'
			if WRT == '한파' : warnTy  = 'CW'
			if WRT == '건조' : warnTy  = 'DR'
			if WRT == '폭풍해일' : warnTy  = 'SS'
			if WRT == '풍랑' : warnTy  = 'WW'
			if WRT == '태풍' : warnTy  = 'TY'
			if WRT == '대설' : warnTy  = 'SN'
			if WRT == '황사' : warnTy  = 'YD'
			if WRT == '폭염' : warnTy  = 'HW'
			data2.append(['-', warnTy, today, 'AM', today, 'AM'])

	while ii <= len(WARNLIST)-1 :
		AA = WARNLIST[ii]
		BB = AA.split(':')

		for WRT in warnType : 
			WARN1 = ' '+WRT+'경보 ' ; WARN2 = ' '+WRT+'주의보 '
			data1 = []
			RM4 = []
			if BB[0] == WARN1 : #경보
				print(BB[0])
				warn2 = [] ; RM3 = []
				CC = BB[1].split(',')
				RM = BB[1].split(')')
				for DDD in RM : # ~~ 제외 목록만들기
					if '제외' in DDD : 
						EE = DDD[DDD.find('(')+1:]
						SV = DDD.replace(', ',' ').split(' ')
						iii = 0
						while iii < len(SV) : 
							if '(' in SV[iii] : 
								SV2 = SV[iii].split('(')
								SAVE = [SV2[0].strip()] # 제외 지역을 제외한 지역 적용을 위해 인천/~남도/~북도 등 살리는 지점정보
							iii += 1
						FF = EE.split(',')
						for RM1 in FF : 
							RM2 = RM1.strip().replace(')','')
							RM3 = RM2.strip().replace(' 제외','')
							RM4.append(RM2)
							RM4.append(RM3)
						#print(SAVE)
						bbb = 0
						while bbb < len(SAVE):
							rewarn = WARN_AREA_FN().warning_area(warn2 ,SAVE[bbb], today, 'AM', WRT,'Y')
							bbb += 1
						data1 = data1 + rewarn
						#print(data1)
				for DD in CC:
					if '(' in DD :
						EE = DD[DD.find('(')+1:]
						FF = EE.strip().replace(')','')
					else :
						EE = DD
						FF = EE.strip().replace(')','')

					WARN_AREA = FF.strip()
					WARNING = WARN_AREA_FN().warning_area(warn2 ,WARN_AREA, today, 'AM', WRT,'Y')
					data1 = WARNING

				if len(RM4) >= 1 : # ~~ 제외 목록이 있을 경우 리스트에서 제거
					kk = 0
					while kk <= len(RM4)-1 : 
						RMSTN = RM4[kk]
						kkk = 0
						while kkk < len(data1) : 
							if data1[kkk][0] == RMSTN : 
								data1.pop(kkk)
							kkk += 1
						kk += 1	

			if BB[0]  == WARN2 : #주의보
				print(BB[0])
				warn3 = [] ; RM3 = []
				CC = BB[1].split(',')
				RM = BB[1].split(')')
				for DDD in RM : # ~~ 제외 목록만들기
					if '제외' in DDD : 
						EE = DDD[DDD.find('(')+1:]
						SV = DDD.replace(', ',' ').split(' ')
						iii = 0
						while iii < len(SV) : 
							if '(' in SV[iii] : 
								SV2 = SV[iii].split('(')
								SAVE = [SV2[0].strip()] # 제외 지역을 제외한 지역 적용을 위해 인천/~남도/~북도 등 살리는 지점정보
							iii += 1
						FF = EE.split(',')
						for RM1 in FF : 
							RM2 = RM1.strip().replace(')','')
							RM3 = RM2.strip().replace(' 제외','')
							RM4.append(RM2)
							RM4.append(RM3)
						#print(SAVE)
						bbb = 0
						while bbb < len(SAVE):
							rewarn = WARN_AREA_FN().warning_area(warn3 ,SAVE[bbb], today, 'AM', WRT,'N')
							bbb += 1
						data1 = data1 + rewarn
						#print(data1)
				for DD in CC:
					if '(' in DD :
						EE = DD[DD.find('(')+1:]
						FF = EE.strip().replace(')','')
					else :
						EE = DD
						FF = EE.strip().replace(')','')

					WARN_AREA = FF.strip()
					WARNING = WARN_AREA_FN().warning_area(warn3 ,WARN_AREA, today, 'AM', WRT,'N')
					data1 = WARNING

				if len(RM4) >= 1 : # ~~ 제외 목록이 있을 경우 리스트에서 제거
					kk = 0
					while kk <= len(RM4)-1 : 
						RMSTN = RM4[kk]
						kkk = 0
						while kkk < len(data1) : 
							if data1[kkk][0] == RMSTN : 
								data1.pop(kkk)
							kkk += 1
						kk += 1	

				data2 = data2 + data1
		ii += 1
	#for WARN_1 in data2 : print(WARN_1[0],WARN_1[1],WARN_1[2],WARN_1[3])

	#[예비특보현황]---------------------------------------------------------------------------------------------
	WARNLIST = re.split('\(\d\)',WARNING2)
	#print(WARNLIST)

	if '없음' in WARNLIST :
		print('no reserve Warning')
	else :
		ii = 1
		while ii <= len(WARNLIST)-1 :
			for WRT in warnType : 
				data3 = []
				if WRT in WARNLIST[ii]  : 
					RE_WARN = RESERVE_WARN().re_warning(YR,ii,WARNLIST,WRT)
					data3 = RE_WARN
					data4 = data4 + data3

			ii = ii + 1		

	#for WARN_2 in data4 : print(WARN_2[0],WARN_2[1],WARN_2[2],WARN_2[3])

	#[특보해제예고]---------------------------------------------------------------------------------------------
	for WRT in warnType :
		if WRT == '호우' : warnTy  = 'SR'
		if WRT == '강풍' : warnTy  = 'SW'
		if WRT == '한파' : warnTy  = 'CW'
		if WRT == '건조' : warnTy  = 'DR'
		if WRT == '폭풍해일' : warnTy  = 'SS'
		if WRT == '풍랑' : warnTy  = 'WW'
		if WRT == '태풍' : warnTy  = 'TY'
		if WRT == '대설' : warnTy  = 'SN'
		if WRT == '황사' : warnTy  = 'YD'
		if WRT == '폭염' : warnTy  = 'HW'

		#WARNING3 = '(2) 풍랑주의보 변경\r\n o 해제 예고 : 9월 15일 오후(15시~18시)\r\n (1) 강풍주의보 변경\r\n o 해제 예고 : 16일 오후\r\n ' # 테스트용 자료
		WARNLIST2 = WARNING3.strip().split('\r\n')
		jj = 0
		while jj < len(WARNLIST2)-1 : 
			if WRT in WARNLIST2[jj] : 
				AA = WARNLIST2[jj+1].split(':')
				BB = AA[1].strip().split(' ')
				YR = today[0:4] ; DY =  today[6:]
				MN2 = today[4:6] #오늘의 월
				DY2 = today[6:]  #오늘의 일
				if len(BB) == 2 : #일자+시간
					MN = today[4:6]
					DY = BB[0].replace('일','')
					if MN2 == '12' and DY2 == '31' and int(DY) < 31 : #오늘이 연말이면, 해제예고 년월 변경
						YR = int(YR)+1 ; MN = 1
					if '아침' in BB[1] or '오전' in BB[1] : HR = 'AM' # 해제예고시각이 새벽이면 오전에 영향x, 새벽 제외
					if '저녁' in BB[1] or '오후' in BB[1] or '밤' in BB[1]: HR = 'PM' #해제예고시각이 밤(18시 이후)이면 오후까지 영향을 줌, 밤 포함
					EDY = str(date(int(YR),int(MN),int(DY)).strftime('%Y%m%d'))
					kk = 0
					while kk < len(data2) : 
						if warnTy == data2[kk][1] and (EDY != data2[kk][4] or HR != data2[kk][5]) :
							#print(data2[kk][5])
							data2[kk][4] = EDY ; data2[kk][5] = HR
						kk += 1 
				elif len(BB) == 3 : #월+일자+시간
					MN = BB[0].replace('월','')
					DY = BB[1].replace('일','')
					if MN2 == '12' and DY2 == '31' and int(DY) < 31 : #오늘이 연말이면, 해제예고 년월 변경
						YR = int(YR)+1 ; MN = 1
					if '아침' in BB[1] or '오전' in BB[1] : HR = 'AM' # 해제예고시각이 새벽이면 다음날 오전에 영향x, 새벽 제외
					if '저녁' in BB[1] or '오후' in BB[1] or '밤' in BB[1]: HR = 'PM' #해제예고시각이 밤(18시 이후)이면 오후까지 영향을 줌, 밤 포함
					EDY = str(date(int(YR),int(MN),int(DY)).strftime('%Y%m%d'))
					#print(WRT, warnTy, EDY, HR)
					kk = 0
					while kk < len(data2) : 
						if warnTy == data2[kk][1] and (EDY != data2[kk][4] or HR != data2[kk][5]) : data2[kk][4] = EDY ; data2[kk][5] = HR
						kk += 1 
			jj += 2
	#for WARN_1 in data2 : print(WARN_1[0],WARN_1[1],WARN_1[2],WARN_1[3],WARN_1[4],WARN_1[5])

	with open(dir1+'/KMA_WARNING.csv','w',encoding='utf8') as file:
		file.write('WARNING_AREA,TYPE,START_DAY,START_TIME,END_DAY,END_TIME\n')
		for i in data2:
			file.write('{0},{1},{2},{3},{4},{5}\n'.format(i[0],i[1],i[2],i[3],i[4],i[5])) # WARNING
		for i in data4:
			file.write('{0},{1},{2},{3},{4},{5}\n'.format(i[0],i[1],i[2],i[3],i[4],i[5])) # RESERVE WARNING
	print('SR : Strong Rain, 호우주의보/경보/예비특보')
	print('SW : Strong Wind, 강풍주의보/경보/예비특보')
	print('CW : Cold Wave,   한파주의보/경보/예비특보')
	print('DR : Dry,         건조주의보/경보/예비특보')
	print('SS : Storm Surge, 폭풍해일주의보/경보/예비특보')
	print('WW : Wind Wave,   풍랑주의보/경보/예비특보')
	print('TY : Typhoon,     태풍주의보/경보/예비특보')
	print('SN : Snow(Havy),  대설주의보/경보/예비특보')
	print('YD : Yellow Dust, 황사주의보/경보/예비특보')
	print('HW : Heat Wave,   폭염주의보/경보/예비특보')
	print('#경보(Warning)는 약어 뒤에 숫자1 붙음')
	print('#주의보(Watch)는 약어 뒤에 숫자2 붙음')
	print('#예비특보(Reserve Warning)는 약어 뒤에 숫자3 붙음')
	print("#KMA Warning data collection Complete========")
