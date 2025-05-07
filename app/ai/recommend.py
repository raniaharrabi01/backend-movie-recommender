import joblib
import pandas as pd
import numpy as np

def recommend_movies(query_id, n=5):
    # Charger les données
    df = pd.read_csv("app/ai/model/processed_movies.csv")
    embeddings = np.load("app/ai/model/embeddings.npy")
    model = joblib.load("app/ai/model/knn_model.pkl")
    query_id = int(query_id) 

    # Vérifier que l'ID existe dans les données
    if query_id not in df["id"].values:
        return f"❌ Film avec l'ID {query_id} non trouvé dans les données."

    # Trouver l'index du film demandé
    idx = df[df["id"] == query_id].index[0]

    # Trouver les n films les plus similaires (en ignorant le film lui-même)
    distances, indices = model.kneighbors([embeddings[idx]], n_neighbors=n+1)

    recommended_indices = indices.flatten()[1:]  # On saute le premier (le film lui-même)
    recommended_movies = []
    for i, movie_idx in enumerate(recommended_indices):
        movie = df.iloc[movie_idx]
        recommended_movies.append({
            "id": movie["id"],
            "title": movie["title"],
            "overview": movie["overview"],
        })
    recommended_ids = [int(df.iloc[i]["id"]) for i in recommended_indices]
    return recommended_ids

# Exemple de test
if __name__ == "__main__":
    results = recommend_movies(822119, n=6)
    for movie_id in results:
        print("🎬 : ",movie_id)
        print("-" * 40)
