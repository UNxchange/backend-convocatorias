import json
import re

# Carga el archivo JSON original
with open('DataConvenios.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

processed_data = []
for item in data:
    # Ignorar registros incompletos o malformados
    if not item.get("institution") or not item.get("country"):
        print(f"Omitiendo registro incompleto: {item}")
        continue
    
    # Pre-procesamiento del campo de idiomas
    languages_str = item.get("languages", "").strip()
    if languages_str:
        # Usa una expresión regular para dividir por espacios o comas, y limpia los resultados
        languages_list = [lang.strip() for lang in re.split(r'[\s,]+', languages_str) if lang.strip()]
        item["languages"] = list(set(languages_list)) # Usa set para eliminar duplicados
    else:
        item["languages"] = []

    processed_data.append(item)

# Guarda el archivo JSON procesado y limpio
with open('DataConvenios_limpio.json', 'w', encoding='utf-8') as f:
    json.dump(processed_data, f, indent=4, ensure_ascii=False)

print("Pre-procesamiento completado. Se ha generado 'DataConvenios_limpio.json'")