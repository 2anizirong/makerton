document.addEventListener('DOMContentLoaded', () => {
    const mainElement = document.querySelector('main');
    const favoriteIcon = document.getElementById('favorite-icon');
    
    // 장소명이랑 유저 이름 불러오기
    const placeName = mainElement.getAttribute('data-place-name');
    const userName = mainElement.getAttribute('data-user-name');

    // 유저 로그인 확인
    if (userName) {
        // 유저가 로그인을 한 경우 즐겨찾기 표시 할 수 있게 아이콘 표시
        favoriteIcon.style.display = 'inline';

        // 로컬 스토리지에서 즐겨찾기 장소 목록 가져오기
        let favoritePlaces = JSON.parse(localStorage.getItem('favoritePlaces')) || [];

        // 해당 장소가 현재 이미 즐겨찾기로 표시되어 있는지 확인
        const isFavorite = favoritePlaces.includes(placeName);

        if (isFavorite) {
            // 즐겨찾기 표시가 되어있으면 아이콘 활성화
            favoriteIcon.classList.add('active');
            favoriteIcon.textContent = '★';
        }

        // 아이콘 클릭 시 즐겨찾기 상태로 계속 토글시키기
        favoriteIcon.onclick = () => {
            if (favoriteIcon.classList.contains('active')) {
                // 즐겨찾기 해제
                favoriteIcon.classList.remove('active');
                favoriteIcon.textContent = '☆';
                favoritePlaces = favoritePlaces.filter(place => place !== placeName);
            } else {
                // 즐겨찾기 추가
                favoriteIcon.classList.add('active');
                favoriteIcon.textContent = '★';
                favoritePlaces.push(placeName);
            }

            // 로컬 스토리지 업뎃
            localStorage.setItem('favoritePlaces', JSON.stringify(favoritePlaces));
        };
    } else {
        // 유저 로그인 안한 경우 즐겨찾기 아이콘 숨김
        favoriteIcon.style.display = 'none';
    }
});
