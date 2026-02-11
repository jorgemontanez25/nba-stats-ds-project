import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import os

# Paths
PROJ_ROOT = ""
PROCESSED_DATA_PATH = f"data/processed/02_analysis_data.csv"

def check_data(df, name):
    print(f"--- Checking {name} ---")
    if isinstance(df, np.ndarray):
        df = pd.DataFrame(df)
    
    nans = df.isna().sum().sum()
    infs = np.isinf(df).sum().sum()
    print(f"Total NaNs: {nans}")
    print(f"Total Infs: {infs}")
    
    if nans > 0:
        print("Columns with NaNs:")
        print(df.isna().sum()[df.isna().sum() > 0])
    
    if infs > 0:
        # Check which columns have infs
        is_inf = np.isinf(df)
        inf_counts = is_inf.sum()
        print("Columns with Infs:")
        print(inf_counts[inf_counts > 0])

# Load Data
print("Loading data...")
df = pd.read_csv(PROCESSED_DATA_PATH)

df = df.sort_values(by=['player_id', 'season'])
df['target_next_ws'] = df.groupby('player_id')['ws'].shift(-1)
df_model = df.dropna(subset=['target_next_ws']).copy()

features = [
    'age', 'g', 'gs', 'mp', 
    'per', 'ts_percent', 'usg_percent', 'ws', 'bpm', 'vorp',
    'rel_ts', 'rel_x3par', 'x3p_ar', 'f_tr',
    'orb_percent', 'drb_percent', 'ast_percent', 'stl_percent', 'blk_percent'
]

X_raw = df_model[features]
check_data(X_raw, "Raw X (before imputation)")

# Impute
print("\nApplying SimpleImputer...")
imputer = SimpleImputer(strategy='constant', fill_value=0)
X_imputed_val = imputer.fit_transform(X_raw)
X = pd.DataFrame(X_imputed_val, columns=features)
check_data(X, "X (after imputation)")

y = df_model['target_next_ws']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale
print("\nScaling...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
check_data(X_train_scaled, "X_train_scaled")

# Check if scaler introduced NaNs (e.g. from Infs in input)
