import sys
import os
sys.path.insert(0, r'D:\ethiopian_payroll_engine')

print("=== Ethiopian Payroll Engine - Test Run ===")
print()

# Test 1: Tax calculation
print("1. Testing tax calculation...")
from payroll_engine.tax import calculate_tax
test_cases = [
    (1500, 0.0),
    (3000, 150.0),
    (5000, 500.0),
    (8000, 950.0),
    (12000, 1750.0),
    (20000, 4950.0),
]
for gross, expected in test_cases:
    result = calculate_tax(gross)
    status = "PASS" if abs(result - expected) < 0.01 else "FAIL"
    print(f"   Tax for ETB {gross}: ETB {result:.2f} (expected {expected}) [{status}]")

# Test 2: Pension calculation
print("\n2. Testing pension calculation...")
from payroll_engine.pension import employee_pension, employer_pension
basic = 5000
emp = employee_pension(basic)
emp_total = employer_pension(basic)
print(f"   Employee pension (7% of {basic}): ETB {emp:.2f} (expected 350.00)")
print(f"   Employer pension (11% of {basic}): ETB {emp_total:.2f} (expected 550.00)")

# Test 3: Tax explanation
print("\n3. Testing tax explanation...")
from payroll_engine.main import generate_tax_explanation
explanation = generate_tax_explanation(5000, 500)
print(f"   Explanation generated: {len(explanation)} chars")
print(f"   First 100 chars: {explanation[:100]}...")

# Test 4: Telegram module import
print("\n4. Testing Telegram module import...")
try:
    from payroll_engine.telegram import send_payslip_notification_sync
    print("   Telegram module imported successfully")
except Exception as e:
    print(f"   Telegram module import error: {e}")

# Test 5: Full pipeline with sample CSV
print("\n5. Testing full payroll pipeline with sample_employees.csv...")
from payroll_engine.main import process_payroll
employees = process_payroll(r'D:\ethiopian_payroll_engine\sample_employees.csv')
print(f"   Processed {len(employees)} employees:")
for emp in employees:
    telegram_info = emp.get('telegram_id', 'N/A')
    print(f"   - {emp['id']} {emp['name']}: Gross={emp['gross']:.0f}, Tax={emp['tax']:.0f}, Net={emp['net']:.0f}, Telegram={telegram_info}")

print()
print("=== All tests completed ===")
