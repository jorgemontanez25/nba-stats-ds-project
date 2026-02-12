import json

nb_path = r"C:\Users\jmontanez\Documents\NBA-stats-ds-project\notebooks\2_analysis\02_detailed_analysis.ipynb"

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Cell 4 seems to be the one based on previous output
cell = nb['cells'][4]
source = cell['source']

with open("cell4_content.txt", "w", encoding="utf-8") as f:
    for i, line in enumerate(source):
        f.write(f"{i+1}: {line}")
