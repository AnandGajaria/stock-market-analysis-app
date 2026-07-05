import plotly.express as px
import numpy as np


# Function to plot interactive plot
def interactive_plot(df):
    fig = px.line()
    for i in df.columns[1:]:
         fig.add_scatter(x = df['Date'],y = df[i], name = i)
    fig.update_layout(width = 450,margin=dict(l=20, r=20, t=50, b=20),legend=dict(orientation="h",yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1))
    return fig

# Function to normalize the prices based on the initial price
def normalize(df):
    x = df.copy()

    numeric_columns = x.select_dtypes(include=[np.number]).columns
    x[numeric_columns] = x[numeric_columns] / x[numeric_columns].iloc[0]

    return x


def daily_return(df):
    df_daily_return = df.copy()

    numeric_columns = df_daily_return.select_dtypes(include=[np.number]).columns

    df_daily_return[numeric_columns] = (
        df_daily_return[numeric_columns]
        .pct_change()
        .fillna(0)
        * 100
    )

    return df_daily_return


def calculate_beta(stocks_daily_return, stock):
    clean_df = stocks_daily_return[['sp500', stock]].dropna()

    clean_df = clean_df[
        (clean_df['sp500'] != 0) &
        (clean_df[stock] != 0)
    ]

    if clean_df.empty:
        return 0, 0

    b, a = np.polyfit(clean_df['sp500'], clean_df[stock], 1)
    return b, a
