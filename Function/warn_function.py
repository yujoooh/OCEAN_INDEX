from datetime import date, timedelta
from Function.warn_area_function import WARN_AREA_FN
class RESERVE_WARN: # 예비특보
	
	def re_warning(self,YR,ii,WARNLIST, TYPE):
		warn = []
		AA = WARNLIST[ii].split('\r\n')
		jj = 1
		if TYPE == '호우' : warnType  = 'SR3'
		if TYPE == '강풍' : warnType  = 'SW3'
		if TYPE == '한파' : warnType  = 'CW3'
		if TYPE == '건조' : warnType  = 'DR3'
		if TYPE == '폭풍해일' : warnType  = 'SS3'
		if TYPE == '풍랑' : warnType  = 'WW3'
		if TYPE == '태풍' : warnType  = 'TY3'
		if TYPE == '대설' : warnType  = 'SN3'
		if TYPE == '황사' : warnType  = 'YD3'
		if TYPE == '폭염' : warnType  = 'HW3'
		
		if AA[-1] :
			len_AA = len(AA) - 1
		else:
			len_AA = len(AA) - 2
		while jj <= len_AA :
			#[풍랑예비특보 발효 예정시각]
			BB = AA[jj].split(':')
			RE_SDAY = BB[0][1:].strip().split(' ')
			RE_SMM = RE_SDAY[0].replace('월','')
			RE_SDD = RE_SDAY[1].replace('일','')
			RE_SHH = RE_SDAY[2]
			
			RE_SDAY = str(date(int(YR),int(RE_SMM),int(RE_SDD)).strftime('%Y%m%d'))
			RE_EDAY = str(date(int(YR),int(RE_SMM),int(RE_SDD)).strftime('%Y%m%d'))
			if RE_SHH == '새벽' or  RE_SHH == '아침' or RE_SHH == '오전' :
				RE_SHR = 'AM' ; RE_EHR = 'PM' # 예비특보는 해제예고가 없으므로 1일만 적용
			elif RE_SHH == '오후' or  RE_SHH == '낮'  or  RE_SHH == '이른오후' or  RE_SHH == '늦은오후':
				RE_SHR = 'PM' ; RE_EHR = 'AM' # 예비특보는 해제예고가 없으므로 1일만 적용
				RE_SDAY = str(date(int(YR),int(RE_SMM),int(RE_SDD)).strftime('%Y%m%d'))
				RE_EDAY = str((date(int(YR),int(RE_SMM),int(RE_SDD)) + timedelta(1)).strftime('%Y%m%d'))
			elif RE_SHH == '밤' or RE_SHH == '저녁' or RE_SHH == '늦은밤' : # 밤이나 저녁이면 다음날 오전부터 적용 : 09~18시 기준으로 서비스 하기 때문
				RE_SHR = 'AM' ; RE_EHR = 'PM'  # 예비특보는 해제예고가 없으므로 1일만 적용
				RE_SDAY = str((date(int(YR),int(RE_SMM),int(RE_SDD)) + timedelta(1)).strftime('%Y%m%d'))
				RE_EDAY = str((date(int(YR),int(RE_SMM),int(RE_SDD)) + timedelta(1)).strftime('%Y%m%d'))
			else :
				RE_SHR = 'AM' ; RE_EHR = 'PM' # 예비특보는 해제예고가 없으므로 1일만 적용
			
			RM4 = []
			CC = BB[1].split(',')
			RM = BB[1].split(')')
			warn2 =[]
			#print(TYPE, RE_SDAY, BB[1])
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

					bbb = 0
					while bbb < len(SAVE):
						rewarn = WARN_AREA_FN().warning_area(warn2 ,SAVE[bbb], RE_SDAY, RE_SHR, TYPE,'N')
						bbb += 1
					warn = warn + rewarn

			for DD in CC:
				if '(' in DD :
					EE = DD[DD.find('(')+1:]
					FF = EE.strip().replace(')','')
				else :
					EE = DD
					FF = EE.strip().replace(')','')

				RE_WARN_AREA = FF
				if RE_WARN_AREA == '전해상' :
					warn.append(['전해상', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해중부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해중부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해중부안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해중부바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['인천·경기북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['인천·경기남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['충남북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['충남남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부북쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부북쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부북쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부남쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부남쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부남쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전북북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전북남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남북부서해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남중부서해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남남부서해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

					warn.append(['동해남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부남쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부남쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부북쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부북쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['울산앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경북남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경북북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해중부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해중부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해중부안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해중부바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['강원북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['강원중부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['강원남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					
					warn.append(['남해동부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해동부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해동부안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해동부바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경남서부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경남중부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['거제시동부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['부산앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해서부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해서부서쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해서부동쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남서부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남동부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

					warn.append(['제주도앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도동부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도서부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도남서쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도남동쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도남쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도남쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					
				elif RE_WARN_AREA == '서해전해상' :
					warn.append(['서해전해상', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해중부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해중부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해중부안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해중부바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['인천·경기북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['인천·경기남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['충남북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['충남남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부북쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부북쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부북쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부남쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부남쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부남쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전북북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전북남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남북부서해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남중부서해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남남부서해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
								
				elif RE_WARN_AREA == '서해중부전해상' :
					warn.append(['서해전해상', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해중부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해중부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해중부안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해중부바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['인천·경기북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['인천·경기남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['충남북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['충남남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					
				elif RE_WARN_AREA == '서해남부전해상' :
					warn.append(['서해남부전해상', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부북쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부북쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부북쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부남쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부남쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부남쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전북북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전북남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남북부서해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남중부서해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남남부서해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

				elif RE_WARN_AREA == '서해중부앞바다' :
					warn.append(['서해중부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['인천·경기북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['인천·경기남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['충남북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['충남남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

				elif RE_WARN_AREA == '서해중부먼바다' :
					warn.append(['서해중부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해중부안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해중부바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

				elif RE_WARN_AREA == '서해남부앞바다' :
					warn.append(['서해남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전북북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전북남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남북부서해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남중부서해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남남부서해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

				elif RE_WARN_AREA == '서해남부먼바다' :
					warn.append(['서해남부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부북쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부북쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부북쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부남쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부남쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['서해남부남쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

				elif RE_WARN_AREA == '남해전해상' :
					warn.append(['남해전해상', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해동부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해동부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해동부안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해동부바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경남서부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경남중부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['거제시동부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['부산앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해서부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해서부서쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해서부동쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남서부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남동부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

				elif RE_WARN_AREA == '남해동부전해상' :
					warn.append(['남해동부전해상', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해동부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해동부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해동부안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해동부바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경남서부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경남중부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['거제시동부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['부산앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					
				elif RE_WARN_AREA == '남해서부전해상' :
					warn.append(['남해서부전해상', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해서부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해서부서쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해서부동쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남서부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남동부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					
				elif RE_WARN_AREA == '남해서부앞바다' :
					warn.append(['남해서부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남서부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전남동부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

				elif RE_WARN_AREA == '남해서부먼바다' :
					warn.append(['남해서부서쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해서부동쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
				
				elif RE_WARN_AREA == '남해동부앞바다' :
					warn.append(['남해동부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경남서부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경남중부남해앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['거제시동부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['부산앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

				elif RE_WARN_AREA == '제주도전해상' :
					warn.append(['제주도전해상', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도동부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도서부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도남서쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도남동쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도남쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도남쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
				
				elif RE_WARN_AREA == '제주도앞바다' :
					warn.append(['제주도앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도동부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도서부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

				elif RE_WARN_AREA == '동해전해상' :
					warn.append(['동해전해상', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부남쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부남쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부북쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부북쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['울산앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경북남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경북북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

					warn.append(['동해중부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해중부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해중부안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해중부바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['강원북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['강원중부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['강원남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					
				elif RE_WARN_AREA == '동해남부전해상' :				
					warn.append(['동해남부전해상', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부남쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부남쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부북쪽안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해남부북쪽바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['울산앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경북남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경북북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

				elif RE_WARN_AREA == '동해중부전해상' :	
					warn.append(['동해중부전해상', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해중부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해중부먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해중부안쪽먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해중부바깥먼바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['강원북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['강원중부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['강원남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					
				elif RE_WARN_AREA == '동해남부앞바다' :				
					warn.append(['동해남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['울산앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경북남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경북북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

				elif RE_WARN_AREA == '동해중부앞바다' :	
					warn.append(['동해중부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['강원북부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['강원중부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['강원남부앞바다', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	

				elif RE_WARN_AREA == '경기도' :	
					warn.append(['광명', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['과천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['안산', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['시흥', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['부천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['김포', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['강화', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['동두천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['연천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['포천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['가평', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['고양', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['양주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['의정부', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['파주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['수원', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['성남', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['안냥', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['구리', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['남양주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['오산', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['평택', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['군포', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['의왕', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['하남', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['용인', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['이천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['안성', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['화성', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['여주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['광주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	 #전라도 광주와 구분 필요
					warn.append(['양평', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['옹진', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['서해5도', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	

				elif RE_WARN_AREA == '강원도' :	
					warn.append(['강릉평지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['동해평지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['태백', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['삼척평지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['속초평지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['고성평지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['양양평지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['영월', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['평창평지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['정선평지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['횡성', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['원주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['철원', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['화천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['홍천평지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['춘천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['양구평지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['인제평지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['강원북부산지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['강원중부산지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['강원남부산지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	

				elif RE_WARN_AREA == '전라남도' :	
					warn.append(['나주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['담양', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['곡성', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['구례', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['장성', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['화순', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['고흥', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['보성', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['여수', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['광양', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['순천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['장흥', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['강진', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['해남', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['완도', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['영암', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['무안', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['함평', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['영광', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['목포', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['신안', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['진도', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					#warn.append(['흑산도.홍도', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	#특보 목록 조회결과 전라남도 범주에 미포함
					warn.append(['거문도.초도', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	

				elif RE_WARN_AREA == '충청남도' :	
					warn.append(['천안', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['공주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['아산', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['논산', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['금산', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['부여', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['청양', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['예산', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['태안', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['당진', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['서산', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['보령', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['서천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['홍성', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['계룡', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	

				elif RE_WARN_AREA == '충청북도' :	
					warn.append(['청주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['보은', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['괴산', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['옥천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['영동', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['충주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['제천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['진천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['음성', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['단양', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['증평', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	

				elif RE_WARN_AREA == '전라북도' :	
					warn.append(['고창', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['부안', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['군산', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['김제', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['완주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['진안', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['무주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['장수', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['임실', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['순창', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['익산', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['정읍', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['전주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남원', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

				elif RE_WARN_AREA == '경상북도' :	
					warn.append(['구미', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['영천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경산', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['군위', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['청도', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['고령', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['성주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['칠곡', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['김천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['상주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['문경', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['예천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['안동', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['영주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['의성', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['청송', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['영양평지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['봉화평지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['울릉도-독도', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['영덕', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['울진평지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['포항', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['경북북동산지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

				elif RE_WARN_AREA == '경상남도' :	
					warn.append(['양산', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['창원', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['김해', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['밀양', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['의령', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['함안', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['창녕', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['진주', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['하동', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['산청', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['함양', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['거창', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['합천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['통영', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['사천', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['거제', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['고성', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['남해', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

				elif RE_WARN_AREA == '제주도' :	
					warn.append(['제주도산지', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도서부', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도북부', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])
					warn.append(['제주도동부', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['제주도남부', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	
					warn.append(['추자도', warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])	

				else :
					#print(RE_WARN_AREA, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR)
					warn.append([RE_WARN_AREA, warnType, RE_SDAY, RE_SHR, RE_EDAY, RE_EHR])

			if len(RM4) >= 1 : # ~~ 제외 목록이 있을 경우 리스트에서 제거
				kk = 0
				while kk <= len(RM4)-1 : 
					RMSTN = RM4[kk]
					#print(RMSTN)
					kkk = 0
					while kkk < len(warn) : 
						if warn[kkk][0] == RMSTN : 
							warn.pop(kkk)
						kkk += 1
					kk += 1	
			jj += 1
		return warn
