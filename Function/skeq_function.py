class IndexScore:
	
	def sail_score(self,value):
		if   value <  0.5 : score = 5
		elif value <  1.5 : score = 4
		elif value <  2.5 : score = 3
		elif value <  3   : score = 2
		else              : score = 1
		return score
	
	def ton_score(self,value):
		if   value <= 100  : score = 1
		elif value <= 500  : score = 2
		elif value <= 1000 : score = 3
		elif value <= 5000 : score = 4
		elif value >  5000 : score = 5
		return score

	def wind_score(self,value):
		if   value == -999 : score = 0
		elif value < 2    : score = 5
		elif value < 5    : score = 4
		elif value < 9    : score = 3
		elif value < 14   : score = 2
		else               : score = 1
		return score

	def wave_score(self,value):
		if   value == -999 : score = 0
		elif value < 0.5   : score = 5
		elif value < 1.0   : score = 4
		elif value < 2.0   : score = 3
		elif value < 3.0   : score = 2
		else               : score = 1
		return score

	def warn_score(self,value):
		#if   value == '-' :	score = 5
		if   value.strip() == '-' :	score = 5
		else             : score = 1
		return score

	def total_score(self, sail, ton, wind, wave, warn):
		if wave == 0 :
			score = 0
		elif wave == 1 or wind == 1 : 
			score = 1
		elif wave ==2 or wind == 2 :
			score = 1.5
		else :
			score = (wave*1.8 + wind*0.9 + sail*0.8 + ton*0.5)/4.
		service_score = score
		if service_score > warn : service_score = warn
		return score, service_score

	def quotient_score(self,value) :
		if value == 0 : score = '체험불가'
		elif value < 1.5 : score = '매우나쁨'
		elif value < 2.5 : score = '나쁨'
		elif value < 3.5 : score = '보통'
		elif value < 4.5 : score = '좋음'
		elif value >= 4.5 : score = '매우좋음'
		return score
