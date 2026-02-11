import json

nb_path = 'notebooks/1_eda/01_advanced_eda.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    # Print cell type and start of source to identify locations
    source_snippet = "".join(cell['source'])[:100].replace("\n", " ")
    print(f"Cell {i} ({cell['cell_type']}): {source_snippet}...")
