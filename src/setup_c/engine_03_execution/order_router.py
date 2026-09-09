def route_order(symbol: str, action: str, quantity: int, price: float, slippage_tolerance_pct: float = 0.2) -> dict:
    if quantity <= 0 or price <= 0:
        return {"status": "REJECTED", "reason": "Invalid quantity or price"}
    
    max_slippage = price * (slippage_tolerance_pct / 100.0)
    execution_price = price + max_slippage if action.upper() == 'BUY' else price - max_slippage
    
    return {
        "status": "EXECUTED",
        "symbol": symbol,
        "action": action.upper(),
        "quantity": quantity,
        "expected_price": price,
        "executed_price": round(execution_price, 2),
        "slippage": round(max_slippage, 2)
    }
