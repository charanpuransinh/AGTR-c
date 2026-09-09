def calculate_variance_risk_premium(iv: float, realized_vol: float) -> float:
    """
    Calculates Variance Risk Premium (VRP) as the spread between Implied Volatility and Realized Volatility.
    """
    return round(iv - realized_vol, 4)

def detect_iv_crush(iv_current: float, iv_previous: float, drop_threshold_pct: float = 15.0) -> dict:
    """
    Detects sudden IV Crush events (e.g., post-events like earnings or macro announcements) 
    where option sellers benefit from rapid premium collapse.
    """
    if iv_previous <= 0:
        return {"iv_crush_detected": False, "drop_pct": 0.0}
        
    drop_pct = ((iv_previous - iv_current) / iv_previous) * 100.0
    is_crush = drop_pct >= drop_threshold_pct
    
    return {
        "iv_crush_detected": is_crush,
        "drop_pct": round(drop_pct, 2),
        "current_iv": iv_current,
        "previous_iv": iv_previous
    }

def analyze_term_structure(expiries_dte: list, atm_ivs: list) -> str:
    """
    Analyzes Volatility Term Structure across multiple expiries.
    - Contango: Near-term IV < Far-term IV (Normal market)
    - Backwardation: Near-term IV > Far-term IV (Panic / Event risk)
    """
    if not expiries_dte or len(expiries_dte) != len(atm_ivs) or len(expiries_dte) < 2:
        return "INSUFFICIENT_DATA"
        
    # Sort by DTE
    sorted_pairs = sorted(zip(expiries_dte, atm_ivs))
    near_iv = sorted_pairs[0][1]
    far_iv = sorted_pairs[-1][1]
    
    if near_iv > far_iv:
        return "BACKWARDATION"
    elif near_iv < far_iv:
        return "CONTANGO"
    return "FLAT"

def analyze_zero_dte_metrics(spot_price: float, strike: float, ltp: float, dte: float) -> dict:
    """
    Evaluates 0DTE (Zero Days to Expiry) high-gamma acceleration and time-decay risk.
    """
    is_zero_dte = dte <= 1.0
    moneyness = abs(spot_price - strike) / spot_price * 100.0
    is_atm_zero_dte = is_zero_dte and (moneyness <= 0.5)
    
    risk_level = "EXTREME" if is_atm_zero_dte else ("HIGH" if is_zero_dte else "NORMAL")
    
    return {
        "is_0dte": is_zero_dte,
        "atm_zero_dte_trigger": is_atm_zero_dte,
        "risk_classification": risk_level,
        "premium_decay_velocity": "MAXIMUM" if is_zero_dte else "STANDARD"
    }
