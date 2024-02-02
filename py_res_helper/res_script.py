import re
import os
import pyperclip
from PyPDF2 import PdfReader, PdfWriter
from docx2pdf import convert


def process_file(filename):
    with open(filename, "r") as file:
        data = file.read()

    # Remove special characters
    data = re.sub(r"\W+", " ", data)

    # Replace multiple spaces with a single space
    data = re.sub(r"\s+", " ", data)

    # Remove line breaks
    data = data.replace("\n", " ")

    # Copy to clipboard
    pyperclip.copy(data)


def merge_pdfs(pdf1_name: str, pdf2_name, output_name):
    docx_file = pdf1_name.replace(".pdf", ".docx")

    convert(docx_file, pdf1_name)

    # Create a PDF file writer object
    writer = PdfWriter()

    # Add the pages from the first file
    for page in PdfReader(pdf1_name).pages:
        writer.add_page(page)

    # Add the pages from the second file
    for page in PdfReader(pdf2_name).pages:
        writer.add_page(page)

    # Write the result to the output file
    with open(output_name, "wb") as output_file:
        writer.write(output_file)

    os.startfile(docx_file)
    os.startfile(output_name)


# Call the function with the path to your file
process_file(
    r"C:\Users\AHMED\Desktop\AHMED\Resume\others\Analyse the following job posting a.txt"
)

# Call the function with your file names
merge_pdfs(
    r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed Qureshi Cover Letter.pdf",
    r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed_Qureshi_Resume_ProjPortfolio.pdf",
    r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed_Qureshi_Cover_Resume_ProjPortfolio.pdf",
)
