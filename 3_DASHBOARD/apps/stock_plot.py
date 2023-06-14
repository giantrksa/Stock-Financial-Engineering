# -*- coding: utf-8 -*-
"""
stock_plot page

@author: Gian
Copyright © AWStudio
"""


import streamlit as st
import streamlit.components.v1 as components
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def app():
    st.title('Stock View Analysis')


    # ----------------------------------------------------------------------------------------- #
    #                                       LIBRARY                                             #
    # ----------------------------------------------------------------------------------------- #
    import sqlalchemy
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np
    import plotly.graph_objs as go
    from plotly.subplots import make_subplots
    from scipy.fft import fft, fftfreq, fftshift
    from scipy.signal import welch

    import yfinance as yf
    import plotly.graph_objs as go


    # ----------------------------------------------------------------------------------------- #
    #                            DATABASE CONNECTION AND LOAD DATA                              #
    # ----------------------------------------------------------------------------------------- #
    # ---- set database connection
    database_username = 'gian'
    database_password = 'bolobolo123'
    database_ip       = '220.92.62.203:13306'
    database_name     = 'gian_database'
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                format(database_username, database_password, 
                                                        database_ip, database_name))

    lq45 = ["ASII", "BBCA", "BBRI", "BBNI", "BMRI", "UNTR", "TLKM", "INDF", "UNVR", "WIKA", "EXCL", "ADRO", "ANTM", "AALI", "ICBP", "INCO", "ITMG", "JPFA", "JSMR", "KLBF", "LPKR", "MNCN", "PGAS", "PTBA", "PTPP", "SMGR", "SRIL", "SMBR", "TKIM", "TINS"]

    # streamlit slider
    days = st.slider(' ', 7, 1092, 356)

    st.subheader('Select stocks to view')
    # ----------------------------------------------------------------------------------------- #
    #                                       STOCK ANALYSIS                                      #
    # ----------------------------------------------------------------------------------------- #
    # Define the selectbox for choosing the dataset
    col_select = st.selectbox("Select a dataset", lq45)

    # streamlit write
    st.subheader("Querying data of " + str(col_select) + " last "+str(days)+" days")

    # Define stock ticker symbol
    stock_data = pd.read_sql(f'SELECT * FROM dm_stock_{col_select} LIMIT {days} ',con=database_connection)



    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=stock_data['Date'],
                                        open=stock_data['Open'],
                                        high=stock_data['High'],
                                        low=stock_data['Low'],
                                        close=stock_data['Close'],
                                        name='Candle Bar')])

    # Add close line
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], name='Close', line_color='pink', opacity=0.7))

    # Update chart layout
    fig.update_layout(title=col_select + ' Candlestick Chart',
                    xaxis_rangeslider_visible=False,
                    width=1200, height=800)

    # Show chart
    st.plotly_chart(fig)

    
