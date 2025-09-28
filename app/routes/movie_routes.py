from flask import Blueprint, request, jsonify
from app.services.tmdb_service import fetch_and_save_movies 
from app.services.movies_service import get_movies, get_movie_details_from_db


movie_bp = Blueprint("movie", __name__)

@movie_bp.route("/api/movies/db")
def get_movies_route():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    query = request.args.get('search', None)
    data = get_movies(page, limit, query)
    return jsonify(data)


@movie_bp.route("/api/movies/<int:movie_id>")
def get_movie_by_id(movie_id):
    # Appeler le service pour récupérer les détails du film
    movie = get_movie_details_from_db(movie_id)
    if not movie:
        return jsonify({"error": f"Film avec l'ID {movie_id} non trouvé."}), 404
    return jsonify(movie)

