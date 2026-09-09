from src.setup_c.engine_04_risk.position_sizer import calculate_position_size

def test_position_sizing():
    result = calculate_position_size(account_balance=100000, risk_per_trade_pct=1.0, entry_price=500, stop_loss_price=480, lot_size=25)
    assert result["risk_amount"] == 1000.0
    assert result["quantity"] == 50
    assert result["lots"] == 2
