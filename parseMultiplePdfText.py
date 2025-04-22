import re
from pdfminer.high_level import extract_text

def extract_text_from_pdf(file_path):
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return None

def main():
    pdf_files = ["KAILO SUMBER KASIH 1.pdf", "lenny.pdf", "linna.pdf"]  

    for pdf_file in pdf_files:
        text = extract_text_from_pdf(pdf_file)

        if text:
            pattern = re.compile(r"[a-zA-Z]+,{1}\s{1}")
            matches = pattern.findall(text)
            names = [n[:-2] for n in matches]
            print(f"File: {pdf_file}")
            print(f"Extracted Names: {names}")
            print("=" * 50)

if __name__ == "__main__":
    main()
