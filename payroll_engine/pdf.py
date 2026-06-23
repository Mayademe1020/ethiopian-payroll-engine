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
