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
	#소조 후 1~2일 매우좋음, 소조 1일전~소조 좋음, 중조 보통, 대조 1일전~대조, 나쁨, 대조 후 1~2일
	def tide_score(self,value):
		if   value >= 1  and value <= 2   : score = 5
		elif value >= 14 and value <= 15  : score = 4
		elif (value >= 3  and value <= 6) or (value >= 11  and value <= 13) : score = 3
		elif value >= 7  and value <= 8  : score = 2
		elif value >= 9  and value <= 10   : score = 1
		return score

	def wave_score(self,value):
		if   value == -999 : score = 0
		elif value <= 0.2   : score = 5
		elif value <= 0.5   : score = 4
		elif value <= 1.0   : score = 3
		elif value <= 2.0   : score = 2
		else                : score = 1
		return score

	def current_score(self,value):
		if   value < 0.4*0.51444444 : score = 5
		elif value < 0.7*0.51444444 : score = 4
		elif value < 0.9*0.51444444 : score = 3
		elif value < 1.0*0.51444444 : score = 2
		else             			: score = 1
		return score

	def sst_score(self,value):
		if   value == -999 : score = 0
		elif value < 18    : score = 1
		elif value < 20    : score = 2
		elif value < 22    : score = 3
		elif value < 24    : score = 4
		else               : score = 5
		return score

	def warn_score(self,value):
		#if   value == '-' :	score = 5
		if   value.strip() == '-' :	score = 5
		else             : score = 1
		return score

	def total_score(self, tide, wave, current, sst, warn):
		if wave == 0 or sst == 0: 
			score = 0
		else :
			score = round((tide*0.8 + wave*1.8 + current*1.0 + sst*0.4)/4.,2)
		service_score = score
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
