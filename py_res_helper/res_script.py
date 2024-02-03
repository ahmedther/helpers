import re
import os
import psutil
import pyperclip
from PyPDF2 import PdfReader, PdfWriter
from docx2pdf import convert
from docx import Document


class ResumeHelper:
    def __init__(self):
        self.process_to_kill = [
            "WINWORD.EXE",
            "FoxitPDFEditor.exe",
            # "Notepad.exe",
            "Acrobat.exe",
        ]
        self.template_path = f"{os.getcwd()}\\templates"
        self.docx_output = (
            f"{os.getcwd()}\\output_files\\Ahmed_Qureshi_Cover_Letter.docx"
        )
        self.docx_template = (
            f"{self.template_path}\Ahmed_Qureshi_Cover_Letter_Template.docx"
        )
        self.notepad_template = f"{self.template_path}\\notepad_template.txt"

    def close_apps(self):
        for process in (
            process
            for process in psutil.process_iter()
            if process.name() in self.process_to_kill
        ):
            process.kill()

    def format_and_copy_data_from_notepad(self):
        with open(self.notepad_template, "r") as file:
            data = file.read()

        # Remove special characters
        data = re.sub(r"\W+", " ", data)

        # Replace multiple spaces with a single space
        data = re.sub(r"\s+", " ", data)

        # Remove line breaks
        data = data.replace("\n", " ")

        # Copy to clipboard
        pyperclip.copy(data)

    def replace_string_in_docx_template_table(self, replace_text, file, save_location):
        doc = Document(file)
        # Remove extra spaces
        text = re.sub(" +", " ", pyperclip.paste())

        # Replace multiple line breaks with a single one
        text = re.sub("\r\n\r\n", "\n\n", text)
        text = re.sub("\\n+", "\\n\\n", text)

        cell = doc.tables[0].rows[3].cells[0]
        for i in range(len(cell.paragraphs)):
            for run in cell.paragraphs[i].runs:
                if replace_text in run.text:
                    run.text = run.text.replace(replace_text, text.strip())

        doc.save(save_location)

    def generate_and_merge_pdfs(
        self,
        docx_file,
        pdf1_name: str = r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed Qureshi Cover Letter.pdf",
        pdf2_name=r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed_Qureshi_Resume_ProjPortfolio.pdf",
        output_name=r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed_Qureshi_Cover_Resume_ProjPortfolio.pdf",
    ):

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

        os.startfile(output_name)

    def launch_file(self, filename):
        os.startfile(filename)

    def run(self):
        run = True
        while run:
            self.close_apps()

            open_notepad = input(
                "\n\nPress 1 to Open the Notepad Template. Otherwise Press Enter To Continue... "
            )
            if open_notepad == "1":
                self.launch_file(self.notepad_template)

            input("\n\nPress Enter Process and Copy Data From the Notepad Template ")

            self.format_and_copy_data_from_notepad()

            input("\n\nPress Enter To Copy the Company Name On The Word Template ")

            self.replace_string_in_docx_template_table(
                "COMPANY", self.docx_template, self.docx_output
            )
            input("\n\nPress Enter To Copy the Body On The Word Template ")
            self.replace_string_in_docx_template_table(
                "body", self.docx_output, self.docx_output
            )
            self.launch_file(self.docx_output)

            input("\n\nPress Enter To Generate and Merge PDFs ")

            self.generate_and_merge_pdfs(
                docx_file=self.docx_output,
                pdf1_name=r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed Qureshi Cover Letter.pdf",
                pdf2_name=r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed_Qureshi_Resume_ProjPortfolio.pdf",
                output_name=r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed_Qureshi_Cover_Resume_ProjPortfolio.pdf",
            )
            continue_run = input(
                """
\n\nAll Operations are Completed\n
---------------------------------
|                               |
|   Script execution complete   |
|                               |
---------------------------------
\n\nPress Enter to Start Again...
"""
            )
            if continue_run == "1":
                run = False


if __name__ == "__main__":
    helper = ResumeHelper()
    helper.run()


# def merge_pdfs(
#     pdf1_name: str = r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed Qureshi Cover Letter.pdf",
#     pdf2_name=r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed_Qureshi_Resume_ProjPortfolio.pdf",
#     output_name=r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed_Qureshi_Cover_Resume_ProjPortfolio.pdf",
# ):
#     docx_file = pdf1_name.replace(".pdf", ".docx")

#     convert(docx_file, pdf1_name)

#     # Create a PDF file writer object
#     writer = PdfWriter()

#     # Add the pages from the first file
#     for page in PdfReader(pdf1_name).pages:
#         writer.add_page(page)

#     # Add the pages from the second file
#     for page in PdfReader(pdf2_name).pages:
#         writer.add_page(page)

#     # Write the result to the output file
#     with open(output_name, "wb") as output_file:
#         writer.write(output_file)

#     os.startfile(docx_file)
#     os.startfile(output_name)


# # # Call the function with the path to your file
# # process_file(
# #     r"C:\Users\AHMED\Desktop\AHMED\Resume\others\Analyse the following job posting a.txt
# # )

# # # Call the function with your file names
# # merge_pdfs(
# #     r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed Qureshi Cover Letter.pdf",
# #     r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed_Qureshi_Resume_ProjPortfolio.pdf",
# #     r"C:\Users\AHMED\Desktop\AHMED\Resume\pdf\Ahmed_Qureshi_Cover_Resume_ProjPortfolio.pdf",
# # )
