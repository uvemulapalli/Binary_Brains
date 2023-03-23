import yfinance as yf
import pandas as pd
import json
from pymongo import MongoClient;

# database & collection
myclient = MongoClient("mongodb://21af924e8e2c.mylabserver.com:8080/")
db = myclient["TradeData"];
Collection = db["Options"];

x = Collection.find_one();
print(Collection.name, x);
