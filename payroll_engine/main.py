import csv
import os
from payroll_engine.tax import calculate_tax
from payroll_engine.pension import employee_pension, employer_pension
from payroll_engine.pdf import generate_payslip
from payroll_engine.disbursement import record_disbursement_intent, confirm_disbursement

def validate_employee_row(row, line_num):
    required = ['employee_id', 'name', 'basic_salary', 'allowances']
    for field in required:
        if field not in row or row[field] is None or row[field].strip() == '':
            raise ValueError(f"Line {line_num}: Missing or empty required field '{field}'")
    # basic_salary
    try:
        basic = float(row['basic_salary'])
    except ValueError:
        raise ValueError(f"Line {line_num}: basic_salary must be a number")
    if basic < 0:
        raise ValueError(f"Line {line_num}: basic_salary must be non-negative")
    # allowances
    try:
        allow = float(row['allowances'])
    except ValueError:
        raise ValueError(f"Line {line_num}: allowances must be a number")
    if allow < 0:
        raise ValueError(f"Line {line_num}: allowances must be non-negative")
    # bank_or_telebirr is optional
    return basic, allow

def process_payroll(csv_path):
    employees = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # Check that required columns exist
        if not reader.fieldnames:
            raise ValueError("CSV file is empty or has no headers")
        missing = [f for f in ['employee_id', 'name', 'basic_salary', 'allowances'] if f not in reader.fieldnames]
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")
        for line_num, row in enumerate(reader, start=2):  # line 1 is header
            try:
                basic, allow = validate_employee_row(row, line_num)
            except ValueError as e:
                raise ValueError(str(e))
            gross = basic + allow
            tax = calculate_tax(gross)
            emp_pen = employee_pension(basic)
            emp_pen_total = employer_pension(basic)
            net = gross - tax - emp_pen
            # Record disbursement intent
            intent_record = record_disbursement_intent(row['employee_id'], net)
            # Optionally confirm immediately (for demo)
            # confirm_disbursement(intent_record['intent_id'])
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
                'bank': row.get('bank_or_telebirr', ''),
                'disbursement_intent_id': intent_record['intent_id'],
                'disbursement_status': intent_record['status']
            })
    if len(employees) == 0:
        raise ValueError("No data rows in CSV")
    return employees

if __name__ == '__main__':
    emps = process_payroll('sample_employees.csv')
    print('Ethiopian Payroll Engine - Sample Output')
    print('='*60)
    pdf_files = []
    disbursement_intents = []
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
        print(f"Disbursement Intent ID: {emp['disbursement_intent_id']}")
        print(f"Disbursement Status: {emp['disbursement_status']}")
        print('-'*60)
        pdf_file = generate_payslip(emp)
        pdf_files.append(pdf_file)
        disbursement_intents.append(emp['disbursement_intent_id'])
    total_gross = sum(e['gross'] for e in emps)
    total_tax = sum(e['tax'] for e in emps)
    total_net = sum(e['net'] for e in emps)
    print('Summary')
    print('='*60)
    print(f"Total Employees: {len(emps)}")
    print(f"Total Gross Payroll: ETB {total_gross:,.2f}")
    print(f"Total Tax Withheld: ETB {total_tax:,.2f}")
    print(f"Total Net Pay: ETB {total_net:,.2f}")
    print(f"Generated PDF payslips: {', '.join(pdf_files)}")
    print(f"Recorded disbursement intents: {len(disbursement_intents)}")
    # Optionally confirm all intents
    # for intent_id in disbursement_intents:
    #     confirm_disbursement(intent_id)
    # print("All disbursements confirmed.")
