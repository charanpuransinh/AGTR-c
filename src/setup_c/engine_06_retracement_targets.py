import numpy as np

def calculate_fibonacci_retracements(high: float, low: float, trend: str = "BULLISH") -> dict:
    """
    Computes precise Fibonacci Retracement entry zones (Golden Pocket) 
    and Extension profit targets automatically based on swing high and low.
    """
    diff = high - low
    if trend == "BULLISH":
        levels = {
            "entry_0_382": high - (diff * 0.382),
            "entry_0_500": high - (diff * 0.500),
            "golden_pocket_0_618": high - (diff * 0.618),
            "target_1_272": high + (diff * 0.272),
            "target_1_618": high + (diff * 0.618),
            "target_2_618": high + (diff * 1.618)
        }
    else:
        levels = {
            "entry_0_382": low + (diff * 0.382),
            "entry_0_500": low + (diff * 0.500),
            "golden_pocket_0_618": low + (diff * 0.618),
            "target_1_272": low - (diff * 0.272),
            "target_1_618": low - (diff * 0.618),
            "target_2_618": low - (diff * 1.618)
        }
    return levels

def calculate_measured_move_target(leg_a_start: float, leg_a_end: float, retracement_end: float) -> dict:
    """
    Calculates ABCD / Measured Move price targets where Leg C = Leg A projection.
    """
    leg_size = abs(leg_a_end - leg_a_start)
    if leg_a_end > leg_a_start:
        target = retracement_end + leg_size
    else:
        target = retracement_end - leg_size
        
    return {
        "measured_move_target": target,
        "projected_leg_size": leg_size
    }

def calculate_atr_dynamic_brackets(entry_price: float, atr: float, multiplier_sl: float = 1.5, multiplier_tp: float = 3.0, direction: str = "BUY") -> dict:
    """
    Calculates dynamic ATR-based Stop Loss and Risk-Reward Targets.
    """
    if direction == "BUY":
        stop_loss = entry_price - (atr * multiplier_sl)
        target_1 = entry_price + (atr * multiplier_tp)
        target_2 = entry_price + (atr * (multiplier_tp * 1.5))
    else:
        stop_loss = entry_price + (atr * multiplier_sl)
        target_1 = entry_price - (atr * multiplier_tp)
        target_2 = entry_price - (atr * (multiplier_tp * 1.5))
        
    risk = abs(entry_price - stop_loss)
    reward = abs(target_1 - entry_price)
    risk_reward_ratio = round(reward / risk, 2) if risk > 0 else 0.0
    
    return {
        "entry": entry_price,
        "stop_loss": round(stop_loss, 2),
        "target_1": round(target_1, 2),
        "target_2": round(target_2, 2),
        "risk_reward_ratio": risk_reward_ratio
    }
