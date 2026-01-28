#!/usr/bin/env python3
"""
Document Processor - Week 1
============================

This module handles:
1. PDF text extraction
2. Image OCR (Optical Character Recognition)
3. Text preprocessing and cleaning

Author: Built for FinDoc Intelligence project
"""

import os
import re
from pathlib import Path
from typing import Dict, Optional, Union

# PDF processing
import pdfplumber

# Image processing and OCR
from PIL import Image
import pytesseract


class DocumentProcessor:
    """
    Main class for processing financial documents.
    
    Handles PDFs, images (PNG, JPG), and performs OCR.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the document processor.
        
        Args:
            config: Configuration dictionary (optional)
        """
        self.config = config or {}
        
        # Supported file formats
        self.pdf_formats = ['.pdf']
        self.image_formats = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']
        
        print("✅ DocumentProcessor initialized")
        print(f"   Supported formats: PDF, {', '.join(self.image_formats)}")
    
    
    def process_document(self, file_path: Union[str, Path]) -> Dict:
        """
        Main method to process any document.
        
        Automatically detects file type and uses appropriate method.
        
        Args:
            file_path: Path to the document
            
        Returns:
            Dictionary containing:
                - text: Extracted text
                - file_type: Type of file (pdf/image)
                - file_name: Name of the file
                - success: Boolean indicating success
                - error: Error message if any
        """
        file_path = Path(file_path)
        
        # Check if file exists
        if not file_path.exists():
            return {
                'success': False,
                'error': f"File not found: {file_path}",
                'text': '',
                'file_type': None,
                'file_name': file_path.name
            }
        
        # Get file extension
        file_ext = file_path.suffix.lower()
        
        print(f"\n📄 Processing: {file_path.name}")
        print(f"   File type: {file_ext}")
        
        # Route to appropriate processor
        try:
            if file_ext in self.pdf_formats:
                text = self.extract_from_pdf(file_path)
                file_type = 'pdf'
            
            elif file_ext in self.image_formats:
                text = self.extract_from_image(file_path)
                file_type = 'image'
            
            else:
                return {
                    'success': False,
                    'error': f"Unsupported file format: {file_ext}",
                    'text': '',
                    'file_type': None,
                    'file_name': file_path.name
                }
            
            # Clean the extracted text
            cleaned_text = self.clean_text(text)
            
            print(f"✅ Extraction successful!")
            print(f"   Characters extracted: {len(cleaned_text)}")
            
            return {
                'success': True,
                'text': cleaned_text,
                'raw_text': text,  # Keep raw text too
                'file_type': file_type,
                'file_name': file_path.name,
                'file_path': str(file_path),
                'error': None
            }
            
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'text': '',
                'file_type': file_ext,
                'file_name': file_path.name
            }
    
    
    def extract_from_pdf(self, pdf_path: Union[str, Path]) -> str:
        """
        Extract text from PDF file using pdfplumber.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text as string
        """
        print("   Method: PDF text extraction (pdfplumber)")
        
        text_content = []
        
        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)
            print(f"   Pages: {num_pages}")
            
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract text from page
                page_text = page.extract_text()
                
                if page_text:
                    text_content.append(page_text)
                    print(f"   ✓ Page {page_num}/{num_pages}: {len(page_text)} chars")
                else:
                    print(f"   ⚠ Page {page_num}/{num_pages}: No text found")
        
        # Combine all pages
        full_text = "\n\n".join(text_content)
        
        return full_text
    
    
    def extract_from_image(self, image_path: Union[str, Path]) -> str:
        """
        Extract text from image using OCR (Tesseract).
        
        Args:
            image_path: Path to image file
            
        Returns:
            Extracted text as string
        """
        print("   Method: OCR (Optical Character Recognition)")
        
        # Open image
        image = Image.open(image_path)
        
        # Get image info
        width, height = image.size
        mode = image.mode
        print(f"   Image: {width}x{height} pixels, mode: {mode}")
        
        # Convert to RGB if needed (Tesseract works best with RGB)
        if mode != 'RGB':
            print(f"   Converting from {mode} to RGB")
            image = image.convert('RGB')
        
        # Perform OCR
        # lang='eng' means English language
        # config parameter can be used for fine-tuning
        print("   Running Tesseract OCR...")
        text = pytesseract.image_to_string(image, lang='eng')
        
        return text
    
    
    def clean_text(self, text: str) -> str:
        """
        Clean and preprocess extracted text.
        
        Removes extra whitespace, fixes common OCR errors, etc.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in text.split('\n')]
        
        # Remove empty lines
        lines = [line for line in lines if line]
        
        # Rejoin with single newlines
        cleaned = '\n'.join(lines)
        
        return cleaned
    
    
    def save_extracted_text(self, result: Dict, output_dir: Union[str, Path]) -> Optional[Path]:
        """
        Save extracted text to a file.
        
        Args:
            result: Result dictionary from process_document()
            output_dir: Directory to save the text file
            
        Returns:
            Path to saved file, or None if failed
        """
        if not result['success']:
            print("❌ Cannot save - extraction failed")
            return None
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create output filename
        original_name = Path(result['file_name']).stem
        output_file = output_dir / f"{original_name}_extracted.txt"
        
        # Write text to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Extracted from: {result['file_name']}\n")
            f.write(f"# File type: {result['file_type']}\n")
            f.write(f"# Characters: {len(result['text'])}\n")
            f.write("\n" + "="*80 + "\n\n")
            f.write(result['text'])
        
        print(f"💾 Saved extracted text: {output_file}")
        return output_file


def main():
    """
    Test the document processor with our sample files.
    """
    print("="*80)
    print("  Document Processor - Test Run")
    print("="*80)
    
    # Initialize processor
    processor = DocumentProcessor()
    
    # Sample files to test
    sample_dir = Path("data/sample_docs")
    
    test_files = [
        sample_dir / "credit_report_techflow_solutions.pdf",
        sample_dir / "credit_report_techflow_solutions_photo.jpg",
    ]
    
    # Output directory
    output_dir = Path("data/processed")
    
    # Process each file
    for file_path in test_files:
        if file_path.exists():
            result = processor.process_document(file_path)
            
            if result['success']:
                # Save extracted text
                processor.save_extracted_text(result, output_dir)
                
                # Show preview
                preview = result['text'][:500] + "..." if len(result['text']) > 500 else result['text']
                print(f"\n📝 Preview of extracted text:")
                print("-" * 80)
                print(preview)
                print("-" * 80)
            
            print()  # Empty line between files
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print("\n Test complete!")


if __name__ == "__main__":
    main()