import json
import os

nb_path = 'notebooks/2_analysis/02_detailed_analysis.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Find Cell 1 (Imports/Setup)
for cell in cells:
    if cell['cell_type'] == 'code':
        source = cell['source']
        source_str = "".join(source)
        
        # Check if this is the setup cell (contains PROJ_ROOT definition)
        if "PROJ_ROOT =" in source_str:
            # Check if PROCESSED_DIR is missing
            if "PROCESSED_DIR =" not in source_str:
                # Find line with PROCESSED_DATA_PATH to insert nearby
                new_source = []
                for line in source:
                    new_source.append(line)
                    if "PROCESSED_DATA_PATH =" in line:
                        new_source.append("PROCESSED_DIR = f\"{PROJ_ROOT}data/processed/\"\n")
                
                cell['source'] = new_source
                print("Injected PROCESSED_DIR definition.")
            else:
                print("PROCESSED_DIR already defined.")
            break

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Variable fix applied.")
