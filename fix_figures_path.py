import json
import os

nb_path = 'notebooks/3_modeling/03_predictive_modeling.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# 1. Inject FIGURES_DIR definition into Setup Cell
setup_found = False
for cell in cells:
    source = "".join(cell['source'])
    if "PROCESSED_DATA_PATH =" in source and "FIGURES_DIR" not in source:
        # Add FIGURES_DIR
        new_lines = [
            'FIGURES_DIR = f"{PROJ_ROOT}figures/"\n',
            'os.makedirs(FIGURES_DIR, exist_ok=True)\n'
        ]
        
        # Insert before last line (usually the os.makedirs calls)
        cell_source_lines = cell['source']
        # Find insertion point (before existing os.makedirs or at end)
        insert_idx = len(cell_source_lines)
        for i, line in enumerate(cell_source_lines):
            if "os.makedirs" in line:
                insert_idx = i
                break
        
        cell_source_lines[insert_idx:insert_idx] = new_lines
        cell['source'] = cell_source_lines
        setup_found = True
        print("Injected FIGURES_DIR definition.")
        break
    elif "FIGURES_DIR" in source:
        print("FIGURES_DIR already defined.")
        setup_found = True

# 2. Fix the savefig calls (Revert user's manual incorrect fix and use FIGURES_DIR)
# User likely has: plt.savefig("../figures/...", ...)
# We want: plt.savefig(f"{FIGURES_DIR}prediction_v2_actual_vs_pred.png")

for cell in cells:
    if cell['cell_type'] == 'code':
        source = cell['source']
        new_source = []
        modified = False
        for line in source:
            if "plt.savefig" in line:
                # Naive replacement of string literal path with variable
                if '"../figures/' in line or "'../figures/" in line:
                    # Replace hardcoded relative path
                    line = line.replace('"../figures/', 'f"{FIGURES_DIR}')
                    line = line.replace("'../figures/", 'f"{FIGURES_DIR}')
                    # Remove end quote if it was inside the path? No, path structure differs.
                    # "../figures/file.png" -> f"{FIGURES_DIR}file.png"
                    # User line: plt.savefig("../figures/prediction_v2_actual_vs_pred.png",dpi=300)
                    # We want: plt.savefig(f"{FIGURES_DIR}prediction_v2_actual_vs_pred.png", dpi=300)
                    # The replace above creates: plt.savefig(f"{FIGURES_DIR}prediction_v2_actual_vs_pred.png",dpi=300)
                    modified = True
                elif "FIGURES_DIR" not in line and "prediction" in line:
                     # Fallback if they undid changes or it's just a filename
                     # E.g. plt.savefig("prediction.png")
                     pass 
            new_source.append(line)
        
        if modified:
            cell['source'] = new_source
            print("Fixed plt.savefig call.")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook patched.")
