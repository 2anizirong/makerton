const editProfileBtn = document.getElementById('editProfileBtn');
const modal = document.getElementById('editProfileModal');
const closeBtn = document.querySelector('.close');
const profileImageUpload = document.getElementById('profileImageUpload');
const profileImage = document.getElementById('profileImage');
const saveProfileImageBtn = document.getElementById('saveProfileImageBtn');

editProfileBtn.onclick = () => {
    modal.style.display = 'block';
};

closeBtn.onclick = () => {
    modal.style.display = 'none';
};

window.onclick = (event) => {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};

// 페이지 로드 시 localStorage에서 저장된 이미지 로드
const storedImage = localStorage.getItem('profileImage');
if (storedImage) {
    profileImage.src = storedImage;
}

// 프로필 이미지 변경 및 localStorage에 저장
saveProfileImageBtn.onclick = () => {
    const file = profileImageUpload.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            // 프로필 이미지 업데이트 및 localStorage에 저장
            profileImage.src = e.target.result;
            localStorage.setItem('profileImage', e.target.result);

            // 모달 창 닫기 (편집 기능이 모달로 구현되어 있다고 가정)
            document.getElementById('editProfileModal').style.display = 'none';
        };
        reader.readAsDataURL(file);
    }
};