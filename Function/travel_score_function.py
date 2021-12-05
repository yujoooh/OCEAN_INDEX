class IndexScore:
	def sky_score(self, weight, value) : 
		if   value >= 1.0 and value < 2.0 : score = weight 
		elif value >= 2.0  and value < 3.5 : score = weight*0.7  
		elif value >= 3.5                   : score = weight*0.3
		return round(score,1)

	def temp_score(self, weight, value):
		#print(weight, value)
		if   value >= 15 and value <= 21 : score = weight
		elif value < 3 or value > 35     : score = 0 # 폭염/한파특보 기준... 어차피 특보 발효되면 매우나쁨...(안전하게!)
		elif value > 21                  : score = weight - ((value - 21) * weight / 14) # 14 : 기온 21~35 범위 1도 간격 수
		elif value < 15                  : score = weight - ((15 - value) * weight / 12) # 12 : 기온 3~15 범위 1도 간격 수
		return round(score,1)

	def wspd_score(self, weight, value):
		if   value <= 14                 : score = ((14 - value) * weight / 14)
		elif value > 14                  : score = 0 # 강풍주의보 발효기준 이상이므로..(안전하게!)
		return round(score,1)

	def sst_score(self, weight, value):
		rate = 0.8  # 수온이 22 이상일 경우 낚시에만 지장이 있는 것이므로, 최대점수(weight)의 80%로 설정 (체험 6개중 낚시만 고수온에 영향.. 원래 약 83%)
		if   value >= 20 and value <= 22 : score = weight
		elif value <= 15                  : score = 0                # 수온이 15 이하일 경우 저체온증이 우려되므로(보수적으로 적용)
		elif value > 22                  : score = weight - ((value - 22) * (weight*(1-rate))/3)# 22도 이상일 바다낚시만 어려움(20% 비율로 천천히 감소)
		elif value < 20                  : score = weight - ((20 - value) * (weight*rate)/4)# 20도 이하일 때(80% 비율로 급격히 감소)
		return round(score,1)

	def wave_score(self, weight, value):
		rate = 0.85 # 파고 0일경우 없을 경우 서핑만 못하는 것이므로, 최대점수(weight)의 80%로 설정 (체험 8개중 파고가 0일때 제일 좋은게 7가지.. 원래 약 87.5%)
		if value == 0.5                  : score = weight
		elif value > 2.0                 : score = 0   # 파고가 2m 이상일 경우 안전이 우려되므로(보수적으로 적용)
		elif value > 0.5                 : score = weight - ((value - 0.5) * weight / 1.5) # 선형감소
		elif value < 0.5                 : score = weight * rate # 파고 0.5m 이하 최대점수의 85% 고정
		return round(score,1)

	def tide_score(self, weight, value):
		# 7~11물(대조기)에도 스노클링, 스쿠버, 바다낚시 가능하므로, 최대점수(weight)의 80%로 설정(3개체험중 2개 + 바다낚시 절반 원래 약 83%)
		if value >= 7 and value <= 11    : score = weight * 0.5 # 대조기
		elif value >= 12 and value <= 14 : score = weight * 0.8 # 중조기
		elif value >= 4 and value <= 6   : score = weight * 0.8 # 중조기
		else                             : score = weight       # 소조기
		return round(score,1)

	def current_score(self, weight, value):
		ms_to_knot = 0.51444444 # m/s to knot 단위변환
		if   value/ms_to_knot < 1.0 : score = (1.0 - value/ms_to_knot) * weight / 1.0 
		else                        : score = 0
		return round(score,1)

	def rain_score(self, score_sum, value):
		if   value <= 1.0 : score = score_sum # 매우좋음(76~100), 좋음(66~75), 보통(56~66), 나쁨(41~55), 매우나쁨(0~40)
		elif value <= 5 : score = 60 # 보통(중간점수)
		elif value < 10 : score = 45 # 나쁨(중간점수)
		else            : score = 20 # 매우나쁨(중간점수)
		return round(score,1)

	def warn_score(self, rain_scre, warn1, warn2): # 강수점수 반영후 점수, 해상특보, 육상특보
		if   warn1 == '-' and warn2 == '-': score = rain_scre # 해상 or 육상 특보가 없을 경우.
		elif warn2 == 'HW2' or warn2 == 'HW3' : # 폭염주의보/예비특보일경우 1단계 하향
			if rain_scre > 75   : score = 70
			elif rain_scre > 65 : score = 60
			elif rain_scre > 55 : score = 50
			elif rain_scre > 40 : score = 20
			else            : score = 20
		else                             : score = 20 # 매우나쁨(중간점수)
		return round(score,1)

	def score_class(self, value) : 
		if value > 75   : s_class = '매우좋음'
		elif value > 65 : s_class = '좋음'
		elif value > 55 : s_class = '보통'
		elif value > 40 : s_class = '나쁨'
		else            : s_class = '매우나쁨'
		return s_class
