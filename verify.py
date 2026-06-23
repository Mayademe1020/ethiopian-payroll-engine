import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from payroll_engine.tax import calculate_tax
from payroll_engine.pension import employee_pension, employer_pension
from payroll_engine.main import generate_tax_explanation

print("=" * 60)
print("  Ethiopian Payroll Engine — Verification")
print("=" * 60)

# Test tax calculation (correct expected values)
test_cases = [
    (1500, 0.0, "Tax-free bracket"),
    (3000, 150.0, "15% bracket"),
    (5000, 500.0, "Mixed brackets"),
    (8500, 1275.0, "Multiple brackets"),
    (16000, 3550.0, "Top bracket"),
    (2000, 0.0, "Boundary: exactly 2000"),
    (2001, 0.15, "Boundary: just above 2000"),
    (4000, 300.0, "Boundary: exactly 4000"),
    (4001, 300.2, "Boundary: just above 4000"),
    (14000, 2750.0, "Boundary: exactly 14000"),
    (14001, 2750.35, "Boundary: just above 14000"),
]

print("\n--- Tax Calculation Tests ---")
all_pass = True
for gross, expected, label in test_cases:
    result = calculate_tax(gross)
    status = "PASS" if abs(result - expected) < 0.02 else "FAIL"
    if status == "FAIL":
        all_pass = False
    print(f"  [{status}] ETB {gross:>8,.0f} -> Tax: ETB {result:>10,.2f} (expected ETB {expected:>10,.2f}) — {label}")

# Test pension
print("\n--- Pension Tests ---")
for basic in [3500, 8000, 12000, 16000]:
    emp_pen = employee_pension(basic)
    emp_pen_total = employer_pension(basic)
    print(f"  Basic: ETB {basic:>8,.0f} | Employee (7%): ETB {emp_pen:>8,.2f} | Employer (11%): ETB {emp_pen_total:>9,.2f}")

# Test tax explanation
print("\n--- Tax Explanation (ETB 8,500 gross) ---")
explanation = generate_tax_explanation(8500, 1275)
print(explanation)

print("\n" + "=" * 60)
if all_pass:
    print("  All tests PASSED")
else:
    print("  Some tests FAILED")
print("=" * 60)
