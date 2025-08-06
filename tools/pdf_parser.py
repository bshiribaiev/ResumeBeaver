# tools/pdf_parser.py
from PyPDF2 import PdfReader
import logging

def extract_pdf_text(file_path: str) -> str:
    """
    Extract clean text from PDF resume files.
    
    Enhanced PDF processing that handles multiple page layouts
    and preserves document structure for better parsing.
    
    Args:
        file_path (str): Path to PDF file
        
    Returns:
        str: Extracted text content
        
    Raises:
        Exception: If PDF cannot be processed
        
    Example:
        >>> text = extract_pdf_text("resume.pdf")
        >>> print(f"Extracted {len(text)} characters")
    """
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            
            # Enhanced: Add metadata extraction
            num_pages = len(reader.pages)
            
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                
                # Enhanced: Add page separation for better structure
                if page_num > 0:
                    text += "\n--- PAGE BREAK ---\n"
                
                text += page_text
            
            # Enhanced: Log processing info
            logging.info(f"Processed PDF: {num_pages} pages, {len(text)} characters")
            
        return text.strip()
        
    except Exception as e:
        logging.error(f"PDF extraction error for {file_path}: {str(e)}")
        raise Exception(f"Error reading PDF: {str(e)}")

# Keep your original function name for backward compatibility
def extract_text_from_pdf(file_path: str) -> str:
    """Backward compatibility wrapper"""
    return extract_pdf_text(file_path)