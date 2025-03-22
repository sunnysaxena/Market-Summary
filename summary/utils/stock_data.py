import time
from datetime import datetime

import pandas as pd
import yfinance as yf
from trade_utils import feature_extraction as fe


def check_expiry_day(df, symbol, date_column="Date"):
    """
    Add a column 'Expiry' to check if the given date is a Thursday (Expiry Day).

    Parameters:
        df (pd.DataFrame): Input DataFrame with a date column.
        date_column (str): Name of the column containing dates.

    Returns:
        pd.DataFrame: DataFrame with an additional 'Expiry' column (True/False).
    """
    df[date_column] = pd.to_datetime(df[date_column])  # Ensure date format
    if symbol == '^NSEI':
        df["Expiry"] = df[date_column].dt.day_name() == "Thursday"  # Check for Thursday
    elif symbol == '^BSESN':
        df["Expiry"] = df[date_column].dt.day_name() == "Tuesday"  # Check for Thursday
    else:
        df["Expiry"] = 'Monthly Expiry'

    return df


def get_stock_data(symbol: str, start_date, end_date) -> pd.DataFrame:
    """
    Fetch stock data from Yahoo Finance
    """
    try:
        # Convert date objects to datetime if they aren't already
        if not isinstance(start_date, datetime):
            start_date = datetime.combine(start_date, datetime.min.time())
        if not isinstance(end_date, datetime):
            end_date = datetime.combine(end_date, datetime.min.time())

        time.sleep(2)
        stock = yf.Ticker(symbol)
        df = stock.history(start=start_date, end=end_date)

        # Round values to 2 decimal places
        df = df.round(2)

        # Reset index to make Date a column
        df = df.reset_index()

        # Format date column
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        # df['Date'] = df['Date'].astype(str)  # Ensure Date is in string format

        # Renaming columns
        df.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
        }, inplace=True)

        # apply trend classification
        df['Trend'] = df.apply(lambda row: fe.classify_trend_v2(row, df.shift(1).loc[row.name]), axis=1)

        # Apply the function
        df = check_expiry_day(df, symbol)
        df = check_expiry_day(df, symbol)

        df = fe.extract_feature(df)

        print(df.columns)

        # Renaming columns
        df.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'open_change': 'Open Change',
            'mkt_change': 'MKT Change',
            'mkt_change_%': 'Change %',
            'open_high': 'Open High',
            'open_low': 'Open Low',
            'open_close': 'Open Close',
        }, inplace=True)

        # Select and rename columns
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Expiry', 'Volume',
                 'Open Change', 'Open High', 'Open Low', 'Open Close', 'MKT Change', 'Change %','Trend']]
        return df
    except Exception as e:
        raise Exception(f"Error fetching data for {symbol}: {str(e)}")


def get_stock_info(symbol: str) -> dict:
    """
    Get basic stock information
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        # expiry_dates = stock.options  # List of expiry dates (strings: YYYY-MM-DD)
        # expiry_dates = pd.to_datetime(expiry_dates)  # Convert to datetime format
        # print(expiry_dates)

        return {
            'name': info.get('longName', symbol),
            'sector': info.get('sector', 'N/A'),
            'currency': info.get('currency', 'INR')
        }
    except:
        return {
            'name': symbol,
            'sector': 'N/A',
            'currency': 'INR'
        }
