"""
Smart Notes Organizer - OCR Utilities

This module provides utilities for extracting text from various file types
including images (using Tesseract OCR) and PDFs.
"""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

def extract_text_from_file(file_path):
    """
    Extract text from a file based on its type.
    
    Args:
        file_path (Path): Path to the file
        
    Returns:
        str: Extracted text or empty string if extraction fails
    """
    file_path = Path(file_path)
    file_extension = file_path.suffix.lower()
    
    try:
        if file_extension in ['.jpg', '.jpeg', '.png']:
            return extract_text_from_image(file_path)
        elif file_extension == '.pdf':
            return extract_text_from_pdf(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_extension}")
            return ""
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {str(e)}")
        return ""

def extract_text_from_image(image_path):
    """
    Extract text from an image using Tesseract OCR.
    
    Args:
        image_path (Path): Path to the image file
        
    Returns:
        str: Extracted text
    """
    try:
        from PIL import Image
        import pytesseract
        
        logger.info(f"Extracting text from image: {image_path}")
        
        # Open the image
        image = Image.open(image_path)
        
        # Extract text using pytesseract
        text = pytesseract.image_to_string(image)
        
        logger.debug(f"Extracted {len(text)} characters from {image_path}")
        return text
    except ImportError:
        logger.error("pytesseract or PIL not installed. Install with: pip install pytesseract pillow")
        return ""
    except Exception as e:
        logger.error(f"Error in OCR processing: {str(e)}")
        return ""

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyMuPDF.
    
    Args:
        pdf_path (Path): Path to the PDF file
        
    Returns:
        str: Extracted text
    """
    try:
        import fitz  # PyMuPDF
        
        logger.info(f"Extracting text from PDF: {pdf_path}")
        
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        # Extract text from each page
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        
        logger.debug(f"Extracted {len(text)} characters from {pdf_path}")
        return text
    except ImportError:
        logger.error("PyMuPDF not installed. Install with: pip install pymupdf")
        return ""
    except Exception as e:
        logger.error(f"Error in PDF processing: {str(e)}")
        return ""