import yfinance as yf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import pandas as pd


def get_data(ticker):
    ticker = ticker.strip().upper()

    stock_data = yf.download(
        ticker,
        start="2024-01-01",
        progress=False,
        auto_adjust=False
    )

    if stock_data.empty:
        raise ValueError(f"No data found for ticker: {ticker}")

    # Handle newer yfinance MultiIndex columns
    if isinstance(stock_data.columns, pd.MultiIndex):
        if "Close" in stock_data.columns.get_level_values(0):
            close_price = stock_data["Close"]
        else:
            close_price = stock_data.xs("Close", axis=1, level=-1)
    else:
        close_price = stock_data["Close"]

    # Convert to one clean Close column
    if isinstance(close_price, pd.DataFrame):
        close_price = close_price.iloc[:, 0]

    close_price = pd.to_numeric(close_price, errors="coerce").dropna()

    if len(close_price) < 100:
        raise ValueError("Not enough stock price data for prediction.")

    return pd.DataFrame({"Close": close_price})


def stationary_check(close_price):
    series = pd.Series(np.asarray(close_price).ravel()).dropna()

    if len(series) < 20:
        return 0

    adf_test = adfuller(series)
    p_value = round(adf_test[1], 3)

    return p_value


def get_rolling_mean(close_price):
    rolling_price = close_price[["Close"]].rolling(window=7).mean().dropna()
    return rolling_price


def get_differencing_order(close_price):
    p_value = stationary_check(close_price)

    d = 0

    while p_value > 0.05 and d < 2:
        d += 1
        close_price = close_price.diff().dropna()
        p_value = stationary_check(close_price)

    return d


def fit_model(data, differencing_order):
    series = pd.Series(np.asarray(data).ravel()).dropna()

    # Smaller ARIMA order is much more stable than (30, d, 30)
    model = ARIMA(series, order=(5, differencing_order, 5))
    model_fit = model.fit()

    predictions = model_fit.forecast(steps=30)

    return np.asarray(predictions).ravel()


def evaluate_model(original_price, differencing_order):
    series = pd.Series(np.asarray(original_price).ravel()).dropna()

    train_data = series[:-30]
    test_data = series[-30:]

    predictions = fit_model(train_data, differencing_order)

    rmse = np.sqrt(mean_squared_error(test_data, predictions))

    return round(rmse, 2)


def scaling(close_price):
    scaler = StandardScaler()

    values = np.asarray(close_price["Close"]).reshape(-1, 1)
    scaled_data = scaler.fit_transform(values)

    return scaled_data, scaler


def get_forecast(original_price, differencing_order):
    predictions = fit_model(original_price, differencing_order)

    start_date = datetime.now() + timedelta(days=1)
    forecast_index = pd.date_range(start=start_date, periods=30, freq="D")

    forecast_df = pd.DataFrame(
        {"Close": predictions},
        index=forecast_index
    )

    return forecast_df


def inverse_scaling(scaler, scaled_data):
    close_price = scaler.inverse_transform(
        np.asarray(scaled_data).reshape(-1, 1)
    )

    return close_price.ravel()