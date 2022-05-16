'main.py' #main script to call other scrips for specific actions

'required libraries and scrits'
import pandas as pd
from scipy.optimize import minimize

#these code is provided in the 
from residualmse import sum_of_squares, model
from prod_5y_linearx import E, R, H, fT, x, fS, fL, fCO2, objective_z, cons1, stock_balance

if __name__ == '__main__':

    '1.- Input the final database for each well with all data preprocessed'
    path = 'C:/User/Downloads/GeothermalStockModelling/BJ-11.xlsx'
    data11 = pd.ExcelFile(f'{path}')
    BJ11 = pd.read_excel(data11, 1)

    path = 'C:/User/Downloads/GeothermalStockModelling/BJ-12.xlsx'
    data12 = pd.ExcelFile(f'{path}')
    BJ12 = pd.read_excel(data12, 0)

    '2.- Optimization for BJ-11'
    iparams11 = [40, 70, 180, 200] #initial parameters for the stock model parametrization for well BJ-11
    
    #minimization of the sum of squares error, use maximum known pressure as minimum bound for the maximum pressure variable (x[0]). 
    res = minimize(sum_of_squares, iparams11, method='L-BFGS-B', args = BJ11, bounds = ((31.8, None), (0, None), (0, None), (0, None))) 
    par11 = res.x #get the optimized parameters
    
    print('--- BJ-11 ---')
    #print(par11)
    print('P_max: {} [bar]; Q_max: {} [MW], S_max: {} [MWyr]; R_max: {} [MW]'.format(par11[0], par11[1], par11[2], par11[3]))
    print('Sum of squares error: {}' .format(sum_of_squares(par11, BJ11))) #error of the optimum parameters

    #uncomment the following two lines to get a filled database with the optimal parameters and the calculated stock, extraction and recharge values for each timestep
    #database11, dt, extraction_data, extraction_pred, recharge_pred, stock_pred, diff = model(par11, BJ11)
    #print(database11)
    
    '3.- Optimization for BJ-12' #same code as 2.- just for well BJ-12
    iparams12 = [40, 80, 160, 100]
    res = minimize(sum_of_squares, iparams12, method='L-BFGS-B', args = BJ12, bounds = ((0, None), (0, None), (0, None), (0, None)))
    par12 = res.x
    print('--- BJ-12 ---')
    #print(par12)
    print('P_max: {} [bar]; Q_max: {} [MW], S_max: {} [MWyr]; R_max: {} [MW]'.format(par12[0], par12[1], par12[2], par12[3]))
    print('Sum of squares error: {}' .format(sum_of_squares(par12, BJ12)))

    #database12, dt, extraction_data, extraction_pred, recharge_pred, stock_pred, diff = model(par12, BJ12)
    #print(database12)

    '4.- Production optimization initial variables'
    params = [par11, par12] #add all parameters to a list
    
    'timestep settings: one step = one month'
    n_years = 5 #choose the wanted amount of years
    n_timesteps = (24 * n_years) + 1 #12 for monthly, 24 for twoweekly calculations. Change depending on the amount of timesteps wanted in a year 
    deltat = 1/24 #Period between timestes. If changed, remember to also change it in stock_balance() and stock_balance_ex()

    'Number of wells'
    n_wells = 2 #Number of wells
    n_pars = 2 #Number of variables, in our case, Pressure & Stock

    'Initial VARIABLE list' #Create the variable list formatted as [P11(t=0), P12(t=0), S11(t=0), S12(t=0), ..., P11(t=120), P12(t=120), S11(t=120), S12(t=120)] 
    #where P11 is Pressure of BJ-11 in bars, P12 is Pressure of BJ-12 in bars, S11 is stock of BJ-11 in MWyr and S12 is stock of BJ-12 in MWyr
    
    z0 = [1 for y in range(n_timesteps * n_wells * n_pars)] #z0 = T x 2N where T is timesteps and N is number of wells (multiplied to have Pressure and Stock for each well)
    'To create the list as wanted with [P11, P12, S11, S12, ...] structure'
    for t in range(n_timesteps): #loop creating each 4 variables for each timestep
        y = t*4
        z0[y] = 12.1 #random initial value for pressure of the first well (index = 0)
        z0[y+1] = 10.1 #random initial value for pressure of the second well (index = 1)
        z0[y+2]= params[0][2] - 5 #random initial value for stock of the first well (index = 2)
        z0[y+3] = params[1][2] - 5 #random initial value for stock of the second well (index = 3)
    #print(z0)

    'Boundaries for each t' #Same as creating a variable list but for boundaries
    
    bnds = [1 for y in range(n_timesteps * n_wells * n_pars)] 
    'To create the list as wanted with [P11, P12, S11, S12, ...] structure also for bounds of each variable'
    for t in range(n_timesteps): 
        y = t*4
        bnds[y] = (12, 26)
        bnds[y+1] = (10, 26)
        bnds[y+2]= (0, params[0][2])
        bnds[y+3] = (0, params[1][2])
    #print(bnds) 

    cons = ({'type': 'ineq', 'fun': cons1, 'args': params}, 
            {'type': 'eq', 'fun': stock_balance, 'args': params})

    '5.- Production optimization'#production strategy optimization, increase maxiter if more iterations are needed to reach optimum
    res = minimize(objective_z, z0, args = (params), method = 'SLSQP', bounds = bnds, constraints = cons, options= {'maxiter': 1000})     
    f_z = res.x
    print(f_z)
    print(objective_z(f_z, params))

    '5.- Production estrategy database'
    df = pd.DataFrame(columns = ['Year', 'P11', 'S11', 'E11', 'R11', 'H11', 'TF11', 'SF11', 'LF11',\
        'P12', 'S12', 'E12', 'R12', 'H12', 'TF12', 'SF12', 'LF12', \
        'Obj', 'Total Steam', 'Total Water', 'CO211', 'CO212', 'Total CO2']) #Create dataframe showing different parameters calculated from initial variables

    'Create a new row for each timestep for the needed parameters'
    for t in range(int(len(f_z)/4)):
        y = t*4
        new_row = {'Year': t/24, 'P11': f_z[y], 'S11': f_z[y+2], 'E11': E(f_z[y], f_z[y+2], params[0]), 'R11': R(f_z[y+2], params[0]), \
            'H11': H(f_z[y], 0), 'TF11': fT(E(f_z[y], f_z[y+2], params[0]), H(f_z[y], 0)), \
            'SF11': fS(fT(E(f_z[y], f_z[y+2], params[0]), H(f_z[y], 0)), x(f_z[y], 0)), \
            'LF11': fL(fT(E(f_z[y], f_z[y+2], params[0]), H(f_z[y], 0)), x(f_z[y], 0)), \
            'P12': f_z[y+1], 'S12': f_z[y+3], 'E12': E(f_z[y+1], f_z[y+3], params[1]), 'R12': R(f_z[y+3], params[1]), \
            'H12': H(f_z[y+1], 1), 'TF12': fT(E(f_z[y+1], f_z[y+3], params[1]), H(f_z[y+1], 1)), \
            'SF12': fS(fT(E(f_z[y+1], f_z[y+3], params[1]), H(f_z[y+1], 1)), x(f_z[y+1], 1)), \
            'LF12': fL(fT(E(f_z[+1], f_z[y+3], params[1]), H(f_z[y+1], 1)), x(f_z[y+1], 1)), \
            'Obj': -1*objective_z(f_z[y:y+4], params)}

        df = df.append(new_row, ignore_index=True) 
    df['Total Steam'] = df[['SF11','SF12']].sum(axis=1)
    df['Total Water'] = df[['LF11','LF12']].sum(axis=1)
    df['CO211'] = df[['SF11']]*3981
    df['CO212'] = df[['SF12']]*1052
    df['Total CO2'] = df[['CO211','CO212']].sum(axis=1)
    
    print(df)
    print('Total objective: {}'.format(-1*objective_z(f_z, params))) #final revenue in $/h
    
    #Uncomment the following two lines to get the dataframe into an excel where data can be better visualised.
    #path = 'C:/Users/...'
    #df.to_excel(path) 
