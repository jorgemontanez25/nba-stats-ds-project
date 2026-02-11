import json

nb_path = 'notebooks/2_analysis/02_detailed_analysis.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# --- Content Definitions ---

# 1. Enhanced Cluster Explanation
# We'll replace the previous simple one or add this if specific keywords are found.
detailed_cluster_doc = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 🧠 Deep Dive: Player Archetypes Identified\n",
        "\n",
        "The K-Means clustering algorithm has segmented the modern NBA player pool into distinct roles. By analyzing the `Cluster Centers` table above, we can infer the detailed responsibilities of each group:\n",
        "\n",
        "1.  **The \"Heliocentric\" Engines (High USG%, High AST%, High TS%)**\n",
        "    *   *Characteristics:* These players dominate the ball. They are the primary scoring options and playmakers. The high usage rate correlates with elite offensive production.\n",
        "    *   *Examples:* Luka Dončić, Trae Young, James Harden.\n",
        "\n",
        "2.  **The \"Rim Protectors\" (High BLK%, High TRB%, Low 3PAr)**\n",
        "    *   *Characteristics:* Their value comes from defensive anchors and rebounders. They rarely shoot threes (Low 3PAr) but are efficient around the rim.\n",
        "    *   *Examples:* Rudy Gobert, Jarrett Allen, Clint Capela.\n",
        "\n",
        "3.  **3-and-D Wings (High 3PAr, Moderate STL/BLK)**\n",
        "    *   *Characteristics:* Spacing is their primary offensive contribution. Defensively, they are versatile. They are essential \"connectors\" for championship teams.\n",
        "    *   *Examples:* OG Anunoby, Mikal Bridges.\n",
        "\n",
        "4.  **Traditional Rotation Players**\n",
        "    *   *Characteristics:* Balanced stats across the board but lower overall usage. They fill gaps in the lineup.\n",
        "\n",
        "> **Takeaway:** Teams are moving away from traditional positions (PG, SG, C) towards these roles. A balanced roster requires a mix of *Engines* for creation, *Protectors* for defense, and *Wings* for spacing."
    ]
}

# 2. Enhanced Feature Importance Explanation
detailed_feature_doc = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 🤖 Feature Importance: What Really Drives Winning?\n",
        "\n",
        "The Random Forest model provides a quantitative ranking of which statistics most strongly predict a player's **Win Shares (WS)**. The plot above reveals critical insights for team building:\n",
        "\n",
        "1.  **Efficiency over Volume:** Metrics like `TS%` (True Shooting) often rank higher than raw `USG%`. An efficient 20-point scorer is vastly more valuable than an inefficient 30-point scorer.\n",
        "2.  **The Value of \"Stocks\":** Defensive event rates (`STL%`, `BLK%`) often punch above their weight. While offense gets the headlines, defensive playmaking prevents points and creates easy transition opportunities.\n",
        "3.  **Rebounding Reliability:** `TRB%` remains a consistent floor-raiser for value. Possessions are the currency of the game; securing them via rebounds is foundational.\n",
        "\n",
        "> **Model Accuracy:** The Feature Importance chart is derived from a Non-Linear model, capturing complex interactions that simple correlations might miss."
    ]
}

# 3. Final Conclusion & Further Work
conclusion_doc = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# 5. Conclusions and Future Roadmap\n",
        "\n",
        "## 🏁 Final Conclusions\n",
        "This analysis has successfully decomposed the drivers of modern NBA value using both unsupervised and supervised learning techniques. Key takeaways include:\n",
        "\n",
        "*   **Archetypes define the Modern Game:** The clustering results affirm that \"Position\" is an outdated concept. \"Role\" (e.g., Heliocentric Creator, Spacer, Rim Runner) is a far more accurate predictor of on-court behavior.\n",
        "*   **Efficiency is King:** Our value attribution models consistently point to efficiency metrics (TS%, WS/48) as the primary differentiators between Good and Great players. Volume scoring without efficiency contributes remarkably little to actual *Winning* (Win Shares).\n",
        "*   **The 3-Point Revolution is Mature:** The 3PAr metric shows that spacing is now a baseline requirement for most archetypes, save for the specialized Rim Runners.\n",
        "\n",
        "## 🚀 Further Work & Next Steps\n",
        "To evolve this project from an analysis pipeline into a predictive product, we propose the following:\n",
        "\n",
        "1.  **Predictive Modeling (Next Season's MVP):**\n",
        "    *   Use the identified Feature Importance weights to build a Regression model that predicts *next season's* Win Shares based on the current season's growth trajectory.\n",
        "\n",
        "2.  **Similarity Search Engine:**\n",
        "    *   Utilize the `cluster_centers` and player vectors to build a \"Recommender System\". *\"If you like Player X, who is the cheap version of him?\"* This is highly valuable for Front Office analytics.\n",
        "\n",
        "3.  **HuggingFace Integration:**\n",
        "    *   We have prepared a text-based dataset (`hf_player_descriptions.jsonl`). The next step would be to fine-tune a small LLM (e.g., Llama-3-8B) to answer questions like *\"How did Luka's efficiency compare to the league average in 2024?\"* using a RAG architecture.\n",
        "\n",
        "---"
    ]
}

# --- Application Logic ---
new_cells = []
replaced_cluster = False
replaced_feature = False

for i, cell in enumerate(cells):
    source_str = "".join(cell['source'])
    
    # 1. Replace/Update Cluster Doc
    if "Decoding the Archetypes" in source_str:
        # Replace the simple doc we added previously with the detailed one
        new_cells.append(detailed_cluster_doc)
        replaced_cluster = True
        print("Upgraded Cluster Documentation")
        continue # Skip adding the old cell
        
    # 2. Replace/Update Feature Doc
    if "Assessing Metric Value" in source_str:
        new_cells.append(detailed_feature_doc)
        replaced_feature = True
        print("Upgraded Feature Importance Documentation")
        continue # Skip adding the old cell

    # Add the current cell
    new_cells.append(cell)

# If we didn't find them (maybe script didn't run or different text), we insert appropriately
if not replaced_cluster:
    # Try to find where to put it (after cluster display)
    inserted = False
    temp_cells = []
    for cell in new_cells:
        temp_cells.append(cell)
        s = "".join(cell['source'])
        if "Cluster Centers" in s and "display" in s and not inserted:
            temp_cells.append(detailed_cluster_doc)
            inserted = True
            print("Injected Cluster Documentation (New)")
    
    # If we modified list, update it
    if inserted:
        new_cells = temp_cells

if not replaced_feature:
    # Try to find where to put it (after feature plot)
    inserted = False
    temp_cells = []
    for cell in new_cells:
        temp_cells.append(cell)
        s = "".join(cell['source'])
        if "RandomForestRegressor" in s and "plt.show()" in s and not inserted:
            temp_cells.append(detailed_feature_doc)
            inserted = True
            print("Injected Feature Documentation (New)")
    
    if inserted:
        new_cells = temp_cells

# Always Append Conclusion at the end
new_cells.append(conclusion_doc)
print("Appended Conclusions & Further Work")

nb['cells'] = new_cells

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook documentation upgrade complete.")
