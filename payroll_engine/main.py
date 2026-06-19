import csv
from payroll_engine.tax import calculate_tax
from payroll_engine.pension import employee_pension, employer_pension

def process_payroll(csv_path):
    employees = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            basic = float(row['basic_salary'])
            allow = float(row['allowances'])
            gross = basic + allow
            tax = calculate_tax(gross)
            emp_pen = employee_pension(basic)
            emp_pen_total = employer_pension(basic)
            net = gross - tax - emp_pen
            employees.append({
                'id': row['employee_id'],
                'name': row['name'],
                'basic': basic,
                'allowances': allow,
                'gross': gross,
                'tax': tax,
                'pension_employee': emp_pen,
                'pension_employer': emp_pen_total,
                'net': net,
                'bank': row['bank_or_telebirr']
            })
    return employees

if __name__ == '__main__':
    emps = process_payroll('sample_employees.csv')
    print('Ethiopian Payroll Engine - Sample Output')
    print('='*60)
    for emp in emps:
        print(f"Employee ID: {emp['id']}")
        print(f"Name: {emp['name']}")
        print(f"Basic Salary: ETB {emp['basic']:,.2f}")
        print(f"Allowances: ETB {emp['allowances']:,.2f}")
        print(f"Gross Salary: ETB {emp['gross']:,.2f}")
        print(f"Income Tax (2025): ETB {emp['tax']:,.2f}")
        print(f"Employee Pension (7%): ETB {emp['pension_employee']:,.2f}")
        print(f"Employer Pension (11%): ETB {emp['pension_employer']:,.2f}")
        print(f"Net Pay: ETB {emp['net']:,.2f}")
        print(f"Payment Method: {emp['bank']}")
        print('-'*60)
    total_gross = sum(e['gross'] for e in emps)
    total_tax = sum(e['tax'] for e in emps)
    total_net = sum(e['net'] for e in emps)
    print('Summary')
    print('='*60)
    print(f"Total Employees: {len(emps)}")
    print(f"Total Gross Payroll: ETB {total_gross:,.2f}")
    print(f"Total Tax Withheld: ETB {total_tax:,.2f}")
    print(f"Total Net Pay: ETB {total_net:,.2f}")
