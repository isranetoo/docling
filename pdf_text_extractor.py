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
                return "Error: PDF must have at least 2 pages.", None
            
            full_text = pdf_reader.pages[1].extract_text()
            lines = split_text_into_lines(full_text)
            
            keywords = ['VOTO', 'Ementa', 'Falência']
            positions = [full_text.lower().find(keyword.lower()) for keyword in keywords]
            valid_positions = [pos for pos in positions if pos != -1]
            
            if not valid_positions:
                print(full_text)
                return full_text, None
            
            first_keyword_pos = min(valid_positions)
            extracted_text = full_text[:first_keyword_pos].strip()
            
            nomes_a_procurar = ['APELANTE', 'APELANTES', 'APELADO', 'APELADOS', 'AGRAVANTE', 'AGRAVANTES', 'AGRAVADO', 'AGRAVADOS',
                                "REQTE", "AUTOR", "AUTORA", "EMBARGTE", "IMPUGTE", "REPRTATEAT", "EMBARGDA", "RECLAMANTE", "LIQDTEAT",
                                "IMPUGDO",  "HERDEIRO", "HERDEIRA", "INVTANTE", "RECONVINTE", "EXEQTE", "IMPTTE", "ALIMENTADO",
                                "RECORRENTE", "EXQTE", "REQUERENTE", "REMETENTE", "DEPRECANTE", "APELANTE", "AGRAVTE",
                                "EXEQUENTE", "EXEQÜENTE", "EMBARGANTE", "EMBTE", "AGRAVANTE", "AGRAVANT", "POLO ATIVO", "ATIVA",
                                "INVENTARIANTE", "IMPUGNANTE", "SUSCITANTE", "CONFTE", "PROMOVENTE", "DEMANDANTE", "DEPRECAN", "OPOENTE",
                                "CONSIGNANTE", "MPF", "MINISTÉRIO PÚBLICO", "MP", "ORDENANTE", "RECORREN", "REQUISITANTE"
                            ]
            resultados = {}
            
            for nome in nomes_a_procurar:
                for line in lines:
                    match = re.search(rf'(?i){nome}: (.+)', line)
                    if match:
                        resultados[nome] = match.group(1)
                        break
            
            return extracted_text, resultados

    except FileNotFoundError:
        return "Error: PDF file not found.", None
    except Exception as e:
        return f"Error processing PDF: {str(e)}", None

if __name__ == "__main__":
    folder_path = "scratch"
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            result, resultados = extract_text_before_keywords(pdf_path)
            print(f"\nExtracted text from {filename}:")
            print("-" * 50)
            print(result)
            if resultados:
                for nome, texto in resultados.items():
                    if texto:
                        print(f"{nome}: {texto}")
            print("-" * 50)

