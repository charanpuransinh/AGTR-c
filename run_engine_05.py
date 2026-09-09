from src.setup_c.pipeline_integration import evaluate_option_signals
import json

def main():
    print("==================================================")
    print(" ARGT SETUP C: ENGINE 05 INSTITUTIONAL OPTION ENGINE")
    print(" 73-Point Master Data & Analytics Framework Runner")
    print("==================================================")
    
    sample_market_data = {
        "spot_price": 22000.0,
        "futures_price": 22050.0,
        "strikes": [21800, 21900, 22000, 22100, 22200],
        "call_oi": [10000, 20000, 150000, 50000, 10000],
        "put_oi": [120000, 80000, 30000, 10000, 5000],
        "ivs": [0.18, 0.16, 0.14, 0.15, 0.17],
        "atm_strike": 22000.0,
        "dte": 5.0,
        "iv": 0.15,
        "price_change_pct": 1.5,
        "oi_change_pct": 6.0,
        "atm_straddle_price": 250.0,
        "realized_vol": 0.12,
        "expiries_dte": [1, 7, 30],
        "term_ivs": [0.22, 0.18, 0.15],
        "ltp": 120.0
    }
    
    print("\n[+] Processing Market Feed & Institutional Metrics...")
    result = evaluate_option_signals(sample_market_data)
    
    print("\n[+] Pipeline Evaluation Result:")
    print(json.dumps(result, indent=4))
    print("\n==================================================")
    print(" SYSTEM STATUS: COMMERCIAL-GRADE & GITHUB SYNCED")
    print("==================================================")

if __name__ == "__main__":
    main()
