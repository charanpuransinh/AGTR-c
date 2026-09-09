import math

def calculate_d1(S: float, K: float, T: float, r: float, sigma: float) -> float:
    if T <= 0 or sigma <= 0 or S <= 0 or K <= 0:
        return 0.0
    return (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))

def calculate_delta(S: float, K: float, T: float, r: float, sigma: float, option_type: str = 'CE') -> float:
    if T <= 0 or sigma <= 0:
        return 0.0
    d1 = calculate_d1(S, K, T, r, sigma)
    cdf_d1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    if option_type.upper() == 'CE':
        return round(cdf_d1, 4)
    return round(cdf_d1 - 1.0, 4)

def calculate_gamma(S: float, K: float, T: float, r: float, sigma: float) -> float:
    if T <= 0 or sigma <= 0 or S <= 0:
        return 0.0
    d1 = calculate_d1(S, K, T, r, sigma)
    pdf_d1 = (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * d1 ** 2)
    return round(pdf_d1 / (S * sigma * math.sqrt(T)), 6)

def calculate_theta(S: float, K: float, T: float, r: float, sigma: float, option_type: str = 'CE') -> float:
    if T <= 0 or sigma <= 0 or S <= 0:
        return 0.0
    d1 = calculate_d1(S, K, T, r, sigma)
    d2 = d1 - sigma * math.sqrt(T)
    pdf_d1 = (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * d1 ** 2)
    cdf_d2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
    cdf_neg_d2 = 0.5 * (1.0 + math.erf(-d2 / math.sqrt(2.0)))
    
    first_term = -(S * pdf_d1 * sigma) / (2.0 * math.sqrt(T))
    if option_type.upper() == 'CE':
        theta = first_term - r * K * math.exp(-r * T) * cdf_d2
    else:
        theta = first_term + r * K * math.exp(-r * T) * cdf_neg_d2
    return round(theta / 365.0, 4)

def calculate_vega(S: float, K: float, T: float, r: float, sigma: float) -> float:
    if T <= 0 or sigma <= 0 or S <= 0:
        return 0.0
    d1 = calculate_d1(S, K, T, r, sigma)
    pdf_d1 = (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * d1 ** 2)
    return round((S * math.sqrt(T) * pdf_d1) / 100.0, 4)
