import numpy as np
import pandas as pd
from scipy.optimize import minimize

def model(params, database): #params = ['P_max', 'Q_max', 'S_max', 'R_max']
    #get data steps from database
    dt = []
    for i in range(len(database)):
        dt.append(database.loc[i]['Dt'])

    #get the calculated extraction data from the inputed database
    extraction_data = [0]
    for i in range(len(database)-1):
        extraction_data.append(database.loc[i+1]['Extraction_d'])
    #print(Extraction_data, len(Extraction_data))
    
    #model to get each of the new extraction values

    for i in range(len(dt)):
        if i == 0: #to create first line of the database and create parameter arrays
            extraction_pred = [0] #First timestep considers null extraction
            database.at[0, 'Extraction'] = extraction_pred[0]
            recharge_pred = [0] #First timestep considers null recharge
            database.at[0, 'Recharge'] =recharge_pred[0]
            stock_pred = [params[2]] # Initial stock = S_max
            database.at[0, 'Stock'] = stock_pred[0]
        else: #For the rest of timesteps, calculate stock, recharge and extraction with the equations described in the thesis 
            stock_p = stock_pred[i-1] - extraction_pred[i-1] * dt[i] + recharge_pred[i-1] * dt[i] #(Eq. 37)
            #print(dt[i], stock_p, stock_pred[i-1], extraction_pred[i-1], recharge_pred[i-1])
            stock_pred.append(stock_p)
            database.at[i, 'Stock'] = stock_p

            if database.loc[i]['Flow'] == 0: #(Eq. 35)
                ext_p = 0
            else:
                ext_p = params[1] * (stock_pred[i]/params[2]) * np.sqrt((1-(database.loc[i]['Pressure']/params[0])**2)) #(Eq. 39)
            extraction_pred.append(ext_p)
            database.at[i, 'Extraction'] = ext_p

            recharge_p = params[3] * (params[2] - stock_pred[i]) / params[2] #(Eq. 38)
            #print(dt[i], recharge_p, stock_pred[i])
            recharge_pred.append(recharge_p)
            database.at[i, 'Recharge'] = recharge_p
            
    #extraction_pred.append(params[1] * (stock_p/params[2]) * np.sqrt((1-(database.iloc[-1]['Pressure']/params[0])**2)))
    #database.at[59, 'Extraction'] = params[1] * (stock_p/params[2]) * np.sqrt((1-(database.iloc[-1]['Pressure']/params[0])**2))
    #recharge_pred.append(params[3] * (params[2] - stock_p) / params[2])
    #database.at[59, 'Recharge'] = params[3] * (params[2] - stock_p) / params[2]

    diff = []
    for i in range(len(dt)):
        if database.loc[i]['Data Quality'] == 'Estimated' or  database.loc[i]['Data Quality'] == 'Unchecked' : #(Eq. 34)
            d = 0
        else:
            d = (extraction_data[i]-extraction_pred[i])**2 #Calculates the residual square of the extractions for each timestep
        diff.append(d)
        database.at[i, 'Diff'] = d
    #returns all values (similar to excel)    
    return database, dt, extraction_data, extraction_pred, recharge_pred, stock_pred, diff #Returns the calculated database and the different lists individually if needed to print

def sum_of_squares(params, database): #Calculates the total sum of the residuals squared (Eq. 36). This is the equation which will get minimized to get the 
  #parameters that get the smalles sum of squares and therefore are considered the optimal parameters to define the stock model of the reservoir.
    x, dt, extraction_data, extraction_pred, recharge_pred, stock_pred, diff = model(params, database) #Calculate the model for the parameters inputed

    #return Extraction_data, extraction_pred
    #get the sum of errors
    obj = 0
    for i in range(len(diff)):
        obj += diff[i]
    return obj #return the sum of residuals squared
