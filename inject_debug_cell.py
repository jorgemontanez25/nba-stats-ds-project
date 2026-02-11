import json

nb_path = 'notebooks/3_modeling/03_predictive_modeling.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Find the cell that creates X and splits data
# We want to insert a check AFTER it.
target_cell_index = -1
for i, cell in enumerate(cells):
    source = "".join(cell['source'])
    if "X_train_scaled = scaler.fit_transform(X_train)" in source:
        target_cell_index = i
        break

if target_cell_index != -1:
    # Create Debug Cell
    debug_source = [
        "# --- DEBUG CELL ---\n",
        "print(\"Checking for NaNs/Infs in Data...\")\n",
        "print(f\"X (imputed) NaNs: {X.isna().sum().sum()}\")\n",
        "print(f\"X_train NaNs: {X_train.isna().sum().sum()}\")\n",
        "print(f\"X_train_scaled NaNs: {np.isnan(X_train_scaled).sum()}\")\n",
        "print(f\"X_train_scaled Infs: {np.isinf(X_train_scaled).sum()}\")\n",
        "\n",
        "if np.isnan(X_train_scaled).sum() > 0:\n",
        "    print(\"ERROR: NaNs found in scaled data!\")\n",
        "    # Find which column caused it\n",
        "    df_scaled = pd.DataFrame(X_train_scaled, columns=features)\n",
        "    print(df_scaled.isna().sum()[df_scaled.isna().sum() > 0])\n",
        "else:\n",
        "    print(\"Data looks clean. Proceeding to Model.\")\n"
    ]
    
    debug_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": debug_source
    }
    
    # Insert after the split/scale cell
    cells.insert(target_cell_index + 1, debug_cell)
    
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    
    print("Injected debug cell into notebook.")
else:
    print("Could not find target cell to inject debug code.")
