class Statistic:
        
#model : KHOA(WRF, WW3, ROMS), KMA(CWW3, RWW3)
#fcst_time : ampm,daily
	def min_max_ave(self, model, fcst_time, vars, X, Y, T):
		import numpy as np

		#KHOA 모델 오전/오후 추출
		if model == 'KHOA' and fcst_time == 'ampm' :
			VAR_AM_MIN = np.min(vars[T+1:T+5,Y,X])
			VAR_AM_MAX = np.max(vars[T+1:T+5,Y,X])
			VAR_AM_AVERAGE = np.mean(vars[T+1:T+5,Y,X])
			

			VAR_PM_MIN = np.min(vars[T+5:T+11,Y,X])
			VAR_PM_MAX = np.max(vars[T+5:T+11,Y,X])
			VAR_PM_AVERAGE = np.mean(vars[T+5:T+11,Y,X])
			#print(VAR_AM_AVERAGE, VAR_PM_AVERAGE)

			if VAR_AM_MIN < 0.1 and VAR_AM_MIN >= 0: VAR_AM_MIN = 0.1
			if VAR_AM_AVERAGE < 0.1 and VAR_AM_AVERAGE >= 0: VAR_AM_AVERAGE = 0.1
			if VAR_AM_MAX < 0.1 and VAR_AM_MAX >= 0: VAR_AM_MAX = 0.1
			
			if VAR_PM_MIN < 0.1 and VAR_PM_MIN >= 0: VAR_PM_MIN = 0.1
			if VAR_PM_AVERAGE < 0.1 and VAR_PM_AVERAGE >= 0: VAR_PM_AVERAGE = 0.1
			if VAR_PM_MAX < 0.1 and VAR_PM_MAX >= 0: VAR_PM_MAX = 0.1
			
			return VAR_AM_MIN, VAR_AM_MAX, VAR_AM_AVERAGE, VAR_PM_MIN, VAR_PM_MAX, VAR_PM_AVERAGE, X, Y, T

		#KHOA 모델 일자료 추출
		elif model == 'KHOA' and fcst_time == 'daily' : 
			VAR_DAY_MIN = np.min(vars[T+1:T+11,Y,X])
			VAR_DAY_MAX = np.max(vars[T+1:T+11,Y,X])
			VAR_DAY_AVERAGE = np.mean(vars[T+1:T+11,Y,X])
			
			if VAR_DAY_MIN < 0.1 and VAR_DAY_MIN >= 0 : VAR_DAY_MIN = 0.1
			if VAR_DAY_AVERAGE < 0.1 and VAR_DAY_AVERAGE >= 0 : VAR_DAY_AVERAGE = 0.1
			if VAR_DAY_MAX < 0.1 and VAR_DAY_MAX >= 0 : VAR_DAY_MAX = 0.1
			
			return VAR_DAY_MIN, VAR_DAY_MAX, VAR_DAY_AVERAGE, X, Y, T

		#KMA 모델 오전/오후 추출
		elif model == 'KMA' and fcst_time == 'ampm' :
			VAR_AM_MIN = np.min(vars[T+4:T+6,Y,X])
			VAR_AM_MAX = np.max(vars[T+4:T+6,Y,X])
			VAR_AM_AVERAGE = np.mean(vars[T+4:T+6,Y,X])
            
			VAR_PM_MIN = np.min(vars[T+5:T+8,Y,X])
			VAR_PM_MAX = np.max(vars[T+5:T+8,Y,X])
			VAR_PM_AVERAGE = np.mean(vars[T+5:T+8,Y,X])
			
			if VAR_AM_MIN < 0.1 : VAR_AM_MIN = 0.1
			if VAR_AM_AVERAGE < 0.1 : VAR_AM_AVERAGE = 0.1
			if VAR_AM_MAX < 0.1 : VAR_AM_MAX = 0.1
			
			if VAR_PM_MIN < 0.1 : VAR_PM_MIN = 0.1
			if VAR_PM_AVERAGE < 0.1 : VAR_PM_AVERAGE = 0.1
			if VAR_PM_MAX < 0.1 : VAR_PM_MAX = 0.1
			return VAR_AM_MIN, VAR_AM_MAX, VAR_AM_AVERAGE, VAR_PM_MIN, VAR_PM_MAX, VAR_PM_AVERAGE

		#KMA 모델 일자료 추출
		elif model == 'KMA' and fcst_time == 'daily' :
			VAR_DAY_MIN = np.min(vars[T+4:T+8,Y,X])
			VAR_DAY_MAX = np.max(vars[T+4:T+8,Y,X])
			VAR_DAY_AVERAGE = np.mean(vars[T+4:T+8,Y,X])
			
			if VAR_DAY_MIN < 0.1 : VAR_DAY_MIN = 0.1
			if VAR_DAY_AVERAGE < 0.1 : VAR_DAY_AVERAGE = 0.1
			if VAR_DAY_MAX < 0.1 : VAR_DAY_MAX = 0.1
			return VAR_DAY_MIN, VAR_DAY_MAX, VAR_DAY_AVERAGE, X, Y, T
	
