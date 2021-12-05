def temp_score(value):
	if   value < 20 : score = 1
	elif value < 22 : score = 2
	elif value < 24 : score = 3
	elif value < 27 : score = 4
	else            : score = 5
	return score
	
def sst_score(self,value):
	if   value < 14 : score = 1
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
	if   value < 0.5 : score = 5
	elif value < 1.0 : score = 4
	elif value < 1.5 : score = 3
	elif value < 2.0 : score = 2
	else             : score = 1
	return score

def rain_score(self,value):
	if   value == 0  : score = 5
	elif value <= 5  : score = 3
	elif value <= 10 : score = 2
	else             : score = 1
	return score

def warn_score(self,value):
	if   value == 1 : score = 1
	else            : score = 5
	return score

def total_score(self, temp, sst, wind, wave, rain, warn):
	if temp < 16:
		score = (temp*0.2 + sst*1 + wind*1 + wave*1.8)/4. 
	else :
		score = (temp*0.2 + sst*0.4 + wind*1.2 + wave*2.2)/4. 
	
	if score > rain : score = rain
	if score > warn : score = warn
	return score