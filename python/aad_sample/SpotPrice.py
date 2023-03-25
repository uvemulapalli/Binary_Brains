from flask import Flask, jsonify
from flask_restful import Resource, Api
import yfinance as yf;
  
app = Flask(__name__)
api = Api(app)
  
 
class SpotPrice(Resource):
 
    def get(self, symbol):
        sym =  yf.Ticker(symbol);
        price = sym.fast_info.last_price;
        return jsonify({'marketPrice': price})
  
  
api.add_resource(SpotPrice, '/spotPrice/<string:symbol>')
  
# driver function
if __name__ == '__main__':  
    app.run(debug = True,port=8001)