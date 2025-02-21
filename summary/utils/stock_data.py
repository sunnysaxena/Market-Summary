import time
import yfinance as yf
import pandas as pd
from trade_utils import feature_extraction as fe
from datetime import datetime, timedelta


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

        df = fe.extract_feature(df)

        # Renaming columns
        df.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'open_change': 'Open Change',
            'mkt_change': 'MKT Change',
            'open_high': 'Open High',
            'open_low': 'Open Low',
            'open_close': 'Open Close',
        }, inplace=True)

        # Select and rename columns
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume',
                 'Open High', 'Open Low', 'Open Close',
                 'Open Change', 'MKT Change', 'Trend']]

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
