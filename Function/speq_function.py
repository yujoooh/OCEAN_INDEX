class IndexScore:
	def temp_score(self,value):
		if   value < 20 : score = 1
		elif value < 22 : score = 2
		elif value < 24 : score = 3
		elif value < 27 : score = 4
		else            : score = 5
		return score
	
	def sst_score(self,value):
		if value == -999 : score = 0
		elif value < 14 : score = 1
		elif value < 18 : score = 2
		elif value < 20 : score = 3
		elif value < 22 : score = 4
		else            : score = 5
		return score

	def wind_score(self,value):
		if   value < 2  : score = 5
		elif value < 5  : score = 4
		elif value < 8  : score = 3
		elif value < 10 : score = 2
		else            : score = 1
		return score

	def wave_score(self,value):
		if value == -999 : score = 0
		elif value < 0.5 : score = 5
		elif value < 1.0 : score = 4
		elif value < 1.5 : score = 3
		elif value < 2.0 : score = 2
		else             : score = 1
		return score

	def rain_score(self,value):
		if   value < 1  : score = 5
		elif value <= 5  : score = 3
		elif value <= 10 : score = 2
		else             : score = 1
		return score                

	def warn_score(self,value):
		#if   value == '-' :	score = 5
		if   value.strip() == '-' :	score = 5
		else             : score = 1
		return score

	def total_score(self, temp, sst_1, sst, wind, wave, rain, warn):
		if sst == 0 or wave == 0 : 
			score = 0	
		elif sst_1 < 16 :
			score = (temp*0.2 + sst*1 + wind*1 + wave*1.8)/4.
		else  :
			score = (temp*0.2 + sst*0.4 + wind*1.2 + wave*2.2)/4.
		
		service_score = score
		if service_score > rain : service_score = rain
		if service_score > warn : service_score = warn
		return score, service_score

	def quotient_score(self,value) : 
		if value == 0 : score = '체험불가'
		elif value < 2 : score = '매우나쁨'
		elif value < 3 : score = '나쁨'
		elif value < 4 : score = '보통'
		elif value < 4.7 : score = '좋음'
		elif value >= 4.7 : score = '매우좋음'
		return score
