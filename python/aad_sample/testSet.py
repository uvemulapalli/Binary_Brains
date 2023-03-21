from BlackScholes import BlackScholes
from flask import Flask, request
import csv

app = Flask(__name__)
sizes = [1024, 8192]

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.


@app.route('/generate_test', methods=['POST'])
# ‘/’ URL is bound with hello_world() function.
def generate_test():
    # read csv file
    filefromreq = request.form['filename']
    with open('testing.csv', 'w', newline='') as writefile:
        writer = csv.writer(writefile)
        writer.writerow(["Instrument", "xTrain", "yTrain", "dx_dyTrain"])
    with open(filefromreq) as readfile:
        reader = csv.reader(readfile)
        for row in reader:
            print("row", row)
            insticker = row.__getattribute__('InstrumentTicker')
            strikeprice = row.__getattribute__('StrikePrice')
            expiry = row.__getattribute__('Expiry')
            spotprice = row.__getattribute__('SpotPrice')
            volatility = row.__getattribute__('Volatality')
            key = insticker
        # extract expiry month
            #expirymonth = 0.5
            bs: BlackScholes = BlackScholes(volatility,1,expiry,spotprice)
            xTrain, ytrain, dx_dyTrain = bs.testSet(bs,spotprice-10,spotprice+10)
        #save to csv for now
            writer.writerow([xTrain,ytrain,dx_dyTrain])
    return

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    #dict_obj = ModelDictionary()
    app.run()