
# In[109]:
import numpy as np
import pandas as pd
import html5lib
import bs4
import seaborn as sns
import matplotlib.pyplot as plt
from yahoofinancials import YahooFinancials
import yfinance as yf
import scipy.stats as stats
import datetime
from datetime import date
import streamlit as st
from PIL import Image
# In[6]:
st.write("""
## *Bearish or Bullish*?
""")
st.write("""
This web app analyzes the risk and returns of any stock in the yahoo finance DB. 
It visually analyze the time plot of the **stock**
,the **volatility** and a **graphical description** of the daily return for that particular stock

Database: Yahoo Finance
""")
plt.style.use("bmh")

## Loading dataset

## Enter Ticker
st.sidebar.subheader("Company")
ticker = st.sidebar.text_input("Ticker","AMZN")

## Select Period
st.sidebar.subheader(" Period")
st.sidebar.write("Enter Start and End Date")
start_date= st.sidebar.date_input("Start date", datetime.date(2021,1,1))
end_date= st.sidebar.date_input("End date", date.today())
### Try to cache company information with arg to fn being the ticker

#def dl_fin(ticker,about,date):
# make 2 fucntions
## 1st fn for the ticker info
## 2nd fn would be for date related info
## Cache both separately 
## catch error in the cache 
## have a different return value to make it known in the main fn
## Try with plotly...cumulative returns 
## Add a download button for the df would be as a csv (st.download())
## Add cumulative returns against a benchmark
## st.mulitple_select??

## Loading dataset
try:
    stock = yf.download(ticker,start =start_date,end=end_date)
    stockinfo = yf.Ticker(ticker)

    share = YahooFinancials('AAPL')

    # Benchmark index is S&P 500
    benchmark = yf.download("SPY",start =start_date,end=end_date)

    ## Company _Name
    company_name =stockinfo.info["longName"]
    st.header(company_name)
    if st.button("About"):
        info = stockinfo.info['longBusinessSummary']
        st.write(info)

    # View the dataset
    st.subheader("The Stock Information")
    st.write("The Open price is the first price traded in a given time period and the last price traded is the Close Price. The High and Low can happen any time in-between these two extremes.")
    st.write("OHLC for the past 5 days") 
    st.dataframe(stock.tail(5).sort_index(ascending=False))


    ### Time plot
    st.subheader("Time plot")
    st.write(" A display of closing stock price over a given time period")
                
    st.line_chart(stock["Close"])

    ## volatility clustering plot
    st.subheader(" Daily returns of the Closing Price")
    st.write("The price return is the rate of return on an investment portfolio, where the return measure takes into account only the capital appreciation of the portfolio, while the income generated by the assets in the portfolio, in the form of interest and dividends, is ignored.") 
    returns = stock['Close'].pct_change().dropna()
    st.line_chart(returns)

    st.subheader("Descriptive Summary of the daily returns ")
    summ_return =pd.DataFrame({"Minimum":returns.min(),"Maximum":returns.max(),"Average":returns.mean(),"Variance":returns.var(),
                               "Kurtosis":returns.kurtosis(),"Skewness": returns.skew(),"Volatility(%)":(returns.std()*100)},index=["Value"])

    st.dataframe(summ_return)
    # Benchmark retuns
    benchmark_returns = benchmark["Close"].pct_change().dropna()
    
    ## The Density Distribution of Daily Returns
    fig, ax = plt.subplots(figsize=(8,3))
    plt.title("Histogram of returns")
    plt.xlabel("daily returns")
    plt.ylabel("Frequncy")
    ax.hist(returns, bins =100,histtype='stepfilled')
    st.pyplot(fig)
    
except:
    st.write("""
             The ticker you entered is invalid.

             If valid, Consider Using a more recent start date for the Ticker you are trying to Analyze(e.g 2019/01/01) to View the Beta, Value at Risk and Alpha Value of the stock.
             """)    