import pandas as pd
import numpy as np
from src.setup_c.engine_08_market_structure import detect_market_structure_breaks, identify_order_blocks

def test_market_structure():
    np.random.seed(42)
    n = 50
    df = pd.DataFrame({
        'open': np.linspace(21000, 21500, n),
        'high': np.linspace(21100, 21600, n),
        'low': np.linspace(20900, 21400, n),
        'close': np.linspace(21050, 21550, n),
        'volume': np.random.randint(5000, 15000, n)
    })
    res = detect_market_structure_breaks(df)
    assert "structure_state" in res
    assert "bos_bullish" in res

def test_order_blocks():
    df = pd.DataFrame({
        'open': [21000, 21050, 20950, 21200],
        'high': [21060, 21080, 21000, 21400],
        'low': [20990, 21020, 20900, 21180],
        'close': [21050, 21030, 20910, 21380],
        'volume': [10000, 10000, 10000, 30000]
    })
    res = identify_order_blocks(df)
    assert isinstance(res, dict)
