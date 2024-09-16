document.addEventListener('DOMContentLoaded', () => {
    const locationList = document.getElementById('location-list');
    const favoritePlaces = JSON.parse(localStorage.getItem('favoritePlaces')) || [];

    if (favoritePlaces.length > 0) {
        // 장소 즐겨찾기 눌렀을 때 개인 페이지에 장소 표시
        locationList.innerHTML = `<p>총 ${favoritePlaces.length}개</p>`;
        favoritePlaces.forEach(place => {
            const locationItem = document.createElement('div');
            locationItem.classList.add('location-item');
            locationItem.innerHTML = `
                <span>★</span> ${place}
                <button class="remove-btn" data-place="${place}">×</button>
            `;
            locationList.appendChild(locationItem);
        });

        // 'x' 버튼 눌렀을 때 개인 페이지에서 해당 장소 제거
        document.querySelectorAll('.remove-btn').forEach(button => {
            button.onclick = () => {
                const placeToRemove = button.getAttribute('data-place');
                const updatedPlaces = favoritePlaces.filter(place => place !== placeToRemove);
                localStorage.setItem('favoritePlaces', JSON.stringify(updatedPlaces));
                locationList.innerHTML = '';
                locationList.dispatchEvent(new Event('DOMContentLoaded'));
            };
        });
    } else {
        locationList.innerHTML = '<p>아직 즐겨찾기한 장소가 없습니다.</p>';
    }
});
