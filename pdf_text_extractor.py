import PyPDF2
import re

def extract_text_before_keywords(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            full_text = ''
            for page in pdf_reader.pages:
                full_text += page.extract_text()

            voto_index = full_text.find('VOTO')
            ementa_index = full_text.find('Ementa')

            if voto_index == -1 and ementa_index == -1:
                return "Neither 'VOTO' nor 'Ementa' found in the document."
            
            if voto_index == -1:
                cut_index = ementa_index
            elif ementa_index == -1:
                cut_index = voto_index
            else:
                cut_index = min(x for x in (voto_index, ementa_index) if x >= 0)

            return full_text[:cut_index].strip()

    except FileNotFoundError:
        return "Error: PDF file not found."
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

if __name__ == "__main__":
    pdf_path = input("Enter the path to your PDF file: ")
    result = extract_text_before_keywords(pdf_path)
    print("\nExtracted text:")
    print("-" * 50)
    print(result)
    print("-" * 50)
