import streamlit as st


st.set_page_config(
    page_title="Stock Market Analysis App",
    page_icon="📈",
    layout="wide",
)

st.title("Stock Market Analysis App 📈")

st.markdown(
    """
    Welcome to the **Stock Market Analysis App**.

    This app helps you explore stock market data in a simple and visual way. 
    You can view company information, analyze historical stock prices, compare stocks with the market, 
    and generate basic price forecasts.

    The goal of this app is to make stock data easier to understand, especially for users who are new to finance or investing.
    """
)

st.warning(
    "Note: This app is for learning and analysis purposes only. It does not provide financial or investment advice."
)

st.image("app.png", use_column_width=True)

st.markdown(
    """<hr style="height:2px;border:none;color:#0078ff;background-color:#0078ff;" />""",
    unsafe_allow_html=True
)

st.markdown("## What You Can Do With This App")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 1. Stock Analysis")
    st.write(
        """
        Select a company and date range to view its historical stock performance.
        You can see recent prices, price movement, basic company information, and simple charts.
        """
    )

    st.markdown("### 2. Stock Prediction")
    st.write(
        """
        Generate a simple 30-day stock price forecast using historical price data.
        This feature is useful for understanding possible future trends, but it should not be treated as a guaranteed prediction.
        """
    )

with col2:

    st.markdown("### 3. Stock Risk / CAPM Beta")
    st.write(
        """
        Understand whether a stock is usually more risky, less risky, or similar to the market.
        The result is shown in a simple way so users without a finance background can understand it easily.
        """
    )

    st.markdown("### 4. CAPM Return")
    st.write(
        """
        Compare selected stocks with the overall market and estimate expected return.
        This section gives a basic idea of how a stock may perform compared with market movement.
        """
    )

st.markdown(
    """<hr style="height:2px;border:none;color:#0078ff;background-color:#0078ff;" />""",
    unsafe_allow_html=True
)

st.markdown("## How To Use The App")

st.write(
    """
    Use the sidebar on the left to open any section of the app.

    A good starting point is **Stock Analysis**, where you can select a company, choose a start date and end date, 
    and view the stock's performance for that selected period.
    """
)

st.markdown("## Recommended Flow")

st.write(
    """
    1. Start with **Stock Analysis** to understand the company and its price history.  
    2. Use **Stock Prediction** to view a simple forecast.  
    3. Use **Stock Risk / CAPM Beta** to understand how risky the stock is compared with the market.  
    4. Use **CAPM Return** only if you want to explore expected return calculations.
    """
)