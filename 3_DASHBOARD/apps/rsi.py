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
    st.title('Relative Strength Index Analysis')


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


    # Create Plotly figure
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles=('{} Stock Price'.format(col_select), 'Relative Strength Index'.format(col_select)))

    # Add BBRI stock price trace
    fig.add_trace(go.Candlestick(x=stock_data['Date'], open=stock_data['Open'], high=stock_data['High'], low=stock_data['Low'], close=stock_data['Close'], name='{} Stock Price'.format(col_select)), row=1, col=1)

    # Add RSI trace
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['RSI'], name='RSI', line=dict(color='#19D3F3')), row=2, col=1)

    # Add buy and sell signals to plot
    fig.add_trace(go.Scatter(x=stock_data[stock_data['Buy']==1]['Date'], y=stock_data[stock_data['Buy']==1]['Close'], name='Buy', mode='markers', marker=dict(color='#636EFA', symbol='triangle-up', size=10)), row=1, col=1)
    fig.add_trace(go.Scatter(x=stock_data[stock_data['Sell']==1]['Date'], y=stock_data[stock_data['Sell']==1]['Close'], name='Sell', mode='markers', marker=dict(color='#FFA15A', symbol='triangle-down', size=10)), row=1, col=1)

    # Add Buy and sell Recommendation trace
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Buy Recommendation']*25, name='Buy Recommendation', line=dict(color='#636EFA')), row=2, col=1)
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Sell Recommendation']*25, name='Sell Recommendation', line=dict(color='#FFA15A')), row=2, col=1)


    # Update layout
    fig.update_layout(width=1200, height=800, title='{} Stock Price and Relative Strength Index'.format(col_select), hovermode="x unified", xaxis_rangeslider_visible=False)

    # Show chart
    st.plotly_chart(fig)
