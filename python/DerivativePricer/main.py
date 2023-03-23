fimport yfinance as yf
import pandas as pd
import json
from pymongo import MongoClient;


def options_chain(symbol):

    tk = yf.Ticker(symbol)
    # Expiration dates
    exps = tk.options

    # Get options for each expiration
    options = pd.DataFrame()
    for e in exps:
        opt = tk.option_chain(e)
        opt = pd.DataFrame().append(opt.calls).append(opt.puts)
        opt['expirationDate'] = e
        options = options.append(opt, ignore_index=True)
        
  
    # Boolean column if the option is a CALL
    options['CALL'] = options['contractSymbol'].str[4:].apply(
        lambda x: 1 if (x == "C") else 0)
    
    options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
    options['mark'] = (options['bid'] + options['ask']) / 2 # Calculate the midpoint of the bid-ask
    options.drop('lastTradeDate',axis=1,inplace=True);
    options.drop('inTheMoney',axis=1,inplace=True);
    options.fillna(value = 0,inplace = True);
  
    return options;


symlist = ['AAPL','IBM','MSFT','GOOGL'];

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

data = [];
data = [json.loads(line)
        for line in open(json_file, 'r', encoding='utf-8')];

     
# Inserting the loaded data in the Collection
# if JSON contains data more than one entry
# insert_many is used else insert_one is used
if isinstance(data, list):
    Collection.insert_many(data) 
else:
    Collection.insert_one(data);

print(Collection.name);
