console.log("Chargement de search.js");

document.addEventListener('DOMContentLoaded', function() {
    console.log("Initialisation de la recherche");
    
    const searchInput = document.getElementById('searchInput');
    const suggestionsContainer = document.getElementById('suggestions');
    const selectedMovie = document.getElementById('selectedMovie');
    const moviePoster = selectedMovie.querySelector('.movie-poster img');
    const movieTitle = selectedMovie.querySelector('.movie-title');
    const recommendationsButton = selectedMovie.querySelector('.recommendations-button');

    console.log("Éléments trouvés:", {
        searchInput: !!searchInput,
        suggestionsContainer: !!suggestionsContainer,
        selectedMovie: !!selectedMovie,
        moviePoster: !!moviePoster,
        movieTitle: !!movieTitle,
        recommendationsButton: !!recommendationsButton
    });

    // Fonction pour rechercher les films
    function searchMovies(query) {
        console.log("Recherche pour:", query);
        
        if (!query || query.length < 2) {
            console.log("Requête trop courte");
            suggestionsContainer.innerHTML = '';
            suggestionsContainer.style.display = 'none';
            return;
        }

        console.log("Envoi de la requête à /api/suggest");
        fetch(`/api/suggest?query=${encodeURIComponent(query)}`)
            .then(response => {
                console.log("Réponse reçue:", response.status);
                return response.json();
            })
            .then(data => {
                console.log("Données reçues:", data);
                suggestionsContainer.innerHTML = '';
                
                if (data.suggestions && data.suggestions.length > 0) {
                    console.log(`${data.suggestions.length} suggestions trouvées`);
                    
                    data.suggestions.forEach(movie => {
                        const div = document.createElement('div');
                        div.className = 'suggestion-item';
                        div.textContent = movie.title;
                        
                        div.addEventListener('click', () => {
                            console.log("Clic sur le film:", movie);
                            
                            // Mettre à jour l'input
                            searchInput.value = movie.title;
                            
                            // Afficher le film sélectionné
                            if (movie.poster_path) {
                                moviePoster.src = movie.poster_path;
                                moviePoster.style.display = 'block';
                            } else {
                                moviePoster.style.display = 'none';
                            }
                            
                            movieTitle.textContent = movie.title;
                            selectedMovie.style.display = 'block';
                            
                            // Cacher les suggestions
                            suggestionsContainer.style.display = 'none';
                            
                            // Configurer le lien des recommandations
                            recommendationsButton.onclick = function(e) {
                                e.preventDefault();
                                console.log("Navigation vers les recommandations");
                                window.location.href = `/recommendations?movie_index=${movie.movie_index}`;
                                return false;
                            };
                        });
                        
                        suggestionsContainer.appendChild(div);
                    });
                    suggestionsContainer.style.display = 'block';
                } else {
                    console.log("Aucune suggestion trouvée");
                    suggestionsContainer.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Erreur lors de la recherche:', error);
                suggestionsContainer.style.display = 'none';
            });
    }

    // Gestionnaire d'événements pour la saisie
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        console.log("Saisie détectée:", this.value);
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            searchMovies(this.value.trim());
        }, 300);
    });

    // Fermer les suggestions si on clique en dehors
    document.addEventListener('click', function(e) {
        if (!suggestionsContainer.contains(e.target) && e.target !== searchInput) {
            suggestionsContainer.style.display = 'none';
        }
    });
});
