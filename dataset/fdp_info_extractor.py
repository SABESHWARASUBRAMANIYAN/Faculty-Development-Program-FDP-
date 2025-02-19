import pdfplumber
import re

def extract_fdp_info(pdf_file_path):
    text = ""
    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    # Regular expressions to extract specific information
    name_pattern = r"Name\s*:\s*(.*)"
    designation_pattern = r"Designation\s*:\s*(.*)"
    department_pattern = r"Department\s*:\s*(.*)"
    program_pattern = r"Programme\s*Attended\s*:\s*(.*)"
    date_range_pattern = r"From\s*:\s*(\d{2}/\d{2}/\d{4})\s*To\s*:\s*(\d{2}/\d{2}/\d{4})"
    coordinator_pattern = r"Name\s*of\s*Coordinator\s*:\s*(.*)"
    sponsor_pattern = r"Sponsor\s*:\s*(.*)"

    # Extract information using regular expressions
    name = re.search(name_pattern, text, re.IGNORECASE)
    name = name.group(1).strip() if name else None

    designation = re.search(designation_pattern, text, re.IGNORECASE)
    designation = designation.group(1).strip() if designation else None

    department = re.search(department_pattern, text, re.IGNORECASE)
    department = department.group(1).strip() if department else None

    program = re.search(program_pattern, text, re.IGNORECASE)
    program = program.group(1).strip() if program else None

    date_range = re.search(date_range_pattern, text, re.IGNORECASE)
    from_date = date_range.group(1) if date_range else None
    to_date = date_range.group(2) if date_range else None

    coordinator = re.search(coordinator_pattern, text, re.IGNORECASE)
    coordinator = coordinator.group(1).strip() if coordinator else None

    sponsor = re.search(sponsor_pattern, text, re.IGNORECASE)
    sponsor = sponsor.group(1).strip() if sponsor else None

    # Return extracted information as a dictionary
    fdp_info = {
        "Name": name,
        "Designation": designation,
        "Department": department,
        "Program Attended": program,
        "From Date": from_date,
        "To Date": to_date,
        "Coordinator Name": coordinator,
        "Sponsor": sponsor
    }

    return fdp_info

# Example usage:
pdf_file_path = "C:\\Users\\DHAVASHRI\\Documents\\project\\uploads\\fdp.pdf"

fdp_info = extract_fdp_info(pdf_file_path)
print(fdp_info)
