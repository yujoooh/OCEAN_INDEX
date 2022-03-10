class IndexScore:
    #[파랑]
    def wave_score(self, value):
        if  0.5 <= value < 1.0 : score = 5
        elif 1.0 <= value < 1.5   : score = 4
        elif 1.5 <= value < 2.0   : score = 3
        elif 2.0 <= value < 3.0 or 0 <= value < 0.5  : score = 2
        elif value >=3.0  : score = 1
        else                : score = 0
        return score
    def wave_dir_score(self, value):
        if  75.0 <= value <= 105 : score = 5
        elif 60.0 <= value < 75.0 or 105.0 < value <= 120.0  : score = 4
        elif 45.0 <= value < 60.0 or 120.0 < value <= 135.0   : score = 3
        elif 30.0 <= value < 45.0 or 135.0 < value <= 150.0   : score = 2
        elif 0.0 <= value < 30.0 or 150.0 < value <= 180.0  : score = 1
        else                : score = 0
        return score

    def Rpeak_score(self, value):
        if  8.0 <= value < 10.0 : score = 5
        elif 6.0 <= value < 8.0   : score = 4
        elif 10.0 <= value < 12.0   : score = 3
        elif 12.0 <= value < 14.0   : score = 2
        elif 14.0 <= value or value < 6.0  : score = 1
        else                : score = 0
        return score
    
    #[바람]
    def wind_score(self, value):
        if  0 <= value < 3 : score = 5
        elif 3 <= value < 5   : score = 4
        elif 5 <= value < 9   : score = 3
        elif 9 <= value < 14   : score = 2
        elif value >= 14  : score = 1
        else                : score = 0
        return score

    def wind_dir_score(self, value):
        if  0 <= value < 0.05 : score = 5
        elif 0.05 <= value < 0.10   : score = 4
        elif 0.05 <= value < 0.15   : score = 3
        elif 0.05 <= value < 0.20   : score = 2
        elif 0.05 <= value < 0.25  : score = 1
        else                : score = 0
        return score

    #[수온]
    def temp_score(self, value):
        if  value > 20 : score = 5
        elif 15 <= value < 20   : score = 4
        elif 10 <= value < 15   : score = 3
        elif 5 <= value < 10   : score = 2
        elif value < 5  : score = 1
        else                : score = 0
        return score

    #[특보]
    def warn_score(self,value):
        #if   value == '-' :	score = 5
        if   value.strip() == '-' :	score = 5
        else             : score = 1
        return score
    
    def total_score(self, wave, rpeak, wavedir, wind, sst, warn):
        score = (wave*2.0 + wavedir*2.0 + rpeak*1.0 + wind*0.6+ sst*0.4)/5
        service_score = score
        
        if service_score > warn : service_score = warn
        return score, service_score
    
    def quotient_score(self,value) :
        if 0 <= value <= 1 : score = '체험불가'
        elif 1 < value <= 2 : score = '매우나쁨'
        elif 2 < value <= 3 : score = '나쁨'
        elif 3 < value <= 4 : score = '보통'
        elif 4 < value <=4.5 : score = '좋음'
        else : score = '매우좋음'
        return score