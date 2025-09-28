import joblib
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd

def train_knn_model():
    # Charger les embeddings générés par SBERT
    embeddings = np.load("app/ai/model/embeddings.npy")
    df = pd.read_csv("app/ai/model/processed_movies.csv")

    # Entraîner le modèle KNN
    model = NearestNeighbors(metric="cosine", algorithm="brute")
    model.fit(embeddings)

    # Sauvegarder le modèle  
    joblib.dump(model, "app/ai/model/knn_model.pkl")
    print("✅ Modèle KNN entraîné et sauvegardé.")

if __name__ == "__main__":
    train_knn_model()
