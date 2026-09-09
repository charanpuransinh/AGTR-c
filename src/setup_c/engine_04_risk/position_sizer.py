import math

def calculate_position_size(account_balance: float, risk_per_trade_pct: float, entry_price: float, stop_loss_price: float, lot_size: int = 1) -> dict:
    if account_balance <= 0 or entry_price <= 0 or stop_loss_price <= 0 or entry_price == stop_loss_price:
        return {"quantity": 0, "lots": 0, "risk_amount": 0.0}
    
    risk_amount = account_balance * (risk_per_trade_pct / 100.0)
    risk_per_share = abs(entry_price - stop_loss_price)
    
    raw_quantity = risk_amount / risk_per_share
    lots = max(1, math.floor(raw_quantity / lot_size)) if raw_quantity >= lot_size else 0
    total_quantity = lots * lot_size if lot_size > 1 else math.floor(raw_quantity)
    
    return {
        "quantity": int(total_quantity),
        "lots": int(lots) if lot_size > 1 else int(total_quantity),
        "risk_amount": round(risk_amount, 2)
    }
