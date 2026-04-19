import zipfile
import glob
import re

def extract_text_from_docx(file_path):
    with zipfile.ZipFile(file_path, 'r') as z:
        content = z.read('word/document.xml').decode('utf-8')
        # Simple regex to extract text from XML tags
        text = re.sub('<[^>]+>', ' ', content)
        # Normalize whitespace
        text = re.sub('\s+', ' ', text).strip()
        return text

if __name__ == "__main__":
    files = glob.glob('Tài liệu*.docx')
    if files:
        print(f"Reading {files[0]}:")
        print(extract_text_from_docx(files[0]))
    else:
        print("No docx file found.")
