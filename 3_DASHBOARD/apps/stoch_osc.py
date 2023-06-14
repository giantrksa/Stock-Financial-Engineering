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
    st.title('Stochastic Oscillator Analysis')


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
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, )

    # Add BBRI stock price trace
    fig.add_trace(go.Candlestick(x=stock_data['Date'], open=stock_data['Open'], high=stock_data['High'], low=stock_data['Low'], close=stock_data['Close'], name='{} Stock Price'.format(col_select)), row=1, col=1)

    # Add Oscillator trace
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Stochastic Oscillator'], hovertemplate=stock_data['Condition'],name='Stochastic Oscillator', line=dict(color='slategray')), row=2, col=1)
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=[20]*len(stock_data['Date']), name='Oversold', line=dict(color='#d62728', width=1, dash='dash'), ), row=2, col=1)
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=[80]*len(stock_data['Date']), name='Overbought', line=dict(color='#FFA15A', width=1, dash='dash'), ), row=2, col=1)

    # # Update layout
    fig.update_layout(hovermode="x unified", 
                    width = 1200,
                    height=800, 
                    title='{} Stock Price and Stochastic Oscillator'.format(col_select), 
                    xaxis_rangeslider_visible=False,
                    xaxis_title='Date',
                    yaxis_title='Stochastic Oscillator',
                    # Update line colors
                    plot_bgcolor='#fff',
                    paper_bgcolor='#fff',
                    font=dict(color='black'),
                    yaxis=dict(gridcolor='lightgray'),
                    xaxis=dict(gridcolor='lightgray'),
                    margin=dict(l=20, r=20, t=40, b=20))

    # Show chart
    st.plotly_chart(fig)


    # Show Table
    st.subheader("Last 4 Days Transaction")
    st.table(stock_data[['Date', 'Stochastic Oscillator', 'Condition']].head())
    st.subheader("Stock Status ")



    recom = str(stock_data['Condition'].head(1).values[0])
    result = f'<p style="font-family:sans-serif; color:Green; font-size: 42px;">{recom}</p>'
    st.markdown(result, unsafe_allow_html=True)
