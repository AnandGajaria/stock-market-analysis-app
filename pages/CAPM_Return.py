# importing libraries
import streamlit as st
import pandas_datareader.data as web
import datetime
import pandas as pd
import yfinance as yf
from pages.utils import capm_functions

# setting page config
st.set_page_config(

        page_title="Calculate Beta",
        page_icon="chart_with_upwards_trend",
        layout="wide",
    )

st.title('Capital Asset Pricing Model 📈')

# getting input from user
col1, col2= st.columns([1,1])
with col1:
    stocks_list = st.multiselect("Choose 4 Stocks" , ('TSLA', 'AAPL','NFLX','MGM','MSFT','AMZN','NVDA','GOOGL'),['TSLA', 'AAPL','MSFT','NFLX'], key = "stock_list",)
with col2:
    year = st.number_input("Number of Years",1,10)

try:
    tickers = list(stocks_list) + ['^GSPC']

    data = yf.download(
        tickers,
        period=f'{int(year)}y',
        progress=False,
        auto_adjust=False
    )

    if data.empty:
        st.error("No data downloaded. Check your internet connection or try again later.")
        st.stop()

    # Get closing prices
    if isinstance(data.columns, pd.MultiIndex):
        stocks_df = data['Close'].copy()
    else:
        stocks_df = data[['Close']].copy()

    stocks_df.rename(columns={'^GSPC': 'sp500'}, inplace=True)

    required_columns = list(stocks_list) + ['sp500']
    missing_columns = [col for col in required_columns if col not in stocks_df.columns]

    if missing_columns:
        st.error(f"Missing data for: {missing_columns}")
        st.stop()

    stocks_df = stocks_df[required_columns]
    stocks_df.dropna(inplace=True)
    stocks_df.reset_index(inplace=True)

    if stocks_df.empty:
        st.error("Downloaded data is empty after cleaning. Try a longer year range.")
        st.stop()

    col1, col2 = st.columns([1, 1])
    company_names = {
        "TSLA": "Tesla",
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "NFLX": "Netflix",
        "NVDA": "NVIDIA",
        "AMZN": "Amazon",
        "GOOGL": "Alphabet",
        "META": "Meta",
        "sp500": "S&P 500"
    }

    display_df = stocks_df.copy()

    # Format date nicely
    display_df["Date"] = pd.to_datetime(display_df["Date"]).dt.strftime("%Y-%m-%d")

    # Rename columns only for display
    display_df.rename(columns=company_names, inplace=True)

    with col1:
        st.markdown('### Dataframe head')
        st.dataframe(display_df.head())

    with col2:
        st.markdown('### Dataframe tail')
        st.dataframe(display_df.tail())

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('### Price of all the Stocks')
        st.plotly_chart(capm_functions.interactive_plot(stocks_df))

    with col2:
        st.markdown('### Price of all the Stocks After Normalizing')
        st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)))

    stocks_daily_return = capm_functions.daily_return(stocks_df)

    beta = {}
    alpha = {}

    for stock in stocks_list:
        b, a = capm_functions.calculate_beta(stocks_daily_return, stock)
        beta[stock] = b
        alpha[stock] = a

    col1, col2 = st.columns([1, 1])

    beta_df = pd.DataFrame({
        'Stock': list(beta.keys()),
        'Beta Value': [round(i, 2) for i in beta.values()]
    })

    with col1:
        st.markdown('### Calculated Beta Value')
        st.dataframe(beta_df)

    rf = 0
    rm = stocks_daily_return['sp500'].mean() * 252

    return_df = pd.DataFrame({
        'Stock': list(beta.keys()),
        'Return Value': [round(rf + value * (rm - rf), 2) for value in beta.values()]
    })

    with col2:
        st.markdown('### Calculated Return using CAPM')
        st.dataframe(return_df)

except Exception as e:
    st.error("Something went wrong.")
    st.exception(e)
