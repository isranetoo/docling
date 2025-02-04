import PyPDF2
import re
import os

def split_text_into_lines(text):
    return text.split('\n')

def extract_text_before_keywords(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            if len(pdf_reader.pages) < 2:
                return "Error: PDF must have at least 2 pages.", None, None, None, None
            
            full_text = pdf_reader.pages[1].extract_text()
            lines = split_text_into_lines(full_text)
            
            keywords = ['VOTO', 'Ementa', 'Falência']
            positions = [full_text.find(keyword) for keyword in keywords]
            valid_positions = [pos for pos in positions if pos != -1]
            
            if not valid_positions:
                print(full_text)
                return full_text, None, None, None, None
            
            first_keyword_pos = min(valid_positions)
            extracted_text = full_text[:first_keyword_pos].strip()
            
            active_party = re.search(r'Parte Ativa: (.+)', extracted_text)
            passive_party = re.search(r'Parte Passiva: (.+)', extracted_text)
            
            apelante = re.search(r'Apelante: (.+)', extracted_text)
            apelada = re.search(r'Apelada: (.+)', extracted_text)
            
            nome_parte_ativa = active_party.group(1) if active_party else None
            nome_parte_passiva = passive_party.group(1) if passive_party else None
            nome_apelante = apelante.group(1) if apelante else None
            nome_apelada = apelada.group(1) if apelada else None
            
            return extracted_text, nome_parte_ativa, nome_parte_passiva, nome_apelante, nome_apelada

    except FileNotFoundError:
        return "Error: PDF file not found.", None, None, None, None
    except Exception as e:
        return f"Error processing PDF: {str(e)}", None, None, None, None

if __name__ == "__main__":
    folder_path = "scratch"
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            result, nome_parte_ativa, nome_parte_passiva, nome_apelante, nome_apelada = extract_text_before_keywords(pdf_path)
            print(f"\nExtracted text from {filename}:")
            print("-" * 50)
            print(result)
            print("-" * 50)