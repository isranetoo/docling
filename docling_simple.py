from docling.document_converter import DocumentConverter
import os
import re
import json
from PyPDF2 import PdfReader

def extract_uppercase_after_term(content, term):
    pattern = f'{term}[^.]*?([A-Z][A-Z\s]+(?=[a-z]|\.|$))'
    matches = re.finditer(pattern, content, re.IGNORECASE)
    results = []
    for match in matches:
        if len(match.groups()) > 0:
            uppercase_text = match.group(1).strip()
            if uppercase_text:
                results.append(uppercase_text)
    return results

def save_search_results(content, search_terms, base_filename):
    results_dict = {}
    for term, file_suffix in search_terms.items():
        uppercase_matches = extract_uppercase_after_term(content, term)
        if uppercase_matches:
            results_dict[file_suffix] = uppercase_matches[0]  
    
    if results_dict:
        json_filename = f"{os.path.splitext(base_filename)[0]}_results.json"
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(results_dict, json_file, ensure_ascii=False, indent=4)
        print(f"Saved results to: {json_filename}")
    else:
        print("No matches found to save")

def process_pdf(pdf_path, search_terms):
    reader = PdfReader(pdf_path)
    all_content = []
    
    print(f"Processing {len(reader.pages)} pages...")
    for page_num, page in enumerate(reader.pages, 1):
        print(f"Processing page {page_num}/{len(reader.pages)}")
        text = page.extract_text()
        all_content.append(text)
    
    return "\n".join(all_content)

searc = {
    "apelante": 'apelante',
    "apelado": 'apelado',
    "apelada": 'apelada',
    "embargante": 'embargante',
    "embargado": 'embargado',
    "embargada": 'embargada',
    "agravante": 'agravante',
    "agravado": 'agravado',
    "agravada": 'agravada',
}

source = "doc_168639972.pdf"

pdf_content = process_pdf(source, searc)

converter = DocumentConverter()
result = converter.convert(source)
output_filename = os.path.splitext(source)[0] + ".md"

markdown_content = result.document.export_to_markdown()

with open(output_filename, "w", encoding="utf-8") as f:
    f.write(markdown_content)
print(f"Converted document saved to: {output_filename}")

save_search_results(pdf_content, searc, source)


