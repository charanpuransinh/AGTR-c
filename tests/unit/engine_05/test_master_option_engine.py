from src.setup_c.engine_05_option.master_option_engine import run_complete_option_analysis

def test_master_option_orchestrator():
    sample_data = {
        "spot_price": 22000.0,
        "futures_price": 22050.0,
        "strikes": [21800, 21900, 22000, 22100, 22200],
        "call_oi": [10000, 20000, 150000, 50000, 10000],
        "put_oi": [120000, 80000, 30000, 10000, 5000],
        "ivs": [0.18, 0.16, 0.14, 0.15, 0.17],
        "atm_strike": 22000.0,
        "dte": 5.0,
        "iv": 0.15,
        "price_change_pct": 1.2,
        "oi_change_pct": 4.5
    }
    res = run_complete_option_analysis(sample_data)
    assert res["status"] == "ENGINE_05_SUCCESS"
    assert "dealer_positioning" in res
    assert "skew_and_buildup" in res
    assert "exposures" in res
    assert "volatility_context" in res
    assert "flow_and_basis" in res
