from Trade import Trade;
from Range import Range;
import Constants;
from BumpScenarios import BumpScenarios;
import random;
import json;

tradeList = [];
random.seed(3);

                
for n in range(1,100):
    multiplier = random.random() + 1;
    ID = "TID_"+ str(n);
    myTrade = Trade(ID,40*multiplier,40*multiplier,multiplier,0.08*multiplier,0.3*multiplier)
    tradeList.append(myTrade);
    
scenario_spot           = BumpScenarios(Constants.RF_SPOT, Constants.BUMP_TYPE_PCT, Range(-10.0, 10.0, 1.0));
scenario_strike         = BumpScenarios(Constants.RF_STRIKE, Constants.BUMP_TYPE_PCT, Range(-10.0, 10.0, 1.0));
scenario_intrest_rate   = BumpScenarios(Constants.RF_IR, Constants.BUMP_TYPE_PCT, Range(-1.0, 1.0, 0.1));
scenario_intrest_vol    = BumpScenarios(Constants.RF_VOL, Constants.BUMP_TYPE_PCT, Range(-10.0, 10.0, 1.0));
scenario_ttm            = BumpScenarios(Constants.RF_TTM, Constants.BUMP_TYPE_PCT, Range(-99.0, -1.0, 5.0));

print(scenario_spot.display());
s = scenario_spot.getBumpedValue(10);

bumpedTrades = [];

for t in tradeList:
    print("Bumping " + t.tradeId);
    bumpedTrades.append(t);
    list1 = scenario_spot.getBumpedTrades(t);
    list2 = scenario_strike.getBumpedTrades(t);
    list3 = scenario_intrest_rate.getBumpedTrades(t);
    list4 = scenario_intrest_vol.getBumpedTrades(t);
    list5 = scenario_ttm.getBumpedTrades(t);
    bumpedTrades.extend(list1);
    bumpedTrades.extend(list2);
    bumpedTrades.extend(list3);
    bumpedTrades.extend(list4);
    bumpedTrades.extend(list5);
    
with open('TradeData.txt', 'w') as f:
    for x in bumpedTrades:
        result = json.dumps(x.__dict__);
        f.write(result);
        f.write("\n");
f.close();

file = open('TradeData.txt', 'r');
record = file.read();
print(record);
file.close();
