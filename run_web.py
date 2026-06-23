#!/usr/bin/env python
"""Run the Ethiopian Payroll Engine web application."""
import os
import sys

# Change to the directory where this script lives
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Add current dir to path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web_app import app

if __name__ == '__main__':
    print("=" * 60)
    print("  Ethiopian Payroll Engine — Web Application")
    print("=" * 60)
    print()
    print("  Open your browser and go to:")
    print("    http://localhost:5000")
    print()
    print("  Press Ctrl+C to stop")
    print("=" * 60)
    app.run(debug=False, host='0.0.0.0', port=5000)
