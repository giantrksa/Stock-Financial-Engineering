# Auto Moving Average Analysis and Trading Strategy

The code uses the auto moving average analysis to create a trading strategy. It uses Bayesian optimization to find the optimal parameters for the moving averages.

First, it defines an objective function to minimize using Bayesian optimization. The function calculates two moving averages, one short-term and one long-term, based on the closing prices of the stock. A signal is generated when the short-term moving average crosses the long-term moving average. The signal is then used to compute the returns of the trading strategy. The objective function returns the negative sum of the strategy returns, which is what the Bayesian optimizer attempts to minimize.

Once the Bayesian optimizer has found the optimal parameters for the moving averages, these are added to the stock data. The difference between the two moving averages is also calculated, as well as the moving average of this difference. A function is then defined to determine if there is a crossover between these two last values, which is used to generate a new signal.

Lastly, a Plotly chart is created displaying the candlestick chart of the stock's prices, the two moving averages, and the volume of the stock. The latest crossover signal is also shown.

# Relative Strength Index

The code then calculates the Relative Strength Index (RSI) for the stock. RSI is a momentum indicator that measures the speed and change of price movements. It is often used to identify overbought or oversold conditions in a market.

The code defines a function to calculate the RSI based on the closing prices of the stock. It then creates two new columns in the stock data: one to indicate when the RSI is below a certain threshold (indicating a buy signal), and one to indicate when the RSI is above a certain threshold (indicating a sell signal).

A Plotly chart is then created displaying the stock's prices, the RSI, and the buy and sell signals.

# Bollinger Bands

Bollinger Bands are a type of statistical chart characterizing the prices and volatility over time of a financial instrument or commodity, using a formulaic method propounded by John Bollinger in the 1980s. They consist of a simple moving average (SMA) and two standard deviation lines, one above and one below the SMA. The distance between the SMA and the standard deviation lines shows the volatility of the stock.

The code calculates the upper and lower Bollinger Bands and the moving average. A Plotly chart is then created displaying the stock's prices and the Bollinger Bands.

# Stochastic Oscillator

The Stochastic Oscillator is a momentum indicator that uses support and resistance levels. It compares a particular closing price of a security to a range of its prices over a certain period of time.

The code calculates the Stochastic Oscillator and creates a new column in the stock data to indicate the condition of the stock: oversold, overbought, or normal. A Plotly chart is then created displaying the stock's prices and the Stochastic Oscillator.

# Data Extraction

The code uses the `yfinance` library to download stock data from Yahoo Finance. It defines the stock ticker symbol, specifies the date range, and downloads the data. The stock data includes opening, high, low, closing, adjusted closing prices, and the volume of the stock.

The downloaded data is used to create a candlestick chart using the `plotly.graph_objs` library, which visualizes the stock's price movement within a specified period. The chart includes a line plot of the closing prices.

```python

```
