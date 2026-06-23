import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from payroll_engine.main import process_payroll, validate_employee_row

def test_validate_employee_row():
    # Valid row
    row = {'employee_id': 'E001', 'name': 'Test', 'basic_salary': '5000', 'allowances': '200'}
    basic, allow = validate_employee_row(row, 2)
    assert basic == 5000.0
    assert allow == 200.0

    # Missing employee_id
    row = {'employee_id': '', 'name': 'Test', 'basic_salary': '5000', 'allowances': '200'}
    try:
        validate_employee_row(row, 2)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Missing or empty required field 'employee_id'" in str(e)

    # Negative basic_salary
    row = {'employee_id': 'E001', 'name': 'Test', 'basic_salary': '-100', 'allowances': '200'}
    try:
        validate_employee_row(row, 2)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "basic_salary must be non-negative" in str(e)

    # Non-numeric basic_salary
    row = {'employee_id': 'E001', 'name': 'Test', 'basic_salary': 'abc', 'allowances': '200'}
    try:
        validate_employee_row(row, 2)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "basic_salary must be a number" in str(e)

def test_process_payroll_valid():
    csv_content = """employee_id,name,basic_salary,allowances,bank_or_telebirr
E001,Alemayehu,3500,500,Telebirr:0911111111
E002,Belay,8000,1000,Bank:CBE12345
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        fname = f.name
    try:
        employees = process_payroll(fname)
        assert len(employees) == 2
        assert employees[0]['id'] == 'E001'
        assert employees[0]['basic'] == 3500.0
        assert employees[0]['allowances'] == 500.0
        assert employees[0]['gross'] == 4000.0
        assert employees[0]['tax'] == 300.0
        assert employees[0]['pension_employee'] == 3500.0 * 0.07
        assert employees[0]['pension_employer'] == 3500.0 * 0.11
        assert employees[0]['net'] == 4000.0 - 300.0 - (3500.0*0.07)
        # Second employee
        assert employees[1]['id'] == 'E002'
        assert employees[1]['basic'] == 8000.0
        assert employees[1]['allowances'] == 1000.0
        assert employees[1]['gross'] == 9000.0
        assert employees[1]['tax'] == 1400.0
        assert employees[1]['pension_employee'] == 8000.0 * 0.07
        assert employees[1]['pension_employer'] == 8000.0 * 0.11
        assert employees[1]['net'] == 9000.0 - 1400.0 - (8000.0*0.07)
    finally:
        os.unlink(fname)

def test_process_payroll_missing_column():
    csv_content = """employee_id,name,basic_salary
E001,Alemayehu,3500,500,Telebirr:0911111111
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        fname = f.name
    try:
        try:
            process_payroll(fname)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Missing required columns" in str(e)
            assert "allowances" in str(e)
    finally:
        os.unlink(fname)

def test_process_payroll_empty_file():
    csv_content = """employee_id,name,basic_salary,allowances,bank_or_telebirr
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        fname = f.name
    try:
        try:
            process_payroll(fname)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "No data rows in CSV" in str(e)
    finally:
        os.unlink(fname)

if __name__ == '__main__':
    test_validate_employee_row()
    test_process_payroll_valid()
    test_process_payroll_missing_column()
    test_process_payroll_empty_file()
    print("All tests passed")
