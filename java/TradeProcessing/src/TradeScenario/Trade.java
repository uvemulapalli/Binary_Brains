package TradeScenario;

public class Trade {
	public String getTradeId() {
		return tradeId;
	}

	public double getSpot() {
		return spot;
	}

	public double getStrike() {
		return strike;
	}

	public double getTimeToMaturity() {
		return timeToMaturity;
	}

	public double getIntrestRate() {
		return intrestRate;
	}

	public double getSigma() {
		return sigma;
	}

	public void setTradeId(String tradeId) {
		this.tradeId = tradeId;
	}

	public void setSpot(double spot) {
		this.spot = spot;
	}

	public void setStrike(double strike) {
		this.strike = strike;
	}

	public void setTimeToMaturity(double timeToMaturity) {
		this.timeToMaturity = timeToMaturity;
	}

	public void setIntrestRate(double intrestRate) {
		this.intrestRate = intrestRate;
	}

	public void setSigma(double sigma) {
		this.sigma = sigma;
	}

	public double getValueByRiskFactor(String rf) {
		double currentValue;
		if(BumpScenarios.RF_SPOT.equals(rf)) {
			currentValue = getSpot();
			
		}
		else if(BumpScenarios.RF_STRIKE.equals(rf)) {
			currentValue = getStrike();
			
		}
		else if(BumpScenarios.RF_IR.equals(rf)) {
			currentValue = getIntrestRate();
			
		}
		else if(BumpScenarios.RF_VOL.equals(rf)) {
			currentValue = getSigma();
			
		}
		else if(BumpScenarios.RF_TTM.equals(rf)) {
			currentValue = getTimeToMaturity();
			
		}else {
			currentValue = Double.NaN;
		}

		return currentValue;
	}

	public void setRiskFactorValue(String rf, Double value) {
		if(BumpScenarios.RF_SPOT.equals(rf)) {
			setSpot(value);
			
		}
		else if(BumpScenarios.RF_STRIKE.equals(rf)) {
			setStrike(value);
			
		}
		else if(BumpScenarios.RF_IR.equals(rf)) {
			setIntrestRate(value);
			
		}
		else if(BumpScenarios.RF_VOL.equals(rf)) {
			setSigma(value);
			
		}
		else if(BumpScenarios.RF_TTM.equals(rf)) {
			setTimeToMaturity(value);
			
		}
	}
	
	
	String tradeId;
	private double spot;
	private double strike;
	private double timeToMaturity;
	private double intrestRate;
	private double sigma; /*volatility*/

	Trade(String tradeId, double spot, double strike, double timeToMaturity, double intrestRate, double sigma){ 
		this.tradeId=tradeId;
		this.spot=spot;
		this.strike=strike; 
		this.timeToMaturity=timeToMaturity; 
		this.intrestRate=intrestRate; 
		this.sigma=sigma;
	}
	
	Trade(Trade t){ 
		this.tradeId=t.tradeId;
		this.spot=t.spot;
		this.strike=t.strike; 
		this.timeToMaturity=t.timeToMaturity; 
		this.intrestRate=t.intrestRate; 
		this.sigma=t.sigma;
	}
	
	@Override
	public String toString() {
	StringBuilder sb = new StringBuilder();
	sb.append("TID").append(tradeId).append(", ");
	sb.append("S0=").append(spot).append(", ");
	sb.append("K=").append(strike).append(", ");
	sb.append("T=").append(timeToMaturity).append(", ");
	sb.append("r=").append(intrestRate).append(", ");
	sb.append("sigma=").append(sigma);
	
		return sb.toString();
	}
}
