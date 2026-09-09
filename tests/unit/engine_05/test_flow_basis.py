from src.setup_c.engine_05_option.flow_basis_analytics import calculate_basis, calculate_intrinsic_time_value, detect_unusual_activity, calculate_pin_probability

def test_basis():
    res = calculate_basis(22000, 22050)
    assert res["basis"] == 50.0
    assert res["structure"] == "PREMIUM_CONTANGO"

def test_intrinsic_time_value():
    res = calculate_intrinsic_time_value(22000, 21900, 180.0, 'CE')
    assert res["intrinsic_value"] == 100.0
    assert res["time_value"] == 80.0

def test_unusual_activity():
    volumes = [5000, 75000, 1200]
    ois = [10000, 50000, 5000]
    alerts = detect_unusual_activity(volumes, ois)
    assert len(alerts) > 0

def test_pin_probability():
    prob = calculate_pin_probability(22005, 22000, 0.5, 22000)
    assert prob > 50.0
