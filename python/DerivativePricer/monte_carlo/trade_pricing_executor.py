import json
import time
import os
# -*- coding:utf-8 -*-
#######################################################################
# Copyright (C) 2016 Shijie Huang (harveyh@student.unimelb.edu.au)    #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################
from monte_carlo_class import MonteCarloOptionPricing

# Opening JSON file
f = open(os.path.abspath('data\TradesJson_1000.json'))
rf = open(os.path.abspath('data\pricingResults_1000.csv'), "w")
# returns JSON object as
# a dictionary
data_dict = json.load(f)

# Iterating through the json
# list

div_yield = 0.0  # e.g. dividend yield = 1%
no_of_slice = 4  # no. of slices PER YEAR e.g. quarterly adjusted or 252 trading days adjusted
simulation_rounds = int(1000)  # For monte carlo simulation, a large number of simulations required

# print("TradeId, Spot, Strike, timeToMaturity, IR, Sigma, OptionPrice, timeTaken")
rf.write("TradeId, Spot, Strike, timeToMaturity, IR, Sigma, OptionPrice, timeTaken \n")
i=0
totalTimeTaken=0
for dict in data_dict['trades']:
    start = time.time()
    MC = MonteCarloOptionPricing(S0=dict["Spot"],
                                 K=dict["Strike"],
                                 T=dict["timeToMaturity"],
                                 r=dict["IR"],
                                 sigma=dict["Sigma"],
                                 div_yield=div_yield,
                                 simulation_rounds=simulation_rounds,
                                 no_of_slices=no_of_slice,
                                 fix_random_seed=True)
                                 # ,fix_random_seed=5000)

    # stochastic interest rate
    MC.cox_ingersoll_ross_model(a=0.5, b=0.05, sigma_r=0.1)  # use Cox Ingersoll Ross (CIR) model
    # print("simulated IR")

    # stochastic volatility (sigma)
    MC.heston(kappa=2, theta=0.3, sigma_v=0.3, rho=0.5)  # heston model
    # print("simulated VOL")

    MC.stock_price_simulation()
    # print("simulated SPOT")

    value=MC.european_call()
    # time.sleep(3)
    end = time.time()
    timeTaken = (end - start)*1000
    i=i+1
    totalTimeTaken = totalTimeTaken + timeTaken
    # print(dict["TradeId"],",",dict["Spot"],",",dict["Strike"],",",dict["timeToMaturity"],",",dict["IR"],",",dict["Sigma"],",",value,",",timeTaken,"ms")

    resultStr =(json.dumps(dict["TradeId"])+","+json.dumps(dict["Spot"])+","+json.dumps(dict["Strike"])+","+
                json.dumps(dict["timeToMaturity"])+","+json.dumps(dict["IR"])+","+json.dumps(dict["Sigma"])+","+
                str(value)+","+str(timeTaken)+"ms"
                "\n")

    print(resultStr)

    rf.write(resultStr)

print("total trades priced ", i, "totalTimeTaken ", totalTimeTaken/1000)
rf.close()

# Closing file
f.close()
