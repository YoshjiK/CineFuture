import os
from typing import List, Tuple, Dict, Optional
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import joblib

class MovieRecommender:
    def __init__(self, data_path: str = "final_V8.parquet"):
        """
        Initialise le système de recommandation de films
        Args:
            data_path: Chemin vers le fichier parquet contenant les données des films
        """
        # Charge les données depuis le fichier parquet
        self.data = pd.read_parquet(data_path)
        
        # Initialise les modèles comme None
        self.vectorizer = None
        self.model_knn = None
        self.neighbors_mapping = None
        
        # Chemins pour sauvegarder les modèles
        self.model_path = "modelKNN.job"
        self.mapping_path = "cartographie.job"

    def train(self) -> None:
        """
        Entraîne le modèle de recommandation en utilisant CountVectorizer et KNN
        """
        # Extrait la colonne 'bag' qui contient les caractéristiques textuelles des films
        X = self.data.bag.squeeze()

        # Initialise et entraîne le vectorizer pour convertir le texte en matrice de features
        self.vectorizer = CountVectorizer(ngram_range=(1, 2), lowercase=True)
        self.vectorizer.fit(X)
        X_CV = self.vectorizer.transform(X)

        # Initialise et entraîne le modèle KNN
        self.model_knn = NearestNeighbors(n_neighbors=6, metric="cosine")
        self.model_knn.fit(X_CV)

        # Calcule la cartographie des voisins pour tous les films
        _, self.neighbors_mapping = self.model_knn.kneighbors(X_CV)

        # Sauvegarde les modèles
        self.save_models()

    def save_models(self) -> None:
        """
        Sauvegarde les modèles entraînés sur le disque
        """
        joblib.dump(self.model_knn, self.model_path)
        joblib.dump(self.neighbors_mapping, self.mapping_path)

    def load_models(self) -> bool:
        """
        Charge les modèles sauvegardés
        Returns:
            bool: True si le chargement a réussi, False sinon
        """
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.mapping_path):
                self.model_knn = joblib.load(self.model_path)
                self.neighbors_mapping = joblib.load(self.mapping_path)
                return True
            return False
        except Exception as e:
            print(f"Erreur lors du chargement des modèles: {e}")
            return False

    def get_recommendations(self, movie_index: int) -> List[Dict]:
        """
        Obtient les recommandations pour un film donné
        Args:
            movie_index: Index du film dans le dataset
        Returns:
            List[Dict]: Liste des films recommandés avec leurs informations
        """
        if movie_index >= len(self.data) or movie_index < 0:
            return []

        # Récupère les indices des films similaires (ignore le premier qui est le film lui-même)
        similar_indices = self.neighbors_mapping[movie_index][1:]
        
        # Construit la liste des recommandations
        recommendations = []
        for idx in similar_indices:
            movie = self.data.iloc[idx]
            recommendations.append({
                'title': movie['originalTitle'],
                'overview': movie['overview'],
                'poster_path': movie['poster_path']
            })
        
        return recommendations

    def get_movie_index(self, title: str) -> Optional[int]:
        """
        Trouve l'index d'un film par son titre
        Args:
            title: Titre du film à rechercher
        Returns:
            Optional[int]: Index du film ou None si non trouvé
        """
        try:
            return self.data[self.data['originalTitle'] == title].index[0]
        except IndexError:
            return None

# Exemple d'utilisation :
if __name__ == "__main__":
    # Initialise le recommender
    recommender = MovieRecommender()
    
    # Vérifie si les modèles existent déjà
    if not recommender.load_models():
        print("Entraînement des modèles...")
        recommender.train()
    
    # Exemple de recommandation
    movie_index = recommender.get_movie_index("The Matrix")
    if movie_index is not None:
        recommendations = recommender.get_recommendations(movie_index)
        print("\nRecommandations pour 'The Matrix':")
        for movie in recommendations:
            print(f"- {movie['title']}")
