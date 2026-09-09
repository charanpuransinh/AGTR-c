from src.setup_c.engine_05_option.institutional_analytics import calculate_gex_and_walls, detect_iceberg_absorption

def test_gex_and_walls():
    strikes = [21800, 21900, 22000, 22100, 22200]
    call_oi = [10000, 20000, 150000, 50000, 10000]
    put_oi = [120000, 80000, 30000, 10000, 5000]
    res = calculate_gex_and_walls(strikes, call_oi, put_oi, spot_price=22000, iv=0.15, dte=5)
    
    assert res["status"] == "SUCCESS"
    assert res["call_wall"] == 22000
    assert res["put_wall"] == 21800
    assert isinstance(res["gamma_flip_level"], float)

def test_iceberg_detection():
    volumes = [1000, 1200, 5000, 1100]
    price_changes = [0.2, 0.1, 0.01, 0.3]
    signals = detect_iceberg_absorption(volumes, price_changes, threshold_multiplier=2.0)
    assert len(signals) == 1
    assert signals[0]["signal"] == "ICEBERG_ABSORPTION_DETECTED"
