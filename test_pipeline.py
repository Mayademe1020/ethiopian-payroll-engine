import os
import sys
import tempfile

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from payroll_engine.tax import calculate_tax
from payroll_engine.pension import employee_pension, employer_pension
from payroll_engine.main import generate_tax_explanation

print("=" * 60)
print("  Ethiopian Payroll Engine — Direct Test")
print("=" * 60)

# Test tax calculation
test_cases = [
    (1500, 0.0, "Tax-free bracket"),
    (3000, 150.0, "15% bracket"),
    (5000, 500.0, "Mixed brackets"),
    (8500, 1550.0, "Multiple brackets"),
    (16000, 4950.0, "Top bracket"),
]

print("\n--- Tax Calculation Tests ---")
all_pass = True
for gross, expected, label in test_cases:
    result = calculate_tax(gross)
    status = "PASS" if abs(result - expected) < 0.01 else "FAIL"
    if status == "FAIL":
        all_pass = False
    print(f"  [{status}] ETB {gross:,.0f} -> Tax: ETB {result:,.2f} (expected ETB {expected:,.2f}) — {label}")

# Test pension
print("\n--- Pension Tests ---")
basic = 5000
emp_pen = employee_pension(basic)
emp_pen_total = employer_pension(basic)
print(f"  Basic: ETB {basic:,.2f}")
print(f"  Employee pension (7%): ETB {emp_pen:,.2f} (expected ETB {basic * 0.07:,.2f})")
print(f"  Employer pension (11%): ETB {emp_pen_total:,.2f} (expected ETB {basic * 0.11:,.2f})")

# Test tax explanation
print("\n--- Tax Explanation (ETB 8,500 gross) ---")
explanation = generate_tax_explanation(8500, 1550)
print(explanation)

print("\n" + "=" * 60)
if all_pass:
    print("  All tests PASSED")
else:
    print("  Some tests FAILED")
print("=" * 60)
