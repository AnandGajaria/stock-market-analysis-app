# Stock Market Analysis App 📈

A **Streamlit web application** for exploring stock market data through company analysis, price charts, stock forecasting, risk comparison, and CAPM-based return estimation.

This project was developed to make stock market data easier to understand. The app focuses on clean visualizations, simple explanations, and an interactive user experience.

---

## Project Overview

The Stock Market Analysis App allows users to:

- Select companies from dropdown menus instead of manually typing tickers
- Choose custom start and end dates for analysis
- View historical stock prices and visual trends
- Analyze stock movement using charts and technical indicators
- Generate a simple short-term stock price forecast
- Compare stock risk against the S&P 500
- Estimate expected return using CAPM concepts

The application uses live market data from **Yahoo Finance** through the `yfinance` library.

---

## Features

### 1. Home Page

The landing page introduces the app, explains its purpose, and guides users through the recommended workflow.

Recommended flow:

1. Stock Analysis
2. Stock Prediction
3. Stock Risk
4. CAPM Return

---

### 2. Stock Analysis

This section helps users understand a selected company and its stock performance.

Key features:

- Company selection using a dropdown menu
- Custom start date and end date selection
- Analysis appears only after clicking the analysis button
- Latest close price and daily change
- Historical price table
- Line chart and candlestick chart
- Moving average, RSI, and MACD indicators
- Cleaned table column names for better readability

---

### 3. Stock Prediction

This section provides a simple 30-day stock price forecast.

Key features:

- Fetches historical closing prices
- Applies rolling mean smoothing
- Uses ARIMA-based forecasting
- Displays forecasted prices for the next 30 days
- Shows forecast chart

The prediction feature is intended for learning and trend exploration only. It should not be treated as financial advice.

---

### 4. Stock Risk / CAPM Beta

This section explains stock risk in a beginner-friendly way.

Instead of showing too many technical finance metrics, it focuses on:

- Beta value
- Risk level
- Simple explanation of whether the stock is less risky, similar to, or more risky than the market
- A visual comparison of the selected stock against the S&P 500

This makes the page easier to understand for users without a finance background.

---

### 5. CAPM Return

This section estimates expected return using the Capital Asset Pricing Model.

Key features:

- Select multiple stocks
- Compare stock performance with the S&P 500
- Calculate beta values
- Estimate expected return
- Display results in tables and charts

This section is more finance-oriented and is useful for users who want to explore market-based return estimation.

---

## Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **NumPy**
- **Yahoo Finance / yfinance**
- **Plotly**
- **Statsmodels**
- **Scikit-learn**
- **TA library**

---

## Project Structure

```text
Time-Series-Analysis-main/
│
├── Trading_App.py
├── requirements.txt
├── setup.py
├── app.png
│
├── pages/
│   ├── Stock_Analysis.py
│   ├── Stock_Prediction.py
│   ├── Stock_Risk.py
│   ├── CAPM_Return.py
│   │
│   └── utils/
│       ├── capm_functions.py
│       ├── model_train.py
│       └── plotly_figure.py
│
└── README.md
```

Depending on your final file names, `Stock_Risk.py` may still be named `CAPM_Beta.py`.

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/stock-market-analysis-app.git
cd stock-market-analysis-app
```

---

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

### 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

### 4. Install dependencies

You can install dependencies using:

```bash
python -m pip install -e .
```

---

### 5. Run the Streamlit app

```bash
python -m streamlit run Trading_App.py
```

The app will open in your browser at:

```text
http://localhost:8501
```

---

## Example Usage

1. Open the app using Streamlit.
2. Start from the home page.
3. Go to **Stock Analysis**.
4. Select a company from the dropdown.
5. Choose a start date and end date.
6. Click the analysis button.
7. View price charts, company information, and technical indicators.
8. Move to **Stock Prediction** to view a simple forecast.
9. Use **Stock Risk** to understand how risky the stock is compared with the market.


---

## What I Learned

This project helped me practice:

- Building multipage Streamlit applications
- Working with real-time financial data
- Cleaning and transforming stock price data
- Creating interactive Plotly visualizations
- Handling data errors and missing API responses
- Structuring a Python project
- Using Git and GitHub for version control
- Improving user experience for non-technical users

---

## Future Improvements

Possible future enhancements include:

- Add more forecasting models such as Prophet, LSTM, or XGBoost
- Add database support for storing downloaded stock data
- Add Apache Airflow for scheduled data updates
- Add comparison charts for multiple companies
- Add downloadable reports

---

## Disclaimer

This application is built for **educational and analytical purposes only**.

It does **not** provide financial advice, investment recommendations, or guaranteed predictions. Stock market investments involve risk, and users should do their own research or consult a qualified financial advisor before making investment decisions.

---

## Author

**Anand Gajaria**

Project: Stock Market Analysis App
