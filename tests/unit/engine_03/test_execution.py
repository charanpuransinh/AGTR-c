from src.setup_c.engine_03_execution.order_router import route_order

def test_order_execution():
    result = route_order(symbol="NIFTY", action="BUY", quantity=50, price=22000)
    assert result["status"] == "EXECUTED"
    assert result["executed_price"] > 22000

def test_zero_quantity_rejection():
    result = route_order(symbol="NIFTY", action="BUY", quantity=0, price=22000)
    assert result["status"] == "REJECTED"
