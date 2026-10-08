import os
import pickle
import joblib
import pandas as pd
from pathlib import Path

def get_artifacts_dir() -> Path:
    root = Path(__file__).resolve().parent.parent
    candidates = [
        root / "data" / "artifacts",
        root / "artifacts"
    ]
    for path in candidates:
        if os.path.isdir(path) and os.path.exists(path / "tfidf_recommender.pkl"):
            return path
    raise FileNotFoundError(f"Could not find valid artifacts directory in: {candidates}")

def load_all_artifacts():
    artifacts_dir = get_artifacts_dir()
    
    # 1. Load models & metadata
    tfidf = joblib.load(artifacts_dir / "tfidf_recommender.pkl")
    mlp = joblib.load(artifacts_dir / "taste_dl_model.pkl")
    
    with open(artifacts_dir / "label_encoder.pkl", "rb") as f:
        label_encoder = pickle.load(f)
        
    df = pd.read_parquet(artifacts_dir / "recipes_processed.parquet")
    
    # 2. Fast load precomputed matrix (takes <0.2s instead of minutes)
    matrix_path = artifacts_dir / "tfidf_matrix.pkl"
    if matrix_path.exists():
        catalog_matrix = joblib.load(matrix_path)
    else:
        # Fallback only if not precomputed
        catalog_matrix = tfidf.transform(df["clean_ingredients"])
    
    return tfidf, mlp, label_encoder, df, catalog_matrix