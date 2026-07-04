import os
import json
import spacy
from markitdown import MarkItDown


def anonymize_file(source_path, output_path, pseudonym_map_path):
    if not os.path.exists(source_path):
        print(f"Erro: O arquivo {source_path} não existe.")
        return

    with open(source_path, "r", encoding="utf-8") as f:
        original_text = f.read()

    doc = nlp(original_text)
    detected_names = set()

    for entity in doc.ents:
        if entity.label_ == "PER":
            detected_names.add(entity.text)

    pseudonym_map = {}
    anonymized_document = original_text


    for index, name in enumerate(list(detected_names)):
        pseudonym = f"[PESSOA_{index + 1}]"
        pseudonym_map[pseudonym] = name
        anonymized_document = anonymized_document.replace(name, pseudonym)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(anonymized_document)

    with open(pseudonym_map_path, "w", encoding="utf-8") as f:
        json.dump(pseudonym_map, f, ensure_ascii=False, indent=4)

    print(f"Anonimização concluída: {len(detected_names)} identidades protegidas.")
    return anonymized_document


def desanonymize_file(source_path, output_path, pseudonym_map_path):

    if not os.path.exists(pseudonym_map_path) or not os.path.exists(source_path):
        print("Error: Arquivo anonimizado ou mapa de pseudônimos não encontrados.")
        return

    with open(pseudonym_map_path, "r", encoding="utf-8") as f:
        pseudonym_map = json.load(f)

    with open(source_path, "r", encoding="utf-8") as f:
        anonymized_text = f.read()

    restored_text = anonymized_text

    for pseudonym, original_name in pseudonym_map.items():
        restored_text = restored_text.replace(pseudonym, original_name)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(restored_text)

    print("Desanonimização concluída: Nomes originais restaurados.")
    return restored_text



print("loading spaCy...")
try:
    nlp = spacy.load("pt_core_news_lg")
except OSError:
    print("Error: cant find this spacy model!")
    exit()

md = MarkItDown()


if __name__ == "__main__":

    source_file = "documento.pdf"
    
    # SUBSTITUIR PELO PATH CORRETO LEMBRANDO DO LANCE DO ONEDRIVE: Spheniscidae viraria Aluis... Pasta OneDrive > Documentos > tiolu
    md_file = r"C:\Users\Spheniscidae\Documents\testes_python\documento_convertido.md"
    anonymized_file = r"C:\Users\Spheniscidae\Documents\testes_python\documento_anonimizado.md"
    pseudonym_map_file = r"C:\Users\Spheniscidae\Documents\testes_python\mapa_de_pseudonimos.json"

    print(f"\nProcessando {source_file} com o plugin MarkItDown...")
    result = md.convert_local(source_file)

    with open(md_file, "w", encoding="utf-8") as f:
        f.write(result.text_content)
    print(f"Sucesso! Arquivo bruto salvo em {md_file}")

    print(f"\nAplicando filtro de privacidade com spaCy...")
    anonymize_file(
        source_path=md_file, 
        output_path=anonymized_file,
        pseudonym_map_path=pseudonym_map_file
    )
    print(f"Sucesso! O arquivo protegido e a chave JSON foram salvos com sucesso.")