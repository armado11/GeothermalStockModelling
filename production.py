import numpy as np 
import pandas as pd

'Definition of the different equations explained in the methodology: 
#Extraction (Eq. 22)[MW]
def E(P: float, S_t: float, par: list): #input (pressure, stock, ['P_max', 'Q_max', 'S_max', 'R_max']); output(extraction)
    E = par[1]*(S_t/par[2])*(np.sqrt(1-(P/par[0])**2))
    return E

#Recharge (Eq. 21)[MW]
def R(S_t: float, par: list): 
    R = par[3] * (par[2] - S_t) / par[2]
    return R

#Enthalpy (Calculated as a linear function from the known enthalpy values found in Table 2) [kJ/kg]
def H(P: float, index: int): #input (pressure, index); output(enthalpy)
    if index == 0:
        h = -27.74 * P + 2042.1
    elif index == 1: 
        h = -4.2335 * P + 1800.4
    return h

#Well total flow (Eq. 23) [kg/s]
def fT(E: float, H: float): #input (extraction, enthalpy); output (total flow rate)
    fT = E/H * 1e3
    return fT

#Steam ratio (Calculated as a linear function from the known enthalpy and pressure values found in Table 3) [-]
def x(P: float, index: int): #input (pressure, enthalpy); output (steam ratio)
    if index == 0:
        steamratio = -0.018913949312877355 * P + 0.6879148947527665
    elif index == 1: 
        steamratio = -0.006282806955590024 * P + 0.5537159285777753
    return steamratio

#Well steam flow rate (Eq. 24) [kg/s]
def fS(fT: float, x: float): #input (total flow, steam ratio); output (steam flow rate)
    fS = fT * x
    return fS

#Well brine flow rate (Eq. 25) [kg/s]
def fL(fT: float, x: float): #input (total flow, steam ratio); output (liquid flow rate)
    fL = fT * (1 - x) 
    return fL

#Well carbon emission flow rate (Eq. 26) [mg/s]
def fCO2(fS: float, index: int): #input (steam flow, index); output (co2 emission rate)
    par_CO2 = [3981, 1052] #mg/kg of steam
    #par_CO2 = [1052, 3981] 
    CO2 = fS * par_CO2[index]
    return CO2

def objective_z(z, params): #input (pressure, stock), output(objective function) (Eq. 49)
    totalobj = 0
    p_obv = [50/18.1*5, 0.079*3.6, 79*3.6e-6] #Objective coefficients [price of electricity, excess brine tax, carbon emission tax]
    
    for t in range(int(len(z)/4)): #n_timesteps = len(z)/4 as the total lenght of the list is for all 4 variables per step
        y = t*4
        steam = 0
        water = 0
        for i in range(len(params)): #n_wells = len(params)
            steam += E(z[y+i], z[y+i+2], params[i])/H(z[y+i], i)*1e3*x(z[y+i], i) #(Eq. 47)
        #steam = 19.6 if steam >= 19.6 else steam (Eq. 48)
        if steam >= 19.6: 
            steam = 19.6
        #First part of the objective equation concerning revenue from steam
        totalobj += (steam - 1.5)*p_obv[0] 
        #Second part of the objective equation concerning cost of excess brine
        for i in range(len(params)): 
            water += E(z[y+i], z[y+i+2], params[i])/H(z[y+i], i)*1e3*(1-x(z[y+i], i))
        totalobj -= (water-22.0)*p_obv[1] #water tax input
        #Third part of the objective equation concerning cost of carbon emissions
        for i in range(len(params)): 
            totalobj -= fCO2(E(z[y+i], z[y+i+2], params[i])/H(z[y+i], i)*1e3*x(z[y+i], i), i)*p_obv[2] #co2 tax
    return -totalobj 

#Constraint 1 (Eq. 54)
def cons1(z: list, *params: list): #input(z(P11, P12, S11, S12), output = fL11 + fL12 >= 22.)
    c1_arr = [-22.0 for y in range(int(len(z)/4))] 
    for t in range(len(c1_arr)):
        c1 = -22.0
        y = t*4
        for i in range(len(params)): 
            c1 += E(z[y+i], z[y+i+2], params[i])/H(z[y+i], i)*1e3*(1-x(z[y+i], i))
        c1_arr[t] = c1
    return c1_arr

#Stock recalculation for each step (Eq. 55)
def stock_balance(z: list, *params: list):
    deltat = 1/24 #one month
    sb_arr = [0 for y in range(int(len(z)/2))] #array of stock balance (total z / n of n_params) = two stock values per t
    for t in range(int(len(sb_arr)/2)): #for each timestep, divide by t again
        y = t*4
        if y == 0: 
            for i in range(len(params)): 
                sb_arr[2*t+i] = - z[y+i+2] + params[i][2] #Initial stock = Smax
        else: 
            for i in range(len(params)):
                #remember previous stock is actual stock index - 4
                sb_arr[2*t+i] = - z[y+i+2] + z[y-4+i+2] + R(z[y+i+2], params[i]) * deltat - E(z[y+i], z[y+i+2], params[i]) * deltat #(Eq. 55)
    return sb_arr

#Need to create a copy without having *params as the minimize was giving an error without said start adding unlimmited parameters even if the specified were inputed
#These two new functions are only used to show the data, but include no change to the origial cons1 and stock_balance functions. 
def cons1_ex(z: list, params: list): #input(z(P11, P12, S11, S12), output = fL11 + fL12 >= 22.)
    c1_arr = [-22.0 for y in range(int(len(z)/4))] 
    for t in range(len(c1_arr)):
        c1 = -22.0
        y = t*4
        for i in range(len(params)): 
            c1 += E(z[y+i], z[y+i+2], params[i])/H(z[y+i], i)*1e3*(1-x(z[y+i], i))
        c1_arr[t] = c1
    return c1_arr

def stock_balance_ex(z: list, params: list):
    deltat = 1/24 #one month
    sb_arr = [0 for y in range(int(len(z)/2))] #array of stock balance (total z / n of n_params) = two stock values per t
    for t in range(int(len(sb_arr)/2)): #for each timestep, divide by t again
        y = t*4
        if y == 0: 
            for i in range(len(params)): 
                sb_arr[2*t+i] = - z[y+i+2] + params[i][2]
        else: 
            for i in range(len(params)):
                #remember previous stock is actual stock index - 4
                sb_arr[2*t+i] = - z[y+i+2] + z[y-4+i+2] + R(z[y+i+2], params[i]) * deltat - E(z[y+i], z[y+i+2], params[i]) * deltat
    return sb_arr
