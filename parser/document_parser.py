import pdfplumber

def extract_text(file):

    if file.name.endswith(".pdf"):
        text = ""

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"

        return text

    else:
        return file.read().decode("utf-8")