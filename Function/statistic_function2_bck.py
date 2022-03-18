class Statistic2:
#Daily OBS DATA Statistic function
	def min_max_ave(self, fcst_time, vars, T):
		import numpy as np

		#print(vars)
		vars_am = np.array(vars[T+1:T+5])
		vars_pm = np.array(vars[T+5:T+11])
		vars_day = np.array(vars[T+1:T+11])
		if len(vars_am) == 0 : vars_am = np.array([-999,-999,-999,-999])
		if len(vars_pm) == 0 : vars_pm = np.array([-999,-999,-999,-999,-999,-999])
		#print(vars_am, np.count_nonzero(vars_am == -999),vars_pm, np.count_nonzero(vars_pm == -999))
		#print(vars[T:T+10])
		#[Debug]
		#VAR_AM_MIN = np.min(vars_am[vars_am!=-999])  
		#VAR_PM_MIN = np.min(vars_pm[vars_pm!=-999])
		#VAR_DAY_MIN = np.min(vars_day[vars_day!=-999])
		#print(vars[T:T+9],VAR_AM_MIN,VAR_PM_MIN,VAR_DAY_MIN)
        
		#오전/오후 추출
		if fcst_time == 'ampm' :
			if  np.count_nonzero(vars_pm == -999) ==4 : 
				VAR_AM_MIN = -999
				VAR_AM_MAX = -999
				VAR_AM_AVERAGE = -999
			else :
				VAR_AM_MIN = np.min(vars_am[vars_am!=-999])
				VAR_AM_MAX = np.max(vars_am[vars_am!=-999])
				VAR_AM_AVERAGE = np.mean(vars_am[vars_am!=-999])

			if  np.count_nonzero(vars_pm == -999) == 6 : 
				VAR_PM_MIN = -999
				VAR_PM_MAX = -999
				VAR_PM_AVERAGE = -999
			else :        
				VAR_PM_MIN = np.min(vars_pm[vars_pm!=-999])
				VAR_PM_MAX = np.max(vars_pm[vars_pm!=-999])
				VAR_PM_AVERAGE = np.mean(vars_pm[vars_pm!=-999])
			return VAR_AM_MIN, VAR_AM_MAX, VAR_AM_AVERAGE, VAR_PM_MIN, VAR_PM_MAX, VAR_PM_AVERAGE
        
		#일자료 추출
		elif fcst_time == 'daily' : 
			if np.count_nonzero(vars_day == -999) == 10 : 
				VAR_DAY_MIN = -999			
				VAR_DAY_MAX = -999			
				VAR_DAY_AVERAGE = -999
			else :
				VAR_DAY_MIN = np.min(vars_day[vars_day!=-999])
				VAR_DAY_MAX = np.max(vars_day[vars_day!=-999])
				VAR_DAY_AVERAGE = np.mean(vars_day[vars_day!=-999])
			#print(VAR_DAY_MIN, VAR_DAY_MAX, VAR_DAY_AVERAGE)
			return VAR_DAY_MIN, VAR_DAY_MAX, VAR_DAY_AVERAGE
		
