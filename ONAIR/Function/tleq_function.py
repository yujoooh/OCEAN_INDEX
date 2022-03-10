class TL_time_cal:
#[Lunar date to tide time calculation]====================================================================
	def tl_time(self, ymd, start_time, end_time):
		if start_time == '-' :
			start_hr = 0; end_hr = 0; exp_hr = 0; ampm = 'daily'
			start_hr='0:00'
			end_hr='0:00'
			print(ymd, start_hr, end_hr, exp_hr, ampm)
		else :
			st = start_time.split(':') ; shr = int(st[0]) ; smn = int(st[1])
			et =   end_time.split(':') ; ehr = int(et[0]) ; emn = int(et[1])

			if shr <= 9 :
				shr = 9 ; smn = 0
			elif shr >= 18 :
				shr = 18 ; smn = 0
				ehr = 18 ; emn = 0
				
			if ehr >= 18 :
				ehr = 18 ; emn = 0
			
			if shr < 12 and ehr < 12: ampm = 'AM'
			if shr >= 12 and ehr >= 12 : ampm = 'PM'
			if shr < 12 and ehr >= 12 : ampm = 'daily'
			
			if emn != 0 and smn != 0 : exp_hr = round((ehr - shr) + (emn/60 - smn/60),2)
			if emn == 0 and smn != 0 : exp_hr = round((ehr - shr) - smn/60,2)
			if emn != 0 and smn == 0 : exp_hr = round((ehr - shr) + emn/60,2)
			if emn == 0 and smn == 0 : exp_hr = round((ehr - shr),2)
	
			#print(shr, smn, ehr, emn, exp_hr)
			start_hr=str((f'{shr:02d}'))+':'+str((f'{smn:02d}'))
			end_hr=str((f'{ehr:02d}'))+':'+str((f'{emn:02d}'))
			
			print(ymd, start_hr, end_hr, exp_hr, ampm)
	
		return start_hr, end_hr, exp_hr, ampm


class IndexScore:
	#소조 후 1~2일 매우좋음, 소조 1일전~소조 좋음, 중조 보통, 대조 1일전~대조, 나쁨, 대조 후 1~2일

	def exphr_score(self,value):
		if   value == 0     : score = 0
		elif value < 0.5    : score = 1
		elif value < 1.0    : score = 2
		elif value < 1.5    : score = 3
		elif value < 2.0    : score = 4
		else                : score = 5
		return score

	def temp_score(self,value):
		if   value < 16    : score = 1
		elif value < 18    : score = 2
		elif value < 21    : score = 3
		elif value < 24    : score = 4
		else               : score = 5
		return score

	def wind_score(self,value):
		if   value < 2     : score = 5
		elif value < 5     : score = 4
		elif value < 9     : score = 3
		elif value < 14    : score = 2
		else               : score = 1
		return score

	def sky_score(self,value):
		if   value <= 2 : score = 5
		elif value == 3 : score = 3
		elif value == 4 : score = 2
		elif value == 5 : score = 1
		return score
		
	def rain_score(self,value):
		if   value < 1  : score = 5
		elif value <= 5  : score = 3
		elif value <= 10 : score = 2
		else             : score = 1
		return score                

	def warn_score(self,value):
		#if   value == '-' :	score = 5
		if   value.strip() == '-' or value.strip() == 'WW1' or value.strip() == 'WW2' or value.strip() == 'WW3' :	score = 5
		else             : score = 1
		return score

	def total_score(self, exphr, temp, wind, sky, rain, warn):
		if exphr == 1 :
			score = 1
		elif exphr == 0 : 
			score = 0
		else :
			score = round((exphr*2.5 + temp*0.2 + wind*0.5 + sky*0.8)/4.,2)
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
