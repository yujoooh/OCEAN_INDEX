class Tide_time_lunar:
#[Lunar date to tide time calculation]====================================================================
	def lunar_to_mul(self,YMD):
		import lunardate as lunar 
		yr = YMD[0:4] ; mn = YMD[4:6] ; dy = YMD[6:7]
		#yr_lunar = lunar.LunarDate.today().year
		#mn_lunar = lunar.LunarDate.today().month
		#dy_lunar = lunar.LunarDate.today().day
		dy_lunar = lunar.LunarDate.fromSolarDate(yr,mn,dy).day
		
		if dy_lunar + 7 <= 15 : mul = dy_lunar + 7
		if dy_lunar + 7 > 15 and dy_lunar + 7 <= 30 : mul = dy_lunar + 7 - 15
		if dy_lunar + 7 > 30 : mul = dy_lunar + 7 - 30
		
		print(yr_lunar, mn_lunar, dy_lunar, mul)
		return score