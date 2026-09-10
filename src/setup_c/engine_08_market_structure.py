import numpy as np
import pandas as pd

def identify_swing_points(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """
    Identifies institutional swing highs and swing lows for market structure mapping.
    """
    df = df.copy()
    df['swing_high'] = df['high'][(df['high'] == df['high'].rolling(window=window*2+1, center=True).max())]
    df['swing_low'] = df['low'][(df['low'] == df['low'].rolling(window=window*2+1, center=True).min())]
    return df

def detect_market_structure_breaks(df: pd.DataFrame) -> dict:
    """
    Detects Break of Structure (BOS) and Change of Character (ChoCH)
    to determine trend continuation or institutional reversals.
    """
    df = identify_swing_points(df)
    valid_highs = df['swing_high'].dropna()
    valid_lows = df['swing_low'].dropna()

    if len(valid_highs) < 2 or len(valid_lows) < 2:
        return {
            "structure_state": "CONSOLIDATION",
            "bos_bullish": False,
            "bos_bearish": False,
            "choch_detected": False,
            "last_swing_high": float(valid_highs.iloc[-1]) if len(valid_highs) > 0 else 0.0,
            "last_swing_low": float(valid_lows.iloc[-1]) if len(valid_lows) > 0 else 0.0
        }

    last_high = valid_highs.iloc[-1]
    prev_high = valid_highs.iloc[-2]
    last_low = valid_lows.iloc[-1]
    prev_low = valid_lows.iloc[-2]

    current_close = df['close'].iloc[-1]

    bos_bullish = current_close > last_high and last_high > prev_high
    bos_bearish = current_close < last_low and last_low < prev_low

    choch_bullish = current_close > last_high and last_low > prev_low and last_high <= prev_high
    choch_bearish = current_close < last_low and last_high < prev_high and last_low >= prev_low

    structure_state = "BULLISH_TREND" if last_high > prev_high and last_low > prev_low else "BEARISH_TREND"
    if choch_bullish or choch_bearish:
        structure_state = "CHOCH_REVERSAL_ZONE"

    return {
        "structure_state": structure_state,
        "bos_bullish": bool(bos_bullish),
        "bos_bearish": bool(bos_bearish),
        "choch_detected": bool(choch_bullish or choch_bearish),
        "last_swing_high": float(last_high),
        "last_swing_low": float(last_low)
    }

def identify_order_blocks(df: pd.DataFrame) -> dict:
    """
    Locates institutional Bullish and Bearish Order Blocks (last opposing candle
    before an impulsive displacement move).
    """
    df = df.copy()
    df['body_size'] = abs(df['close'] - df['open'])
    avg_body = df['body_size'].mean()

    bullish_obs = []
    bearish_obs = []

    for i in range(1, len(df) - 1):
        # Impulsive bullish move (green candle with body > 1.5x average)
        if df['close'].iloc[i] > df['open'].iloc[i] and df['body_size'].iloc[i] > (avg_body * 1.5):
            # The last red candle before this move is the Bullish Order Block
            if df['close'].iloc[i-1] < df['open'].iloc[i-1]:
                bullish_obs.append({
                    "index": int(i-1),
                    "ob_high": float(df['high'].iloc[i-1]),
                    "ob_low": float(df['low'].iloc[i-1])
                })

        # Impulsive bearish move (red candle with body > 1.5x average)
        elif df['close'].iloc[i] < df['open'].iloc[i] and df['body_size'].iloc[i] > (avg_body * 1.5):
            # The last green candle before this move is the Bearish Order Block
            if df['close'].iloc[i-1] > df['open'].iloc[i-1]:
                bearish_obs.append({
                    "index": int(i-1),
                    "ob_high": float(df['high'].iloc[i-1]),
                    "ob_low": float(df['low'].iloc[i-1])
                })

    return {
        "latest_bullish_ob": bullish_obs[-1] if bullish_obs else None,
        "latest_bearish_ob": bearish_obs[-1] if bearish_obs else None
    }
