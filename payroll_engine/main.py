import csv
import os
from payroll_engine.tax import calculate_tax
from payroll_engine.pension import employee_pension, employer_pension

def validate_employee_row(row, line_num):
    """Validate a single CSV row. Returns (basic, allowances) or raises ValueError."""
    required = ['employee_id', 'name', 'basic_salary', 'allowances']
    for field in required:
        if field not in row or row[field] is None or row[field].strip() == '':
            raise ValueError(f"Line {line_num}: Missing or empty required field '{field}'")
    try:
        basic = float(row['basic_salary'])
    except ValueError:
        raise ValueError(f"Line {line_num}: basic_salary must be a number")
    if basic < 0:
        raise ValueError(f"Line {line_num}: basic_salary must be non-negative")
    try:
        allow = float(row['allowances'])
    except ValueError:
        raise ValueError(f"Line {line_num}: allowances must be a number")
    if allow < 0:
        raise ValueError(f"Line {line_num}: allowances must be non-negative")
    return basic, allow

def process_payroll(csv_path):
    """Process a CSV file of employees and return payroll results."""
    employees = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV file is empty or has no headers")
        missing = [f for f in ['employee_id', 'name', 'basic_salary', 'allowances'] if f not in reader.fieldnames]
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")
        for line_num, row in enumerate(reader, start=2):
            try:
                basic, allow = validate_employee_row(row, line_num)
            except ValueError as e:
                raise ValueError(str(e))
            gross = basic + allow
            tax = calculate_tax(gross)
            emp_pen = employee_pension(basic)
            emp_pen_total = employer_pension(basic)
            net = gross - tax - emp_pen
            employees.append({
                'id': row['employee_id'].strip(),
                'name': row['name'].strip(),
                'basic': basic,
                'allowances': allow,
                'gross': gross,
                'tax': tax,
                'pension_employee': emp_pen,
                'pension_employer': emp_pen_total,
                'net': net,
                'bank': row.get('bank_or_telebirr', '').strip()
            })
    if len(employees) == 0:
        raise ValueError("No data rows in CSV")
    return employees

def generate_tax_explanation(gross, tax_amount):
    """Generate a plain-language English explanation of the tax calculation."""
    brackets = [
        (0, 2000, 0.0),
        (2000, 4000, 0.15),
        (4000, 7000, 0.20),
        (7000, 10000, 0.25),
        (10000, 14000, 0.30),
        (14000, float('inf'), 0.35)
    ]
    lines = [f"Gross salary: ETB {gross:,.2f}", ""]
    remaining = gross
    total = 0.0
    for lower, upper, rate in brackets:
        if remaining <= 0:
            break
        taxable = min(remaining, upper - lower)
        bracket_tax = taxable * rate
        total += bracket_tax
        if taxable > 0:
            if rate == 0:
                lines.append(f"  ETB {lower:,.0f} - ETB {upper:,.0f} @ 0%  =  ETB 0.00  (tax-free)")
            else:
                lines.append(f"  ETB {lower:,.0f} - ETB {upper:,.0f} @ {rate*100:.0f}% =  ETB {bracket_tax:,.2f}")
        remaining -= taxable
    lines.append("")
    lines.append(f"Total tax: ETB {total:,.2f}")
    return "\n".join(lines)

if __name__ == '__main__':
    csv_path = 'sample_employees.csv'
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        exit(1)
    emps = process_payroll(csv_path)
    print('Ethiopian Payroll Engine - Sample Output')
    print('=' * 60)
    for emp in emps:
        print(f"ID: {emp['id']}  |  Name: {emp['name']}")
        print(f"  Basic: ETB {emp['basic']:,.2f}  |  Allowances: ETB {emp['allowances']:,.2f}")
        print(f"  Gross: ETB {emp['gross']:,.2f}")
        print(f"  Tax: ETB {emp['tax']:,.2f}")
        print(f"  Employee Pension (7%): ETB {emp['pension_employee']:,.2f}")
        print(f"  Employer Pension (11%): ETB {emp['pension_employer']:,.2f}")
        print(f"  Net Pay: ETB {emp['net']:,.2f}")
        print(f"  Payment: {emp['bank']}")
        print('-' * 60)
    total_gross = sum(e['gross'] for e in emps)
    total_tax = sum(e['tax'] for e in emps)
    total_net = sum(e['net'] for e in emps)
    print(f"Summary: {len(emps)} employees")
    print(f"  Total Gross: ETB {total_gross:,.2f}")
    print(f"  Total Tax:   ETB {total_tax:,.2f}")
    print(f"  Total Net:   ETB {total_net:,.2f}")