from src.setup_c.engine_05_option.greeks import calculate_delta, calculate_gamma

def test_delta_call_put():
    ce_delta = calculate_delta(S=100, K=100, T=0.25, r=0.05, sigma=0.2, option_type='CE')
    pe_delta = calculate_delta(S=100, K=100, T=0.25, r=0.05, sigma=0.2, option_type='PE')
    assert 0.4 <= ce_delta <= 0.6
    assert -0.6 <= pe_delta <= -0.4

def test_zero_time_to_expiry():
    delta = calculate_delta(S=100, K=100, T=0.0, r=0.05, sigma=0.2, option_type='CE')
    gamma = calculate_gamma(S=100, K=100, T=0.0, r=0.05, sigma=0.2)
    assert delta == 0.0
    assert gamma == 0.0
