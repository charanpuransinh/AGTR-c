import sys
from src.setup_c.engine_01_orchestrator.main_pipeline import run_strategy_pipeline

def main():
    print("Initializing ARGT Setup C Trading Framework...")
    sample_prices = [100 + i * 0.5 for i in range(25)]
    result = run_strategy_pipeline(sample_prices, account_balance=200000, symbol="NIFTY")
    print(f"Pipeline Execution Status: {result}")

if __name__ == "__main__":
    main()
