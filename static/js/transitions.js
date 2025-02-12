document.addEventListener('DOMContentLoaded', () => {
    // Créer l'overlay de transition
    const overlay = document.createElement('div');
    overlay.className = 'transition-overlay';
    document.body.appendChild(overlay);

    // Animer les éléments au chargement de la page
    setTimeout(() => {
        document.querySelector('.nordic-nav')?.classList.add('visible');
        
        // Animer les cartes de films si elles existent
        document.querySelectorAll('.movie-card').forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('visible');
            }, index * 100); // Délai progressif pour chaque carte
        });

        // Animer le conteneur de détails du film s'il existe
        const movieDetails = document.querySelector('.movie-details-container');
        if (movieDetails) {
            setTimeout(() => {
                movieDetails.classList.add('visible');
            }, 100);
        }
    }, 100);

    // Gérer les transitions de page
    document.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (link && link.href && !link.target && !e.ctrlKey && !e.shiftKey && !e.metaKey && !e.altKey) {
            e.preventDefault();
            
            // Animer la sortie
            overlay.style.opacity = '1';
            
            setTimeout(() => {
                window.location.href = link.href;
            }, 500);
        }
    });

    // Gérer le bouton retour du navigateur
    window.addEventListener('popstate', () => {
        overlay.style.opacity = '1';
        
        setTimeout(() => {
            window.location.reload();
        }, 500);
    });
});
