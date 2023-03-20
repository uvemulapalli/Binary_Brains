import Constants;

class Trade(object):
    
    def __init__(self, tradeId, spotPrice, strikePrice,timeToMaturity,intrestRate,sigma):
	    self.tradeId = tradeId
	    self.spotPrice = spotPrice
	    self.strikePrice = strikePrice
	    self.timeToMaturity = timeToMaturity
	    self.intrestRate = intrestRate
	    self.sigma = sigma
        
   
    def display(self):
	    print("TID=",self.tradeId,"Spot=",self.spotPrice,"Strike=",self.strikePrice,"TimeToMaturity=",self.timeToMaturity,"Sigma=",self.sigma,"INterestRate=", self.intrestRate);
        
        
    def setRiskFactorValue(self,riskFactor, value):
        if riskFactor == Constants.RF_SPOT:
            self.spotPrice = value;
        elif riskFactor == Constants.RF_STRIKE:
            self.strikePrice = value;
        elif riskFactor == Constants.RF_VOL:
            self.sigma = value;
        elif riskFactor == Constants.RF_IR:
            self.intrestRate == value;
        elif riskFactor == Constants.RF_TTM:
            self.timeToMaturity = value;
               
    
    def getRiskFactorValue(self,riskFactor):
          if riskFactor == Constants.RF_SPOT:
              return self.spotPrice;
          elif riskFactor == Constants.RF_STRIKE:
              return self.strikePrice;
          elif riskFactor == Constants.RF_VOL:
              return self.sigma;
          elif riskFactor == Constants.RF_IR:
              return self.intrestRate;
          elif riskFactor == Constants.RF_TTM:
              return self.timeToMaturity;
          else:
              return 0.0;
