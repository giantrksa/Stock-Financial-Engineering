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
    print("                             Copyright © GIAN ANTARIKSA                              ")
    print("=====================================================================================")
    print()
    print("PROCESSING TIME :", dt_now)

    # -------------- SET THE PROCESS ONLY HAPPENS AT 00:00 AM EVERY DAY ----
    if dt_now.hour == 21 :

        # ---- set database connection
        database_username = 'gian'
        database_password = 'bolobolo123'
        database_ip       = '220.92.62.203:13306'
        database_name     = 'gian_database'
        database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                    format(database_username, database_password, 
                                                            database_ip, database_name))

        lq45 = ["ASII.JK", "BBCA.JK", "BBRI.JK", "BBNI.JK", "BMRI.JK", "UNTR.JK", "TLKM.JK", "INDF.JK", "UNVR.JK", "WIKA.JK", "EXCL.JK", "ADRO.JK", "ANTM.JK", "AALI.JK", "ICBP.JK", "INCO.JK", "ITMG.JK", "JPFA.JK", "JSMR.JK", "KLBF.JK", "LPKR.JK", "MNCN.JK", "PGAS.JK", "PTBA.JK", "PTPP.JK", "SMGR.JK", "SRIL.JK", "SMBR.JK", "TKIM.JK", "TINS.JK"]


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

