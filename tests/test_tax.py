import sys
sys.path.insert(0, 'payroll_engine')
from tax import calculate_tax

def test_tax_bracket_zero():
    assert calculate_tax(1500) == 0.0

def test_tax_bracket_15():
    assert calculate_tax(3000) == (3000-2000)*0.15  # 150

def test_tax_bracket_20():
    assert calculate_tax(5000) == (2000*0.15)+(3000-4000)*0.20  # 300 + 200 = 500

def test_tax_bracket_35():
    assert calculate_tax(20000) == (2000*0)+(2000*0.15)+(3000*0.20)+(3000*0.25)+(4000*0.30)+(6000*0.35)  # compute