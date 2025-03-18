import numpy as np
from scipy.signal import argrelextrema
from sklearn.linear_model import LinearRegression

# Function to identify support and resistance
def find_support_resistance(df, order=5):
    df = df.copy()
    df['max'] = np.nan
    df['min'] = np.nan

    if not df.empty:
        max_idx = argrelextrema(df['High'].values, np.greater, order=order)[0]
        min_idx = argrelextrema(df['Low'].values, np.less, order=order)[0]
        df.loc[max_idx, 'max'] = df.loc[max_idx, 'High']
        df.loc[min_idx, 'min'] = df.loc[min_idx, 'Low']

    return df

# Function to detect trendlines
def calculate_trendline(df):
    df = df.dropna().copy()
    if df.shape[0] < 2:
        df['Trendline'] = np.nan
        return df

    X = np.array(range(len(df))).reshape(-1, 1)
    y = df['Close'].values

    try:
        model = LinearRegression()
        model.fit(X, y)
        df['Trendline'] = model.predict(X)
    except Exception:
        df['Trendline'] = np.nan

    return df

# Function to detect breakouts
def detect_breakouts(df):
    df['Breakout_Up'] = (df['Close'] > df['max'].shift(1))
    df['Breakout_Down'] = (df['Close'] < df['min'].shift(1))
    return df