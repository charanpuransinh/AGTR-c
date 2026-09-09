from src.setup_c.engine_06_retracement_targets import (
    calculate_fibonacci_retracements, 
    calculate_measured_move_target, 
    calculate_atr_dynamic_brackets
)

def test_fibonacci_engine():
    res = calculate_fibonacci_retracements(22500.0, 21500.0, "BULLISH")
    assert "golden_pocket_0_618" in res
    assert res["golden_pocket_0_618"] == 21882.0

def test_measured_move():
    res = calculate_measured_move_target(21500.0, 22000.0, 21800.0)
    assert res["measured_move_target"] == 22300.0

def test_atr_brackets():
    res = calculate_atr_dynamic_brackets(22000.0, 50.0, 1.5, 3.0, "BUY")
    assert res["stop_loss"] == 21925.0
    assert res["target_1"] == 22150.0
    assert res["risk_reward_ratio"] == 2.0
