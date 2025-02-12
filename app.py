"""
CineFuture - Application de recommandation de films
Ce script est le coeur de l'application web qui permet de découvrir et recommander des films.
Il utilise Flask pour le backend et l'API TMDB pour les informations sur les films.
"""

# Import des bibliothèques nécessaires
from flask import Flask, render_template, jsonify, request, redirect, url_for  # Framework web Flask et ses utilitaires
import pandas as pd  # Pour la manipulation des données
import joblib  # Pour charger le modèle de recommandation
import re  # Pour les expressions régulières
from tmdbv3api import TMDb, Movie  # API TMDB pour les informations sur les films
import requests  # Pour les requêtes HTTP

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration de l'API TMDB
tmdb = TMDb()
tmdb.api_key = "4d36de16e368dd3de2ca7234f0ef230b"  # Clé API pour accéder à TMDB
tmdb.language = "fr"  # Configuration de la langue en français
movie_api = Movie()

# Chargement du dataset contenant les informations des films
df = pd.read_parquet("final_V8.parquet")
print("\nChargement des données terminé")

# Affichage des informations de débogage sur le DataFrame
print("\nInformations sur le DataFrame :")
print(df.info())

print("\nColonnes disponibles :")
print(df.columns.tolist())

print("\nPremier film :")
first_movie = df.iloc[0]
for col in df.columns:
    print(f"{col}: {first_movie[col]}")

# Détermination de la colonne à utiliser pour les titres
title_column = "title" if "title" in df.columns else "originalTitle"
print(f"\nUtilisation de la colonne : {title_column}")

# Création de la liste des titres de films disponibles
movie_titles = df[title_column].dropna().unique().tolist()
print(f"Nombre de titres chargés : {len(movie_titles)}")
print("Exemple de titres :", movie_titles[1:6])

# Chargement de la cartographie des recommandations
recommendations_map = joblib.load("cartographie.job")

def get_movie_poster(poster_path):
    """
    Génère l'URL complète pour l'affiche d'un film
    Args:
        poster_path: Chemin de l'affiche fourni par TMDB
    Returns:
        str: URL complète de l'affiche ou None si pas d'affiche
    """
    if pd.isna(poster_path) or not poster_path:
        return None
    return f"https://image.tmdb.org/t/p/w400{poster_path}"

def get_movie_details_by_title(title):
    """
    Récupère les détails complets d'un film via l'API TMDB
    Args:
        title: Titre du film à rechercher
    Returns:
        dict: Détails du film incluant titre, synopsis, date, note, etc.
    """
    try:
        print(f"\nRecherche des détails pour le film: {title}")
        # Recherche de l'ID du film via l'API TMDB
        search_url = f"https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": "4d36de16e368dd3de2ca7234f0ef230b",
            "query": title,
            "language": "fr-FR",
        }

        response = requests.get(search_url, params=params)
        data = response.json()

        if not data.get("results"):
            print(f"Aucun résultat trouvé pour: {title}")
            return None

        movie_id = data["results"][0]["id"]
        print(f"ID du film trouvé: {movie_id}")

        # Récupération des détails complets du film
        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {
            "api_key": "4d36de16e368dd3de2ca7234f0ef230b",
            "language": "fr-FR",
            "append_to_response": "credits,recommendations,videos",
        }

        print(f"\nRequête API pour les détails du film :")
        print(f"URL : {details_url}")
        print(f"Paramètres : {params}")

        response = requests.get(details_url, params=params)
        movie_data = response.json()

        print(f"Statut de la réponse : {response.status_code}")
        print(f"Clés disponibles dans la réponse : {list(movie_data.keys())}")

        # Recherche de la bande-annonce du film
        trailer = None
        print("\nRecherche de la bande-annonce...")
        if "videos" in movie_data and movie_data["videos"].get("results"):
            print(f"Nombre de vidéos trouvées : {len(movie_data['videos']['results'])}")
            for video in movie_data["videos"]["results"]:
                print(
                    f"Vidéo trouvée - Type: {video.get('type')}, Langue: {video.get('iso_639_1')}, Site: {video.get('site')}"
                )
                # Priorité aux bandes-annonces en français
                if (
                    video["site"] == "YouTube"
                    and video["type"] == "Trailer"
                    and video["iso_639_1"] == "fr"
                ):
                    trailer = f"https://www.youtube.com/embed/{video['key']}"
                    print(f"Bande-annonce FR trouvée : {trailer}")
                    break
            # Si pas de bande-annonce en français, on prend la première disponible
            if not trailer:
                print(
                    "Pas de bande-annonce FR, recherche d'une bande-annonce en autre langue..."
                )
                for video in movie_data["videos"]["results"]:
                    if video["site"] == "YouTube" and video["type"] == "Trailer":
                        trailer = f"https://www.youtube.com/embed/{video['key']}"
                        print(f"Bande-annonce trouvée : {trailer}")
                        break
        else:
            print("Aucune vidéo trouvée dans les données du film")

        print(f"URL finale de la bande-annonce : {trailer}")

        # Formatage des données du film pour l'affichage
        movie_details = {
            "title": movie_data.get("title"),
            "overview": movie_data.get("overview"),
            "release_date": movie_data.get("release_date"),
            "vote_average": movie_data.get("vote_average"),
            "vote_count": movie_data.get("vote_count"),
            "genres": [genre["name"] for genre in movie_data.get("genres", [])],
            "poster_path": (
                f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path')}"
                if movie_data.get("poster_path")
                else None
            ),
            "trailer_url": trailer,
        }

        return movie_details

    except Exception as e:
        print(f"Erreur lors de la recherche des détails du film: {str(e)}")
        return None

# Routes de l'application Flask

@app.route("/")
def home():
    """Page d'accueil de l'application"""
    return render_template("index.html")

@app.route("/search")
def search():
    """Page de recherche de films"""
    return render_template("search.html")

@app.route("/recommendations")
def recommendations():
    """
    Page de recommandations de films
    Récupère les recommandations pour un film sélectionné
    """
    try:
        movie_index = request.args.get("movie_index", type=int)
        if movie_index is None:
            print("Erreur: Index du film manquant")
            return redirect(url_for("home"))

        print(f"Recherche de recommandations pour l'index : {movie_index}")

        # Vérification de la validité de l'index
        if movie_index >= len(df):
            print(f"Erreur: Index invalide : {movie_index}")
            return redirect(url_for("home"))

        # Récupération des détails du film sélectionné
        selected_movie = df.iloc[movie_index]
        selected_movie_details = {
            "title": selected_movie["originalTitle"],
            "poster_path": get_movie_poster(selected_movie["poster_path"]),
            "overview": selected_movie["overview"],
        }

        # Récupération des recommandations
        recommended_indices = recommendations_map[movie_index]
        recommended_movies = []

        print(f"Nombre de recommandations trouvées : {len(recommended_indices)}")
        print("Indices des films recommandés :", recommended_indices)

        # On commence à l'index 0 pour inclure le premier film
        for i in range(1,6):  # Prendre 5 films à partir de l'index 0
            if i < len(recommended_indices):
                idx = recommended_indices[i]
                movie = df.iloc[idx]
                movie_details = {
                    "title": movie["originalTitle"],
                    "original_title": movie["originalTitle"],
                    "poster_path": get_movie_poster(movie["poster_path"]),
                    "overview": movie["overview"],
                    "release_date": (
                        movie["release_date"] if "release_date" in movie else None
                    ),
                    "vote_average": (
                        movie["vote_average"] if "vote_average" in movie else None
                    ),
                    "vote_count": (
                        movie["vote_count"] if "vote_count" in movie else None
                    ),
                    "genres": movie["genres"] if "genres" in movie else None,
                }
                recommended_movies.append(movie_details)
                print(f"Film {i+1} ajouté : {movie_details['title']} (index: {idx})")

        return render_template(
            "recommendations.html",
            selected_movie=selected_movie_details,
            recommended_movies=recommended_movies,
        )

    except Exception as e:
        print(f"Erreur dans recommendations() : {str(e)}")
        return redirect(url_for("home"))

@app.route("/api/suggest")
def suggest():
    """
    API pour les suggestions de films
    Renvoie une liste de films correspondant à la requête de recherche
    """
    query = request.args.get("query", "").lower()
    print(f"\nRecherche pour : '{query}'")

    try:
        # Recherche des titres qui commencent par la requête
        matching_titles = [
            title for title in movie_titles if str(title).lower().startswith(query)
        ]
        print(f"Titres trouvés : {len(matching_titles)}")
        print("Premiers titres trouvés :", matching_titles[:3])

        suggestions = []
        for title in matching_titles[:10]:  # Limiter à 10 suggestions
            try:
                # Trouver le film dans le DataFrame
                movie = df[df[title_column] == title].iloc[0]
                movie_index = df[df[title_column] == title].index[0]

                # Récupérer le poster
                poster_path = movie["poster_path"]
                if not pd.isna(poster_path):
                    poster_url = f"https://image.tmdb.org/t/p/w400{poster_path}"

                    suggestion = {
                        "title": str(title),
                        "poster_path": poster_url,
                        "movie_index": int(movie_index),
                    }
                    suggestions.append(suggestion)
                    print(f"Ajouté : {title} (index: {movie_index})")
            except Exception as e:
                print(f"Erreur pour le titre '{title}': {str(e)}")
                continue

        return jsonify({"suggestions": suggestions})
    except Exception as e:
        print(f"Erreur dans la route suggest: {str(e)}")
        return jsonify({"suggestions": []})

@app.route("/movie_details/<title>")
def view_movie_details(title):
    """
    Page de détails d'un film
    Récupère les détails du film via l'API TMDB
    """
    try:
        print(f"\n=== Affichage des détails pour le film : {title} ===")
        # Recherche des détails du film
        movie_details = get_movie_details_by_title(title)
        if movie_details:
            print("\nDétails du film trouvés :")
            for key, value in movie_details.items():
                print(f"{key}: {value}")
            return render_template("movie_details.html", movie=movie_details)
        else:
            print("Aucun détail trouvé pour ce film")
            return redirect(url_for("home"))
    except Exception as e:
        print(f"Erreur dans view_movie_details(): {str(e)}")
        return redirect(url_for("home"))

@app.route("/about/")
def about():
    """Page à propos"""
    print("Route 'about' appelée")  # Pour le débogage
    return render_template("about.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Utilisation du port donné par Render
    app.run(host="0.0.0.0", port=port, debug=True)
