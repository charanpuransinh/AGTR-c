import pandas as pd
import numpy as np

def compute_institutional_confluence_score(
    market_structure_res: dict, 
    breakout_res: dict, 
    volume_profile_res: dict, 
    current_price: float
) -> dict:
    """
    Computes a final institutional confluence score (out of 100 points) 
    by aggregating market structure, breakout status, and volume magnet alignment.
    """
    score = 0.0
    max_score = 100.0
    breakdown = {}

    # 1. Market Structure Weight (30 points)
    ms_state = market_structure_res.get("structure_state", "")
    if "BULLISH" in ms_state or market_structure_res.get("bos_bullish", False):
        score += 30.0
        breakdown["market_structure"] = 30.0
    elif "CHOCH" in ms_state:
        score += 15.0
        breakdown["market_structure"] = 15.0
    else:
        breakdown["market_structure"] = 0.0

    # 2. Breakout Box & Volume Confirmation Weight (35 points)
    if breakout_res.get("weekly_breakout_bullish", False) and breakout_res.get("volume_confirmed", False):
        score += 35.0
        breakdown["breakout_box"] = 35.0
    elif breakout_res.get("monthly_breakout_bullish", False) and breakout_res.get("volume_confirmed", False):
        score += 35.0
        breakdown["breakout_box"] = 35.0
    elif breakout_res.get("volume_confirmed", False):
        score += 15.0
        breakdown["breakout_box"] = 15.0
    else:
        breakdown["breakout_box"] = 0.0

    # 3. Volume Profile POC Gravity Weight (35 points)
    poc = volume_profile_res.get("poc", current_price)
    val = volume_profile_res.get("value_area_low", current_price)
    vah = volume_profile_res.get("value_area_high", current_price)

    if current_price >= val and current_price <= vah:
        score += 20.0
        breakdown["volume_profile"] = 20.0
    elif current_price > vah:
        score += 35.0
        breakdown["volume_profile"] = 35.0
    else:
        breakdown["volume_profile"] = 10.0

    final_score = min(score, max_score)
    signal_bias = "STRONG_BUY" if final_score >= 75 else ("MODERATE_BUY" if final_score >= 50 else "NEUTRAL_WAIT")

    return {
        "confluence_score": round(final_score, 2),
        "signal_bias": signal_bias,
        "scoring_breakdown": breakdown
    }
