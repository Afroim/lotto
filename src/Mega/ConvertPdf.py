import pdfplumber
import csv
import re

# Define the input and output files
base_path = "C:\\Users\\Alik\\Documents\\Project\\Lotto\\data\\"
# pdf_file_path = base_path + "Mega Millions.pdf"
pdf_file_path = base_path + "Mega Millions17.pdf"
csv_file_path = base_path + "Mega_Millions_17.csv"

# Regular expression pattern to match the 6 numbers
pattern = re.compile(r'(\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+)')

with pdfplumber.open(pdf_file_path) as pdf, open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    for page in pdf.pages:
        text = page.extract_text()
        # Find all matching lines
        matches = pattern.findall(text)

        for match in matches:
            # Remove extra spaces and split into list of numbers
            numbers = match.split()
            # Write the numbers as a row in the CSV
            writer.writerow(numbers)

print(f"Conversion completed. The file is saved as {csv_file_path}")
