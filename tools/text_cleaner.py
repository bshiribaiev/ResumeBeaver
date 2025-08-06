# tools/text_cleaner.py
import re
import logging

def clean_resume_text(text: str) -> str:
    """
    Advanced text cleaning optimized for resume content.
    
    Preserves important structure while removing noise and
    normalizing formatting for better AI processing.
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned and normalized text
    """
    if not text:
        return ""
    
    # Enhanced: Preserve important resume formatting markers
    # Keep section headers by preserving lines that are likely headers
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Preserve section headers (short lines, often in caps)
        if len(line) < 50 and (line.isupper() or ':' in line):
            processed_lines.append(f"\n{line}\n")
        else:
            processed_lines.append(line)
    
    # Join and apply basic cleaning
    text = ' '.join(processed_lines)
    
    # Enhanced cleaning rules
    text = re.sub(r'\s+', ' ', text)  # Collapse whitespace
    text = re.sub(r'[\r\n]+', ' ', text)  # Remove newlines
    text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)  # Fix sentence spacing
    text = re.sub(r'\s+([.,:;!?])', r'\1', text)  # Fix punctuation spacing
    
    return text.strip()

# Keep your original function name for backward compatibility
def clean_text(text: str) -> str:
    """Backward compatibility wrapper"""
    return clean_resume_text(text)