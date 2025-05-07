from database.mongo import favorites_collection
from app.models.favorites import create_favorite
from database.mongo import items_collection
from bson import ObjectId

def add_favorite(data):
    """
    Ajoute un film aux favoris d'un utilisateur.
    """
    favorite = create_favorite(data["user_id"], data["item_id"])
    # Vérifier si le favori existe déjà
    existing_favorite = favorites_collection.find_one({
        "user_id": favorite["user_id"],
        "item_id": favorite["item_id"]
    })
    if existing_favorite:
        return {"message": "Le film est déjà dans les favoris."}, 400

    # Ajouter le favori à la collection
    favorites_collection.insert_one(favorite)
    return {"message": "Film ajouté aux favoris avec succès."}, 201


def remove_favorite(user_id, item_id):
    """
    Supprime un film des favoris d'un utilisateur.
    """
    # Vérifier si le favori existe
    result = favorites_collection.delete_one({
        "user_id": user_id,
        "item_id": item_id
    })
    if result.deleted_count == 0:
        return {"message": "Le film n'est pas dans les favoris."}, 404

    return {"message": "Film supprimé des favoris avec succès."}, 200


from bson.objectid import ObjectId

def get_favorites(user_id):
    favorites_cursor = favorites_collection.find({
        "user_id": user_id,
    })
    favorites = list(favorites_cursor)
    print("🎯 Favoris trouvés :", favorites)
    # Récupérer les IDs des items favoris (assumés ici comme étant des ObjectId stockés en string)
    favorite_item_ids = [ObjectId(fav["item_id"]) for fav in favorites]
    print("🎬 IDs de films favoris :", favorite_item_ids)
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
    print("📽️ Films correspondants formatés :", favorite_movies)
    return favorite_movies


