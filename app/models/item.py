def create_item(title, genre, overview, trailer_url, image_url, director, cast, rating, release_date):
    return {
        "title": title,
        "genre": genre,
        "overview": overview,
        "trailer_url": trailer_url,
        "image_url": image_url,
        "director" : director,
        "cast" : cast,
        "rating" : rating,
        "release_date" : release_date
    }