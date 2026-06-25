import asyncio
import sys
sys.path.insert(0, r'D:\ethiopian_payroll_engine')

from payroll_engine.telegram import send_payslip_via_telegram

async def send_test():
    print("Sending test payslip notification...")
    
    # The URL would be your actual server URL in production
    result = await send_payslip_via_telegram(
        telegram_id="@alemayehu_b",  # From sample CSV (without @ in actual send)
        employee_name="Alemayehu Bekele",
        payslip_url="http://localhost:5000/payslips/payslip_E001_test.pdf",
        pay_period="June 2026"
    )
    
    if result:
        print("✅ Message sent successfully!")
    else:
        print("❌ Failed to send message")

asyncio.run(send_test())
