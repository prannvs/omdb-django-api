from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
import time

OMDB_API_KEY = getattr(settings, "OMDB_API_KEY")

@api_view(["GET"])
def movie_details(request):
    title = request.GET.get("title")

    if not title:
        return Response({"error": "Movie title is required"}, status=400)

    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    r = requests.get(url)
    data = r.json()

    if data.get("Response") == "False":
        return Response({"error": data.get("Error")}, status=404)

    clean_data = {
        "Title": data.get("Title"),
        "Year": data.get("Year"),
        "Plot": data.get("Plot"),
        "Country": data.get("Country"),
        "Awards": data.get("Awards"),
        "Director": data.get("Director"),
        "Ratings": data.get("Ratings"),
    }

    return Response(clean_data)

@api_view(["GET"])
def episode_details(request):
    Title = request.GET.get('Title')
    Season = request.GET.get('Season')
    Epnumber = request.GET.get('Epnumber')

    if not Title or not Season or not Epnumber:
        return Response({"error": "Please provide series_title, Season, and episode_number"},status=400)

    url = (f"http://www.omdbapi.com/?t={Title}&Season={Season}&Episode={Epnumber}&apikey={OMDB_API_KEY}")

    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "False":
        return Response({"error": data.get("Error")}, status=404)

    result = {
        "Title": data.get("Title"),
        "Released": data.get("Released"),
        "Season": data.get("Season"),
        "Episode": data.get("Episode"),
        "Plot": data.get("Plot"),
        "Director": data.get("Director"),
        "Writer": data.get("Writer"),
        "Actors": data.get("Actors"),
        "imdbRating": data.get("imdbRating"),
    }
    return Response(result)

genrekeys = {
    "action": ["fight", "battle", "hero", "war", "mission", "chase", "spy"],
    "adventure": ["journey", "quest", "treasure", "explore", "island", "expedition"],
    "animation": ["cartoon", "animated", "pixar", "disney", "magic"],
    "biography": ["true story", "based on", "life of", "biopic"],
    "comedy": ["funny", "friends", "party", "holiday", "crazy"],
    "crime": ["detective", "police", "gangster", "murder", "heist"],
    "drama": ["life", "family", "story", "truth", "journey"],
    "fantasy": ["magic", "dragon", "king", "realm", "myth"],
    "horror": ["ghost", "dark", "fear", "haunted", "zombie", "killer"],
    "mystery": ["murder", "detective", "secret", "clue"],
    "romance": ["love", "heart", "kiss", "wedding", "dream"],
    "sci-fi": ["space", "alien", "robot", "future", "planet"],
    "thriller": ["chase", "danger", "spy", "murder", "crime"],
    "war": ["battle", "army", "soldier", "fight", "rescue"],
    "western": ["cowboy", "gun", "outlaw", "frontier", "train"],
    "musical": ["music", "song", "dance", "band", "stage"],
    "documentary": ["real", "history", "nature", "story", "world"],
}


@api_view(["GET"])
def genre(request):
    genre = request.GET.get("genre")

    if not genre:
        return Response({"error": "Genre parameter is required"}, status=400)

    genre = genre.lower()

    keywords = genrekeys.get(genre, ["movie","film"])
    collectm = []
    c=1
    for keyword in keywords:
        if keyword=='movie' or keyword=='film':
            if c>25:
                c=1
                continue
            else:
                c+=1
        else:
            if c>7:
                c=1
                continue
            else:
                c+=1
        url = f"http://www.omdbapi.com/?s={keyword}&type=movie&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        time.sleep(1)
        data = response.json()

        if data.get("Response") == "False":
            continue

        for item in data.get("Search", []):
            imdb_id = item.get("imdbID")
            if not imdb_id:
                continue

            url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
            response = requests.get(url)
            details = response.json()

            if genre in details.get("Genre", "").lower():
                rating = details.get("imdbRating")
                try:
                    rating = float(rating)
                except (TypeError, ValueError):
                    rating = 0.0

                collectm.append({
                    "Title": details.get("Title"),
                    "Year": details.get("Year"),
                    "Genre": details.get("Genre"),
                    "imdbRating": rating,
                    "Plot": details.get("Plot"),
                    "Director": details.get("Director"),
                    "Poster": details.get("Poster"),
                })

    sorted_movies = sorted(collectm, key=lambda x: x["imdbRating"], reverse=True)

    top_movies = sorted_movies[:15]

    if not top_movies:
        return Response({"message": f"No movies found for genre '{genre}'"}, status=404)

    return Response(top_movies)

@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok"}, status=200)

@api_view(["GET"])
def recommend_movies(request):
    favmovie = request.GET.get("favmovie")
    
    if not favmovie:
        return Response({"error": "favmovie parameter is required"}, status=400)
    
    url = f"http://www.omdbapi.com/?t={favmovie}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data.get("Response") == "False":
        return Response({"error": data.get("Error")}, status=404)
    
    genrelist = data.get("Genre", "").split(", ")
    directorlist = data.get("Director", "").split(", ")
    actorlist = data.get("Actors", "").split(", ")
    
    collected = set()
    recommendations = []

    def fetch(name,list):
        movies = []
        for value in list:
            url = f"http://www.omdbapi.com/?s={value}&type=movie&apikey={OMDB_API_KEY}"
            r = requests.get(url)
            time.sleep(1)
            results = r.json()
            
            if results.get("Response") == "False":
                continue
            
            for item in results.get("Search", []):
                imdb_id = item.get("imdbID")
                if imdb_id in collected or imdb_id == data.get("imdbID"):
                    continue

                detail_url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
                detail_resp = requests.get(detail_url).json()

                if name == "Genre":
                    if not any(g.lower() in detail_resp.get("Genre", "").lower() for g in list):
                        continue
                elif name == "Director":
                    if not any(d.lower() in detail_resp.get("Director", "").lower() for d in list):
                        continue
                elif name == "Actors":
                    if not any(a.lower() in detail_resp.get("Actors", "").lower() for a in list):
                        continue

                try:
                    rating = float(detail_resp.get("imdbRating", 0))
                except ValueError:
                    rating = 0.0

                movie_data = {
                    "Title": detail_resp.get("Title"),
                    "Year": detail_resp.get("Year"),
                    "Genre": detail_resp.get("Genre"),
                    "Director": detail_resp.get("Director"),
                    "Actors": detail_resp.get("Actors"),
                    "imdbRating": rating,
                    "Plot": detail_resp.get("Plot"),
                }
                movies.append(movie_data)
                collected.add(imdb_id)

                if len(movies) >= 20:
                    break
            if len(movies) >= 20:
                break

        movies.sort(key=lambda x: x["imdbRating"], reverse=True)
        return movies

    level1 = fetch("Genre", genrelist)
    recommendations.extend(level1)

    if len(recommendations) < 20:
        level2 = fetch("Director", directorlist)
        recommendations.extend(level2)

    if len(recommendations) < 20:
        level3 = fetch("Actors", actorlist)
        recommendations.extend(level3)

    recommendations = sorted(recommendations, key=lambda x: x["imdbRating"], reverse=True)[:20]

    if not recommendations:
        return Response({"message": "No recommendations found."}, status=404)

    return Response(recommendations)