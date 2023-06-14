import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from apps import stock_plot, auto_ma, rsi, stoch_osc


# Define the home page
def home_page():
    # Libraries
    from PIL import Image

    # Title
    st.title('Stock Analysis by AWStudio')


    st.write(
        """
        
            Technical analysis is a method of evaluating stocks 
            
        and other financial instruments by analyzing statistical trends and patterns in historical market data. 

        This approach typically involves the use of charts and other visual aids to identify key support and resistance levels, 
        
        as well as indicators such as moving averages, relative strength index (RSI), and Bollinger Bands. 

        By examining these factors, investors can gain insights into the likely future direction of a given stock or the broader market, 
        
        and make informed decisions about when to buy, sell, or hold their positions.

        """
    )

    st.subheader('Expectation')
    st.write(
        """
        In this project, we will be using Python and various libraries such as 
        
        pandas, yfinance, and plotly to perform technical analysis on the LQ45 stocks listed on the IDX. 
        
        Our goal is to create visualizations and tools that will help investors better understand 
        
        the behavior of these stocks and make more informed trading decisions.
        """
    )

    st.subheader('Future Works')
    st.write(
        """
        We will update soon~~
        """
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.info('**Data Scientist: Gian**')
    with c2:
        st.info('**Conceptor: Audia**')
    with c3:
        st.info('**GitHub: [@giantrksa](https://github.com/giantrksa/)**')


# Define the pages of our app
PAGES = {
    "Introduction":home_page,
    "Stock View": stock_plot.app,
    "Auto Moving Average": auto_ma.app,
    "Relative Strength Index": rsi.app,
    "Stochastic Oscillator": stoch_osc.app,
}

# Define the sidebar menu
with st.sidebar:
    st.sidebar.image("aws.png", use_column_width=True, output_format="PNG")
    st.sidebar.title('Stock Analysis by AWS')
    page = option_menu("Features", list(PAGES.keys()))

# Display the selected page
PAGES[page]()
