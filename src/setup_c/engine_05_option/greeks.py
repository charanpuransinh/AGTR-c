import math

def calculate_d1(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """Calculates d1 for Black-Scholes pricing."""
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        return 0.0
    return (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))

def calculate_delta(S: float, K: float, T: float, r: float, sigma: float, option_type: str = 'CE') -> float:
    """Calculates Option Delta with zero-division safety."""
    if T <= 0 or sigma <= 0:
        return 0.0
    d1 = calculate_d1(S, K, T, r, sigma)
    # Standard normal CDF approximation
    cdf_d1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    if option_type.upper() == 'CE':
        return cdf_d1
    else:
        return cdf_d1 - 1.0
