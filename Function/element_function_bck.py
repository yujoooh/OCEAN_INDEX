class Element_extract:
	def travel(self, DF, FCST_AREA): # 
		import pandas as pd
		from datetime import date, timedelta, datetime
		from Function.travel_score_function import IndexScore
		
		ELEMENT_DF = pd.read_csv('./Info/Element_Info.csv')
		ELEMENT_DF.columns = ['WARN1','WARN2','RAIN','SKY','TEMP','WSPD','SST','WAVE','MUL','CURRENT','CARNIVAL']

		CARNIVAL_DF = pd.read_csv('./Info/Carnival_Info.csv')
		CARNIVAL_DF.columns = ['AREA','01','02','03','04','05','06','07','08','09','10','11','12','Note']
		#print(CARNIVAL_DF)
		FORECAST_AREA = DF['FC_AREA'].drop_duplicates().values.tolist()

		today = str(datetime.today().strftime('%Y%m%d'))
		afterday1 = (date.today() + timedelta(1)).strftime('%Y%m%d')
		afterday2 = (date.today() + timedelta(2)).strftime('%Y%m%d')
		afterday3 = (date.today() + timedelta(3)).strftime('%Y%m%d')
		afterday4 = (date.today() + timedelta(4)).strftime('%Y%m%d')
		afterday5 = (date.today() + timedelta(5)).strftime('%Y%m%d')
		afterday6 = (date.today() + timedelta(6)).strftime('%Y%m%d')
		DATE = [today, afterday1, afterday2, afterday3, afterday4, afterday5, afterday6]
		FINAL = []
		#[여행종류별 예측지표 추출]--------------------------------------------------------------

		for FC_AREA in FORECAST_AREA : 
			for DY in DATE :
				MON = DY[4:6] 
				SELECT_AREA = CARNIVAL_DF[CARNIVAL_DF['AREA'].isin([FCST_AREA])] # Carnival_Info에서 지역선택
				NUM_CARNIVAL = SELECT_AREA.iloc[0].loc[MON] # 해당월 축제수 추출

				VARS = ['WARN1','WARN2','RAIN','SKY','TEMP','WSPD','SST','WAVE','MUL','CURRENT'] # variables
				for VAR in VARS :
					LIST = ELEMENT_DF[VAR].values.tolist()
					ii = 0
					while ii < len(LIST) :  		#LIST = "'" + "', '".join(LIST) + "'" # 텍스트 형태의 구분자 만들기
						if LIST[ii] == '-' :
							LIST.pop(ii) ; ii -= 1
						ii += 1
					#[해당 변수가 포함되는 여행 종류 select ]
					LIST2 = DF[DF['TRAVEL1'].isin(LIST) | DF['TRAVEL2'].isin(LIST) | DF['TRAVEL3'].isin(LIST) | DF['TRAVEL4'].isin(LIST) | DF['TRAVEL5'].isin(LIST)]
					LIST3_AM = LIST2[LIST2['FC_AREA'].isin([FC_AREA]) & LIST2['DATE'].isin([DY]) & LIST2['HR'].isin(['09', '12'])] #[오전 자료선택]
					LIST3_PM = LIST2[LIST2['FC_AREA'].isin([FC_AREA]) & LIST2['DATE'].isin([DY]) & LIST2['HR'].isin(['12', '15', '18'])] #[오후 자료선택]
					LIST3_DY = LIST2[LIST2['FC_AREA'].isin([FC_AREA]) & LIST2['DATE'].isin([DY]) & LIST2['HR'].isin(['09', '12', '15', '18'])] #[일 자료선택]
					globals()['NUM_{}'.format(VAR)] = LIST3_AM[VAR].count()/2 #[자료의 수(가중치 산정용) : 오전은 09, 12시 자료만 셀렉 되었으며, 이중 절반이 전체 여행에서 해당 변수가 활용되는 수]

					#print(LIST2)
					if VAR == 'WARN1' or VAR == 'WARN2' : 
						#[특보 종류 취합 및 중복값 제거]--------------------------------------------------------------
						WARN1_A = list(set(LIST3_AM['WARN1'].values.tolist())) # 해상특보 종류(오전)
						WARN1_P = list(set(LIST3_PM['WARN1'].values.tolist())) # 해상특보 종류(오후)
						WARN1_D = list(set(LIST3_DY['WARN1'].values.tolist())) # 해상특보 종류(일)
						WARN2_A = list(set(LIST3_AM['WARN2'].values.tolist())) # 육상특보 종류(오전)
						WARN2_P = list(set(LIST3_PM['WARN2'].values.tolist())) # 육상특보 종류(오후)
						WARN2_D = list(set(LIST3_DY['WARN2'].values.tolist())) # 육상특보 종류(일)

						if '-' in WARN1_A : WARN1_A.remove('-') # 중복제거
						if '-' in WARN1_P : WARN1_P.remove('-') # 중복제거
						if '-' in WARN1_D : WARN1_D.remove('-') # 중복제거
						if '-' in WARN2_A : WARN2_A.remove('-') # 중복제거
						if '-' in WARN2_P : WARN2_P.remove('-') # 중복제거						
						if '-' in WARN2_D : WARN2_D.remove('-') # 중복제거

						if 'DR' in WARN1_A : WARN1_A.remove('DR') # 건조주의보는 지수영향X, 시계열만 표출
						if 'DR' in WARN1_P : WARN1_P.remove('DR') # 건조주의보는 지수영향X, 시계열만 표출
						if 'DR' in WARN1_D : WARN1_D.remove('DR') # 건조주의보는 지수영향X, 시계열만 표출
						if 'DR' in WARN2_A : WARN2_A.remove('DR') # 건조주의보는 지수영향X, 시계열만 표출
						if 'DR' in WARN2_P : WARN2_P.remove('DR') # 건조주의보는 지수영향X, 시계열만 표출						
						if 'DR' in WARN2_D : WARN2_D.remove('DR') # 건조주의보는 지수영향X, 시계열만 표출

						if len(WARN1_A) == 0 : WARN1_A = '-'
						if len(WARN1_P) == 0 : WARN1_P = '-'  
						if len(WARN1_D) == 0 : WARN1_D = '-'  
						if len(WARN2_A) == 0 : WARN2_A = '-'
						if len(WARN2_P) == 0 : WARN2_P = '-'
						if len(WARN2_D) == 0 : WARN2_D = '-'
						
						globals()['WARN1_{}'.format('AM')] = '·'.join(WARN1_A) ; globals()['WARN1_{}'.format('PM')] = '·'.join(WARN1_P) ; globals()['WARN1_{}'.format('DY')] = '·'.join(WARN2_D)
						globals()['WARN2_{}'.format('AM')] = '·'.join(WARN2_A) ; globals()['WARN2_{}'.format('PM')] = '·'.join(WARN2_P) ; globals()['WARN2_{}'.format('DY')] = '·'.join(WARN2_D)
					else :

						globals()['AM_MIN_{}'.format(VAR)]  = round(LIST3_AM[VAR].min(),1)
						globals()['AM_MEAN_{}'.format(VAR)] = round(LIST3_AM[VAR].mean(),1) # 바다여행의 전체적인 평균 상태를 지수로 제공할 것이므로 이 값을 활용
						globals()['AM_MAX_{}'.format(VAR)]  = round(LIST3_AM[VAR].max(),1)  # 위험 요소에 대한 것은 기상특보로 일괄 적용 가능하기 때문에, 이는 활용하지 않음
						globals()['PM_MIN_{}'.format(VAR)]  = round(LIST3_PM[VAR].min(),1)
						globals()['PM_MEAN_{}'.format(VAR)] = round(LIST3_PM[VAR].mean(),1) # 바다여행의 전체적인 평균 상태를 지수로 제공할 것이므로 이 값을 활용
						globals()['PM_MAX_{}'.format(VAR)]  = round(LIST3_PM[VAR].max(),1)  # 위험 요소에 대한 것은 기상특보로 일괄 적용 가능하기 때문에, 이는 활용하지 않음
						globals()['DY_MIN_{}'.format(VAR)]  = round(LIST3_DY[VAR].min(),1)
						globals()['DY_MEAN_{}'.format(VAR)] = round(LIST3_DY[VAR].mean(),1) # 바다여행의 전체적인 평균 상태를 지수로 제공할 것이므로 이 값을 활용
						globals()['DY_MAX_{}'.format(VAR)]  = round(LIST3_DY[VAR].max(),1)  # 위험 요소에 대한 것은 기상특보로 일괄 적용 가능하기 때문에, 이는 활용하지 않음


				#print(DY, NUM_RAIN, NUM_SKY, NUM_TEMP, NUM_WSPD, NUM_SST, NUM_WAVE, NUM_MUL, NUM_CURRENT)

				FCST_NUM = NUM_SKY + NUM_TEMP + NUM_WSPD + NUM_SST + NUM_WAVE + NUM_MUL + NUM_CURRENT # 예측지표 총합
				WEIGHT_SKY  = NUM_SKY  / FCST_NUM * 100 #날씨 가중치(최대점수)
				WEIGHT_TEMP = NUM_TEMP / FCST_NUM * 100 #기온 가중치(최대점수)
				WEIGHT_WSPD = NUM_WSPD / FCST_NUM * 100 #풍속 가중치(최대점수)
				WEIGHT_SST  = NUM_SST  / FCST_NUM * 100 #수온 가중치(최대점수)
				WEIGHT_WAVE = NUM_WAVE / FCST_NUM * 100 #파고 가중치(최대점수)
				WEIGHT_MUL  = NUM_MUL  / FCST_NUM * 100 #물때 가중치(최대점수)
				WEIGHT_CURR = NUM_CURRENT / FCST_NUM * 100 #유속 가중치(최대점수)
				ADD_CARNIVAL = NUM_CARNIVAL * 2.0          #축제수(추가점수)  가중치 변경하면서 조정 필요

				#print(WEIGHT_TEMP, WEIGHT_WSPD, WEIGHT_SST, WEIGHT_WAVE, WEIGHT_MUL, WEIGHT_CURR, WEIGHT_SKY)
				if DY == today or DY == afterday1 or DY == afterday2 : TIME = ['AM','PM']
				if DY == afterday3 or DY == afterday4 or DY == afterday5 or DY == afterday6 : TIME = ['DY']
				for TM in TIME : 
					SKY_SCRE = IndexScore().sky_score(WEIGHT_SKY,globals()['{}_MEAN_SKY'.format(TM)])
					TEMP_SCRE = IndexScore().temp_score(WEIGHT_TEMP,globals()['{}_MEAN_TEMP'.format(TM)])
					WSPD_SCRE = IndexScore().wspd_score(WEIGHT_WSPD,globals()['{}_MEAN_WSPD'.format(TM)])
					SST_SCRE = IndexScore().sst_score(WEIGHT_SST,globals()['{}_MEAN_SST'.format(TM)])
					WAVE_SCRE = IndexScore().wave_score(WEIGHT_WAVE,globals()['{}_MEAN_WAVE'.format(TM)])
					MUL_SCRE = IndexScore().tide_score(WEIGHT_MUL,globals()['{}_MEAN_MUL'.format(TM)])
					CURRENT_SCRE = IndexScore().current_score(WEIGHT_CURR,globals()['{}_MEAN_CURRENT'.format(TM)])
					SCORE_SUM = SKY_SCRE + TEMP_SCRE + WSPD_SCRE + SST_SCRE + WAVE_SCRE + MUL_SCRE + CURRENT_SCRE + ADD_CARNIVAL # 강수/특보 반영 전 점수
					RAIN_SCRE = IndexScore().rain_score(SCORE_SUM,globals()['{}_MEAN_RAIN'.format(TM)]) # 강수량 점수 반영
					WARN_SCRE = IndexScore().warn_score(RAIN_SCRE,globals()['WARN1_{}'.format(TM)],globals()['WARN2_{}'.format(TM)])  # 특보점수 반영(해상, 육상)

					globals()['FINAL_SCRE_{}'.format(TM)] = WARN_SCRE # 최종 예보점수
					globals()['SCRE_CLASS_{}'.format(TM)] = IndexScore().score_class(globals()['FINAL_SCRE_{}'.format(TM)])  # 예보등급

					#[Sea Travel Average & Score Data Frame]
					if TM == 'AM' : FINAL.append([FC_AREA, DY, 'AM', AM_MEAN_TEMP, TEMP_SCRE, AM_MEAN_WSPD, WSPD_SCRE, AM_MEAN_SST, SST_SCRE, AM_MEAN_WAVE, WAVE_SCRE, AM_MEAN_MUL, MUL_SCRE, AM_MEAN_CURRENT, CURRENT_SCRE, AM_MEAN_SKY, SKY_SCRE, NUM_CARNIVAL, AM_MEAN_RAIN, WARN1_AM, WARN2_AM, FINAL_SCRE_AM, SCRE_CLASS_AM])
					if TM == 'PM' : FINAL.append([FC_AREA, DY, 'PM', PM_MEAN_TEMP, TEMP_SCRE, PM_MEAN_WSPD, WSPD_SCRE, PM_MEAN_SST, SST_SCRE, PM_MEAN_WAVE, WAVE_SCRE, PM_MEAN_MUL, MUL_SCRE, PM_MEAN_CURRENT, CURRENT_SCRE, PM_MEAN_SKY, SKY_SCRE, NUM_CARNIVAL, PM_MEAN_RAIN, WARN1_PM, WARN2_PM, FINAL_SCRE_PM, SCRE_CLASS_PM])
					if TM == 'DY' : FINAL.append([FC_AREA, DY, 'DY', DY_MEAN_TEMP, TEMP_SCRE, DY_MEAN_WSPD, WSPD_SCRE, DY_MEAN_SST, SST_SCRE, DY_MEAN_WAVE, WAVE_SCRE, DY_MEAN_MUL, MUL_SCRE, DY_MEAN_CURRENT, CURRENT_SCRE, DY_MEAN_SKY, SKY_SCRE, NUM_CARNIVAL, DY_MEAN_RAIN, WARN1_DY, WARN2_DY, FINAL_SCRE_DY, SCRE_CLASS_DY])

		#for i in FINAL : print(i)
		FINAL_DF = pd.DataFrame(FINAL)
		FINAL_DF.columns = ['FC_AREA', 'DATE','HR','MEAN_TEMP','TEMP_SCRE','MEAN_WSPD','WSPD_SCRE','MEAN_SST','SST_SCRE','MEAN_WHT','WAVE_SCRE','MUL','MUL_SCRE','MEAN_CURR','CURR_SCRE','MEAN_SKY','SKY_SCRE','CARNIVAL_NUM','MEAN_RAIN','WARN_SEA','WARN_LAND','FINAL_SCRE','SCRE_CLASS']
		#print(FINAL_DF)
		return FINAL_DF
