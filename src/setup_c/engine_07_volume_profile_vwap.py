import numpy as np
import pandas as pd

def calculate_volume_profile_poc(df: pd.DataFrame, bins: int = 20) -> dict:
    """
    Computes the Point of Control (POC), Value Area High (VAH), and Value Area Low (VAL)
    from price and volume arrays to identify institutional magnet zones.
    """
    price_min = df['low'].min()
    price_max = df['high'].max()
    hist, bin_edges = np.histogram(df['close'], bins=bins, weights=df['volume'])
    
    poc_bin_index = np.argmax(hist)
    poc_price = (bin_edges[poc_bin_index] + bin_edges[poc_bin_index + 1]) / 2
    
    total_volume = np.sum(hist)
    value_area_volume = total_volume * 0.70
    
    # Sort bins by volume descending to find the 70% Value Area
    sorted_indices = np.argsort(hist)[::-1]
    cumulative_volume = 0
    va_indices = []
    
    for idx in sorted_indices:
        cumulative_volume += hist[idx]
        va_indices.append(idx)
        if cumulative_volume >= value_area_volume:
            break
            
    va_min = bin_edges[min(va_indices)]
    va_max = bin_edges[max(va_indices) + 1]
    
    return {
        "poc": round(float(poc_price), 2),
        "value_area_low": round(float(va_min), 2),
        "value_area_high": round(float(va_max), 2)
    }

def calculate_vwap_bands(df: pd.DataFrame, num_std_dev: float = 2.0) -> dict:
    """
    Computes Institutional Volume Weighted Average Price (VWAP) along with 
    Standard Deviation bands for breakout and mean-reversion triggers.
    """
    typical_price = (df['high'] + df['low'] + df['close']) / 3.0
    v = df['volume']
    
    vwap = np.sum(typical_price * v) / np.sum(v)
    variance = np.sum(v * (typical_price - vwap) ** 2) / np.sum(v)
    std_dev = np.sqrt(variance)
    
    upper_band_1 = vwap + (std_dev * 1.0)
    lower_band_1 = vwap - (std_dev * 1.0)
    upper_band_2 = vwap + (std_dev * num_std_dev)
    lower_band_2 = vwap - (std_dev * num_std_dev)
    
    return {
        "vwap": round(float(vwap), 2),
        "upper_band_1": round(float(upper_band_1), 2),
        "lower_band_1": round(float(lower_band_1), 2),
        "upper_band_2": round(float(upper_band_2), 2),
        "lower_band_2": round(float(lower_band_2), 2)
    }
