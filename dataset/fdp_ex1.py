import pytesseract
from PIL import Image
import re
# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_fdp_info_from_certificate(pdf_file_path):
    try:
        # Perform OCR using PyTesseract directly on the PDF file
        extracted_text = pytesseract.pytesseract.image_to_string(pdf_file_path)

        # Define regular expressions to match specific patterns
        name_pattern = r"certify that\s*(.+)\n"
        designation_pattern = r"Professor\s*(.+),\n"
        organization_pattern = r"has participated in a One Week Faculty Development Programme on\n\n(.+)\n"
        program_pattern = r"has participated in a One Week Faculty Development Programme on\n\n(.+)\nand"
        coordinator_pattern = r"Organized by the (.+),\n"
        date_pattern = r"during (\d+\"- \d+\" [a-zA-Z]+ \d{4})\."

        # Extract relevant information using regular expressions
        name = re.search(name_pattern, extracted_text)
        designation = re.search(designation_pattern, extracted_text)
        organization = re.search(organization_pattern, extracted_text)
        program = re.search(program_pattern, extracted_text)
        coordinator = re.search(coordinator_pattern, extracted_text)
        date_range = re.search(date_pattern, extracted_text)

        # Store the extracted details in a dictionary
        fdp_info = {
            "Name": name.group(1) if name else None,
            "Designation": designation.group(1) if designation else None,
            "Organization": organization.group(1) if organization else None,
            "Program Attended": program.group(1) if program else None,
            "Coordinator Name": coordinator.group(1) if coordinator else None,
            "From Date": date_range.group(1).split('-')[0].strip() if date_range else None,
            "To Date": date_range.group(1).split('-')[1].strip() if date_range else None,
        }

        return fdp_info
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage:
pdf_file_path = r"C:\Users\DHAVASHRI\Documents\project\uploads\fdp_sam.jpg"
fdp_info = extract_fdp_info_from_certificate(pdf_file_path)

if fdp_info:
    print("Extracted FDP Information:")
    print(fdp_info)
else:
    print("Text extraction failed.")
