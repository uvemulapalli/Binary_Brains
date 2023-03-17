class Trade(object):
    def __init__(self, tradeId, spotPrice, strikePrice,timeToMaturity,intrestRate,sigma):
	    self.tradeId = tradeId
	    self.spotPrice = spotPrice
	    self.strikePrice = strikePrice
	    self.timeToMaturity = timeToMaturity
	    self.intrestRate = intrestRate
	    self.sigma = sigma
	    
    def toString(self):
	    print("TID=",self.tradeId,"Spot=",self.spotPrice,"Strike=",self.strikePrice,"TimeToMaturity=",self.timeToMaturity,"Sigma=",self.sigma)
