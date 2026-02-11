import gradio as gr
import pandas as pd
import numpy as np
import joblib
import os

# --- Load Models & Data ---
MODEL_DIR = "models"
DATA_PATH = "data/processed/02_analysis_data.csv"

print("Loading models...")
try:
    ws_predictor = joblib.load(os.path.join(MODEL_DIR, "ws_predictor_pipeline.pkl"))
    sim_engine = joblib.load(os.path.join(MODEL_DIR, "similarity_engine_v2.pkl"))
    print("Models loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")
    # Create dummy models for testing if files are missing during development
    ws_predictor = None
    sim_engine = None

print("Loading reference data...")
try:
    df_ref = pd.read_csv(DATA_PATH)
    # MUST sort exactly as done during training to ensure indices align
    df_ref = df_ref.sort_values(by=['player_id', 'season']).reset_index(drop=True)
    print(f"Reference data loaded: {len(df_ref)} rows.")
except Exception as e:
    print(f"Error loading data: {e}")
    df_ref = pd.DataFrame()

# Feature list matches the training columns exactly
FEATURES = [
    'age', 'g', 'gs', 'mp', 
    'per', 'ts_percent', 'usg_percent', 'ws', 'bpm', 'vorp',
    'rel_ts', 'rel_x3par', 'x3p_ar', 'f_tr',
    'orb_percent', 'drb_percent', 'ast_percent', 'stl_percent', 'blk_percent'
]

def predict_nba_performance(*inputs):
    """
    Predicts next season's Win Shares and finds similar historical player seasons.
    """
    if ws_predictor is None or sim_engine is None:
        return "Models not loaded.", pd.DataFrame()

    # Create DataFrame from inputs
    input_dict = dict(zip(FEATURES, inputs))
    input_df = pd.DataFrame([input_dict])
    
    # 1. Predict Future WS
    # The pipeline handles scaling/imputation
    pred_ws = ws_predictor.predict(input_df)[0]
    
    # 2. Find Similar Players
    # We use the similarity engine pipeline to transform and search
    # Access the scaler/imputer from the pipeline if needed, or just let the pipeline do it?
    # The saved 'sim_engine' is a Pipeline with steps: ['imputer', 'scaler', 'knn']
    
    # To get neighbors, we need to transform the data first using the first two steps
    # because 'knn' step is the estimator.
    try:
        # Transform using imputer and scaler
        processed_query = sim_engine.named_steps['imputer'].transform(input_df)
        processed_query = sim_engine.named_steps['scaler'].transform(processed_query)
        
        # Get neighbors from the knn step
        knn = sim_engine.named_steps['knn']
        distances, indices = knn.kneighbors(processed_query)
        
        # Look up players in df_ref
        similar_players = []
        for i, idx in enumerate(indices[0]):
            # Skip the first one if it's the player themselves (not possible here since query is new input)
            # But normally index 0 is the closest.
            if idx < len(df_ref):
                player_data = df_ref.iloc[idx]
                similar_players.append({
                    "Player": player_data['player'],
                    "Season": player_data['season'],
                    "Similarity Score": f"{1/(1+distances[0][i]):.2f}", # Mock score or just distance
                    "Distance": f"{distances[0][i]:.3f}",
                    "WS": player_data['ws'],
                    "PER": player_data['per']
                })
        
        sim_df = pd.DataFrame(similar_players)
        
    except Exception as e:
        return f"Prediction: {pred_ws:.2f}\nError in similarity search: {str(e)}", pd.DataFrame()
        
    output_str = f"Predicted Next Season Win Shares: {pred_ws:.2f}"
    
    return output_str, sim_df

# --- Gradio Interface ---
# Create inputs
inputs = []
for feature in FEATURES:
    # Set reasonable default values based on averages/medians if possible, 
    # or just 0 for now. Using approximate league averages for defaults.
    default_val = 0.0
    if feature == 'age': default_val = 25.0
    if feature == 'g': default_val = 60.0
    if feature == 'mp': default_val = 2000.0
    if feature == 'per': default_val = 15.0
    
    inputs.append(gr.Number(label=feature, value=default_val))

# Create Output components
output_text = gr.Textbox(label="Prediction")
output_df = gr.Dataframe(label="Similar Historical Seasons")

demo = gr.Interface(
    fn=predict_nba_performance,
    inputs=inputs,
    outputs=[output_text, output_df],
    title="NBA Player Performance Predictor 🏀",
    description="Enter a player's current season stats to predict their **Next Season Win Shares** and find **Similar Historical Players**.",
    allow_flagging="never"
)

if __name__ == "__main__":
    demo.launch()
