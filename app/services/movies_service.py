from database.mongo import items_collection

def get_movies(page=1, limit=20, query=None):
    skip = (page - 1) * limit

    # Filtre : soit recherche par titre, soit tous les films
    filter_query = {}
    if query:
        filter_query = {"title": {"$regex": f"^{query}", "$options": "i"}}

    # Récupération avec pagination
    raw_movies = items_collection.find(filter_query).skip(skip).limit(limit)

    # Transformer les documents MongoDB en dictionnaires formatés
    movies = []
    for movie in raw_movies:
        movies.append({
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

    # Compter le total pour calculer les pages
    total_movies = items_collection.count_documents(filter_query)
    total_pages = (total_movies // limit) + (1 if total_movies % limit != 0 else 0)

    return {
        "movies": movies,
        "total_movies": total_movies,
        "total_pages": total_pages,
        "current_page": page,
        "limit": limit
    }

def count_movies_in_db():
    # Compter le nombre total de films dans la base de données
    return items_collection.count_documents({})

def get_movie_details_from_db(movie_id):
    # Rechercher le film par son ID dans la collection MongoDB
    movie = items_collection.find_one({"_id": movie_id})
    if not movie:
        return None
    return {
        "id": str(movie["_id"]),
        "title": movie.get("title", "Titre non disponible"),
        "overview": movie.get("overview", "Résumé non disponible"),
        "genres": movie.get("genres", "Genres non disponibles"),
        "image_url": movie.get("image_url", ""),
        "director": movie.get("director", "Réalisateur non disponible"),
        "cast": movie.get("cast", []),
        "rating": movie.get("rating", "Note non disponible"),
        "release_date": movie.get("release_date", "Date de sortie non disponible"),
        "trailer_url": movie.get("trailer_url", "URL de la bande-annonce non disponible")
    }
