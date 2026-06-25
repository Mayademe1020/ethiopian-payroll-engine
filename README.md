# Ethiopian Payroll Engine

This is a core payroll engine for Ethiopian SMEs that calculates income tax (2025 brackets), POSSA pension (employee 7%, employer 11%), and generates net pay. Now includes Telegram notification delivery!

## Features
- **Tax calculation** - Uses the 2025 progressive brackets (0%‑35%) as marginal rates
- **Pension calculation** - Employee 7 %, Employer 11 % of basic salary
- **CSV/Excel import** - Reads employee data with validation
- **Payslip generation** - Creates printable PDF payslips (Amharic + English)
- **Telegram notifications** - Automatically sends payslip alerts to employees via Telegram
- **Compliance health score** - Visual indicator of payroll risks
- **Tax explanations** - Plain-language breakdown of tax calculations
- **Offline capable** - Core engine works without internet (Telegram delivery requires connection)

## How It Works
1. **Prepare CSV** - Include columns: employee_id, name, basic_salary, allowances, bank_or_telebirr, telegram_id (optional)
2. **Upload** - Drag and drop your CSV file
3. **Process** - System calculates taxes, pensions, net pay
4. **Get Results** - 
   - View detailed payroll breakdown
   - Download PDF payslips for each employee
   - See Telegram delivery status
   - Get compliance health score
5. **Employees notified** - Those with Telegram IDs receive payslip links via Telegram

## CSV Format
Your CSV must include these columns:
- `employee_id` - Unique identifier (e.g., E001)
- `name` - Full name (e.g., Alemayehu Bekele)
- `basic_salary` - Basic salary in ETB (e.g., 5000)
- `allowances` - Total allowances in ETB (e.g., 1000)
- `bank_or_telebirr` - Payment info (e.g., CBE:12345678)
- `telegram_id` - **Optional** Telegram username (without @) or chat ID (e.g., alemeyehu or 123456789)

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Telegram Bot (Optional but Recommended)
To enable Telegram notifications:
1. Talk to [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow the prompts
3. You'll receive a bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
4. Set it as an environment variable:
   ```bash
   set TELEGRAM_BOT_TOKEN=your_token_here  # Windows
   export TELEGRAM_BOT_TOKEN=your_token_here  # Linux/Mac
   ```
5. Restart the application

### 3. Run the Application
```bash
python run_web.py
```

### 4. Use the Application
Open your browser to: http://localhost:5000

## Example Usage
1. Download the sample file: [sample_employees.csv](sample_employees.csv)
2. Upload it via the web interface
3. View results - notice the Telegram delivery status column
4. Click "PDF" to download any payslip
5. Click "Explain" to see how tax was calculated

## Technology Stack
- **Backend**: Python/Flask
- **PDF Generation**: ReportLab
- **Telegram Bot**: python-telegram-bot
- **Data Processing**: Pandas
- **Frontend**: HTML/CSS/JavaScript (Bootstrap-inspired)

## License
MIT License - feel free to use and modify for your Ethiopian payroll needs.

## Next Steps (Planned)
- Employee self-service portal via Telegram
- Leave management integration
- Multi-tenant SaaS version
- Biometric attendance integration (ZKTeco, etc.)
- WhatsApp Business API support
- AI-powered compliance assistant

---
Ethiopian Payroll Engine &copy; 2026 - Built for Ethiopian businesses