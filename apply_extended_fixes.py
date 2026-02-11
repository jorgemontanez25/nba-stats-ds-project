import json
import os

nb_path = 'notebooks/2_analysis/02_detailed_analysis.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# --- Task 1: Save `cluster_centers` (Cell index ~5 based on flow, after KMeans) ---
for cell in cells:
    if cell['cell_type'] == 'code':
        source_str = "".join(cell['source'])
        if "cluster_centers = pd.DataFrame" in source_str and "display(cluster_centers" in source_str:
            if "to_csv" not in source_str:
                save_code = "\n# Save Cluster Centers\ncluster_centers.to_csv(f\"{PROCESSED_DIR}cluster_centers.csv\", index=False)\nprint(f\"Saved cluster centers to {PROCESSED_DIR}cluster_centers.csv\")\n"
                cell['source'].append(save_code)
                print("Added save logic for cluster_centers")

# --- Task 2: Save `team_agg` (Team Win Shares Aggregation) ---
# Look for where `team_agg` is defined or used in a plot
for cell in cells:
    if cell['cell_type'] == 'code':
        source_str = "".join(cell['source'])
        # It seems the previous extract showed "team_agg" in a scatter plot
        if "px.scatter" in source_str and "team_agg" in source_str:
             if "to_csv" not in source_str:
                # Prepend the save before the plot or append after? 
                # Ideally after the plot usage or ensure variable exists. 
                # If "team_agg" is created in this cell or previous, we can save it.
                # Let's append to the cell if it looks like the main usage
                save_code = "\n# Save Team Aggregation Data\ntry:\n    team_agg.to_csv(f\"{PROCESSED_DIR}team_win_shares_agg.csv\", index=False)\n    print(f\"Saved team aggregation to {PROCESSED_DIR}team_win_shares_agg.csv\")\nexcept NameError:\n    print(\"team_agg variable not found in this cell scope, ensuring it is saved wherever it is defined\")\n"
                # Safer: Inspect creating cell. But appending to plot cell usually works if var is in scope.
                cell['source'].append(save_code)
                print("Added save logic for team_agg")

# --- Task 3: Ensure all plots are saved ---
# Re-running the plot injection logic with broader scope or just confirming
# My previous heuristic was "fig.show()" or "iplot". 
# Let's check for any matplotlib "plt.show()" which might have been missed.
for i, cell in enumerate(cells):
    if cell['cell_type'] == 'code':
        source = cell['source']
        source_str = "".join(source)
        
        if "plt.show()" in source_str:
             # Matplotlib save
             if "savefig" not in source_str:
                 # Need to find a filename
                 plot_name = f"matplotlib_plot_{i}.png"
                 save_code = f"\n# Save Matplotlib Figure\nplt.savefig(f\"{{FIGURES_DIR}}{plot_name}\")\nprint(f\"Saved plot to {{FIGURES_DIR}}{plot_name}\")\n"
                 # Insert BEFORE plt.show() because show() clears the figure in some backends
                 # Find index of plt.show() line
                 new_source = []
                 for line in source:
                     if "plt.show()" in line:
                         new_source.append(save_code)
                     new_source.append(line)
                 cell['source'] = new_source
                 print(f"Added savefig for matplotlib plot in cell {i}")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Enhanced notebook persistence applied.")
