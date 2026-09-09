"""
ARGT Setup C — Engine 06: RSI Indicator (Wilder's Smoothing)
Zero-Division Safe & Vectorized
"""
import numpy as np
import pandas as pd

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    if series.empty or len(series) < period:
        return pd.Series(index=series.index, dtype=float)
    
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
    
    rs = np.where(avg_loss == 0, 100.0, avg_gain / np.maximum(avg_loss, 1e-10))
    rsi = 100.0 - (100.0 / (1.0 + rs))
    
    return pd.Series(rsi, index=series.index).fillna(50.0)
