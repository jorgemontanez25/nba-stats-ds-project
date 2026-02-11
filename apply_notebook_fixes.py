import json
import os

nb_path = 'notebooks/2_analysis/02_detailed_analysis.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# --- Fix 1: Inject persistence setup in Cell 1 (Imports) ---
# Content to look for: "init_notebook_mode"
setup_code = [
    "\n",
    "# Persistence Paths\n",
    "PROJ_ROOT = \"../../\"\n",
    "FIGURES_DIR = f\"{PROJ_ROOT}figures/\"\n",
    "PROCESSED_DATA_PATH = f\"{PROJ_ROOT}data/processed/02_analysis_data.csv\"\n",
    "\n",
    "import os\n",
    "os.makedirs(FIGURES_DIR, exist_ok=True)\n",
    "os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)\n"
]

found_imports = False
for cell in cells:
    if cell['cell_type'] == 'code':
        source_str = "".join(cell['source'])
        if "init_notebook_mode" in source_str and "FIGURES_DIR" not in source_str:
            # Append setup code
            cell['source'].extend(setup_code)
            found_imports = True
            print("Injected setup code into Import cell.")
            break

# --- Fix 2: Modify Data Loading (Cell 3 usually) ---
# Content to look for: "df_adv = pd.read_csv(ADVANCED_STATS_PATH)"
new_data_loading_source = [
    "# Load and Merge (Persistence Implemented)\n",
    "if os.path.exists(PROCESSED_DATA_PATH):\n",
    "    print(f\"Loading processed data from {PROCESSED_DATA_PATH}...\")\n",
    "    df_clustering = pd.read_csv(PROCESSED_DATA_PATH)\n",
    "    df_analysis = df_clustering.copy() # Keeping logical flow\n",
    "    print(f\"Loaded {len(df_clustering)} rows.\")\n",
    "else:\n",
    "    print(\"Processing raw data...\")\n",
    "    df_adv = pd.read_csv(ADVANCED_STATS_PATH)\n",
    "    df_basic = pd.read_csv(BASIC_STATS_PATH)\n",
    "\n",
    "    # Filter Modern Era\n",
    "    df_adv = df_adv[df_adv['season'] >= 1980].copy()\n",
    "    df_basic = df_basic[df_basic['season'] >= 1980].copy()\n",
    "\n",
    "    # Merge to get a full feature set\n",
    "    # UPDATED: Added drb_percent, orb_percent\n",
    "    cols_adv = ['player_id', 'season', 'team', \n",
    "                'ts_percent', 'per', 'usg_percent', 'ws', 'bpm', 'vorp', \n",
    "                'ast_percent', 'trb_percent', 'stl_percent', 'blk_percent', \n",
    "                'x3p_ar', 'f_tr', 'drb_percent', 'orb_percent']\n",
    "\n",
    "    cols_adv = [c for c in cols_adv if c in df_adv.columns]\n",
    "    master_df = pd.merge(df_basic, df_adv[cols_adv], on=['player_id', 'season', 'team'], how='inner')\n",
    "\n",
    "    # Filter for 'TOT' or unique teams to avoid duplicates\n",
    "    tot_players = master_df[master_df['team'] == 'TOT'][['player_id', 'season']]\n",
    "    master_df = master_df.merge(tot_players, on=['player_id', 'season'], how='left', indicator='is_traded')\n",
    "    df_analysis = master_df[(master_df['team'] == 'TOT') | (master_df['is_traded'] == 'left_only')].copy()\n",
    "    df_analysis.drop(columns=['is_traded'], inplace=True)\n",
    "\n",
    "    print(f\"Analysis Dataset Size: {len(df_analysis)} players\")\n",
    "\n",
    "    # --- FEATURE ENGINEERING ---\n",
    "    season_avgs = df_analysis.groupby('season')[['ts_percent', 'x3p_ar', 'f_tr', 'usg_percent']].transform('mean')\n",
    "    df_analysis['rel_ts'] = (df_analysis['ts_percent'] - season_avgs['ts_percent']) * 100\n",
    "    df_analysis['rel_x3par'] = (df_analysis['x3p_ar'] - season_avgs['x3p_ar']) * 100\n",
    "\n",
    "    # Filter for substantial minutes\n",
    "    df_clustering = df_analysis[df_analysis['mp'] > 1000].copy()\n",
    "    print(f\"Clustering Dataset Size (Min 1000 MP): {len(df_clustering)}\")\n",
    "\n",
    "    # Save processed data\n",
    "    print(f\"Saving processed data to {PROCESSED_DATA_PATH}...\")\n",
    "    df_clustering.to_csv(PROCESSED_DATA_PATH, index=False)\n"
]

found_data = False
for cell in cells:
    if cell['cell_type'] == 'code':
        source_str = "".join(cell['source'])
        if "df_adv = pd.read_csv(ADVANCED_STATS_PATH)" in source_str:
            cell['source'] = new_data_loading_source
            found_data = True
            print("Replaced Data Loading cell.")
            break

# --- Fix 3: Inject Figure Saving ---
# Identify plots by 'fig.show()' or 'px.'
plot_count = 0
for i, cell in enumerate(cells):
    if cell['cell_type'] == 'code':
        source = cell['source']
        source_str = "".join(source)
        
        # Check for typical plot creation/display
        if "fig.show()" in source_str or "iplot(" in source_str:
            plot_name = f"analysis_plot_{plot_count}.html"
            
            # Simple heuristic for naming
            if "kmeans" in source_str.lower() or "cluster" in source_str.lower():
                plot_name = "player_archetypes_clusters.html"
            elif "win share" in source_str.lower() or "ws" in source_str.lower():
                plot_name = "team_win_shares.html"
            elif "feature importance" in source_str.lower():
                plot_name = "feature_importance.html"
            
            # Injection code
            save_code = f"\n# Save Figure\ntry:\n    fig.write_html(f\"{{FIGURES_DIR}}{plot_name}\")\n    print(f\"Saved plot to {{FIGURES_DIR}}{plot_name}\")\nexcept Exception as e:\n    print(f\"Error saving figure: {{e}}\")\n"
            
            # Avoid double injection
            if "fig.write_html" not in source_str:
                cell['source'].append(save_code)
                print(f"Injected save logic for {plot_name} in cell {i}")
                plot_count += 1

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook fixes applied successfully.")
