import random;
import copy;
import Constants;
from Range import Range;
from Trade import Trade;

class BumpScenarios(object):
    def __init__(self, riskFactor, bumpType, ranges):
        self.riskFactor = riskFactor;
        self.bumpType = bumpType;
        self.range = ranges;
        self.isPct = False;
        if bumpType == Constants.BUMP_TYPE_PCT:
            self.isPct = True;
	 
    def display(self):
	    print("RiskFactor=",self.riskFactor,"BumpType=",self.bumpType,"Range=",self.range.display());
    
    def getTradeList():
        tradeList = [];
        random.seed(3);
                
        for n in range(1,100):
            multiplier = random.random() + 1;
            myTrade = Trade("TID_"+n, 40*multiplier, 40*multiplier, 1*multiplier, 0.08*multiplier,0.3*multiplier);
            tradeList.append(myTrade);
        return tradeList;
        
    
    def getBumpedTrades(self,trade):
        bumpedTradeList = [];
        currentValue = trade.getRiskFactorValue(self.riskFactor);
        bumpValueMap = {};
        bumpValueMap = self.getBumpedValue(currentValue);
        
        for key,kValue in bumpValueMap.items():
            nTrade = Trade(None,0.0,0.0,0.0,0.0,0.0);
            nTrade = copy.copy(trade);
            nTrade.setRiskFactorValue(self.riskFactor,kValue);
            newTradeId = str(trade.tradeId) + "_bumped_" + str(self.riskFactor) + "_" + str(key);
            nTrade.tradeId = newTradeId;
            bumpedTradeList.append(nTrade);
        return bumpedTradeList;
            
    def getBumpedValue(self,currentValue):
        retValue = [];
        bumpFactorToBumpedValueMap = {};
        bumpAmount = float(self.range.begin);
        currentValue = float(currentValue or 0.0);
        
      
        while bumpAmount < self.range.end:
            value = 0.0;
            if bumpAmount != 0.0:
                if self.isPct == True:
                    value = currentValue + (currentValue * bumpAmount)/100;
                    bumpFactorToBumpedValueMap[bumpAmount] = value;
                else:
                    value = currentValue + bumpAmount;
                    bumpFactorToBumpedValueMap[bumpAmount] = value;
                retValue.append(value);
            bumpAmount=bumpAmount+self.range.interval;
        return bumpFactorToBumpedValueMap;


