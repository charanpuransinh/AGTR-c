import math

def calculate_gex_and_walls(strikes: list, call_oi: list, put_oi: list, spot_price: float, iv: float, dte: float) -> dict:
    """
    Calculates Gamma Exposure (GEX), Call Wall, Put Wall, and Gamma Flip Level.
    Institutional-grade calculation for market maker positioning.
    """
    if not strikes or len(strikes) != len(call_oi) or len(strikes) != len(put_oi):
        return {"status": "ERROR", "message": "Invalid array lengths"}

    net_gex_by_strike = {}
    total_gex = 0.0
    
    t_years = max(dte / 365.0, 0.0001)
    
    for i, strike in enumerate(strikes):
        # Simplified Black-Scholes Gamma approximation for discrete strikes
        d1 = (math.log(spot_price / strike) + (0.5 * iv ** 2) * t_years) / (iv * math.sqrt(t_years))
        gamma = math.exp(-0.5 * d1**2) / (spot_price * iv * math.sqrt(2 * math.pi * t_years))
        
        # GEX = Gamma * Spot^2 * OI * Contract Multiplier (Assuming 50 for Nifty or 1 as standard unit)
        call_gex = gamma * (spot_price ** 2) * call_oi[i] * 50 * 0.01
        put_gex = gamma * (spot_price ** 2) * put_oi[i] * 50 * 0.01
        
        # Dealers are typically short calls (negative GEX) and short puts (positive GEX relative to market drop, or vice versa depending on convention)
        # Standard convention: Call wall positive gamma contribution, Put wall negative or hedging balance.
        net_strike_gex = put_gex - call_gex 
        net_gex_by_strike[strike] = net_strike_gex
        total_gex += net_strike_gex

    # Call Wall: Strike with highest Call OI
    call_wall = strikes[call_oi.index(max(call_oi))] if call_oi else spot_price
    # Put Wall: Strike with highest Put OI
    put_wall = strikes[put_oi.index(max(put_oi))] if put_oi else spot_price

    # Gamma Flip: Strike where cumulative GEX changes sign
    gamma_flip_level = strikes[0]
    cumulative = 0.0
    prev_cum = 0.0
    for strike in sorted(net_gex_by_strike.keys()):
        prev_cum = cumulative
        cumulative += net_gex_by_strike[strike]
        if prev_cum < 0 and cumulative >= 0:
            gamma_flip_level = strike
            break

    return {
        "status": "SUCCESS",
        "call_wall": float(call_wall),
        "put_wall": float(put_wall),
        "gamma_flip_level": float(gamma_flip_level),
        "total_net_gex": round(total_gex, 2),
        "strike_gex_profile": net_gex_by_strike
    }

def detect_iceberg_absorption(volumes: list, price_changes: list, threshold_multiplier: float = 2.5) -> list:
    """
    Identifies institutional iceberg orders and volume absorption zones 
    where high volume occurs with minimal price movement.
    """
    if not volumes or not price_changes or len(volumes) != len(price_changes):
        return []
    
    avg_volume = sum(volumes) / len(volumes) if volumes else 1.0
    absorption_signals = []
    
    for i, vol in enumerate(volumes):
        price_change = abs(price_changes[i])
        if vol >= (avg_volume * threshold_multiplier) and price_change <= 0.05:
            absorption_signals.append({
                "index": i,
                "volume": vol,
                "price_change": price_change,
                "signal": "ICEBERG_ABSORPTION_DETECTED"
            })
            
    return absorption_signals
