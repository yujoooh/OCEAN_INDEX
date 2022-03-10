class WARN_AREA_FN:
	def warning_area(self, warn, WARN_AREA, SDAY, SHR, TYPE, YN):
		#'강풍', '호우', '한파', '건조', '폭풍해일', '풍랑', '태풍', '대설', '황사', '폭염'
		#print(TYPE)
		if YN =='Y' : #경보
			if TYPE == '호우' : warnType  = 'SR1'
			if TYPE == '강풍' : warnType  = 'SW1'
			if TYPE == '한파' : warnType  = 'CW1'
			if TYPE == '건조' : warnType  = 'DR1'
			if TYPE == '폭풍해일' : warnType  = 'SS1'
			if TYPE == '풍랑' : warnType  = 'WW1'
			if TYPE == '태풍' : warnType  = 'TY1'
			if TYPE == '대설' : warnType  = 'SN1'
			if TYPE == '황사' : warnType  = 'YD1'
			if TYPE == '폭염' : warnType  = 'HW1'
		else : #주의보
			if TYPE == '호우' : warnType  = 'SR2'
			if TYPE == '강풍' : warnType  = 'SW2'
			if TYPE == '한파' : warnType  = 'CW2'
			if TYPE == '건조' : warnType  = 'DR2'
			if TYPE == '폭풍해일' : warnType  = 'SS2'
			if TYPE == '풍랑' : warnType  = 'WW2'
			if TYPE == '태풍' : warnType  = 'TY2'
			if TYPE == '대설' : warnType  = 'SN2'
			if TYPE == '황사' : warnType  = 'YD2'
			if TYPE == '폭염' : warnType  = 'HW2'			
		
		if WARN_AREA == '전해상' :
			warn.append(['전해상', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해중부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해중부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해중부안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해중부바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['인천·경기북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['인천·경기남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['충남북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['충남남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부북쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부북쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부북쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부남쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부남쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부남쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전북북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전북남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남북부서해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남중부서해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남남부서해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])

			warn.append(['동해남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부남쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부남쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부북쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부북쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['울산앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경북남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경북북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해중부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해중부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해중부안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해중부바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['강원북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['강원중부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['강원남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])

			warn.append(['남해동부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해동부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해동부안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해동부바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경남서부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경남중부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['거제시동부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['부산앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해서부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해서부서쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해서부동쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남서부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남동부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])

			warn.append(['제주도앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도동부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도서부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도남서쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도남동쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도남쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도남쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
		
		elif WARN_AREA == '서해전해상' :
			warn.append(['전해상', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해중부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해중부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해중부안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해중부바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['인천·경기북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['인천·경기남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['충남북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['충남남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부북쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부북쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부북쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부남쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부남쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부남쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전북북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전북남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남북부서해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남중부서해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남남부서해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
						
		elif WARN_AREA == '서해중부전해상' :
			warn.append(['서해중부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해중부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해중부안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해중부바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['인천·경기북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['인천·경기남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['충남북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['충남남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			
		elif WARN_AREA == '서해남부전해상' :
			warn.append(['서해남부전해상', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부북쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부북쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부북쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부남쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부남쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부남쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전북북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전북남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남북부서해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남중부서해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남남부서해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])

		elif WARN_AREA == '서해중부앞바다' :
			warn.append(['서해중부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['인천·경기북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['인천·경기남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['충남북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['충남남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])

		elif WARN_AREA == '서해남부앞바다' :
			warn.append(['서해남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전북북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전북남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남북부서해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남중부서해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남남부서해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])

		elif WARN_AREA == '서해남부먼바다' :
			warn.append(['서해남부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부북쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부북쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부북쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부남쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부남쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['서해남부남쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])


		elif WARN_AREA == '남해전해상' :
			warn.append(['남해전해상', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해동부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해동부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해동부안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해동부바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경남서부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경남중부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['거제시동부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['부산앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해서부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해서부서쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해서부동쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남서부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남동부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])

		elif WARN_AREA == '남해동부전해상' :
			warn.append(['남해동부전해상', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해동부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해동부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해동부안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해동부바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경남서부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경남중부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['거제시동부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['부산앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			
		elif WARN_AREA == '남해서부전해상' :
			warn.append(['남해서부전해상', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해서부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해서부서쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해서부동쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남서부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남동부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])

		elif WARN_AREA == '남해서부앞바다' :
			warn.append(['남해서부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남서부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전남동부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])

		elif WARN_AREA == '남해서부먼바다' :
			warn.append(['남해서부서쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해서부동쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
		
		elif WARN_AREA == '남해동부앞바다' :
			warn.append(['남해동부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경남서부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경남중부남해앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['거제시동부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['부산앞바다', warnType, SDAY, SHR, SDAY, 'PM'])

		elif WARN_AREA == '제주도전해상' :
			warn.append(['제주도전해상', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도동부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도서부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도남서쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도남동쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도남쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도남쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
		
		elif WARN_AREA == '제주도앞바다' :
			warn.append(['제주도앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도동부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도서부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])

		elif WARN_AREA == '동해전해상' :
			warn.append(['동해전해상', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부남쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부남쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부북쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부북쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['울산앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경북남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경북북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
            
			warn.append(['동해중부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해중부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해중부안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해중부바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['강원북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['강원중부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['강원남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])


			
		elif WARN_AREA == '동해남부전해상' :				
			warn.append(['동해남부전해상', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부남쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부남쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부북쪽안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해남부북쪽바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['울산앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경북남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경북북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])

		elif WARN_AREA == '동해중부전해상' :	
			warn.append(['동해중부전해상', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해중부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해중부먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해중부안쪽먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해중부바깥먼바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['강원북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['강원중부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['강원남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			
		elif WARN_AREA == '동해남부앞바다' :				
			warn.append(['동해남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['울산앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경북남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경북북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])

		elif WARN_AREA == '동해중부앞바다' :	
			warn.append(['동해중부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['강원북부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['강원중부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['강원남부앞바다', warnType, SDAY, SHR, SDAY, 'PM'])	

		elif WARN_AREA == '경기도' :	
			warn.append(['광명', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['과천', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['안산', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['시흥', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['부천', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['김포', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['강화', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['동두천', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['연천', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['포천', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['가평', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['고양', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['양주', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['의정부', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['파주', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['수원', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['성남', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['안냥', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['구리', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['남양주', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['오산', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['평택', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['군포', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['의왕', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['하남', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['용인', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['이천', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['안성', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['화성', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['여주', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['광주', warnType, SDAY, SHR, SDAY, 'PM'])	 #전라도 광주와 구분 필요
			warn.append(['양평', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['옹진', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['서해5도', warnType, SDAY, SHR, SDAY, 'PM'])	

		elif WARN_AREA == '강원도' :	
			warn.append(['강릉평지', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['동해평지', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['태백', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['삼척평지', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['속초평지', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['고성평지', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['양양평지', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['영월', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['평창평지', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['정선평지', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['횡성', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['원주', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['철원', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['화천', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['홍천평지', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['춘천', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['양구평지', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['인제평지', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['강원북부산지', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['강원중부산지', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['강원남부산지', warnType, SDAY, SHR, SDAY, 'PM'])	

		elif WARN_AREA == '전라남도' :	
			warn.append(['나주', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['담양', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['곡성', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['구례', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['장성', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['화순', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['고흥', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['보성', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['여수', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['광양', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['순천', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['장흥', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['강진', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['해남', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['완도', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['영암', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['무안', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['함평', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['영광', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['목포', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['신안', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['진도', warnType, SDAY, SHR, SDAY, 'PM'])	
			#warn.append(['흑산도.홍도', warnType, SDAY, SHR, SDAY, 'PM'])	#특보 목록 조회결과 전라남도 범주에 미포함
			warn.append(['거문도.초도', warnType, SDAY, SHR, SDAY, 'PM'])	

		elif WARN_AREA == '충청남도' :	
			warn.append(['천안', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['공주', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['아산', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['논산', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['금산', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['부여', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['청양', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['예산', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['태안', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['당진', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['서산', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['보령', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['서천', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['홍성', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['계룡', warnType, SDAY, SHR, SDAY, 'PM'])	

		elif WARN_AREA == '충청북도' :	
			warn.append(['청주', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['보은', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['괴산', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['옥천', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['영동', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['충주', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['제천', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['진천', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['음성', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['단양', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['증평', warnType, SDAY, SHR, SDAY, 'PM'])	

		elif WARN_AREA == '전라북도' :	
			warn.append(['고창', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['부안', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['군산', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['김제', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['완주', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['진안', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['무주', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['장수', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['임실', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['순창', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['익산', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['정읍', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['전주', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남원', warnType, SDAY, SHR, SDAY, 'PM'])

		elif WARN_AREA == '경상북도' :	
			warn.append(['구미', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['영천', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경산', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['군위', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['청도', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['고령', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['성주', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['칠곡', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['김천', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['상주', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['문경', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['예천', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['안동', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['영주', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['의성', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['청송', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['영양평지', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['봉화평지', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['울릉도-독도', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['영덕', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['울진평지', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['포항', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경주', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['경북북동산지', warnType, SDAY, SHR, SDAY, 'PM'])

		elif WARN_AREA == '경상남도' :	
			warn.append(['양산', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['창원', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['김해', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['밀양', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['의령', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['함안', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['창녕', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['진주', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['하동', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['산청', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['함양', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['거창', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['합천', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['통영', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['사천', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['거제', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['고성', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['남해', warnType, SDAY, SHR, SDAY, 'PM'])

		elif WARN_AREA == '제주도' :	
			warn.append(['제주도산지', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도서부', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도북부', warnType, SDAY, SHR, SDAY, 'PM'])
			warn.append(['제주도동부', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['제주도남부', warnType, SDAY, SHR, SDAY, 'PM'])	
			warn.append(['추자도', warnType, SDAY, SHR, SDAY, 'PM'])	

		else :
			#print(WARN_AREA, warnType, SDAY, SHR, SDAY, 'PM')
			warn.append([WARN_AREA, warnType, SDAY, SHR, SDAY, 'PM'])
		
		return warn
