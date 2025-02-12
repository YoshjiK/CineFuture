document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('movieModal');
    const closeBtn = document.querySelector('.modal-close');
    const moviePosters = document.querySelectorAll('.movie-poster');

    // DEBUG: Afficher tous les posters et leurs attributs
    console.log('Nombre de posters trouvés:', moviePosters.length);
    moviePosters.forEach((poster, index) => {
        console.log(`\nPoster ${index + 1}:`, {
            title: poster.getAttribute('data-movie-title'),
            overview: poster.getAttribute('data-movie-overview'),
            poster: poster.getAttribute('data-movie-poster'),
            release: poster.getAttribute('data-movie-release'),
            rating: poster.getAttribute('data-movie-rating'),
            votes: poster.getAttribute('data-movie-votes'),
            genres: poster.getAttribute('data-movie-genres')
        });
    });

    function showModal(movieData) {
        console.log('Affichage du modal avec les données:', movieData);

        // Mise à jour du contenu
        const titleElement = modal.querySelector('.modal-title');
        const posterElement = modal.querySelector('.modal-poster');
        const descriptionElement = modal.querySelector('.modal-description');
        const starsElement = modal.querySelector('.stars');
        const votesElement = modal.querySelector('.vote-count');
        const dateElement = modal.querySelector('.modal-date');
        const genresElement = modal.querySelector('.modal-genres');

        console.log('Éléments trouvés:', {
            title: titleElement,
            poster: posterElement,
            description: descriptionElement,
            stars: starsElement,
            votes: votesElement,
            date: dateElement,
            genres: genresElement
        });

        if (titleElement) titleElement.textContent = movieData.title || '';
        if (posterElement && movieData.posterPath) posterElement.src = movieData.posterPath;
        if (descriptionElement) descriptionElement.textContent = movieData.overview || '';

        // Note et votes
        if (starsElement && movieData.rating) {
            const rating = parseFloat(movieData.rating) / 2;
            const fullStars = Math.floor(rating);
            const stars = '★'.repeat(fullStars) + '☆'.repeat(5 - fullStars);
            starsElement.textContent = stars;
            
            if (votesElement && movieData.votes) {
                const votes = parseInt(movieData.votes).toLocaleString('fr-FR');
                votesElement.textContent = `(${votes} votes)`;
            }
        }

        // Date de sortie
        if (dateElement && movieData.releaseDate) {
            try {
                const date = new Date(movieData.releaseDate);
                const formattedDate = date.toLocaleDateString('fr-FR', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric'
                });
                dateElement.textContent = `Sortie le ${formattedDate}`;
            } catch (error) {
                console.error('Erreur lors du formatage de la date:', error);
                dateElement.textContent = movieData.releaseDate;
            }
        }

        // Genres
        if (genresElement && movieData.genres) {
            genresElement.textContent = movieData.genres;
        }

        // Afficher le modal
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        console.log('Modal affiché !');
    }

    function hideModal() {
        modal.style.display = 'none';
        document.body.style.overflow = '';
        console.log('Modal fermé');
    }

    // Event listeners
    moviePosters.forEach(poster => {
        poster.addEventListener('click', () => {
            const movieTitle = poster.getAttribute('data-movie-title');
            if (movieTitle) {
                window.location.href = `/movie_details/${encodeURIComponent(movieTitle)}`;
            }
        });
    });

    closeBtn.addEventListener('click', hideModal);

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            hideModal();
        }
    });
});
