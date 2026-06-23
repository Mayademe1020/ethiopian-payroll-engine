import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import csv
from payroll_engine.tax import calculate_tax
from payroll_engine.pension import employee_pension, employer_pension
from payroll_engine.pdf import generate_payslip
from payroll_engine.main import generate_tax_explanation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'web_app', 'templates'),
            static_folder=os.path.join(BASE_DIR, 'web_app', 'static'))
app.secret_key = 'supersecretkey_change_in_production'
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
app.config['PAYSLIP_FOLDER'] = os.path.join(BASE_DIR, 'generated_payslips')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'csv'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PAYSLIP_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_payroll_from_csv(filepath):
    employees = []
    total_gross = 0.0
    total_tax = 0.0
    total_net = 0.0

    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                emp_id = row['employee_id'].strip()
                name = row['name'].strip()
                basic = float(row['basic_salary'])
                allowances = float(row['allowances'])
                bank_info = row['bank_or_telebirr'].strip()
                if basic < 0 or allowances < 0:
                    raise ValueError('Negative salary values')
            except (KeyError, ValueError) as e:
                raise ValueError(f"Invalid row {row.get('employee_id', '?')}: {e}")

            gross = basic + allowances
            tax = calculate_tax(gross)
            pension_emp = employee_pension(basic)
            pension_emp_total = employer_pension(basic)
            net = gross - tax - pension_emp

            payslip_filename = f"payslip_{emp_id}_{uuid.uuid4().hex[:8]}.pdf"
            payslip_path = os.path.join(app.config['PAYSLIP_FOLDER'], payslip_filename)
            generate_payslip({
                'employee_id': emp_id,
                'name': name,
                'basic_salary': basic,
                'allowances': allowances,
                'gross': gross,
                'tax': tax,
                'pension_employee': pension_emp,
                'pension_employer': pension_emp_total,
                'net': net,
                'bank_or_telebirr': bank_info
            }, payslip_path)

            tax_explanation = generate_tax_explanation(gross, tax)

            employees.append({
                'id': emp_id,
                'name': name,
                'basic': basic,
                'allowances': allowances,
                'gross': gross,
                'tax': tax,
                'pension_employee': pension_emp,
                'pension_employer': pension_emp_total,
                'net': net,
                'bank': bank_info,
                'payslip_filename': payslip_filename,
                'tax_explanation': tax_explanation
            })
            total_gross += gross
            total_tax += tax
            total_net += net

    return employees, total_gross, total_tax, total_net


def compute_compliance_score(employees):
    score = 100
    messages = []
    for e in employees:
        if e['net'] < 0:
            score -= 20
            messages.append(f"{e['id']} ({e['name']}): negative net pay")
        if e['basic'] < 600:
            score -= 10
            messages.append(f"{e['id']} ({e['name']}): below minimum wage threshold")
    if not messages:
        messages.append("All checks passed — payroll appears compliant.")
    return max(score, 0), "; ".join(messages)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected.')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                employees, total_gross, total_tax, total_net = process_payroll_from_csv(filepath)
                score, message = compute_compliance_score(employees)
                if score >= 90:
                    color = 'success'
                elif score >= 70:
                    color = 'warning'
                else:
                    color = 'danger'
                return render_template('result.html',
                                       employees=employees,
                                       total_employees=len(employees),
                                       total_gross=total_gross,
                                       total_tax=total_tax,
                                       total_net=total_net,
                                       compliance_score=score,
                                       compliance_message=message,
                                       compliance_color=color)
            except Exception as e:
                flash(f'Error: {str(e)}')
                return redirect(request.url)
        else:
            flash('Only .csv files are allowed.')
            return redirect(request.url)
    return render_template('index.html')


@app.route('/payslips/<filename>')
def download_payslip(filename):
    return send_from_directory(app.config['PAYSLIP_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
