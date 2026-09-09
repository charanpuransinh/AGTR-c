def calculate_basis(spot_price: float, futures_price: float) -> dict:
    """
    Calculates Spot-Futures Basis and basis percentage.
    Positive = Contango / Premium, Negative = Backwardation / Discount.
    """
    basis = futures_price - spot_price
    basis_pct = (basis / spot_price) * 100.0 if spot_price > 0 else 0.0
    return {
        "basis": round(basis, 2),
        "basis_pct": round(basis_pct, 4),
        "structure": "PREMIUM_CONTANGO" if basis > 0 else "DISCOUNT_BACKWARDATION"
    }

def calculate_intrinsic_time_value(spot_price: float, strike: float, ltp: float, option_type: str) -> dict:
    """
    Calculates Intrinsic Value and Time Value components of an option's LTP.
    """
    option_type = option_type.upper()
    if option_type == 'CE':
        intrinsic = max(0.0, spot_price - strike)
    elif option_type == 'PE':
        intrinsic = max(0.0, strike - spot_price)
    else:
        intrinsic = 0.0
        
    time_value = max(0.0, ltp - intrinsic)
    return {
        "intrinsic_value": round(intrinsic, 2),
        "time_value": round(time_value, 2),
        "ltp": ltp
    }

def detect_unusual_activity(volumes: list, open_interests: list) -> list:
    """
    Detects unusual options activity and potential block trades where volume is exceptionally high relative to Open Interest.
    """
    if not volumes or not open_interests or len(volumes) != len(open_interests):
        return []
        
    alerts = []
    for i, vol in enumerate(volumes):
        oi = open_interests[i]
        if oi > 0 and vol >= (oi * 0.5) and vol >= 10000:
            alerts.append({
                "strike_index": i,
                "volume": vol,
                "open_interest": oi,
                "signal": "UNUSUAL_OPTIONS_ACTIVITY_BLOCK_TRADE"
            })
    return alerts

def calculate_pin_probability(spot_price: float, strike: float, dte: float, max_pain_strike: float) -> float:
    """
    Estimates the probability of the underlying pinning to a specific strike on expiry
    based on proximity, time remaining, and Max Pain convergence.
    """
    if dte > 3.0:
        return 10.0
        
    distance_pct = abs(spot_price - strike) / spot_price * 100.0
    is_max_pain = (strike == max_pain_strike)
    
    base_prob = max(0.0, 100.0 - (distance_pct * 40.0))
    if is_max_pain:
        base_prob = min(100.0, base_prob + 25.0)
        
    return round(max(0.0, min(100.0, base_prob)), 2)
