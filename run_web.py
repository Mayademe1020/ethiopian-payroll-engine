#!/usr/bin/env python
import os, sys, subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Flush prints immediately
os.environ['PYTHONUNBUFFERED'] = '1'

print()
print("=" * 60)
print("  Ethiopian Payroll Engine")
print("=" * 60)
print()
print("  Starting web server...")
print("  Open: http://localhost:5000")
print()
print("  Press Ctrl+C to stop")
print("=" * 60)
print()

from web_app import app
app.run(debug=False, host='0.0.0.0', port=5000)
