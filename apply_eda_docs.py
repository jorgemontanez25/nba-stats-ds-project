import json

nb_path = 'notebooks/1_eda/01_advanced_eda.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
new_cells = []

# Efficiency Frontier Explanation
efficiency_text = [
    "### 🔎 Key Insights: The Efficiency Frontier\n",
    "\n",
    "**1. The Superstar Zone (Top Right):** Players like **Nikola Jokić** and **Joel Embiid** reside here. They shoulder massive offensive loads (High Usage) while maintaining elite efficiency (High TS%). This combination is rare and defines MVP-caliber impact.\n",
    "\n",
    "**2. High Volume, Low Efficiency (Bottom Right):** Players in this quadrant score a lot but at a cost to team efficiency. They might act as \"floor raisers\" for bad teams but often struggle to lead elite offenses efficiently.\n",
    "\n",
    "**3. Role Player Efficiency (Top Left):** Centers like **Rudy Gobert** or **Jarrett Allen** often show incredibly high TS% but on low usage (dunks/putbacks). While efficient, their offensive role is dependent on others creating for them."
]

efficiency_markdown_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": efficiency_text
}

# Value Attribution Explanation
value_text = [
    "### 📊 What Drives Value (VORP)?\n",
    "\n",
    "By analyzing correlations with **VORP (Value Over Replacement Player)**, we can see which metrics best predict overall player impact:\n",
    "\n",
    "*   **BPM (Box Plus/Minus):** Shows the strongest correlation, as VORP is directly derived from it. It's a comprehensive box-score aggregation.\n",
    "*   **WS/48 (Win Shares Per 48):** Highly correlated, emphasizing that winning contributions (efficiency, defense) align with value metrics.\n",
    "*   **PER (Player Efficiency Rating):** Good correlation but tends to overvalue volume scoring compared to BPM/WS."
]

value_markdown_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": value_text
}

# Logic to insert
# We look for the cells that generate the plots.
# Based on context: Efficiency Frontier is usually early (Cell ~4-5).
# Value/Correlation is usually later.

for i, cell in enumerate(cells):
    new_cells.append(cell)
    
    # Check for Efficiency Frontier Plot
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "Efficiency Frontier" in source and "iplot" in source:
            new_cells.append(efficiency_markdown_cell)
            print("Injected Efficiency Explanation")
            
    # Check for Correlation/Value Plot
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "heatmap" in source.lower() or "correlation" in source.lower():
             # Basic check to avoid duplicates if re-running
             if "What Drives Value" not in source: 
                 new_cells.append(value_markdown_cell)
                 print("Injected Value Explanation")

nb['cells'] = new_cells

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("EDA Notebook documentation enhanced.")
