import pytesseract
from PIL import Image

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Rest of your code remains unchanged
def extract_text_from_pdf(pdf_file_path):
    try:
        # Perform OCR using PyTesseract directly on the PDF file
        extracted_text = pytesseract.pytesseract.image_to_string(pdf_file_path)

        return extracted_text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage:
pdf_file_path = r"C:\Users\DHAVASHRI\Documents\project\uploads\fdp_sam.jpg"
extracted_text = extract_text_from_pdf(pdf_file_path)

if extracted_text:
    print("Extracted Text:")
    print(extracted_text)
else:
    print("Text extraction failed.")    


