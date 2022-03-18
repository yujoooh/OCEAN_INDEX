class Missing_STN:
	def WBUOY(self,ii,STN,WBUOY_LIST):
		if ii == 0 :
			WBUOY_LIST = ['가파도','간절곶','고흥','구룡포','구암','군산','금오도',\
			'김녕','나로도','낙월','남해','노화도','다대포','대치마도',\
			'독도','두미도','맹골수도','변산','불무도','비안도','사량도','삼척',\
			'삽시도','서천','소매물도','신산','신진도','안면도','연곡','연화도',\
			'영광','영락','오륙도','옥도','우도','울릉서부','울릉읍','월포','위도',\
			'이작도','자월도','자은','잠도','장봉도','장안','제주항','조도','죽변',\
			'중문','진도','천수만','청산도','초도','추자도','토성','풍도','한산도',\
			'해금강','혈암','협재','후포']

		for WBUOY in WBUOY_LIST :
			if STN == WBUOY :
				WBUOY_LIST.remove(STN)
	
		return WBUOY_LIST

	def WBUOYID(self,ii,STNID,WBUOYID_LIST):
		if ii == 0 :
			WBUOYID_LIST = [22476, 22483, 22478, 22453, 22443, 22474, 22466, 22491, 22502, 22494, 22498, 22477, 22460, \
			22489, 22441, 22450, 22481, 22497, 22503, 22492, 22501, 22479, 22445, 22473, 22485, 22495, 22444, 22488, 22451, \
			22499, 22475, 22505, 22459, 22447, 22469, 22506, 22464, 22490, 22504, 22461, 22472, 22493, 22484, 22496, 22454, \
			22457, 22500, 22452, 22458, 22449, 22487, 22456, 22507, 22468, 22471, 22470, 22467, 22455, 22442, 22486, 22465]

		for WBUOYID in WBUOYID_LIST :
			if STNID == WBUOYID :
				WBUOYID_LIST.remove(STNID)
		
		return WBUOYID_LIST

	
	def BBUOY(self,ii,STN,BBUOY_LIST):
		if ii == 0 :
			BBUOY_LIST = ['울릉도','덕적도','칠발도','거문도','거제도','동해','포항','마라도','외연도','신안','인천','부안','서귀포','통영','울산','울진']
			#BBUOY_LIST = ['울릉도','덕적도','칠발도','거문도','거제도','동해','포항','마라도','외연도','신안','추자도','인천','부안','서귀포','통영','울산','울진']
		for BBUOY in BBUOY_LIST :
			if STN == BBUOY :
				BBUOY_LIST.remove(STN)
	
		return BBUOY_LIST
		
	def BBUOYID(self,ii,STNID,BBUOYID_LIST):
		if ii == 0 :
			BBUOYID_LIST = [21229,22101,22102,22103,22104,22105,22106,22107,22108,22183,22185,22186,22187,22188,22189,22190]
			#BBUOYID_LIST = [21229,22101,22102,22103,22104,22105,22106,22107,22108,22183,22184,22185,22186,22187,22188,22189,22190]
		for BBUOYID in BBUOYID_LIST :
			if STNID == BBUOYID :
				BBUOYID_LIST.remove(STNID)
		
		return BBUOYID_LIST

	def LAMP(self,ii,STN,LAMP_LIST):
		if ii == 0 :
			LAMP_LIST = ['서수도','가대암','십이동파','갈매여','해수서','지귀도','간여암','이덕서']

		for LAMP in LAMP_LIST :
			if STN == LAMP :
				LAMP_LIST.remove(STN)
	
		return LAMP_LIST

	def LAMPID(self,ii,STNID,LAMPID_LIST):
		if ii == 0 :
			LAMPID_LIST = [955,956,957,958,959,960,961,963]

		for LAMPID in LAMPID_LIST :
			if STNID == LAMPID :
				LAMPID_LIST.remove(STNID)
		
		return LAMPID_LIST
