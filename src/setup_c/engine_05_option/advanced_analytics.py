import math

def calculate_pcr(total_put_oi: float, total_call_oi: float) -> float:
    """Calculates Put-Call Ratio (PCR) from Open Interest with zero division safety."""
    if total_call_oi <= 0:
        return 0.0
    return round(total_put_oi / total_call_oi, 4)

def calculate_max_pain(strikes: list, call_oi: list, put_oi: list) -> float:
    """Calculates the Max Pain strike price where option writers face minimum liability."""
    if not strikes or len(strikes) != len(call_oi) or len(strikes) != len(put_oi):
        return 0.0
    
    min_pain = float('inf')
    max_pain_strike = strikes[0]
    
    for target_strike in strikes:
        total_pain = 0.0
        for i, strike in enumerate(strikes):
            # Pain for Call buyers (loss for writers if market expires at target_strike)
            if target_strike > strike:
                total_pain += (target_strike - strike) * call_oi[i]
            # Pain for Put buyers
            if target_strike < strike:
                total_pain += (strike - target_strike) * put_oi[i]
                
        if total_pain < min_pain:
            min_pain = total_pain
            max_pain_strike = target_strike
            
    return float(max_pain_strike)

def detect_gamma_blast(spot_price: float, strike_price: float, gamma: float, iv: float, threshold_gamma: float = 0.05) -> dict:
    """Detects potential Gamma Blast zones near expiry where Delta accelerates rapidly."""
    is_near_atm = abs(spot_price - strike_price) <= (spot_price * 0.005) # Within 0.5%
    is_high_gamma = gamma >= threshold_gamma
    
    blast_score = 0.0
    if is_near_atm:
        blast_score += 50.0
    if is_high_gamma:
        blast_score += 50.0
        
    return {
        "gamma_blast_active": blast_score >= 100.0,
        "blast_score": blast_score,
        "current_gamma": round(gamma, 6)
    }
