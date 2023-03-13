package TradeScenario;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

public class BumpScenarios {

	public static final String RF_SPOT = "spot";;
	public static final String RF_STRIKE = "strike";
	public static final String RF_IR = "ir";
	public static final String RF_VOL = "vol";
	public static final String RF_TTM = "time_to_maturity";

	public static final String BUMP_TYPE_PCT  = "pct";
	public static final String  BUMP_TYPE_ABS = "abs";


	String rf;
	boolean isPct;
	private Ranges range;

	public BumpScenarios(String rf, String bumpType, Ranges ranges) {
		this.rf = rf;
		this.isPct = BUMP_TYPE_PCT.equals(bumpType) ? true : false;
		this.range = ranges;

	}

	public List<Trade> getBumpedTrades(Trade trade) {
		List<Trade> bumpedTradeList = new ArrayList<>();
		Double currentValue = trade.getValueByRiskFactor(rf);

		for(Entry<Double, Double> entrySet : getBumpedValue(currentValue).entrySet()) {
			Trade t =new Trade(trade);
			t.setRiskFactorValue(rf, entrySet.getValue());
			t.setTradeId(trade.getTradeId()+"_bumped_"+rf+"_"+String.format("%.4f", entrySet.getKey()));
			bumpedTradeList.add(t);
		}
		
		return bumpedTradeList;

	}

	private Map<Double, Double> getBumpedValue(Double currentValue) {
		List<Double> retValue = new ArrayList<>();
		Map<Double, Double> bumpFactorToBumpedValueMap = new HashMap<>();

		double bumpAmount = range.from;
		while(bumpAmount < range.to) {
			double value = 0;
			if(bumpAmount != 0) {
				if(isPct) {
					value = currentValue + (currentValue * bumpAmount)/100;
					bumpFactorToBumpedValueMap.put(bumpAmount, value);

				}else {
					value = currentValue + bumpAmount;
					bumpFactorToBumpedValueMap.put(bumpAmount, value);

				}
				retValue.add(value);
			}
			bumpAmount=bumpAmount+range.interval;
		}		
		return bumpFactorToBumpedValueMap;
	}
}
