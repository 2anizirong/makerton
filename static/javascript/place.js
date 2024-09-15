document.addEventListener('DOMContentLoaded', () => {
    const mainElement = document.querySelector('main');
    const favoriteIcon = document.getElementById('favorite-icon');
    
    // Get place name and user name from data attributes
    const placeName = mainElement.getAttribute('data-place-name');
    const userName = mainElement.getAttribute('data-user-name');

    // Check if user is logged in
    if (userName) {
        // Show the favorite icon if logged in
        favoriteIcon.style.display = 'inline';

        // Get the list of favorite places from localStorage
        let favoritePlaces = JSON.parse(localStorage.getItem('favoritePlaces')) || [];

        // Check if the current place is already a favorite
        const isFavorite = favoritePlaces.includes(placeName);

        if (isFavorite) {
            favoriteIcon.classList.add('active');
            favoriteIcon.textContent = '★';
        }

        // Toggle favorite status on icon click
        favoriteIcon.onclick = () => {
            if (favoriteIcon.classList.contains('active')) {
                // Remove favorite
                favoriteIcon.classList.remove('active');
                favoriteIcon.textContent = '☆';
                favoritePlaces = favoritePlaces.filter(place => place !== placeName);
            } else {
                // Add to favorite
                favoriteIcon.classList.add('active');
                favoriteIcon.textContent = '★';
                favoritePlaces.push(placeName);
            }

            // Update localStorage
            localStorage.setItem('favoritePlaces', JSON.stringify(favoritePlaces));
        };
    } else {
        // Hide the favorite icon if not logged in
        favoriteIcon.style.display = 'none';
    }
});
