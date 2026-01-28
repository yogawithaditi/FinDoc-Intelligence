#!/usr/bin/env python3
"""
Quick Demo - Test Data Extraction
==================================

This script demonstrates the data extractor with sample text.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.data_extractor import DataExtractor

# Sample credit report text (abbreviated)
SAMPLE_TEXT = """
CREDITSAFE CREDIT REPORT

Report Date: 15 December 2024
Report Reference: CS-2024-UK-789456

COMPANY INFORMATION

Company Name: TechFlow Solutions Limited
Trading Name: TechFlow Solutions
Legal Form: Private Limited Company

Registration Number: 08765432
LEI Code: 254900ABCDEF1234GHIJ56
DUNS Number: 123456789

Date of Incorporation: 12 March 2018

CREDIT SCORE & RATING

Credit Score: 75 / 100
Credit Rating: B+ (Good)
Risk Level: LOW TO MEDIUM

Credit Limit (Recommended): £150,000
Payment Terms: Net 30 days

FINANCIAL SUMMARY

Revenue (Turnover): £4,850,000
Profit Before Tax: £485,000
Total Assets: £2,450,000
Total Liabilities: £1,320,000
Net Worth: £1,130,000

Current Ratio: 1.85
Debt-to-Equity Ratio: 0.42
Profit Margin: 10.0%

PAYMENT HISTORY

Payment Summary (Last 12 Months):
- On-Time Payments: 145 (93%)
Average Payment Days: 28 days (Terms: Net 30)
"""

def main():
    print("=" * 80)
    print("  DATA EXTRACTION DEMO")
    print("=" * 80)
    print()
    
    # Initialize extractor
    extractor = DataExtractor()
    
    # Extract data
    print("Extracting data from sample text...")
    extracted = extractor.extract_all(SAMPLE_TEXT)
    
    # Display formatted results
    print(extractor.format_for_display(extracted))
    
    # Show what would be saved to DuckDB
    print("\n📊 DuckDB Format (flattened for database):")
    print("-" * 80)
    db_format = extractor.format_for_duckdb(extracted, document_id=1)
    for key, value in db_format.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Demo complete!")
    print("\nNext: Run this with your actual documents in the Streamlit app!")

if __name__ == "__main__":
    main()