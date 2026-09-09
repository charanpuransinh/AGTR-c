from src.setup_c.engine_05_option.advanced_analytics import calculate_pcr, calculate_max_pain, detect_gamma_blast

def test_pcr_calculation():
    pcr = calculate_pcr(1500000, 1000000)
    assert pcr == 1.5

def test_max_pain_calculation():
    strikes = [21800, 21900, 22000]
    call_oi = [50000, 120000, 300000]
    put_oi = [250000, 100000, 40000]
    max_pain = calculate_max_pain(strikes, call_oi, put_oi)
    assert max_pain in strikes

def test_gamma_blast():
    res = detect_gamma_blast(spot_price=22000, strike_price=22000, gamma=0.08, iv=0.15)
    assert res["gamma_blast_active"] == True
