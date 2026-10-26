def test_lock(direct_deploy):
    c = direct_deploy('contracts/claimtrace.py')
    assert c.lock_claim('Synthetic Atlas report published ten records.', '["The report confirms ten records."]') == '1'
