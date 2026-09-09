"""
ARGT Setup C — Engine 06: VWAP Indicator
Zero-Division Safe Volume Weighted Average Price
"""
import numpy as np
import pandas as pd

def calculate_vwap(high: pd.Series, low: pd.Series, close: pd.Series, volume: pd.Series) -> pd.Series:
    if close.empty:
        return pd.Series(dtype=float)
    
    typical_price = (high + low + close) / 3.0
    cum_tp_vol = (typical_price * volume).cumsum()
    cum_vol = volume.cumsum()
    
    vwap = np.where(cum_vol == 0, close, cum_tp_vol / np.maximum(cum_vol, 1e-10))
    return pd.Series(vwap, index=close.index).ffill().bfill()
