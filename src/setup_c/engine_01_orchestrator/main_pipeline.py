from src.setup_c.engine_06_indicator.rsi import calculate_rsi
from src.setup_c.engine_04_risk.position_sizer import calculate_position_size
from src.setup_c.engine_03_execution.order_router import route_order

def run_strategy_pipeline(prices: list, account_balance: float, symbol: str) -> dict:
    if not prices or len(prices) < 14:
        return {"status": "INSUFFICIENT_DATA"}
    
    import pandas as pd
    rsi_series = calculate_rsi(pd.Series(prices))
    latest_rsi = rsi_series.iloc[-1]
    
    if latest_rsi > 60:
        entry = prices[-1]
        stop_loss = entry * 0.99
        risk_res = calculate_position_size(account_balance, 1.0, entry, stop_loss)
        
        if risk_res["quantity"] > 0:
            order_res = route_order(symbol, "BUY", risk_res["quantity"], entry)
            return {"status": "SIGNAL_EXECUTED", "order": order_res, "rsi": round(latest_rsi, 2)}
            
    return {"status": "NO_SIGNAL", "rsi": round(latest_rsi, 2)}
