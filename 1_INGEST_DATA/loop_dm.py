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

# ========================================================================================= #
#                          LOOP EVERYDAY AT 00:00 AM                                        #
# ========================================================================================= #

while True:

    dt_now = pd.to_datetime(datetime.now(tz=pytz.timezone('Asia/Seoul')))

    print("=====================================================================================")
    print("                          Copyright © Cybertrend Intrabuana                          ")
    print("=====================================================================================")
    print()
    print("PROCESSING TIME :", dt_now)

    # -------------- SET THE PROCESS ONLY HAPPENS AT 00:00 AM EVERY DAY ----
    if dt_now.hour == 12 :

        # ---- set database connection
        server = '10.3.4.99,1433'
        database = 'dwh_dev' 
        username = 'cybertrend'
        password = 'cn70HJBQHRfsoOS'  
        cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()

        query = "SELECT tanggal, jenis, tipe, product_type_name, loc_src_area_name, tonase FROM dwh.DM_production_transaction;"
        df = pd.read_sql(query, cnxn)

        lq45 = ["ASII.JK", "BBCA.JK",]


        dt_now = pd.to_datetime(datetime.now(tz=pytz.timezone('Asia/Jakarta')))

        # Set the start and end dates for the data to be downloaded
        start_date = "2010-01-01"
        end_date = dt_now

        all_stocks = []

        for stocks in lq45:
            # Download the historical data for all tickers
            temp_data = yf.download(stocks, start=start_date, end=end_date)
            temp_data['Stock Name'] = stocks[:-3]
            all_stocks.append(temp_data)

        df_all_stocks = pd.concat(all_stocks).reset_index()
        print(df_all_stocks)

        stocks_df_list = {}
        for i in df_all_stocks['Stock Name'].unique():
            temp_df = df_all_stocks[df_all_stocks['Stock Name'] == i].reset_index(drop=True).drop(['Stock Name'],axis=1)
            stocks_df_list[i] = temp_df
        
        print("Total Stocks New Data :",len(lq45))

        for i in list(stocks_df_list.keys()):
            stocks_df_list[i].to_sql(con=database_connection, 
                name='dl_stock_{}'.format(i), 
                if_exists='replace',
                index=False)

        
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

