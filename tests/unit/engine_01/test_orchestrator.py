from src.setup_c.engine_01_orchestrator.main_pipeline import run_strategy_pipeline

def test_pipeline_execution():
    prices = [100 + i for i in range(20)]
    res = run_strategy_pipeline(prices, account_balance=100000, symbol="BANKNIFTY")
    assert res["status"] in ["SIGNAL_EXECUTED", "NO_SIGNAL"]
