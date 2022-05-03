'main.py' #main script to call other scrips for specific actions

'required libraries and scrits'
import numpy as np
import pandas as pd

from dat_manager import dat_div
from dat_purger import purge_BJ11, purge_BJ12

from scipy.optimize import minimize
from residualmse import sum_of_squares, model
from dataformater import dat_format
from res_par_opt import final_dat

if __name__ == '__main__':

    '1.- Input the final database for each well with all data preprocessed'
    path = 'C:/Users/98man/Desktop/Final BJ-11.xlsx'
    data11 = pd.ExcelFile(f'{path}')
    BJ11 = pd.read_excel(data11, 1)

    path = 'C:/Users/98man/Desktop/Final BJ-12.xlsx'
    data12 = pd.ExcelFile(f'{path}')
    BJ12 = pd.read_excel(data12, 0)

    '2.- Optimization for BJ-11'
    iparams11 = [40, 70, 180, 200]
    res = minimize(sum_of_squares, iparams11, method='L-BFGS-B', args = BJ11, bounds = ((31.8, None), (0, None), (0, None), (0, None)))
    par11 = res.x
    
    print('--- BJ-11 ---')
    #print(par11)
    print('P_max: {} [bar]; Q_max: {} [MW], S_max: {} [MWyr]; R_max: {} [MW]'.format(par11[0], par11[1], par11[2], par11[3]))
    print('Sum of squares error: {}' .format(sum_of_squares(par11, BJ11)))

    #database11, dt, extraction_data, extraction_pred, recharge_pred, stock_pred, diff = model(par11, BJ11)
    #print(database11)

    '3.- Optimization for BJ-12'
    iparams12 = [40, 80, 160, 100]
    res = minimize(sum_of_squares, iparams12, method='L-BFGS-B', args = BJ12, bounds = ((0, None), (0, None), (0, None), (0, None)))
    par12 = res.x

    print('--- BJ-12 ---')
    #print(par12)
    print('P_max: {} [bar]; Q_max: {} [MW], S_max: {} [MWyr]; R_max: {} [MW]'.format(par12[0], par12[1], par12[2], par12[3]))
    print('Sum of squares error: {}' .format(sum_of_squares(par12, BJ12)))

    #database12, dt, extraction_data, extraction_pred, recharge_pred, stock_pred, diff = model(par12, BJ12)
    #print(database12)

    '4.- Production optimization'
    

