def classify_oi_buildup(price_change_pct: float, oi_change_pct: float) -> str:
    """
    Classifies market position build-up based on Price and Open Interest changes.
    - Long Buildup: Price Up (+), OI Up (+)
    - Short Buildup: Price Down (-), OI Up (+)
    - Short Covering: Price Up (+), OI Down (-)
    - Long Unwinding: Price Down (-), OI Down (-)
    """
    if price_change_pct > 0 and oi_change_pct > 0:
        return "LONG_BUILDUP"
    elif price_change_pct < 0 and oi_change_pct > 0:
        return "SHORT_BUILDUP"
    elif price_change_pct > 0 and oi_change_pct < 0:
        return "SHORT_COVERING"
    elif price_change_pct < 0 and oi_change_pct < 0:
        return "LONG_UNWINDING"
    return "NEUTRAL"

def calculate_iv_skew(strikes: list, ivs: list, atm_strike: float) -> dict:
    """
    Calculates Put Skew and Call Skew relative to ATM IV.
    Measures market tail-risk pricing and skew gradients across strikes.
    """
    if not strikes or len(strikes) != len(ivs):
        return {"status": "ERROR"}
        
    atm_iv = ivs[strikes.index(atm_strike)] if atm_strike in strikes else ivs[len(ivs)//2]
    
    otm_put_ivs = [ivs[i] for i, s in enumerate(strikes) if s < atm_strike]
    otm_call_ivs = [ivs[i] for i, s in enumerate(strikes) if s > atm_strike]
    
    avg_put_skew = (sum(otm_put_ivs) / len(otm_put_ivs)) - atm_iv if otm_put_ivs else 0.0
    avg_call_skew = (sum(otm_call_ivs) / len(otm_call_ivs)) - atm_iv if otm_call_ivs else 0.0
    
    return {
        "status": "SUCCESS",
        "atm_iv": round(atm_iv, 4),
        "put_skew": round(avg_put_skew, 4),
        "call_skew": round(avg_call_skew, 4),
        "skew_bias": "PUT_SKEW_HEAVY" if avg_put_skew > avg_call_skew else "CALL_SKEW_HEAVY"
    }
