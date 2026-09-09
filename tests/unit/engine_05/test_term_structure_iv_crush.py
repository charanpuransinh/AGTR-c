from src.setup_c.engine_05_option.term_structure_iv_crush import calculate_variance_risk_premium, detect_iv_crush, analyze_term_structure, analyze_zero_dte_metrics

def test_vrp():
    vrp = calculate_variance_risk_premium(0.18, 0.12)
    assert vrp == 0.06

def test_iv_crush():
    res = detect_iv_crush(0.12, 0.18, drop_threshold_pct=20.0)
    assert res["iv_crush_detected"] == True

def test_term_structure():
    dte_list = [1, 7, 30]
    iv_list = [0.22, 0.18, 0.15]
    structure = analyze_term_structure(dte_list, iv_list)
    assert structure == "BACKWARDATION"

def test_0dte():
    res = analyze_zero_dte_metrics(22000, 22000, 45.0, 0.5)
    assert res["is_0dte"] == True
    assert res["atm_zero_dte_trigger"] == True
