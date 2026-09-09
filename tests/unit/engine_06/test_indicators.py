import pandas as pd
import numpy as np
from src.setup_c.engine_06_indicator.rsi import calculate_rsi
from src.setup_c.engine_06_indicator.vwap import calculate_vwap

def test_rsi_range():
    prices = pd.Series([10, 12, 11, 13, 15, 14, 16, 18, 17, 19, 21, 20, 22, 24, 25, 23])
    rsi = calculate_rsi(prices, period=14)
    assert not rsi.empty
    assert (rsi >= 0).all() and (rsi <= 100).all()

def test_vwap_zero_volume():
    high = pd.Series([100, 102, 104])
    low = pd.Series([98, 100, 102])
    close = pd.Series([99, 101, 103])
    volume = pd.Series([0, 0, 0])
    vwap = calculate_vwap(high, low, close, volume)
    assert not vwap.isnull().any()
