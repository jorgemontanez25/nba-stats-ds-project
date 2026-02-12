# NBA Player Performance Predictor 🏀

A data science project that uses machine learning to predict future NBA player performance (Win Shares) and identify similar historical player seasons.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Gradio](https://img.shields.io/badge/Gradio-FF7C00?style=for-the-badge&logo=gradio&logoColor=white)
![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)


## 🚀 Live Demo
Check out the interactive web application on Hugging Face Spaces:
**[👉 NBA Player Forecaster](https://huggingface.co/spaces/Montanez25/nba-player-forecaster)**

## 📊 Project Overview

This project aims to answer two key questions for NBA analysts and fans:
1.  **Prediction**: How many wins will a player contribute next season? (Win Shares)
2.  **Comparison**: Who are the best historical comparisons for a current player? (Similarity Search)

We analyze historical NBA data (1980-2024), engineer advanced features (PER, True Shooting, Usage Rate), and train robust machine learning models to generate these insights.

## ✨ Features

-   **Predictive Modeling**: Uses a **Gradient Boosting Regressor** pipeline (with imputation and scaling) to forecast next-season Win Shares with high accuracy.
-   **Similarity Engine**: Implements a **K-Nearest Neighbors (KNN)** algorithm on standardized feature vectors to find the most statistically similar player seasons in history.
-   **Interactive Dashboard**: A user-friendly **Gradio** web app that allows users to input stats and get instant predictions.

## 🔬 Methodology

### 1. Data Processing & Feature Engineering
We utilized historical NBA data spanning **1980-2024**. Raw stats were transformed into advanced metrics to capture true player impact:
-   **True Shooting % (TS%)**: Measures scoring efficiency including 3-pointers and free throws.
-   **Usage Rate (USG%)**: Estimates the percentage of team plays used by a player.
-   **PER (Player Efficiency Rating)**: A per-minute rating of productivity (League Average is fixed at 15).

### 2. Exploratory Analysis
Key insights from our deep-dive analysis (`notebooks/2_analysis/`):
-   **Efficiency Frontier**: We mapped the trade-off between Volume (USG%) and Efficiency (TS%). Maintaining >60% TS becomes exponentially harder as Usage exceeds 30%.
-   **Player Archetypes**: Using K-Means clustering, we identified statistical roles (e.g., "Heliocentric Engines", "Rim-Running Bigs") that describe playstyle better than traditional positions (PG/SG/etc.).

### 3. Machine Learning Architecture
The project employs a robust `sklearn.pipeline.Pipeline` to ensure reproducibility and prevent data leakage:
1.  **Imputation**: Handles missing values using median strategies (robust to outliers).
2.  **Scaling**: `StandardScaler` normalizes features to Mean=0, Std=1 (critical for KNN and Regression).
3.  **Modeling**: 
    -   **Prediction**: `GradientBoostingRegressor` minimizes RMSE to forecast Win Shares.
    -   **Similarity**: `NearestNeighbors` calculates Euclidean distance in the high-dimensional feature space.

## 📊 Model Performance
-   **Feature Importance**: Random Forest analysis confirmed that **PER**, **VORP**, and **WS/48** are the strongest predictors of future success, significantly outweighing raw counting stats like Points Per Game.
-   **Error Analysis**: The model performs best on established veterans but has higher variance for rookies/sophomores due to volatile growth curves.

## 📂 Project Structure

```
├── data/
│   ├── processed/      # Cleaned analysis-ready datasets
│   └── raw/            # Original NBA data
├── models/             # Trained ML pipelines (Pickle files)
│   ├── ws_predictor_pipeline.pkl
│   └── similarity_engine_v2.pkl
├── notebooks/          # Juptyer Notebooks for analysis
│   ├── 1_eda/          # Exploratory Data Analysis
│   ├── 2_analysis/     # Deep Dive & Feature Engineering
│   └── 3_modeling/     # Model Training & Evaluation
├── hf_space/           # Deployment code for Hugging Face
│   ├── app.py          # Gradio application
│   └── requirements.txt
└── figures/            # Generated plots and visualizations
```

## 🛠️ Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Jorgemontanez25/NBA-stats-ds-project.git
    cd NBA-stats-ds-project
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♂️ Usage

### Running the Web App Locally
You can test the prediction dashboard on your local machine:

```bash
python hf_space/app.py
```
Open your browser to `http://127.0.0.1:7860`.

### Exploring the Analysis
Launch Jupyter Lab or Notebook to view the detailed analysis:

```bash
jupyter lab notebooks/2_analysis/02_detailed_analysis.ipynb
```

## 🤖 Models & Tech Stack

-   **Language**: Python 3.10+
-   **Libraries**: Scikit-learn, Pandas, NumPy, Matplotlib, Seaborn
-   **App Framework**: Gradio
-   **Deployment**: Hugging Face Spaces (Docker/SDK)

## 📝 License
This project is open-source and available under the [MIT License](LICENSE).