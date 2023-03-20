from flask import Flask, request
from ModelDictionary import ModelDictionary
from Neural_Approximator import Neural_Approximator
import numpy as np
app = Flask(__name__)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/init_instrument', methods=['POST'])
# ‘/’ URL is bound with hello_world() function.
def init_instrument():
    request_data = request.get_json()
    print("Request hit")
    instTicker = request_data['InstrumentTicker']
    strikePrice = request_data['StrikePrice']
    expiry = request_data['Expiry']
    spotPrice = request_data['SpotPrice']
    volatality = request_data['Volatality']

    #Create HashingKey
    key = instTicker;
    #read csv
    #train model
    #store instance
    xTrain,ytrain,dx_dyTrain = getTrainingData()
    approximator = Neural_Approximator(xTrain,ytrain,dx_dyTrain)
    approximator.prepare(3, True, weight_seed=None)


    approximator.train("differential training")


    dict_obj.add(instTicker,approximator)
    print("Request is:", instTicker, strikePrice,expiry, spotPrice,volatality)
    print(dict_obj)
    # two keys are needed because of the nested object
    return instTicker



def getTrainingData():
    xTrain = [123,125,126]
    yTrain = [10,12, 12.1]
    dx_dyTrain =[0.1,0.2,0.3]
    return np.reshape(xTrain,[-1,1]), np.reshape(yTrain,[-1,1]), np.reshape(dx_dyTrain,[-1,1])

@app.route('/get_price', methods=['POST'])
# ‘/’ URL is bound with hello_world() function.
def get_price():
    size=3
    request_data = request.get_json()
    print("Request getPrice hit")
    instTicker = request_data['InstrumentTicker']
    spotPrice = request_data['SpotPrice']
    approximator = dict_obj.get(instTicker)

    predvalues = {}
    preddeltas = {}
    predictions, deltas = approximator.predict_values_and_derivs(np.array(spotPrice).reshape([-1,1]))
    predvalues[("differential", size)] = predictions
    preddeltas[("differential", size)] = deltas[:, 0]
    print("Model is : ", approximator)
    print(predvalues)
    print(preddeltas)
    return instTicker


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    dict_obj = ModelDictionary()
    app.run()