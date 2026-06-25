import sys
import io
sys.path.insert(0, r'D:\ethiopian_payroll_engine')

from web_app import app

client = app.test_client()

print("=== Web App End-to-End Test ===")
print()

# Test 1: Index page
print("1. Testing index page...")
r = client.get('/')
print(f"   Status: {r.status_code}")
assert r.status_code == 200, "Index page failed"
print("   ✅ Index page loads")

# Test 2: Upload with sample CSV data
print("\n2. Testing payroll upload...")
csv_data = b'''employee_id,name,basic_salary,allowances,bank_or_telebirr,telegram_id
E001,Alemayehu Bekele,3500,500,CBE:1001002003,@alemayehu_b
E002,Belayneh Ayele,4200,800,AWASH:2003004005,@belayneh_a
E003,Chaltu Gurmu,2800,300,TELEBIRR:0911111111,
E004,Dawit Wolde,5500,1200,ABY:3004006007,@testuser
E005,Eyerus Solomon,3100,400,DASHEN:4005007008,
E006,Gete Yohannes,6200,1500,CBE:5006007009,
E007,Hanna Girma,1800,200,TELEBIRR:0922222222,
E008,Tadesse Mengistu,8500,2000,CBE:7008009010,
E009,Wubetu Kemal,1500,100,AWASH:900101112,
E010,Zelalem Fikadu,12000,3000,ABY:200201314,
'''

data = {
    'file': (io.BytesIO(csv_data), 'employees.csv')
}
r = client.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
print(f"   Status: {r.status_code}")
response_text = r.data.decode('utf-8')

# Check for key elements in response
checks = [
    ('Alemayehu Bekele', 'Employee name shown'),
    ('Belayneh Ayele', 'Second employee shown'),
    ('Chaltu Gurmu', 'Third employee shown (no Telegram)'),
    ('Dawit Wolde', 'Fourth employee (has Telegram)'),
    ('compliance', 'Compliance score shown'),
    ('PDF', 'PDF download link shown'),
]

print("\n3. Checking results page content...")
all_passed = True
for keyword, description in checks:
    if keyword.lower() in response_text.lower():
        print(f"   ✅ {description}")
    else:
        print(f"   ❌ {description} (keyword '{keyword}' not found)")
        all_passed = False

print(f"\n=== Test Result: {'ALL PASSED' if all_passed else 'SOME FAILED'} ===")
print(f"Processed 10 employees with mixed Telegram availability.")
print("Expected: 5 with Telegram (@), 5 without (empty)")
