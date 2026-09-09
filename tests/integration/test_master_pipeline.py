from src.setup_c.pipeline_integration import evaluate_option_signals

def test_pipeline_integration():
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
        "price_change_pct": 1.5,
        "oi_change_pct": 6.0
    }
    result = evaluate_option_signals(sample_data)
    assert result["pipeline_status"] == "ACTIVE"
    assert "signal" in result
    assert "confidence_score" in result
