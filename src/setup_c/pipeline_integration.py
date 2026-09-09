from src.setup_c.engine_05_option.master_option_engine import run_complete_option_analysis

def evaluate_option_signals(market_data: dict) -> dict:
    """
    Integrates Engine 05 Option Intelligence into the Master Trading Pipeline.
    Evaluates institutional walls, gamma flip, GEX bias, and build-ups to generate actionable triggers.
    """
    analysis = run_complete_option_analysis(market_data)
    
    if analysis.get("status") != "ENGINE_05_SUCCESS":
        return {"signal": "NEUTRAL", "reason": "Engine 05 analysis failed"}
        
    dealer_pos = analysis["dealer_positioning"]
    skew_buildup = analysis["skew_and_buildup"]
    
    call_wall = dealer_pos.get("call_wall", 0.0)
    put_wall = dealer_pos.get("put_wall", 0.0)
    spot = market_data.get("spot_price", 0.0)
    buildup = skew_buildup.get("buildup", "NEUTRAL")
    
    # Decision Matrix based on institutional walls and build-ups
    signal = "HOLD"
    score = 0.0
    
    if buildup == "LONG_BUILDUP" and spot > put_wall:
        signal = "BULLISH_MOMENTUM"
        score += 75.0
    elif buildup == "SHORT_BUILDUP" and spot < call_wall:
        signal = "BEARISH_PRESSURE"
        score += 75.0
    elif buildup == "SHORT_COVERING":
        signal = "BULLISH_REVERSAL"
        score += 65.0
    elif buildup == "LONG_UNWINDING":
        signal = "BEARISH_CORRECTION"
        score += 65.0
        
    return {
        "pipeline_status": "ACTIVE",
        "signal": signal,
        "confidence_score": score,
        "call_wall": call_wall,
        "put_wall": put_wall,
        "net_gex": dealer_pos.get("total_net_gex", 0.0)
    }
