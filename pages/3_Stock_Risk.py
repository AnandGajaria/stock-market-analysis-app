import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import datetime


st.set_page_config(
    page_title="Stock Risk",
    page_icon="📈",
    layout="wide",
)

st.title("Stock Risk Compared With Market 📈")

st.write(
    "This page compares a stock with the S&P 500 market index and shows whether "
    "the stock usually moves more or less than the market."
)


STOCK_OPTIONS = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Tesla": "TSLA",
    "Netflix": "NFLX",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Alphabet / Google": "GOOGL",
    "Meta": "META",
    "JPMorgan Chase": "JPM",
    "Coca-Cola": "KO",
    "Walmart": "WMT",
    "Disney": "DIS",
    "Nike": "NKE",
    "Intel": "INTC",
    "AMD": "AMD",
}


def get_close_prices(stock, start_date, end_date):
    tickers = [stock, "^GSPC"]

    download_end_date = pd.to_datetime(end_date) + pd.Timedelta(days=1)

    data = yf.download(
        tickers,
        start=start_date,
        end=download_end_date,
        progress=False,
        auto_adjust=False,
    )

    if data.empty:
        return pd.DataFrame()

    if isinstance(data.columns, pd.MultiIndex):
        close_df = data["Close"].copy()
    else:
        close_df = data[["Close"]].copy()

    close_df.rename(columns={"^GSPC": "S&P 500"}, inplace=True)
    close_df.rename(columns={stock: "Selected Stock"}, inplace=True)

    required_columns = ["Selected Stock", "S&P 500"]

    if not all(col in close_df.columns for col in required_columns):
        return pd.DataFrame()

    close_df = close_df[required_columns]
    close_df.dropna(inplace=True)

    return close_df


def calculate_beta(price_df):
    returns_df = price_df.pct_change().dropna()

    if len(returns_df) < 30:
        return None

    stock_returns = returns_df["Selected Stock"]
    market_returns = returns_df["S&P 500"]

    if market_returns.var() == 0:
        return None

    beta = stock_returns.cov(market_returns) / market_returns.var()

    return beta


def beta_meaning(beta):
    if beta < 0:
        return "This stock usually moves in the opposite direction of the market."

    if beta < 0.8:
        return "This stock is usually less volatile than the market."

    if beta <= 1.2:
        return "This stock usually moves similarly to the market."

    return "This stock is usually more volatile than the market."


def beta_badge(beta):
    if beta < 0.8:
        return "Lower Risk"
    elif beta <= 1.2:
        return "Market-like Risk"
    else:
        return "Higher Risk"


def make_normalized_chart(price_df, selected_company):
    normalized_df = price_df / price_df.iloc[0]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=normalized_df.index,
            y=normalized_df["Selected Stock"],
            mode="lines",
            name=selected_company,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=normalized_df.index,
            y=normalized_df["S&P 500"],
            mode="lines",
            name="S&P 500",
        )
    )

    fig.update_layout(
        title=f"{selected_company} vs S&P 500",
        height=450,
        xaxis_title="Date",
        yaxis_title="Growth from start date",
        plot_bgcolor="white",
        paper_bgcolor="#e1efff",
    )

    return fig


today = datetime.date.today()
default_start = datetime.date(today.year - 1, today.month, today.day)

col1, col2, col3 = st.columns(3)

with col1:
    selected_company = st.selectbox(
        "Select Company",
        list(STOCK_OPTIONS.keys())
    )

with col2:
    start_date = st.date_input(
        "Start Date",
        default_start
    )

with col3:
    end_date = st.date_input(
        "End Date",
        today
    )


if st.button("Analyze Risk"):
    if start_date >= end_date:
        st.error("Start date must be before end date.")
        st.stop()

    stock = STOCK_OPTIONS[selected_company]

    price_df = get_close_prices(stock, start_date, end_date)

    if price_df.empty:
        st.error("No data found. Try another company or date range.")
        st.stop()

    beta = calculate_beta(price_df)

    if beta is None:
        st.error("Not enough data found. Try selecting a longer date range.")
        st.stop()

    st.subheader(f"{selected_company} Risk Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Beta", f"{beta:.2f}")

    with col2:
        st.metric("Risk Level", beta_badge(beta))

    st.info(beta_meaning(beta))

    st.markdown("### Price Comparison")

    st.write(
        "This chart shows how the selected stock performed compared with the S&P 500. "
        "Both lines start at the same point, so it is easier to compare them."
    )

    st.plotly_chart(
        make_normalized_chart(price_df, selected_company),
        use_container_width=True
    )

else:
    st.info("Select a company and date range, then click Analyze Risk.")