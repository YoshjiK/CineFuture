document.addEventListener('DOMContentLoaded', function() {
    // Création des étoiles
    function createStars(element, count) {
        const stars = document.getElementById(element);
        for(let i = 0; i < count; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            star.style.left = `${Math.random() * 100}%`;
            star.style.top = `${Math.random() * 100}%`;
            star.style.animationDelay = `${Math.random() * 2}s`;
            stars.appendChild(star);
        }
    }

    createStars('stars', 50);
    createStars('stars2', 100);
    createStars('stars3', 150);

    // Animation du titre
    const title = document.querySelector('.glitch');
    if(title) {
        title.addEventListener('mouseover', function() {
            this.style.animation = 'none';
            setTimeout(() => {
                this.style.animation = 'glitch 1s infinite';
            }, 10);
        });
    }
});
