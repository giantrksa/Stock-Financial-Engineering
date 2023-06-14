# -*- coding: utf-8 -*-
"""

@author: Gian - Business Analytics Lab - PKNU

"""

import pandas as pd
import sqlalchemy
import json
from tqdm import tqdm
import time
import yfinance as yf
from datetime import datetime
import pytz
import numpy as np


from sklearn.metrics import mean_squared_error
from bayes_opt import BayesianOptimization


# ========================================================================================= #
#                          LOOP EVERYDAY AT 00:00 AM                                        #
# ========================================================================================= #

while True:

    dt_now = pd.to_datetime(datetime.now(tz=pytz.timezone('Asia/Seoul')))

    print("=====================================================================================")
    print("                    Copyright © GIAN ANTARIKSA - Indonesia                           ")
    print("=====================================================================================")
    print()
    print("PROCESSING TIME :", dt_now)

    # -------------- SET THE PROCESS ONLY HAPPENS AT 00:00 AM EVERY DAY ----
    if dt_now.hour == 21 :

        # ---- set database connection
        database_username = 'gian'
        database_password = 'bolobolo123'
        database_ip       = '172.17.0.6'
        database_name     = 'gian_database'
        database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                    format(database_username, database_password, 
                                                            database_ip, database_name))

        lq45 = ["ASII.JK", "BBCA.JK", "BBRI.JK", "BBNI.JK", "BMRI.JK", "UNTR.JK", "TLKM.JK", "INDF.JK", "UNVR.JK", "WIKA.JK", "EXCL.JK", "ADRO.JK", "ANTM.JK", "AALI.JK", "ICBP.JK", "INCO.JK", "ITMG.JK", "JPFA.JK", "JSMR.JK", "KLBF.JK", "LPKR.JK", "MNCN.JK", "PGAS.JK", "PTBA.JK", "PTPP.JK", "SMGR.JK", "SRIL.JK", "SMBR.JK", "TKIM.JK", "TINS.JK"]


        all_stocks = []

        # Import Dataset

        for stocks in lq45:
            # Download the historical data for BBRI
            temp_data = pd.read_sql('select * from dl_stock_{}'.format(stocks[:-3]),con=database_connection)
            temp_data['Stock Name'] = stocks[:-3]
            all_stocks.append(temp_data)

        df_all_stocks = pd.concat(all_stocks)
        print(df_all_stocks.head())

        stocks_df_list = {}
        for i in df_all_stocks['Stock Name'].unique():
            temp_df = df_all_stocks[df_all_stocks['Stock Name'] == i].reset_index(drop=True).drop(['Stock Name'],axis=1)
            stocks_df_list[i] = temp_df


        # Auto Moving Average
        # Define the objective function to minimize using Bayesian optimization
        def objective_function(ma1, ma2):
            ma1 = int(ma1)
            ma2 = int(ma2)
            if ma1 <= 0 or ma2 <= 0:
                return np.inf
            stock_data['MA1'] = stock_data['Close'].rolling(window=ma1).mean()
            stock_data['MA2'] = stock_data['Close'].rolling(window=ma2).mean()
            stock_data['Signal'] = np.where(stock_data['MA1'] > stock_data['MA2'], 1, 0)
            stock_data['Position'] = stock_data['Signal'].diff()
            stock_data['Position'].fillna(0, inplace=True)
            stock_data['Returns'] = stock_data['Close'].pct_change()
            stock_data['Strategy Returns'] = stock_data['Position'] * stock_data['Returns']
            return -1 * stock_data['Strategy Returns'].sum()

        # Define a function to determine if there is a cross-over
        def determine_crossover(row):
            if row['MA_1-2'] > 0 and row['MA_1-2 MA_2'] < 0:
                return 'Sell'
            elif row['MA_1-2'] < 0 and row['MA_1-2 MA_2'] > 0:
                return 'Buy'
            else:
                return 'Hold'


        stock_ma_list = {}

        for i in list(stocks_df_list.keys()):
            # Define Stock name
            stock_data = stocks_df_list[i]
            
            # Define the bounds for the parameter values
            bounds = {'ma1': (10, 50), 'ma2': (50, 100)}

            # Define the Bayesian optimizer and run the optimization
            optimizer = BayesianOptimization(f=objective_function, pbounds=bounds, random_state=1)
            optimizer.maximize(init_points=10, n_iter=50, acq='ucb', kappa=2.576)

            # Print the best parameter values and objective function value
            print('Best Parameters:', optimizer.max['params'])
            print('Best Objective Function:', -1 * optimizer.max['target'])

            # Determine Best MA
            best_ma1 = round(optimizer.max['params']['ma1'])
            best_ma2 = round(optimizer.max['params']['ma2'])

            # Add the auto moving averages to the dataframe
            stock_data['MA_1'] = stock_data['Close'].rolling(window=best_ma1).mean()
            stock_data['MA_2'] = stock_data['Close'].rolling(window=best_ma2).mean()

            # Create a new column for the difference between the 20-day and 50-day moving averages
            stock_data['MA_1-2'] = stock_data['MA_1'] - stock_data['MA_2']

            # Create a new column for the 50-day moving average of the difference between the 20-day and 50-day moving averages
            stock_data['MA_1-2 MA_2'] = stock_data['MA_1-2'].rolling(window=best_ma2).mean()

            # Apply the determine_crossover function to each row in the dataframe to determine if there is a cross-over
            stock_data['Crossover'] = stock_data.apply(determine_crossover, axis=1)
            
            # Deploy to end
            stock_ma_list[i] = stock_data


        # Relative Strength Index
        # Define function to calculate RSI
        def calculate_rsi(prices, n=14):
            deltas = np.diff(prices)
            seed = deltas[:n+1]
            up = seed[seed>=0].sum()/n
            down = -seed[seed<0].sum()/n
            rs = up/down
            rsi = np.zeros_like(prices)
            rsi[:n] = 100. - 100./(1.+rs)

            for i in range(n, len(prices)):
                delta = deltas[i-1]
                if delta>0:
                    upval = delta
                    downval = 0.
                else:
                    upval = 0.
                    downval = -delta

                up = (up*(n-1) + upval)/n
                down = (down*(n-1) + downval)/n
                rs = up/down
                rsi[i] = 100. - 100./(1.+rs)

            return rsi


        stock_rsi_list = {}

        for i in list(stock_ma_list.keys()):
            # Define Stock name
            stock_data = stock_ma_list[i]

            # Calculate RSI
            stock_rsi = calculate_rsi(stock_data['Close'])
            stock_data['RSI'] = stock_rsi
            
            # Set RSI threshold for buy and sell signals
            buy_threshold = 30
            sell_threshold = 70

            # Create buy and sell recommendation columns
            stock_data['Buy'] = np.where(stock_rsi <= buy_threshold, 1, 0)
            stock_data['Sell'] = np.where(stock_rsi >= sell_threshold, 1, 0)

            # Add buy and sell recommendation column to stock data
            stock_data['Buy Recommendation'] = np.where(stock_rsi < buy_threshold, 1, 0)
            stock_data['Sell Recommendation'] = np.where(stock_rsi > sell_threshold, 1, 0)
            
            # Deploy to end
            stock_rsi_list[i] = stock_data


        # Stochastic Oscillator

        stock_stoch_list = {}

        for i in list(stock_rsi_list.keys()):
            # Calculate Stochastic Oscillator
            stock_data = stock_rsi_list[i]
            stock_data['Stochastic Oscillator'] = (stock_data['Close'] - stock_data['Low'].rolling(window=14).min()) / (stock_data['High'].rolling(window=14).max() - stock_data['Low'].rolling(window=14).min()) * 100
            
            # Define thresholds
            oversold_threshold = 20
            overbought_threshold = 80

            # Create new columns
            stock_data['Condition'] = ''
            stock_data.loc[stock_data['Stochastic Oscillator'] < oversold_threshold, 'Condition'] = 'Oversold'
            stock_data.loc[stock_data['Stochastic Oscillator'] > overbought_threshold, 'Condition'] = 'Overbought'
            stock_data.loc[(stock_data['Stochastic Oscillator'] >= oversold_threshold) & (stock_data['Stochastic Oscillator'] <= overbought_threshold), 'Condition'] = 'Normal'
            # Deploy to end
            stock_stoch_list[i] = stock_data


        # Export to Datamart
        for i in list(stock_stoch_list.keys()):
            stock_stoch_list[i].sort_values(by="Date",ascending=False).to_sql(con=database_connection, 
                name='dm_stock_{}'.format(i), 
                if_exists='replace',
                index=False)
            print(stock_stoch_list[i])

        
    else :
        print("THIS TIME IS ON "+str(dt_now.hour)+" : 00 , PROCESSING CONSTRAINT, ONLY WORKING ON HOURS THAT MENTIONED EVERYDAY")
        print()  
        print("NOT UPDATE TIME :", dt_now)  
        
    print()
    print("=====================================================================================")
    print("   Copying in whole or in part is strictly forbidden without prior written approval  ")
    print("=====================================================================================")
    print()
    

    # ------- TIME SLEEP : SET 1 HOURS  -----------------
    print("WAITING TIME :")
    for i in tqdm(range(0,3600)):
        time.sleep(1)

