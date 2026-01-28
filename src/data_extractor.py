#!/usr/bin/env python3
"""
Data Extractor - Week 2
========================

Extracts structured financial data from document text.

Handles:
1. Company identifiers (LEI, DUNS, Registration Number)
2. Credit metrics (score, rating, limit)
3. Financial data (revenue, profit, ratios)
4. Payment information (history, terms)

Author: Built for FinDoc Intelligence project
"""

import re
from typing import Dict, Optional, List, Tuple
from datetime import datetime
import json


class DataExtractor:
    """
    Extracts structured financial data from text.
    
    Uses regex patterns and NLP techniques to identify and extract
    specific financial metrics and company information.
    """
    
    def __init__(self):
        """Initialize the data extractor with pattern definitions."""
        self.patterns = self._init_patterns()
        print("✅ DataExtractor initialized with financial patterns")
    
    
    def _init_patterns(self) -> Dict:
        """
        Initialize regex patterns for financial data extraction.
        
        Returns:
            Dictionary of compiled regex patterns
        """
        return {
            # Company identifiers
            'company_name': re.compile(
                r'Company Name:\s*(.+?)(?:\n|$)',
                re.IGNORECASE
            ),
            'registration_number': re.compile(
                r'Registration Number:\s*(\d+)',
                re.IGNORECASE
            ),
            'lei_code': re.compile(
                r'LEI Code:\s*([A-Z0-9]{20})',
                re.IGNORECASE
            ),
            'duns_number': re.compile(
                r'DUNS Number:\s*(\d{9})',
                re.IGNORECASE
            ),
            
            # Credit metrics
            'credit_score': re.compile(
                r'Credit Score:\s*(\d+)\s*(?:/|out of)?\s*\d*',
                re.IGNORECASE
            ),
            'credit_rating': re.compile(
                r'Credit Rating:\s*([A-Z][A-Z+\-]*)',
                re.IGNORECASE
            ),
            'credit_limit': re.compile(
                r'Credit Limit.*?[£$€]?\s*([\d,]+)',
                re.IGNORECASE
            ),
            'risk_level': re.compile(
                r'Risk Level:\s*(.+?)(?:\n|$)',
                re.IGNORECASE
            ),
            
            # Financial metrics
            'revenue': re.compile(
                r'Revenue.*?[£$€]\s*([\d,]+)',
                re.IGNORECASE
            ),
            'turnover': re.compile(
                r'Turnover.*?[£$€]\s*([\d,]+)',
                re.IGNORECASE
            ),
            'profit': re.compile(
                r'Profit Before Tax.*?[£$€]\s*([\d,]+)',
                re.IGNORECASE
            ),
            'total_assets': re.compile(
                r'Total Assets:\s*[£$€]\s*([\d,]+)',
                re.IGNORECASE
            ),
            'total_liabilities': re.compile(
                r'Total Liabilities:\s*[£$€]\s*([\d,]+)',
                re.IGNORECASE
            ),
            'net_worth': re.compile(
                r'Net Worth:\s*[£$€]\s*([\d,]+)',
                re.IGNORECASE
            ),
            
            # Financial ratios
            'debt_to_equity': re.compile(
                r'Debt-to-Equity.*?(\d+\.?\d*)',
                re.IGNORECASE
            ),
            'current_ratio': re.compile(
                r'Current Ratio:\s*(\d+\.?\d*)',
                re.IGNORECASE
            ),
            'profit_margin': re.compile(
                r'Profit Margin:\s*(\d+\.?\d*)%?',
                re.IGNORECASE
            ),
            
            # Payment information
            'payment_terms': re.compile(
                r'Payment Terms:\s*(.+?)(?:\n|$)',
                re.IGNORECASE
            ),
            'on_time_percentage': re.compile(
                r'On-Time Payments?:\s*\d+\s*\((\d+)%\)',
                re.IGNORECASE
            ),
            'average_payment_days': re.compile(
                r'Average Payment Days:\s*(\d+)',
                re.IGNORECASE
            ),
            
            # Dates
            'incorporation_date': re.compile(
                r'Date of Incorporation:\s*(\d{1,2}\s+\w+\s+\d{4})',
                re.IGNORECASE
            ),
            'report_date': re.compile(
                r'Report Date:\s*(\d{1,2}\s+\w+\s+\d{4})',
                re.IGNORECASE
            ),
        }
    
    
    def extract_all(self, text: str) -> Dict:
        """
        Extract all available financial data from text.
        
        Args:
            text: Document text to extract from
            
        Returns:
            Dictionary with all extracted data
        """
        if not text:
            return {'error': 'No text provided'}
        
        print("\n🔍 Starting data extraction...")
        
        extracted = {
            'extraction_timestamp': datetime.now().isoformat(),
            'company_info': self._extract_company_info(text),
            'credit_metrics': self._extract_credit_metrics(text),
            'financial_data': self._extract_financial_data(text),
            'payment_info': self._extract_payment_info(text),
            'dates': self._extract_dates(text),
        }
        
        # Count successful extractions
        total_fields = self._count_extracted_fields(extracted)
        extracted['extraction_summary'] = {
            'total_fields_extracted': total_fields,
            'extraction_complete': total_fields > 0
        }
        
        print(f"✅ Extraction complete: {total_fields} fields extracted")
        
        return extracted
    
    
    def _extract_company_info(self, text: str) -> Dict:
        """Extract company identification information."""
        info = {}
        
        # Company name
        match = self.patterns['company_name'].search(text)
        if match:
            info['company_name'] = match.group(1).strip()
        
        # Registration number
        match = self.patterns['registration_number'].search(text)
        if match:
            info['registration_number'] = match.group(1)
        
        # LEI Code
        match = self.patterns['lei_code'].search(text)
        if match:
            info['lei_code'] = match.group(1)
        
        # DUNS Number
        match = self.patterns['duns_number'].search(text)
        if match:
            info['duns_number'] = match.group(1)
        
        return info
    
    
    def _extract_credit_metrics(self, text: str) -> Dict:
        """Extract credit-related metrics."""
        metrics = {}
        
        # Credit score
        match = self.patterns['credit_score'].search(text)
        if match:
            metrics['credit_score'] = int(match.group(1))
        
        # Credit rating
        match = self.patterns['credit_rating'].search(text)
        if match:
            metrics['credit_rating'] = match.group(1)
        
        # Credit limit
        match = self.patterns['credit_limit'].search(text)
        if match:
            value = match.group(1).replace(',', '')
            metrics['credit_limit'] = float(value)
        
        # Risk level
        match = self.patterns['risk_level'].search(text)
        if match:
            metrics['risk_level'] = match.group(1).strip()
        
        return metrics
    
    
    def _extract_financial_data(self, text: str) -> Dict:
        """Extract financial metrics and ratios."""
        data = {}
        
        # Revenue (try both Revenue and Turnover)
        match = self.patterns['revenue'].search(text)
        if not match:
            match = self.patterns['turnover'].search(text)
        if match:
            value = match.group(1).replace(',', '')
            data['revenue'] = float(value)
        
        # Profit
        match = self.patterns['profit'].search(text)
        if match:
            value = match.group(1).replace(',', '')
            data['profit'] = float(value)
        
        # Total Assets
        match = self.patterns['total_assets'].search(text)
        if match:
            value = match.group(1).replace(',', '')
            data['total_assets'] = float(value)
        
        # Total Liabilities
        match = self.patterns['total_liabilities'].search(text)
        if match:
            value = match.group(1).replace(',', '')
            data['total_liabilities'] = float(value)
        
        # Net Worth
        match = self.patterns['net_worth'].search(text)
        if match:
            value = match.group(1).replace(',', '')
            data['net_worth'] = float(value)
        
        # Debt-to-Equity Ratio
        match = self.patterns['debt_to_equity'].search(text)
        if match:
            data['debt_to_equity'] = float(match.group(1))
        
        # Current Ratio
        match = self.patterns['current_ratio'].search(text)
        if match:
            data['current_ratio'] = float(match.group(1))
        
        # Profit Margin
        match = self.patterns['profit_margin'].search(text)
        if match:
            data['profit_margin'] = float(match.group(1))
        
        return data
    
    
    def _extract_payment_info(self, text: str) -> Dict:
        """Extract payment-related information."""
        info = {}
        
        # Payment terms
        match = self.patterns['payment_terms'].search(text)
        if match:
            info['payment_terms'] = match.group(1).strip()
        
        # On-time payment percentage
        match = self.patterns['on_time_percentage'].search(text)
        if match:
            info['on_time_percentage'] = int(match.group(1))
        
        # Average payment days
        match = self.patterns['average_payment_days'].search(text)
        if match:
            info['average_payment_days'] = int(match.group(1))
        
        return info
    
    
    def _extract_dates(self, text: str) -> Dict:
        """Extract important dates."""
        dates = {}
        
        # Incorporation date
        match = self.patterns['incorporation_date'].search(text)
        if match:
            dates['incorporation_date'] = match.group(1)
        
        # Report date
        match = self.patterns['report_date'].search(text)
        if match:
            dates['report_date'] = match.group(1)
        
        return dates
    
    
    def _count_extracted_fields(self, extracted: Dict) -> int:
        """Count total number of successfully extracted fields."""
        count = 0
        
        for category in ['company_info', 'credit_metrics', 'financial_data', 'payment_info', 'dates']:
            if category in extracted:
                count += len(extracted[category])
        
        return count
    
    
    def format_for_display(self, extracted: Dict) -> str:
        """
        Format extracted data for human-readable display.
        
        Args:
            extracted: Dictionary from extract_all()
            
        Returns:
            Formatted string
        """
        lines = []
        lines.append("=" * 80)
        lines.append("EXTRACTED FINANCIAL DATA")
        lines.append("=" * 80)
        lines.append("")
        
        # Company Information
        if extracted.get('company_info'):
            lines.append("📊 COMPANY INFORMATION")
            lines.append("-" * 80)
            for key, value in extracted['company_info'].items():
                label = key.replace('_', ' ').title()
                lines.append(f"  {label}: {value}")
            lines.append("")
        
        # Credit Metrics
        if extracted.get('credit_metrics'):
            lines.append("💳 CREDIT METRICS")
            lines.append("-" * 80)
            for key, value in extracted['credit_metrics'].items():
                label = key.replace('_', ' ').title()
                if 'limit' in key and isinstance(value, (int, float)):
                    lines.append(f"  {label}: £{value:,.0f}")
                else:
                    lines.append(f"  {label}: {value}")
            lines.append("")
        
        # Financial Data
        if extracted.get('financial_data'):
            lines.append("💰 FINANCIAL DATA")
            lines.append("-" * 80)
            for key, value in extracted['financial_data'].items():
                label = key.replace('_', ' ').title()
                if isinstance(value, float) and value > 1000:
                    lines.append(f"  {label}: £{value:,.0f}")
                else:
                    lines.append(f"  {label}: {value}")
            lines.append("")
        
        # Payment Information
        if extracted.get('payment_info'):
            lines.append("💳 PAYMENT INFORMATION")
            lines.append("-" * 80)
            for key, value in extracted['payment_info'].items():
                label = key.replace('_', ' ').title()
                if 'percentage' in key:
                    lines.append(f"  {label}: {value}%")
                else:
                    lines.append(f"  {label}: {value}")
            lines.append("")
        
        # Summary
        if extracted.get('extraction_summary'):
            lines.append("📈 EXTRACTION SUMMARY")
            lines.append("-" * 80)
            summary = extracted['extraction_summary']
            lines.append(f"  Total Fields Extracted: {summary['total_fields_extracted']}")
            lines.append(f"  Extraction Status: {'✅ Complete' if summary['extraction_complete'] else '❌ Failed'}")
        
        lines.append("")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    
    def format_for_duckdb(self, extracted: Dict, document_id: int = None) -> Dict:
        """
        Format extracted data for DuckDB storage.
        
        Args:
            extracted: Dictionary from extract_all()
            document_id: Document ID from database
            
        Returns:
            Flattened dictionary ready for DuckDB insertion
        """
        record = {'document_id': document_id}
        
        # Flatten nested structure
        if 'company_info' in extracted:
            record.update(extracted['company_info'])
        
        if 'credit_metrics' in extracted:
            record.update(extracted['credit_metrics'])
        
        if 'financial_data' in extracted:
            record.update(extracted['financial_data'])
        
        if 'payment_info' in extracted:
            record.update(extracted['payment_info'])
        
        return record


def main():
    """Test the data extractor with sample credit report."""
    from pathlib import Path
    
    print("=" * 80)
    print("  Data Extractor - Test Run")
    print("=" * 80)
    
    # Initialize extractor
    extractor = DataExtractor()
    
    # Load sample extracted text
    sample_file = Path("data/processed/credit_report_techflow_solutions_extracted.txt")
    
    if not sample_file.exists():
        print(f"❌ Sample file not found: {sample_file}")
        print("   Please run document_processor.py first to extract text")
        return
    
    with open(sample_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Extract data
    extracted = extractor.extract_all(text)
    
    # Display results
    print("\n" + extractor.format_for_display(extracted))
    
    # Show JSON structure
    print("\n📄 JSON Structure:")
    print(json.dumps(extracted, indent=2, default=str))
    
    # Save to file
    output_file = Path("data/processed/extracted_data.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dumps(extracted, f, indent=2, default=str)
    
    print(f"\n💾 Saved to: {output_file}")
    print("\n✅ Test complete!")


if __name__ == "__main__":
    main()