package TradeScenario;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

public class TradeDataGenerator {

	public static void main(String[] args) throws IOException {

		TradeDataGenerator tg = new TradeDataGenerator();
		List<Trade> tradeList = tg.getTradeList();
		BumpScenarios scenario_spot = new BumpScenarios(
										BumpScenarios.RF_SPOT, BumpScenarios.BUMP_TYPE_PCT, new Ranges(-10.0, 10.0, 1.0));
		
		BumpScenarios scenario_strike = new BumpScenarios(
										BumpScenarios.RF_STRIKE, BumpScenarios.BUMP_TYPE_PCT, new Ranges(-10.0, 10.0, 1.0));

		BumpScenarios scenario_intrest_rate = new BumpScenarios(
										BumpScenarios.RF_IR, BumpScenarios.BUMP_TYPE_PCT, new Ranges(-1.0, 1.0, 0.1));

		BumpScenarios scenario_intrest_vol = new BumpScenarios(
										BumpScenarios.RF_VOL, BumpScenarios.BUMP_TYPE_PCT, new Ranges(-10.0, 10.0, 1.0));

		BumpScenarios scenario_ttm = new BumpScenarios(
										BumpScenarios.RF_TTM, BumpScenarios.BUMP_TYPE_PCT, new Ranges(-99.0, -1.0, 5.0));
		
		List<Trade> bumpedTrades = new ArrayList<>();
		for(Trade t : tradeList) {
			System.out.println("Bumping " + t.tradeId);
			bumpedTrades.add(t);
			bumpedTrades.addAll(scenario_spot.getBumpedTrades(t));
			bumpedTrades.addAll(scenario_strike.getBumpedTrades(t));
			bumpedTrades.addAll(scenario_intrest_rate.getBumpedTrades(t));
			bumpedTrades.addAll(scenario_intrest_vol.getBumpedTrades(t));
			bumpedTrades.addAll(scenario_ttm.getBumpedTrades(t));
		}
		
		for(Trade tt : bumpedTrades) {
			System.out.println(tt);
		}
		tg.createJson(bumpedTrades);

	}

	private String getJsonFilePath() throws IOException{
		String jsonFileName = "TradesJson.json";
		File jsonFile = new File(jsonFileName);
		String separator = File.separator;
		
			jsonFile = jsonFile.getCanonicalFile();
			String rootPath = jsonFile.getParentFile().getParentFile().getParentFile().getAbsolutePath();
			StringBuilder jsonFilePath = new StringBuilder();
			jsonFilePath.append(rootPath).append(separator);
			jsonFilePath.append("python").append(separator);
			jsonFilePath.append("DerivativePricer").append(separator);
			jsonFilePath.append("monte_carlo").append(separator);
			jsonFilePath.append("data").append(separator);
			jsonFilePath.append(jsonFileName);
			return jsonFilePath.toString();
	}
	
	@SuppressWarnings("unchecked")
	private void createJson(List<Trade> bumpedTrades) throws IOException {
        String path = getJsonFilePath();
        JSONObject tradeData = new JSONObject();
        JSONArray tradeList = new JSONArray();
        
        for(Trade t : bumpedTrades) {
            JSONObject trade = new JSONObject();
            trade.put("TradeId", t.getTradeId());
            trade.put("Spot", t.getSpot());
            trade.put("Strike", t.getStrike());
            trade.put("IR", t.getIntrestRate());
            trade.put("Sigma", t.getSigma());
            trade.put("timeToMaturity", t.getTimeToMaturity());
            tradeList.add(trade);
        }
        tradeData.put("trades", tradeList);
 
        //Write JSON file
        try (FileWriter file = new FileWriter(path)) {
            file.write(tradeData.toJSONString()); 
            file.flush();
        	System.out.println("writing done" + file.toString());

 
        } catch (IOException e) {
            e.printStackTrace();
        }
	}


	public List<Trade> getTradeList() {
		List<Trade> tradeList = new ArrayList<>();

		for(int i = 0; i<=100; i++) {
			double multiplier = 1+Math.random();
			tradeList.add(new Trade("TID_"+i,40*multiplier,40*multiplier,1*multiplier,0.08*multiplier,0.30*multiplier));
		}
		
		return tradeList;
	}
	
}
