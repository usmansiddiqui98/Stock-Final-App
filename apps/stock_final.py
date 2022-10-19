import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime
from datetime import date
import streamlit as st
import plotly.graph_objects as go

# In[6]:
def app():
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


## Enter Ticker
    col1, col2 , col3 = st.columns(3)


    ticker = col1.text_input("Insert Ticker","AMZN")

    start_date= col2.date_input("Enter Start date", datetime.date(2021,1,1))
    end_date= col3.date_input("Enter End date", date.today())


    try:
        @st.cache()
        def get_stock(ticker, start_date , end_date):
            stock = yf.download(ticker,start =start_date,end=end_date)
            return stock

        @st.cache()
        def get_benchmark(start_date , end_date):
            benchmark = yf.download("SPY",start =start_date,end=end_date)
            return benchmark

        @st.cache(allow_output_mutation=True)
        def get_info(ticker):
            stockinfo = yf.Ticker(ticker)
            return stockinfo

        stock = get_stock(ticker, start_date , end_date)
        benchmark = get_benchmark(start_date , end_date)
        stock_info = get_info(ticker)
        info = stock_info.info['longBusinessSummary']
        #info = get_info(ticker).info['longBusinessSummary']

        company_name = stock_info.info["longName"]
        st.header(company_name)
        if st.button("About"):
            st.write(info)



    # View the dataset
        st.subheader("The Stock Information")
        st.write("The Open price is the first price traded in a given time period and the last price traded is the Close Price. The High and Low can happen any time in-between these two extremes.")
        st.write("OHLC for the past 5 days") 
        st.dataframe(stock.tail(5).sort_index(ascending=False))


        @st.experimental_memo
        def convert_df(df):
            return df.to_csv().encode('utf-8')


        csv = convert_df(stock.tail(5).sort_index(ascending=False))

        st.download_button(
    "Press to Download",
    csv,
    "file.csv",
    "text/csv",
    key='download-csv'
    )



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

    st.subheader("Candle Stick Chart for " + str(ticker))
    st.write("""
        Candlestick charts are a technical tool that packs data for multiple time 
        frames into single price bars. 
        This makes them more useful than traditional open-high, low-close bars or simple lines that connect the dots of closing prices. 
        Candlesticks build patterns that predict price direction once completed.
        """)

    fig1 = go.Figure(data = go.Candlestick(x = pd.date_range(start = start_date , end = end_date), 
    open = stock["Open"] , high = stock["High"],
    low = stock["Low"], close = stock["Close"]))
    st.plotly_chart(fig1)

    form = st.form(key = 'my-form')
    ## The cumulative returns of a stock
    t1 = form.text_input("Choose the first ticker" , "")
    t2 = form.text_input("Choose the second ticker" , "")
    ticker_lst = [t1,t2]
    def relativeret(df):
        rel = df.pct_change()
        cumret = (1+rel).cumprod() - 1
        cumret = cumret.fillna(0)
        return cumret


    submit = form.form_submit_button("Submit to compare")
    if submit:
        df = relativeret(yf.download(ticker_lst,start_date,end_date)['Adj Close'])
        st.subheader("Cumulative returns of the Closing Price for " + str(t1) + " and " + str(t2))
        st.line_chart(df) 



    st.markdown("""---""")


## To-do
## 1. All plotly 
## 2. Cache more functions using experimental memo (done)
## 3. add args to fetch and clean be start date and end date (all inputs) (done)
## 4. st.form (done)
## 5. Multiple pages to present mini apps (done)
## 6. Design changes: navigation on the sidebar (done)
## 7. add start, end date and ticker in the same row using st.columms (done)
