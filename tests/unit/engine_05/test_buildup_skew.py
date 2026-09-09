from src.setup_c.engine_05_option.buildup_skew_analytics import classify_oi_buildup, calculate_iv_skew

def test_classify_oi_buildup():
    assert classify_oi_buildup(1.5, 5.0) == "LONG_BUILDUP"
    assert classify_oi_buildup(-1.2, 4.0) == "SHORT_BUILDUP"
    assert classify_oi_buildup(0.8, -3.0) == "SHORT_COVERING"
    assert classify_oi_buildup(-0.5, -2.5) == "LONG_UNWINDING"

def test_calculate_iv_skew():
    strikes = [21800, 21900, 22000, 22100, 22200]
    ivs = [0.18, 0.16, 0.14, 0.15, 0.17]
    res = calculate_iv_skew(strikes, ivs, atm_strike=22000)
    assert res["status"] == "SUCCESS"
    assert "put_skew" in res
