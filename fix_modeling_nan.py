import json

nb_path = 'notebooks/3_modeling/03_predictive_modeling.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Logic: Find the cell where X and y are defined and split.
# We need to add imputation or simple fillna before splitting.
# Or, better, use SimpleImputer in a pipeline, but for this notebook simplicity:
# We will just fillna(0) for stats (reasonable for NBA data) or dropna.
# Let's use SimpleImputer for a "data science" approach.

# 1. Update Imports to include SimpleImputer if not present
for cell in cells:
    source = "".join(cell['source'])
    if "from sklearn.preprocessing import StandardScaler" in source:
        if "SimpleImputer" not in source:
            new_source = source.replace(
                "from sklearn.preprocessing import StandardScaler",
                "from sklearn.preprocessing import StandardScaler\nfrom sklearn.impute import SimpleImputer"
            )
            cell['source'] = [l + "\n" for l in new_source.split("\n") if l]
            print("Added SimpleImputer import.")

# 2. Update Feature Engineering/Split Cell
found_split = False
for cell in cells:
    source = "".join(cell['source'])
    if "X = df_model[features]" in source and "train_test_split" in source:
        # We need to handle NaNs in X before split or after.
        # Let's do it before split to keep it simple.
        
        # New code to inject
        injection = """
# Handle Missing Values in Features
# Some advanced stats might be NaN for players with 0 minutes or attempts
# We'll impute with 0 or mean. For stats, 0 is often safer (no attempts = 0%)
imputer = SimpleImputer(strategy='constant', fill_value=0)
X = pd.DataFrame(imputer.fit_transform(df_model[features]), columns=features)
"""
        # Replace the simple X definition with the imputed one
        new_source = source.replace("X = df_model[features]", "X = df_model[features]" + injection)
        
        # Update cell
        cell['source'] = [l + "\n" for l in new_source.split("\n")]
        found_split = True
        print("Injected Imputation logic.")
        break

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook patched to handle NaNs.")
