import math
from src.setup_c.engine_05_option.greeks import calculate_delta

def calculate_implied_volatility(market_price: float, S: float, K: float, T: float, r: float, option_type: str = 'CE') -> float:
    if market_price <= 0 or T <= 0 or S <= 0 or K <= 0:
        return 0.0
    
    sigma = 0.2  # Initial guess 20%
    for _ in range(100): # Newton-Raphson iterations
        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        pdf_d1 = (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * d1 ** 2)
        cdf_d1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
        cdf_d2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
        
        if option_type.upper() == 'CE':
            price = S * cdf_d1 - K * math.exp(-r * T) * cdf_d2
        else:
            cdf_neg_d1 = 0.5 * (1.0 + math.erf(-d1 / math.sqrt(2.0)))
            cdf_neg_d2 = 0.5 * (1.0 + math.erf(-d2 / math.sqrt(2.0)))
            price = K * math.exp(-r * T) * cdf_neg_d2 - S * cdf_neg_d1
            
        vega = S * math.sqrt(T) * pdf_d1
        diff = price - market_price
        
        if abs(diff) < 1e-5:
            return round(sigma, 4)
        if vega < 1e-8:
            break
        sigma -= diff / vega
        
    return round(max(sigma, 0.0001), 4)
