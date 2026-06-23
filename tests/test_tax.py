import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from payroll_engine.tax import calculate_tax

def test_tax_bracket_zero():
    assert calculate_tax(1500) == 0.0

def test_tax_bracket_15():
    assert calculate_tax(3000) == 150.0  # (3000-2000)*0.15

def test_tax_bracket_20():
    assert calculate_tax(5000) == 500.0  # (2000*0.15)+(1000*0.20)=300+200=500

def test_tax_bracket_35():
    # 20000 gross:
    # 0-2000: 0
    # 2000-4000: 2000*0.15 = 300
    # 4000-7000: 3000*0.20 = 600
    # 7000-10000: 3000*0.25 = 750
    # 10000-14000: 4000*0.30 = 1200
    # 14000-20000: 6000*0.35 = 2100
    # Total = 300+600+750+1200+2100 = 4950
    assert calculate_tax(20000) == 4950.0

def test_tax_bracket_edge():
    assert calculate_tax(2000) == 0.0
    assert calculate_tax(2001) == (2001-2000)*0.15  # 0.15
    assert calculate_tax(4000) == (4000-2000)*0.15  # 300.0
    assert calculate_tax(4001) == (2000*0.15)+(1*0.20)  # 300.0+0.20=300.20
    assert calculate_tax(7000) == (2000*0.15)+(3000*0.20)  # 300+600=900
    assert calculate_tax(7001) == (2000*0.15)+(3000*0.20)+(1*0.25)  # 900+0.25=900.25
    assert calculate_tax(10000) == (2000*0.15)+(3000*0.20)+(3000*0.25)  # 300+600+750=1650
    assert calculate_tax(10001) == 1650 + (1*0.30)  # 1650.30
    assert calculate_tax(14000) == (2000*0.15)+(3000*0.20)+(3000*0.25)+(4000*0.30)  # 300+600+750+1200=2850
    assert calculate_tax(14001) == 2850 + (1*0.35)  # 2850.35

if __name__ == '__main__':
    test_tax_bracket_zero()
    test_tax_bracket_15()
    test_tax_bracket_20()
    test_tax_bracket_35()
    test_tax_bracket_edge()
    print("All tax tests passed")
