# Ethiopian Payroll Engine

This is a core payroll engine for Ethiopian SMEs that calculates income tax (2025 brackets), POSSA pension (employee 7%, employer 11%), and generates net pay.

## Features

- Tax calculation according to Ethiopian 2025 progressive tax brackets.
- POSSA pension calculation (employee 7%, employer 11% of basic salary).
- Net pay computation.
- CSV input for employee roster.
- Outputs payslip‑style summary (can be extended to generate PDF payslips).

## Requirements

- Python 3.11 or later
- No external dependencies for the core engine (the plan includes ReportLab for PDF generation, but not required for the demo).

## Usage

1. Clone the repository.
2. Ensure you have a CSV file with the following columns:
   - `employee_id`
   - `name`
   - `basic_salary`
   - `allowances`
   - `bank_or_telebirr` (optional for output)
3. Run the engine:

   ```bash
   python -m payroll_engine.main path/to/employees.csv
   ```

   If no path is provided, it defaults to `sample_employees.csv`.

## Example

See the output when running with the provided `sample_employees.csv`:

```
Ethiopian Payroll Engine - Sample Output
============================================================
Employee ID: E001
Name: Alemayehu
Basic Salary: ETB 3,500.00
Allowances: ETB 500.00
Gross Salary: ETB 4,000.00
Income Tax (2025): ETB 299.85
Employee Pension (7%): ETB 245.00
Employer Pension (11%): ETB 385.00
Net Pay: ETB 3,455.15
Payment Method: Telebirr:0911111111
...
```

## Implementation Details

The engine is split into modules:
- `tax.py`: Contains `calculate_tax(gross)` function.
- `pension.py`: Contains `employee_pension(basic)` and `employer_pension(basic)` functions.
- `main.py`: Reads CSV, computes payroll, and prints results.

## Future Work

- PDF payslip generation (using ReportLab).
- Integration with Telebirr disbursement API (two‑phase intent → paid).
- Offline‑first Android app (React Native/Expo).
- Comprehensive test suite and CI/CD.

## License

MIT
