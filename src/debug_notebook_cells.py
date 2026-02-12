import json

nb_path = r"C:\Users\jmontanez\Documents\NBA-stats-ds-project\notebooks\2_analysis\02_detailed_analysis.ipynb"

print(f"Reading {nb_path}...")

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source_text = "".join(cell['source'])
        # Check against keywords for our problematic cell
        if "df_clustering" in source_text or "seaborn" in source_text or "sns" in source_text or "pca_1" in source_text:
            print(f"--- Cell {i} ---")
            print(source_text)
            print("----------------")
