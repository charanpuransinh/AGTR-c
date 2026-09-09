from src.setup_c.engine_05_option.vanna_charm_exposures import calculate_vanna_charm, calculate_expected_move, calculate_straddle_strangle_breakeven

def test_vanna_charm_calculation():
    res = calculate_vanna_charm(22000, 22000, 0.15, 7)
    assert "vanna" in res
    assert "charm" in res

def test_expected_move():
    res = calculate_expected_move(22000, 250)
    assert res["expected_move_pts"] > 0
    assert res["upper_bound"] > 22000
    assert res["lower_bound"] < 22000

def test_breakeven():
    res = calculate_straddle_strangle_breakeven(22000, 22000, 22000, 150, 140)
    assert res["total_premium"] == 290
    assert res["upper_breakeven"] == 22290
    assert res["lower_breakeven"] == 21710
