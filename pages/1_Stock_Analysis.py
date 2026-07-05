import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime

from ta.momentum import RSIIndicator
from ta.trend import MACD as MACDIndicator, SMAIndicator
from pages.utils.plotly_figure import plotly_table


st.set_page_config(
    page_title="Stock Analysis",
    page_icon="📄",
    layout="wide",
)

st.title("Stock Analysis")


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


def clean_yfinance_data(data, ticker):
    if isinstance(data.columns, pd.MultiIndex):
        if ticker.upper() in data.columns.get_level_values(-1):
            data = data.xs(ticker.upper(), axis=1, level=-1)
        else:
            data.columns = data.columns.get_level_values(0)

    required_columns = ["Open", "High", "Low", "Close", "Volume"]
    data = data[[col for col in required_columns if col in data.columns]]
    data = data.dropna()

    return data


def safe_value(info, key, default="N/A"):
    value = info.get(key, default)
    if value is None:
        return default
    return value


def format_large_number(value):
    if value == "N/A" or value is None:
        return "N/A"

    try:
        value = float(value)

        if value >= 1_000_000_000_000:
            return f"${value / 1_000_000_000_000:.2f}T"
        elif value >= 1_000_000_000:
            return f"${value / 1_000_000_000:.2f}B"
        elif value >= 1_000_000:
            return f"${value / 1_000_000:.2f}M"
        else:
            return f"${value:,.2f}"
    except:
        return value


def make_price_chart(data, ticker, chart_type):
    fig = go.Figure()

    if chart_type == "Candlestick":
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name=ticker,
            )
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                mode="lines",
                name="Close Price",
            )
        )

    fig.update_layout(
        title=f"{ticker} Price Chart",
        height=500,
        margin=dict(l=0, r=20, t=50, b=0),
        plot_bgcolor="white",
        paper_bgcolor="#e1efff",
        xaxis_title="Date",
        yaxis_title="Price",
    )

    fig.update_xaxes(rangeslider_visible=True)

    return fig


def make_moving_average_chart(data, ticker):
    chart_data = data.copy()
    chart_data["SMA 20"] = SMAIndicator(
        close=chart_data["Close"],
        window=20
    ).sma_indicator()

    chart_data["SMA 50"] = SMAIndicator(
        close=chart_data["Close"],
        window=50
    ).sma_indicator()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_data.index,
            y=chart_data["Close"],
            mode="lines",
            name="Close Price",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=chart_data.index,
            y=chart_data["SMA 20"],
            mode="lines",
            name="SMA 20",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=chart_data.index,
            y=chart_data["SMA 50"],
            mode="lines",
            name="SMA 50",
        )
    )

    fig.update_layout(
        title=f"{ticker} Moving Average",
        height=500,
        margin=dict(l=0, r=20, t=50, b=0),
        plot_bgcolor="white",
        paper_bgcolor="#e1efff",
        xaxis_title="Date",
        yaxis_title="Price",
    )

    fig.update_xaxes(rangeslider_visible=True)

    return fig


def make_rsi_chart(data):
    chart_data = data.copy()

    chart_data["RSI"] = RSIIndicator(
        close=chart_data["Close"],
        window=14
    ).rsi()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_data.index,
            y=chart_data["RSI"],
            mode="lines",
            name="RSI",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=chart_data.index,
            y=[70] * len(chart_data),
            mode="lines",
            name="Overbought",
            line=dict(dash="dash"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=chart_data.index,
            y=[30] * len(chart_data),
            mode="lines",
            name="Oversold",
            line=dict(dash="dash"),
        )
    )

    fig.update_layout(
        title="RSI Indicator",
        height=250,
        margin=dict(l=0, r=20, t=50, b=0),
        plot_bgcolor="white",
        paper_bgcolor="#e1efff",
        yaxis_range=[0, 100],
        xaxis_title="Date",
        yaxis_title="RSI",
    )

    return fig


def make_macd_chart(data):
    chart_data = data.copy()

    macd_indicator = MACDIndicator(close=chart_data["Close"])

    chart_data["MACD"] = macd_indicator.macd()
    chart_data["MACD Signal"] = macd_indicator.macd_signal()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_data.index,
            y=chart_data["MACD"],
            mode="lines",
            name="MACD",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=chart_data.index,
            y=chart_data["MACD Signal"],
            mode="lines",
            name="MACD Signal",
        )
    )

    fig.update_layout(
        title="MACD Indicator",
        height=250,
        margin=dict(l=0, r=20, t=50, b=0),
        plot_bgcolor="white",
        paper_bgcolor="#e1efff",
        xaxis_title="Date",
        yaxis_title="MACD",
    )

    return fig


today = datetime.date.today()

col1, col2, col3 = st.columns(3)

with col1:
    selected_company = st.selectbox(
        "Select Company",
        list(STOCK_OPTIONS.keys())
    )

with col2:
    start_date = st.date_input(
        "Start Date",
        datetime.date(today.year - 1, today.month, today.day)
    )

with col3:
    end_date = st.date_input(
        "End Date",
        today
    )


if "show_stock_analysis" not in st.session_state:
    st.session_state.show_stock_analysis = False

if st.button("Analyze Stock"):
    if start_date >= end_date:
        st.error("Start date must be before end date.")
        st.session_state.show_stock_analysis = False
    else:
        st.session_state.show_stock_analysis = True
        st.session_state.selected_company = selected_company
        st.session_state.selected_ticker = STOCK_OPTIONS[selected_company]
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date


if not st.session_state.show_stock_analysis:
    st.info("Select a company, choose a start date and end date, then click Analyze Stock.")
    st.stop()


selected_company = st.session_state.selected_company
ticker = st.session_state.selected_ticker
start_date = st.session_state.start_date
end_date = st.session_state.end_date

st.subheader(f"{selected_company} ({ticker})")

stock = yf.Ticker(ticker)
info = stock.info

summary = info.get(
    "longBusinessSummary",
    "No business summary available for this company."
)

st.write(summary)

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Sector:**", safe_value(info, "sector"))

with col2:
    st.write("**Full Time Employees:**", safe_value(info, "fullTimeEmployees"))

with col3:
    st.write("**Website:**", safe_value(info, "website"))


col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame(
        index=["Market Cap", "Beta", "EPS", "PE Ratio"]
    )

    df["Value"] = [
        format_large_number(safe_value(info, "marketCap")),
        safe_value(info, "beta"),
        safe_value(info, "trailingEps"),
        safe_value(info, "trailingPE"),
    ]

    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

with col2:
    df = pd.DataFrame(
        index=[
            "Quick Ratio",
            "Revenue Per Share",
            "Profit Margins",
            "Debt To Equity",
            "Return On Equity",
        ]
    )

    df["Value"] = [
        safe_value(info, "quickRatio"),
        safe_value(info, "revenuePerShare"),
        safe_value(info, "profitMargins"),
        safe_value(info, "debtToEquity"),
        safe_value(info, "returnOnEquity"),
    ]

    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)


download_end_date = pd.to_datetime(end_date) + pd.Timedelta(days=1)

data = yf.download(
    ticker,
    start=start_date,
    end=download_end_date,
    progress=False,
    auto_adjust=False,
)

data = clean_yfinance_data(data, ticker)

if len(data) < 2:
    st.error("Not enough data found for the selected company and date range.")
    st.stop()


latest_close = float(data["Close"].iloc[-1])
previous_close = float(data["Close"].iloc[-2])
daily_change = latest_close - previous_close
daily_change_pct = (daily_change / previous_close) * 100

range_start_price = float(data["Close"].iloc[0])
range_return_pct = ((latest_close - range_start_price) / range_start_price) * 100

col1, col2, col3 = st.columns(3)

col1.metric(
    "Latest Close",
    f"${latest_close:,.2f}",
    f"{daily_change:.2f} ({daily_change_pct:.2f}%)"
)

col2.metric(
    "Range Return",
    f"{range_return_pct:.2f}%"
)

col3.metric(
    "Trading Days",
    len(data)
)


display_data = data.copy()
display_data.index = pd.to_datetime(display_data.index).strftime("%Y-%m-%d")

st.write("##### Historical Data For Selected Range")

fig_tail = plotly_table(
    display_data.tail(10).sort_index(ascending=False).round(2)
)

fig_tail.update_layout(height=260)
st.plotly_chart(fig_tail, use_container_width=True)


st.markdown(
    """<hr style="height:2px;border:none;color:#0078ff;background-color:#0078ff;" /> """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    chart_type = st.selectbox(
        "Chart Type",
        ["Line", "Candlestick"]
    )

with col2:
    indicator = st.selectbox(
        "Indicator",
        ["None", "Moving Average", "RSI", "MACD"]
    )


if indicator == "Moving Average":
    st.plotly_chart(
        make_moving_average_chart(data, ticker),
        use_container_width=True
    )
else:
    st.plotly_chart(
        make_price_chart(data, ticker, chart_type),
        use_container_width=True
    )

    if indicator == "RSI":
        st.plotly_chart(
            make_rsi_chart(data),
            use_container_width=True
        )

    elif indicator == "MACD":
        st.plotly_chart(
            make_macd_chart(data),
            use_container_width=True
        )