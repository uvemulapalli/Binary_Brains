import yfinance as yf
import pandas as pd
import json
from pymongo import MongoClient;
#from flask import Flask, jsonify;

#app = Flask('Options')

#@app.route('/home/<string:symbol>', methods = ['GET'])
#def getMarketPrice(symbol):
#    price =  yf.Ticker.fast_info.lastTradeDate
#    return jsonify({'marketPrice': price})


def options_chain(symbol):

    tk = yf.Ticker(symbol);

    # Expiration dates
    exps = tk.options[2:6]

    # Get options for each expiration
    options = pd.DataFrame()
    for e in exps:
        opt = tk.option_chain(e)
        p = tk.fast_info.last_price;
        opt = pd.DataFrame().append(opt.calls)
        opt['ticker'] = symbol;
        opt['expirationDate'] = e
        opt['spotPrice'] = p
        opt.drop(columns=['change','volume','openInterest','lastTradeDate','bid','ask','inTheMoney','percentChange','currency','contractSize'],axis=1,inplace=True);
        opt.rename(columns = {'impliedVolatility':'volatility'}, inplace = True)
        opt.rename(columns = {'strike':'strikePrice'}, inplace = True)
        options = options.append(opt, ignore_index=True);
        options.fillna(value = 0,inplace = True);
  
    return options;


symlist = ['AAPL','AMZN','TSLA','MSFT','CSCO','META','V','PG','BAC','GOOGL'];

optList = [];

for symbol in symlist:
    records = options_chain(symbol).to_dict(orient = 'records');
    optList.extend(records);
   

print("**********************************************************************")

json_file = "TradeData.json";
f = open(json_file, 'w');

for item in optList:
    f.write(str(item) + '\n')
f.close();

f = open(json_file);
contents = f.read().replace('\'','\"');
f.close();

f = open(json_file,'w');
f.write(contents);
f.close();

myclient = MongoClient("mongodb://21af924e8e2c.mylabserver.com:8080/")
  
# database & collection
db = myclient["TradeData"];
Collection = db["Options"];

#Empty the table

#db.Options.delete_many({});

data = [];
data = [json.loads(line)
        for line in open(json_file, 'r', encoding='utf-8')];

     
if isinstance(data, list):
    Collection.insert_many(data) 
else:
    Collection.insert_one(data);

print(Collection.name);

#app.run(debug = True);
