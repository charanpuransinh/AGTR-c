import pandas as pd
import numpy as np
from src.setup_c.engine_07_volume_profile_vwap import calculate_volume_profile_poc, calculate_vwap_bands

def test_volume_profile_poc():
    np.random.seed(42)
    df = pd.DataFrame({
        'high': np.linspace(22000, 22100, 50),
        'low': np.linspace(21900, 22000, 50),
        'close': np.linspace(21950, 22050, 50),
        'volume': np.random.randint(1000, 5000, 50)
    })
    res = calculate_volume_profile_poc(df)
    assert "poc" in res
    assert "value_area_high" in res
    assert "value_area_low" in res

def test_vwap_bands():
    df = pd.DataFrame({
        'high': [22100, 22150, 22200],
        'low': [21900, 21950, 22000],
        'close': [22000, 22050, 22100],
        'volume': [10000, 15000, 20000]
    })
    res = calculate_vwap_bands(df)
    assert "vwap" in res
    assert res["upper_band_2"] > res["vwap"]
    assert res["lower_band_2"] < res["vwap"]
