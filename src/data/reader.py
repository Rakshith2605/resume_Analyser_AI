import PyPDF2

def upload_and_read_pdf(pdf_file):

    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Extract text from all pages
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    return text.strip()