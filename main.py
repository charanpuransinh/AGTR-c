import pandas as pd
import numpy as np
from src.setup_c.master_pipeline import run_master_institutional_pipeline
from src.setup_c.engine_11_risk_manager import validate_risk_parameters

def execute_trading_system():
    np.random.seed(42)
    n = 100
    df = pd.DataFrame({
        'open': np.linspace(21000, 22000, n),
        'high': np.linspace(21100, 22100, n),
        'low': np.linspace(20900, 21900, n),
        'close': np.linspace(21050, 22050, n),
        'volume': np.random.randint(5000, 25000, n)
    })
    
    current_price = float(df['close'].iloc[-1])
    current_atr = 75.5
    account_balance = 500000.0
    
    pipeline_output = run_master_institutional_pipeline(df, current_price, current_atr)
    risk_output = validate_risk_parameters(
        pipeline_output["execution_brackets"], 
        account_balance=account_balance, 
        risk_percentage=1.0
    )
    
    print("==========================================")
    print(" AGTR SETUP C: MASTER EXECUTION REPORT")
    print("==========================================")
    print(f"Signal Bias      : {pipeline_output['signal_bias']}")
    print(f"Confluence Score : {pipeline_output['master_confluence_score']} / 100")
    print(f"Entry Price      : {pipeline_output['execution_brackets']['entry']}")
    print(f"Stop Loss        : {pipeline_output['execution_brackets']['stop_loss']}")
    print(f"Target 1         : {pipeline_output['execution_brackets']['target_1']}")
    print(f"Risk-Reward Ratio: {pipeline_output['execution_brackets']['risk_reward_ratio']}")
    print(f"Position Sizing  : {risk_output['recommended_quantity']} units")
    print("==========================================")

if __name__ == "__main__":
    execute_trading_system()
