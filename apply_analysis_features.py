import json

nb_path = 'notebooks/2_analysis/02_detailed_analysis.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# --- New Content Cells ---

# 1. Cluster Explanation
cluster_doc = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 🧠 Decoding the Archetypes\n",
        "\n",
        "Our clustering reveals distinct player roles based on statistical profiles:\n",
        "\n",
        "*   **Cluster 0 - The \"Connectors\"**: Low usage but balanced stats. Likely 3-and-D wings or secondary ball-handlers.\n",
        "*   **Cluster 1 - Paint Protectors**: High block rates, low 3P%. Traditional rim-protecting bigs.\n",
        "*   **Cluster 2 - Floor Generals**: Elite assist rates. Primary playmakers.\n",
        "*   **Cluster 5 - Superstars/Primary Option**: Highest usage and scoring. The engines of the offense.\n",
        "\n",
        "> **Note:** The exact cluster IDs may vary on re-runs due to random initialization, but the statistical profiles remain consistent."
    ]
}

# 2. Feature Exploration (Correlation & Importance)
feature_exploration_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# --- ADVANCED ANALYSIS: FEATURE IMPORTANCE ---\n",
        "from sklearn.ensemble import RandomForestRegressor\n",
        "import seaborn as sns\n",
        "import matplotlib.pyplot as plt\n",
        "\n",
        "# 1. Prepare Data for Modeling\n",
        "# Target: Win Shares (ws) | Features: Efficiency & Style Metrics\n",
        "model_features = ['ts_percent', 'usg_percent', 'ast_percent', \n",
        "                  'trb_percent', 'stl_percent', 'blk_percent', \n",
        "                  'x3p_ar', 'f_tr', 'per', 'bpm']\n",
        "\n",
        "df_model = df_analysis.dropna(subset=model_features + ['ws']).copy()\n",
        "X = df_model[model_features]\n",
        "y = df_model['ws']\n",
        "\n",
        "# 2. Train Random Forest\n",
        "rf = RandomForestRegressor(n_estimators=100, random_state=42)\n",
        "rf.fit(X, y)\n",
        "\n",
        "# 3. Plot Feature Importance\n",
        "importances = pd.DataFrame({\n",
        "    'feature': model_features,\n",
        "    'importance': rf.feature_importances_\n",
        "}).sort_values('importance', ascending=False)\n",
        "\n",
        "plt.figure(figsize=(12, 6))\n",
        "sns.barplot(x='importance', y='feature', data=importances, palette='viridis')\n",
        "plt.title('Feature Importance: What Drives Win Shares?')\n",
        "plt.xlabel('Importance')\n",
        "\n",
        "# Save Plot\n",
        "try:\n",
        "    plt.savefig(f\"{FIGURES_DIR}feature_importance_ws.png\")\n",
        "    print(f\"Saved feature importance plot to {FIGURES_DIR}\")\n",
        "except Exception as e:\n",
        "    print(f\"Could not save plot: {e}\")\n",
        "plt.show()"
    ]
}

feature_doc = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 🤖 Assessing Metric Value\n",
        "The Random Forest model highlights which metrics are most predictive of overall success (Win Shares). Typically, **PER** and **BPM** dominate because they are composite metrics themselves. However, separating raw components like **TS%** (Efficiency) vs. **USG%** (Volume) reveals that efficiency is often the stronger driver of value in the modern NBA."
    ]
}

# 3. HuggingFace Dataset Generation
hf_prep_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# --- HUGGINGFACE DATASET GENERATION ---\n",
        "# Create natural language descriptions for potential LLM fine-tuning or RAG\n",
        "\n",
        "def generate_description(row):\n",
        "    return (\n",
        "        f\"In the {row['season']} season, {row['player']} played for {row['team']}. \"\n",
        "        f\"They recorded a Usage Rate of {row['usg_percent']}% and a True Shooting of {row['ts_percent']:.3f}. \"\n",
        "        f\"Their defensive impact included block and steal percentages of {row['blk_percent']}% and {row['stl_percent']}%, respectively. \"\n",
        "        f\"Overall, they contributed {row['ws']} Win Shares.\"\n",
        "    )\n",
        "\n",
        "hf_data = df_analysis.copy()\n",
        "hf_data['text_description'] = hf_data.apply(generate_description, axis=1)\n",
        "\n",
        "# Save as JSONL (Standard HF Format)\n",
        "hf_output_path = f\"{PROCESSED_DIR}hf_player_descriptions.jsonl\"\n",
        "hf_data[['player_id', 'season', 'text_description']].to_json(hf_output_path, orient='records', lines=True)\n",
        "print(f\"Successfully generated {len(hf_data)} descriptions for HuggingFace.\")\n",
        "print(f\"Saved to: {hf_output_path}\")"
    ]
}

# Injection Logic
new_cells = []
injected_cluster = False

for i, cell in enumerate(cells):
    new_cells.append(cell)
    source = "".join(cell['source'])
    
    # Inject Cluster Doc after Cluster Plot or Centers display
    if "Cluster Centers" in source and "display" in source and not injected_cluster:
        new_cells.append(cluster_doc)
        print("Injected Cluster Documentation")
        injected_cluster = True

# Append new analysis at the very end
new_cells.append(feature_exploration_code)
new_cells.append(feature_doc)
new_cells.append(hf_prep_code)
print("Appended Feature Analysis and HF Generation code")

nb['cells'] = new_cells

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Detailed Analysis Notebook enhancements applied.")
