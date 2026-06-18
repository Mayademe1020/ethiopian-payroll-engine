# Ethiopian Payroll Engine Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a core Ethiopian payroll engine that correctly calculates income tax (2025 brackets), POSSA pension (employee 7%, employer 11%), generates payslip and compliance PDFs, and supports CSV/Excel import for SME accountants.

**Architecture:** Modular Python backend with separate modules for tax calculation, pension, payslip generation (ReportLab), and data import. Offline-first Android front‑end (React Native) will call the same Python logic via a lightweight API or reuse the same code via Pyodide for MVP.

**Tech Stack:** Python 3.11, pandas (optional), ReportLab for PDF, CSV module for import, SQLite for offline storage, React Native/Expo for mobile, Telebirr API stub (later real), Docker for deployment.

---

### Task 1: Set up project skeleton and dependencies

**Objective:** Create repository structure, virtual environment, and lock required packages.

**Files:**
- Create: `payroll_engine/requirements.txt`
- Create: `payroll_engine/__init__.py` (empty)
- Create: `payroll_engine/tax.py`
- Create: `payroll_engine/pension.py`
- Create: `payroll_engine/payslip.py`
- Create: `payroll_engine/main.py` (entry point)
- Create: `tests/__init__.py`
- Create: `tests/test_tax.py`
- Create: `tests/test_pension.py`
- Create: `.gitignore`

**Step 1: Write requirements.txt**
```
reportlab>=3.6.0
pandas>=2.0.0   # optional for CSV handling
```
**Step 2: Install dependencies (simulated)** - In real environment run `pip install -r requirements.txt`.

**Step 3: Commit**
```bash
git add payroll_engine/requirements.txt payroll_engine/__init__.py payroll_engine/tax.py payroll_engine/pension.py payroll_engine/payslip.py payroll_engine/main.py tests/__init__.py tests/test_tax.py tests/test_pension.py .gitignore
git commit -m "feat: initialize project skeleton"
```

### Task 2: Implement tax calculation (TDD)

**Objective:** Implement `calculate_tax(gross)` according to 2025 Ethiopian brackets.

**Files:**
- Modify: `payroll_engine/tax.py`
- Modify: `tests/test_tax.py`

**Step 1: Write failing test**
```python
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
```

**Step 2: Run test to verify failure** - Expect FAIL (function not defined).

**Step 3: Write minimal implementation**
```python
def calculate_tax(gross):
    brackets = [
        (0, 2000, 0.0),
        (2001, 4000, 0.15),
        (4001, 7000, 0.20),
        (7001, 10000, 0.25),
        (10001, 14000, 0.30),
        (14001, float('inf'), 0.35)
    ]
    tax = 0.0
    for lower, upper, rate in brackets:
        if gross > lower:
            taxable = min(gross, upper) - lower
            if taxable > 0:
                tax += taxable * rate
        else:
            break
    return tax
```

**Step 4: Run test to verify pass** - Expect PASS.

**Step 5: Commit**
```bash
git add payroll_engine/tax.py tests/test_tax.py
git commit -m "feat: implement tax calculation with TDD"
```

### Task 3: Implement pension calculation (TDD)

**Objective:** Implement employee (7%) and employer (11%) pension on basic salary.

**Files:**
- Modify: `payroll_engine/pension.py`
- Modify: `tests/test_pension.py`

**Step 1: Write failing test**
```python
import sys
sys.path.insert(0, 'payroll_engine')
from pension import employee_pension, employer_pension

def test_employee_pension():
    assert employee_pension(5000) == 350.0

def test_employer_pension():
    assert employer_pension(5000) == 550.0
```

**Step 2: Run test to verify failure**.

**Step 3: Write minimal implementation**
```python
def employee_pension(basic):
    return basic * 0.07

def employer_pension(basic):
    return basic * 0.11
```

**Step 4: Run test to verify pass**.

**Step 5: Commit**
```bash
git add payroll_engine/pension.py tests/test_pension.py
git commit -m "feat: implement pension calculations"
```

### Task 4: Integrate tax, pension, and net pay in main processing script

**Objective:** Create `main.py` that reads CSV, computes tax, pension, net, and prints payslip‑like output.

**Files:**
- Create: `sample_employees.csv` (provided)
- Modify: `payroll_engine/main.py`

**Step 1: Write script skeleton**
```python
import csv
from tax import calculate_tax
from pension import employee_pension, employer_pension

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
    for e in emps:
        print(f"Employee {e['id']} - {e['name']}: Gross {e['gross']:.2f}, Tax {e['tax']:.2f}, Net {e['net']:.2f}")
```

**Step 2: Run script to verify output matches earlier demonstration**.

**Step 3: Commit**
```bash
git add sample_employees.csv payroll_engine/main.py
git commit -m "feat: create main payroll processing script"
```

### Task 5: Add PDF payslip generation using ReportLab

**Objective:** Create a function that, given an employee record, outputs a PDF payslip (Amharic + English) to a folder.

**Files:**
- Create: `payroll_engine/pdf.py`
- Modify: `payroll_engine/main.py` to call PDF generation
- Create: `output_payslips/` directory

**Step 1: Write failing test (optional)** – we can manually verify.

**Step 2: Implement PDF generation**
```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os

def generate_payslip(emp, out_dir='output_payslips'):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    filename = os.path.join(out_dir, f"payslip_{emp['id']}.pdf")
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    # Simple layout
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30*mm, height-20*mm, "Employee Payslip")
    c.setFont("Helvetica", 10)
    c.drawString(30*mm, height-30*mm, f"ID: {emp['id']}")
    c.drawString(30*mm, height-35*mm, f"Name: {emp['name']}")
    c.drawString(30*mm, height-40*mm, f"Basic Salary: ETB {emp['basic']:,.2f}")
    c.drawString(30*mm, height-45*mm, f"Allowances: ETB {emp['allowances']:,.2f}")
    c.drawString(30*mm, height-50*mm, f"Gross Salary: ETB {emp['gross']:,.2f}")
    c.drawString(30*mm, height-55*mm, f"Income Tax: ETB {emp['tax']:,.2f}")
    c.drawString(30*mm, height-60*mm, f"Employee Pension (7%): ETB {emp['pension_employee']:,.2f}")
    c.drawString(30*mm, height-65*mm, f"Employer Pension (11%): ETB {emp['pension_employer']:,.2f}")
    c.drawString(30*mm, height-70*mm, f"Net Pay: ETB {emp['net']:,.2f}")
    c.drawString(30*mm, height-75*mm, f"Payment Method: {emp['bank']}")
    c.showPage()
    c.save()
    return filename
```

**Step 3: Update main.py to generate PDFs for each employee**.

**Step 4: Run and verify PDFs appear in output_payslips/**.

**Step 5: Commit**
```bash
git add payroll_engine/pdf.py payroll_engine/main.py
git commit -m "feat: add PDF payslip generation"
```

### Task 6: Implement CSV/Excel import with validation

**Objective:** Accept CSV with required columns, validate data types, and provide helpful error messages.

**Files:**
- Modify: `payroll_engine/main.py` (add validation)
- Create: `tests/test_import.py`

**Step 1: Write test for missing column**.

**Step 2: Implement validation** – check columns, ensure numeric fields are positive, etc.

**Step 3: Commit**.

### Task 7: Add offline‑first Android prototype (React Native/Expo)

**Objective:** Create a minimal Expo app that lets the user upload a CSV, run the same Python logic via a simple Flask API (or reuse same logic via Pyodide), and display/download payslip.

**Files:**
- Create: `mobile/App.js`
- Create: `mobile/components/Upload.js`
- Create: `mobile/screens/HomeScreen.js`
- Create: `mobile/backend/api.py` (Flask stub that calls payroll_engine functions)

**Step 1: Initialize Expo project**.

**Step 2: Build upload screen**.

**Step 3: Connect to backend**.

**Step 4: Display payslip and allow download**.

**Step 5: Commit**.

### Task 8: Stub Telebirr disbursement (two‑phase) and integrate

**Objective:** Implement a mock Telebirr API that records intent and confirms payment, later replace with real sandbox.

**Files:**
- Create: `payroll_engine/disbursement.py`
- Modify: `payroll_engine/main.py` to call disbursement after net pay calculation.

**Step 1: Write intent → confirm flow**.

**Step 2: Commit**.

### Task 9: Write comprehensive test suite and achieve ≥80% coverage

**Objective:** Add tests for edge cases (new hire mid‑month, termination, overtime, leave deductions) and ensure all core functions are covered.

**Files:**
- Create: `tests/test_edge_cases.py`
- Run coverage tool.

**Step 1: Add tests**.

**Step 2: Commit**.

### Task 10: Prepare deployment Dockerfile and CI pipeline

**Objective:** Create Dockerfile that builds the Python API and runs tests on push.

**Files:**
- Create: `Dockerfile`
- Create: `.github/workflows/ci.yml`

**Step 1: Write Dockerfile**.

**Step 2: Write CI workflow**.

**Step 3: Commit**.

---

**Verification & Acceptance Criteria**

- Tax calculation matches manual computation for at least 10 random gross salaries.
- Payslip PDFs are generated correctly and can be opened.
- CSV import rejects malformed files with clear error messages.
- Disbursement intent → paid flow works without double‑payment.
- Mobile prototype can upload a CSV and display at least one payslip.
- All unit tests pass; coverage ≥80%.

**Risks & Tradeoffs**

- Using ReportLab may require licensing for commercial use; verify or switch to open‑source alternative (e.g., WeasyPrint) if needed.
- Offline‑first Android adds complexity; for MVP we can rely on CSV upload via web.
- Telebirr integration depends on API approval; keep stub interchangeable.

**Next Steps After Plan Approval**

1. Offer to execute using `subagent-driven-development` – dispatch a fresh subagent per task with two‑stage review.
2. If approved, begin with Task 1.

*Plan saved to `.hermes/plans/2026-06-18_0001-ethiopian-payroll-engine.md`.*