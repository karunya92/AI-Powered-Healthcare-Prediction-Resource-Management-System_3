import pandas as pd
from datetime import datetime


def format_date(date_value):
    """
    Format date as YYYY-MM-DD
    """
    try:
        return pd.to_datetime(date_value).strftime("%Y-%m-%d")
    except Exception:
        return ""


def current_timestamp():
    """
    Return current timestamp
    """
    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def dataframe_to_csv(df):
    """
    Convert dataframe to CSV bytes
    """
    return df.to_csv(
        index=False
    ).encode("utf-8")


def safe_float(value):
    """
    Convert value to float safely
    """
    try:
        return float(value)
    except Exception:
        return 0.0


def safe_int(value):
    """
    Convert value to int safely
    """
    try:
        return int(value)
    except Exception:
        return 0