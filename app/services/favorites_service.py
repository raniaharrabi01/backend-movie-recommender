from database.mongo import favorites_collection
from app.models.favorites import create_favorite
from database.mongo import items_collection
from bson import ObjectId

def add_favorite(data):
    """
    Ajoute ou supprime un film des favoris d'un utilisateur.
    Si le film est déjà dans les favoris, il sera supprimé.
    Sinon, il sera ajouté.
    """
    favorite = create_favorite(data["user_id"], data["item_id"])
    
    # Vérifier si le favori existe déjà
    existing_favorite = favorites_collection.find_one({
        "user_id": favorite["user_id"],
        "item_id": favorite["item_id"]
    })
    
    if existing_favorite:
        # Supprimer le film des favoris si il existe déjà
        favorites_collection.delete_one({
            "user_id": favorite["user_id"],
            "item_id": favorite["item_id"]
        })
        return {"message": "Film retiré des favoris avec succès."}, 200
    
    # Ajouter le favori à la collection si il n'existe pas
    favorites_collection.insert_one(favorite)
    return {"message": "Film ajouté aux favoris avec succès."}, 201


def get_favorites(user_id):
    favorites_cursor = favorites_collection.find({
        "user_id": str(user_id),
    })
    favorites = list(favorites_cursor)
    favorite_item_ids = [int(fav["item_id"]) for fav in favorites]
    favorite_movies_cursor = items_collection.find({"_id": {"$in": favorite_item_ids}})
    favorite_movies = []
    for movie in favorite_movies_cursor:
        favorite_movies.append({
            "id": str(movie["_id"]),
            "title": movie.get("title", "Titre non disponible"),
            "overview": movie.get("overview", "Résumé non disponible"),
            "genres": movie.get("genres", "Genres non disponibles"),
            "image_url": movie.get("image_url", ""),
            "director": movie.get("director", "Réalisateur non disponible"),
            "cast": movie.get("cast", []),
            "rating": movie.get("rating", "Note non disponible"),
            "release_date": movie.get("release_date", "Date de sortie non disponible")
        })
    return favorite_movies


