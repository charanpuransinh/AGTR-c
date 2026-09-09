from src.setup_c.engine_01_orchestrator.main_pipeline import run_strategy_pipeline
from src.setup_c.engine_05_option.greeks import calculate_delta

def test_full_integration_sanity():
    prices = [150 + i for i in range(20)]
    pipeline_res = run_strategy_pipeline(prices, 150000, "FINNIFTY")
    delta_res = calculate_delta(100, 100, 0.1, 0.05, 0.2, 'CE')
    
    assert pipeline_res["status"] in ["SIGNAL_EXECUTED", "NO_SIGNAL", "INSUFFICIENT_DATA"]
    assert 0.4 <= delta_res <= 0.6
