def validate_risk_parameters(execution_brackets: dict, account_balance: float, risk_percentage: float = 1.0) -> dict:
    entry = execution_brackets.get("entry", 0.0)
    stop_loss = execution_brackets.get("stop_loss", 0.0)
    risk_per_unit = abs(entry - stop_loss)
    if risk_per_unit == 0:
        return {"status": "INVALID_RISK", "quantity": 0}
    max_capital_risk = account_balance * (risk_percentage / 100.0)
    position_quantity = int(max_capital_risk / risk_per_unit)
    return {
        "status": "APPROVED",
        "risk_per_unit": round(risk_per_unit, 2),
        "max_capital_risk": round(max_capital_risk, 2),
        "recommended_quantity": max(position_quantity, 1)
    }
