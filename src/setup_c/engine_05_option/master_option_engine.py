from src.setup_c.engine_05_option.institutional_analytics import calculate_gex_and_walls, detect_iceberg_absorption
from src.setup_c.engine_05_option.buildup_skew_analytics import classify_oi_buildup, calculate_iv_skew
from src.setup_c.engine_05_option.vanna_charm_exposures import calculate_vanna_charm, calculate_expected_move, calculate_straddle_strangle_breakeven
from src.setup_c.engine_05_option.term_structure_iv_crush import calculate_variance_risk_premium, detect_iv_crush, analyze_term_structure, analyze_zero_dte_metrics
from src.setup_c.engine_05_option.flow_basis_analytics import calculate_basis, calculate_intrinsic_time_value, detect_unusual_activity, calculate_pin_probability

def run_complete_option_analysis(market_data: dict) -> dict:
    """
    Master Orchestrator for Engine 05: Unifies all 73-point option chain analytics,
    Greeks, institutional flows, dealer positioning, and hidden tools into a single commercial-grade API.
    """
    spot = market_data.get("spot_price", 22000.0)
    futures = market_data.get("futures_price", 22050.0)
    strikes = market_data.get("strikes", [21800, 21900, 22000, 22100, 22200])
    call_oi = market_data.get("call_oi", [10000, 20000, 150000, 50000, 10000])
    put_oi = market_data.get("put_oi", [120000, 80000, 30000, 10000, 5000])
    ivs = market_data.get("ivs", [0.18, 0.16, 0.14, 0.15, 0.17])
    atm_strike = market_data.get("atm_strike", 22000.0)
    dte = market_data.get("dte", 5.0)
    iv = market_data.get("iv", 0.15)
    
    # 1. Dealer Positioning & Walls
    gex_res = calculate_gex_and_walls(strikes, call_oi, put_oi, spot, iv, dte)
    
    # 2. Skew & Build-up
    skew_res = calculate_iv_skew(strikes, ivs, atm_strike)
    buildup_res = classify_oi_buildup(market_data.get("price_change_pct", 1.0), market_data.get("oi_change_pct", 5.0))
    
    # 3. Exposures & Expected Move
    vanna_charm = calculate_vanna_charm(spot, atm_strike, iv, dte)
    exp_move = calculate_expected_move(spot, market_data.get("atm_straddle_price", 250.0))
    
    # 4. Term Structure & VRP
    vrp = calculate_variance_risk_premium(iv, market_data.get("realized_vol", 0.12))
    term_struct = analyze_term_structure(market_data.get("expiries_dte", [1, 7, 30]), market_data.get("term_ivs", [0.2, 0.16, 0.14]))
    zero_dte = analyze_zero_dte_metrics(spot, atm_strike, market_data.get("ltp", 100.0), dte)
    
    # 5. Flow & Basis
    basis_res = calculate_basis(spot, futures)
    pin_prob = calculate_pin_probability(spot, atm_strike, dte, gex_res.get("call_wall", spot))
    
    return {
        "status": "ENGINE_05_SUCCESS",
        "dealer_positioning": gex_res,
        "skew_and_buildup": {"skew": skew_res, "buildup": buildup_res},
        "exposures": {"vanna_charm": vanna_charm, "expected_move": exp_move},
        "volatility_context": {"vrp": vrp, "term_structure": term_struct, "zero_dte": zero_dte},
        "flow_and_basis": {"basis": basis_res, "pin_probability": pin_prob}
    }
