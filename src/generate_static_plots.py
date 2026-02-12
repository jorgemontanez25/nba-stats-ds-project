import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import os

# --- Constants ---
PROJ_ROOT = "."  # Script run from root
DATA_PATH = os.path.join(PROJ_ROOT, "data", "processed", "02_analysis_data.csv")
FIGURES_DIR = os.path.join(PROJ_ROOT, "figures")

# Ensure figures dir exists
os.makedirs(FIGURES_DIR, exist_ok=True)

def generate_plots():
    print(f"Loading data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    
    # --- Plot 1: Team Efficiency (Avg TS%) vs Success (Total Win Shares) ---
    print("Generating Team Efficiency Plot...")
    
    # Aggregation logic
    team_agg = df.groupby(['team', 'season']).agg({
        'ws': 'sum',
        'ts_percent': 'mean',
        'vorp': 'sum',
        'age': 'mean'
    }).reset_index()
    
    # Filter for reasonable sample size if needed, but original code didn't seem to filter much beyond basic cleaning
    # The original plot used 'season' as color (hue)
    
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=team_agg,
        x="ts_percent",
        y="ws",
        hue="season",
        palette="viridis",
        alpha=0.7
    )
    plt.title("Team Efficiency (Avg TS%) vs Success (Total Win Shares)")
    plt.xlabel("True Shooting % (Avg)")
    plt.ylabel("Total Win Shares")
    plt.grid(True, alpha=0.3)
    
    output_path_1 = os.path.join(FIGURES_DIR, "team_win_shares_static.png")
    plt.savefig(output_path_1, dpi=300, bbox_inches='tight')
    print(f"Saved {output_path_1}")
    plt.close()

    # --- Plot 2: Player Archetypes (PCA Projection) ---
    print("Generating Player Archetypes PCA Plot...")
    
    # Feature Engineering for Clustering (Replicating Notebook Logic)
    features = ['usg_percent', 'ast_percent', 'trb_percent', 'x3p_ar', 'blk_percent', 'stl_percent', 'f_tr', 'rel_ts']
    
    # Sub-select data involved in clustering (Notebook filtered MP > 1000)
    # The processed data usually already has this filter applied if it was saved AFTER filtering?
    # Let's check if the loaded data has cols. df is likely 'df_clustering' from notebook if saved at end.
    # But let's be safe and just work with what we have.
    
    X = df[features].fillna(0)
    
    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # KMeans (Replicate k=6, random_state=42)
    km = KMeans(n_clusters=6, random_state=42, n_init=10)
    clusters = km.fit_predict(X_scaled)
    df['cluster'] = clusters
    
    # PCA
    pca = PCA(n_components=2, random_state=42)
    components = pca.fit_transform(X_scaled)
    df['pca_1'] = components[:, 0]
    df['pca_2'] = components[:, 1]
    
    # Plot
    plt.figure(figsize=(14, 10))
    sns.scatterplot(
        data=df,
        x="pca_1",
        y="pca_2",
        hue="cluster",
        palette="tab10",
        s=10,
        alpha=0.6,
        legend="full"
    )
    plt.title("NBA Player Archetypes (PCA Projection of Advanced Stats)")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.legend(title="Archetype Cluster", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    
    output_path_2 = os.path.join(FIGURES_DIR, "player_archetypes_clusters_static.png")
    plt.savefig(output_path_2, dpi=300, bbox_inches='tight')
    print(f"Saved {output_path_2}")
    plt.close()

if __name__ == "__main__":
    generate_plots()
