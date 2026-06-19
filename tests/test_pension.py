import sys
sys.path.insert(0, 'payroll_engine')
from pension import employee_pension, employer_pension

def test_employee_pension():
    assert employee_pension(5000) == 350.0

def test_employer_pension():
    assert employer_pension(5000) == 550.0

def test_employee_pension_zero():
    assert employee_pension(0) == 0.0

def test_employer_pension_zero():
    assert employer_pension(0) == 0.0

def test_employee_pension_fraction():
    assert employee_pension(1234.56) == 1234.56 * 0.07

def test_employer_pension_fraction():
    assert employer_pension(1234.56) == 1234.56 * 0.11
