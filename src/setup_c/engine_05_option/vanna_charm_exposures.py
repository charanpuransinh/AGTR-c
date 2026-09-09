import math

def calculate_vanna_charm(spot_price: float, strike: float, iv: float, dte: float, r: float = 0.06) -> dict:
    """
    Calculates Vanna (Delta sensitivity to IV changes) and Charm (Delta sensitivity to time decay).
    Crucial for dealer re-hedging flows near expiry.
    """
    if dte <= 0 or iv <= 0 or spot_price <= 0:
        return {"vanna": 0.0, "charm": 0.0}
        
    t = dte / 365.0
    d1 = (math.log(spot_price / strike) + (r + 0.5 * iv ** 2) * t) / (iv * math.sqrt(t))
    d2 = d1 - iv * math.sqrt(t)
    
    # Standard normal probability density function
    nd1_prime = math.exp(-0.5 * d1**2) / math.sqrt(2 * math.pi)
    
    # Vanna = - e^{-rt} * d1_prime / IV (or derivative w.r.t vol)
    vanna = -nd1_prime * d2 / iv
    
    # Charm = Delta decay over time (- d(Delta)/dt)
    # Approximation for call option charm
    term1 = nd1_prime * (2 * r * t - d2 * iv * math.sqrt(t)) / (2 * t * iv * math.sqrt(t))
    charm = -term1 if t > 0 else 0.0
    
    return {
        "vanna": round(vanna, 6),
        "charm": round(charm, 6)
    }

def calculate_expected_move(spot_price: float, atm_straddle_price: float) -> dict:
    """
    Calculates 1-Standard Deviation Expected Move based on ATM Straddle price or IV.
    """
    expected_move_pts = atm_straddle_price * 0.85 # Standard empirical multiplier for 1 SD
    upper_bound = spot_price + expected_move_pts
    lower_bound = spot_price - expected_move_pts
    
    return {
        "expected_move_pts": round(expected_move_pts, 2),
        "upper_bound": round(upper_bound, 2),
        "lower_bound": round(lower_bound, 2)
    }

def calculate_straddle_strangle_breakeven(spot_price: float, call_strike: float, put_strike: float, call_prem: float, put_prem: float) -> dict:
    """
    Calculates combined premium, straddle/strangle cost, and upper/lower breakeven points.
    """
    total_premium = call_prem + put_prem
    upper_breakeven = call_strike + total_premium
    lower_breakeven = put_strike - total_premium
    
    return {
        "total_premium": round(total_premium, 2),
        "upper_breakeven": round(upper_breakeven, 2),
        "lower_breakeven": round(lower_breakeven, 2)
    }
