class Tide_time_lunar:
#[Lunar date to tide time calculation]====================================================================
	def lunar_to_mul(self,YMD):
		import lunardate as lunar 
		yr = int(YMD[0:4]) ; mn = int(YMD[4:6]) ; dy = int(YMD[6:8])
		yr_lunar = lunar.LunarDate.fromSolarDate(yr,mn,dy).year
		mn_lunar = lunar.LunarDate.fromSolarDate(yr,mn,dy).month
		dy_lunar = lunar.LunarDate.fromSolarDate(yr,mn,dy).day
		
		if dy_lunar + 7 <= 15 : mul = dy_lunar + 7
		if dy_lunar + 7 > 15 and dy_lunar + 7 <= 30 : mul = dy_lunar + 7 - 15
		if dy_lunar + 7 > 30 : mul = dy_lunar + 7 - 30
		
		#print(YMD, yr_lunar, mn_lunar, dy_lunar, mul)
		return mul


class IndexScore:

	def tide_score(self,fish_type, value):
		if fish_type == 'RF' : #우럭
			if (value >= 14 and value <= 15 ) or value == 1 : score = 5
			if (value >= 2 and value <= 3 ) or (value >= 11 and value <= 13) : score = 4
			if (value >= 4 and value <= 5 ) or (value >= 9 and value <= 10) : score = 3
			if value == 6 or value == 8 : score = 2
			if value == 7 : score = 1	
			
		elif fish_type == 'OP' : #벵에돔
			if  value >= 7 and value <= 9 : score = 5
			if (value >= 5 and value <= 6 ) or (value >= 10 and value <= 11) : score = 4
			if (value >= 3 and value <= 4 ) or (value >= 12 and value <= 13) : score = 3
			if value == 2 or value == 14 : score = 2
			if value == 15 or value == 1 : score = 1	
			
		elif fish_type == 'BP' : #감성돔
			if  value >= 7 and value <= 9 : score = 5
			if (value >= 5 and value <= 6 ) or (value >= 10 and value <= 11) : score = 4
			if (value >= 3 and value <= 4 ) or (value >= 12 and value <= 13) : score = 3
			if value == 2 or value == 14 : score = 2
			if value == 15 or value == 1 : score = 1			

		elif fish_type == 'RP' : #참돔
			if  value == 7 : score = 5
			if (value >= 5 and value <= 6 ) or (value >= 8 and value <= 9) : score = 4
			if (value >= 3 and value <= 4 ) or (value >= 10 and value <= 11) : score = 3
			if (value >= 1 and value <= 2 ) or (value >= 12 and value <= 13) : score = 2
			if value == 14 or value == 15 : score = 1	
		
		elif fish_type == 'SB' : #농어
			if  value == 7 : score = 5
			if (value >= 5 and value <= 6 ) or (value >= 8 and value <= 9) : score = 4
			if (value >= 3 and value <= 4 ) or (value >= 10 and value <= 11) : score = 3
			if (value >= 1 and value <= 2 ) or (value >= 12 and value <= 13) : score = 2
			if value == 14 or value == 15 : score = 1	

		elif fish_type == 'RB' : #돌돔
			if  value == 4 or value == 12: score = 5
			if  value == 3 or value == 5 or value == 11 or value == 13 : score = 4
			if  value == 2 or value == 6 or value == 10 : score = 3
			if  value == 1 or value == 7 or value == 9 or value == 14 : score = 2
			if  value == 15 or value == 8 : score = 1

		elif fish_type == 'GR' : #열기
			if (value >= 14 and value <= 15 ) or value == 1 : score = 5
			if (value >= 2 and value <= 3 ) or (value >= 12 and value <= 13) : score = 4
			if value == 4 or value == 11 : score = 3
			if (value >= 5 and value <= 6 ) or (value >= 9 and value <= 10) : score = 2
			if value >= 7 and value <= 8: score = 1	
			
		elif fish_type == 'GP' : #볼락
			if (value >= 14 and value <= 15 ) or value == 1 : score = 5
			if (value >= 2 and value <= 3 ) or (value >= 12 and value <= 13) : score = 4
			if value == 4 or value == 11 : score = 3
			if (value >= 5 and value <= 6 ) or (value >= 9 and value <= 10) : score = 2
			if value >= 7 and value <= 8: score = 1	
		return score

	def wave_score(self,value):
		if   value == -999 : score = 0
		elif value <= 0.2   : score = 5
		elif value <= 0.5   : score = 4
		elif value <= 1.0   : score = 3
		elif value <= 2.0   : score = 2
		else                : score = 1
		return score

	def sst_score(self,fish_type, value):
		if fish_type == 'RF' : #우럭
			if  value >= 16 and value < 20 : score = 5
			if (value >= 14 and value < 16) or (value >= 20 and value < 22) : score = 4
			if (value >= 11 and value < 14) or (value >= 22 and value < 25) : score = 3
			if (value >= 8  and value < 11) or (value >= 25 and value < 30) : score = 2
			if value < 8 or value >= 30 : score = 1
			
		elif fish_type == 'OP' : #벵에돔
			if  value >= 17 and value < 21: score = 5
			if (value >= 15 and value < 17) or (value >= 21 and value < 23) : score = 4
			if (value >= 14 and value < 15) or (value >= 23 and value < 24) : score = 3
			if (value >= 13 and value < 14) or (value >= 24 and value < 25) : score = 2
			if value < 13 or value >= 25 : score = 1
			
		elif fish_type == 'BP' : #감성돔
			if  value >= 17 and value < 19: score = 5
			if (value >= 15 and value < 17) or (value >= 19 and value < 21) : score = 4
			if (value >= 13 and value < 15) or (value >= 21 and value < 23) : score = 3
			if (value >= 11 and value < 13) or (value >= 23 and value < 25) : score = 2
			if value < 11 or value >= 25 : score = 1			

		elif fish_type == 'RP' : #참돔
			if  value >= 18 and value < 21: score = 5
			if (value >= 15 and value < 18) or (value >= 21 and value < 24) : score = 4
			if (value >= 12 and value < 15) or (value >= 24 and value < 26) : score = 3
			if (value >= 10 and value < 12) or (value >= 26 and value < 28) : score = 2
			if value < 10 or value >= 28 : score = 1	
		
		elif fish_type == 'SB' : #농어
			if  value >= 19 and value < 21: score = 5
			if (value >= 18 and value < 19) or (value >= 21 and value < 23) : score = 4
			if (value >= 17 and value < 18) or (value >= 23 and value < 26) : score = 3
			if (value >= 16 and value < 17) or (value >= 26 and value < 28) : score = 2
			if value < 16 or value >= 28 : score = 1	

		elif fish_type == 'RB' : #돌돔
			if  value >= 23 and value < 26: score = 5
			if (value >= 20 and value < 23) or (value >= 26 and value < 27) : score = 4
			if (value >= 17 and value < 20) or (value >= 27 and value < 28) : score = 3
			if (value >= 8 and value < 17) or (value >= 28 and value < 30)  : score = 2
			if value < 8 or value >= 30 : score = 1

		elif fish_type == 'GR' : #열기
			if  value >= 13 and value < 16: score = 5
			if (value >= 11 and value < 13) or (value >= 16 and value < 18) : score = 4
			if (value >= 10 and value < 11) or (value >= 18 and value < 20) : score = 3
			if (value >= 9  and value < 10) or (value >= 20 and value < 21) : score = 2
			if value < 9 or value >= 21 : score = 1

		elif fish_type == 'GP' : #볼락
			if  value >= 14 and value < 15: score = 5
			if (value >= 13 and value < 14) or (value >= 15 and value < 16) : score = 4
			if (value >= 12 and value < 13) or (value >= 16 and value < 17) : score = 3
			if (value >= 11 and value < 12) or (value >= 17 and value < 18) : score = 2
			if value < 11 or value >= 18 : score = 1
		#print(fish_type, value, score)
		if value == -999 : score = 0
		return score

	def temp_score(self,value):
		if   value < 16   : score = 1
		elif value < 18   : score = 2
		elif value < 21   : score = 3
		elif value < 24   : score = 4
		else              : score = 5
		return score

	def wind_score(self,value):
		if   value == -999 : score = 0
		elif value <= 2    : score = 5
		elif value <= 5    : score = 4
		elif value <= 9    : score = 3
		elif value <= 14   : score = 2
		else               : score = 1
		return score

	def warn_score(self,value):
		#if   value == '-' :	score = 5
		if   value.strip() == '-' :	score = 5
		else             : score = 1
		return score

	def total_score(self, tide, wave, sst, temp, wind, warn):
		if wave == 0 or sst == 0 :
			score = 0 
		elif (wave*1.8 + wind*1.2)/3 < 3:
			score = round((wave*1.8 + wind*1.2)/3,2)
		else :
			score = round((tide*0.8 + wave*1.8 + sst*1.0 + temp*0.2 + wind*1.2)/5.,2)
		service_score = score
		if service_score > warn : service_score = warn
		return score, service_score

	def quotient_score(self,value) :
		if value == 0 : score = '금어기'
		elif value < 2 : score = '매우나쁨'
		elif value < 3 : score = '나쁨'
		elif value < 4 : score = '보통'
		elif value < 4.7 : score = '좋음'
		elif value >= 4.7 : score = '매우좋음'
		return score
