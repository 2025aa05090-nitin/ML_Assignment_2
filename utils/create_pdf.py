from fpdf import FPDF
import re

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'ML Assignment 2 Submission - 2025aa05090', 0, 1, 'R')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, label, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln()

pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Read content
with open("submission_report.md", "r") as f:
    text = f.read()

# Simple Markdown Parsing
lines = text.split('\n')
for line in lines:
    if line.startswith('# '):
        # Title
        pdf.set_font('Arial', 'B', 24)
        pdf.cell(0, 15, line.replace('# ', ''), 0, 1, 'C')
        pdf.ln(10)
    elif line.startswith('## '):
        # Header
        pdf.chapter_title(line.replace('## ', ''))
    elif line.startswith('### '):
        # Subheader
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, line.replace('### ', ''), 0, 1, 'L')
    elif line.startswith('![BITS_lab_screenshot]'):
        # Image
        try:
            pdf.image('BITS_lab_screenshot.png', w=170)
            pdf.ln(5)
            pdf.set_font('Arial', 'I', 9)
            pdf.cell(0, 5, 'Screenshot of assignment execution on BITS Virtual Lab', 0, 1, 'C')
            pdf.ln(10)
        except Exception as e:
            pdf.set_text_color(255, 0, 0)
            pdf.cell(0, 10, f"Error loading image: {e}", 0, 1)
            pdf.set_text_color(0, 0, 0)
    elif line.strip().startswith('|'):
        # Table row (very basic handling)
        pdf.set_font('Courier', '', 9)
        pdf.multi_cell(0, 5, line)
    else:
        # Normal text
        pdf.set_font('Arial', '', 11)
        # Handle bold/links roughly if needed, or just print
        clean_line = line.replace('**', '').replace('`', '')
        if clean_line.strip():
            pdf.multi_cell(0, 6, clean_line)
        else:
            pdf.ln(2)

pdf.output("ML_Assignment_2_Submission.pdf")
print("PDF Generated Successfully!")
